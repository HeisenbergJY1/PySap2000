# -*- coding: utf-8 -*-
"""
application.py - SAP2000 application connection manager.

Design inspired by `dlubal.api`.

Usage:
    from PySap2000 import Application
    from PySap2000.structure_core import Point, Frame
    
    with Application() as app:
        # Create points
        app.create_object(Point(no=1, x=0, y=0, z=0))
        app.create_object(Point(no=2, x=10, y=0, z=0))
        
        # Create a frame
        app.create_object(Frame(no=1, start_point=1, end_point=2, section="W14X30"))
        
        # Run analysis
        app.calculate()
"""

import gc
import inspect
import comtypes.client
from typing import Optional, List, Union, TypeVar, Type, TYPE_CHECKING
from PySap2000.exceptions import SAPConnectionError, ObjectError
from PySap2000.logger import get_logger
from PySap2000.com_helper import com_ret, com_data

if TYPE_CHECKING:
    from PySap2000.utils.protocols import Creatable, Deletable, Gettable, Updatable

_logger = get_logger("application")

T = TypeVar('T')

# Minimum supported SAP2000 version
MIN_SAP2000_VERSION = 20.0


class Application:
    """
    SAP2000 application connection manager.

    Design inspired by `dlubal.api.rfem.Application`:
    - uses a context manager to manage the connection lifecycle
    - provides a unified CRUD interface
    - supports batch operations

    Note:
        This class is not thread-safe. The SAP2000 COM interface expects all
        calls to run on the same thread. Do not share one `Application`
        instance across multiple threads.
    
    Raises:
        SAPConnectionError: Raised when SAP2000 cannot be attached or started
    """
    
    def __init__(
        self,
        attach_to_instance: bool = True,
        program_path: str = "",
        model_file: str = ""
    ):
        """
        Initialize the SAP2000 connection.

        Args:
            attach_to_instance: If True, attach to a running instance; otherwise
                start a new one
            program_path: SAP2000 executable path when starting a new instance
            model_file: Model filename used to validate that the expected model
                is open

        Example:
            # Option 1: attach to any already-open model
            with Application() as app:
                pass

            # Option 2: attach to a specific open model by filename
            with Application(model_file="bridge.sdb") as app:
                # Raises if the current model is not bridge.sdb
                app.calculate()
        """
        self._sap_object = None
        self._model = None
        self._in_modification = False
        self._owns_instance = not attach_to_instance

        if attach_to_instance:
            self._attach_to_instance()
        else:
            self._start_application(program_path)

        # Check SAP2000 version
        self._check_version()

        # Validate the model filename
        if model_file:
            self._verify_model_file(model_file)

    def _ensure_connected(self):
        """
        Ensure the COM connection is still valid.

        All public methods that use `self._model` should call this first.

        Raises:
            SAPConnectionError: Raised when the COM connection is no longer valid
        """
        if self._model is None:
            raise SAPConnectionError(
                "SAP2000 connection is closed. Create a new Application instance or "
                "verify that SAP2000 is still running."
            )

    def _check_version(self):
        """
        Check that the connected SAP2000 version meets the minimum requirement.

        Raises:
            SAPConnectionError: Raised when the version is too old
        """
        try:
            version_info = self._model.GetVersion()
            version_number = com_data(version_info, 1, default=0.0)
            if version_number < MIN_SAP2000_VERSION:
                raise SAPConnectionError(
                    f"SAP2000 v{version_number} is not supported. "
                    f"Minimum required version: v{MIN_SAP2000_VERSION}"
                )
        except SAPConnectionError:
            raise
        except Exception as e:
            _logger.warning(f"Unable to verify SAP2000 version: {e}")

    def _verify_model_file(self, expected_file: str):
        """
        Validate the filename of the currently open model.

        Args:
            expected_file: Expected file path or filename

        Raises:
            SAPConnectionError: Raised when the currently open model does not match
        """
        import os
        current_file = self.get_model_filename(include_path=False)
        expected_name = os.path.basename(expected_file)

        if current_file != expected_name:
            raise SAPConnectionError(
                "Model file does not match.",
                details={
                    'expected': expected_name,
                    'actual': current_file,
                    'suggestion': f'Open {expected_name} in SAP2000.',
                }
            )

    def is_alive(self) -> bool:
        """
        Check whether the COM connection is still alive.

        Returns:
            `True` if the connection is valid, `False` otherwise
        """
        try:
            if self._model is None:
                return False
            _ = self._model.GetVersion()
            return True
        except Exception:
            return False

    def __del__(self):
        """
        Destructor safety net for resource cleanup.

        This helps when the user forgets to call `disconnect()`.
        """
        try:
            self.disconnect()
        except Exception:
            pass
    
    def _attach_to_instance(self):
        """Attach to a running SAP2000 instance, retrying up to three times."""
        from PySap2000.utils.retry import retry_on_com_error

        @retry_on_com_error(max_retries=3, delay=1.0, backoff=2.0)
        def _connect():
            self._sap_object = comtypes.client.GetActiveObject('CSI.SAP2000.API.SapObject')
            self._model = self._sap_object.SapModel

        try:
            _connect()
            self._print_connection_info()
        except Exception as e:
            from PySap2000.exceptions import SAP2000NotRunningError
            raise SAP2000NotRunningError(
                "Could not connect to SAP2000. Ensure SAP2000 is running.",
                details={'error': str(e)}
            )
    
    def _start_application(self, program_path: str = ""):
        """Start a new SAP2000 instance."""
        try:
            helper = comtypes.client.CreateObject('SAP2000v1.Helper')
            try:
                helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
            except AttributeError:
                _logger.warning(
                    "comtypes.gen.SAP2000v1 is not available; trying the default "
                    "Helper interface. If this fails, run "
                    "comtypes.client.GetModule('SAP2000v1.tlb') once manually."
                )
            if program_path:
                self._sap_object = helper.CreateObject(program_path)
            else:
                self._sap_object = helper.CreateObjectProgID('CSI.SAP2000.API.SapObject')
            self._sap_object.ApplicationStart()
            self._model = self._sap_object.SapModel
            self._print_connection_info()
        except SAPConnectionError:
            raise
        except Exception as e:
            raise SAPConnectionError(f"Cannot start SAP2000: {e}")
    
    def _print_connection_info(self):
        """Print connection info and configure logging in the model directory."""
        from PySap2000.logger import setup_logger
        import os

        version_info = self._model.GetVersion()
        version = com_data(version_info, 0, default="")
        filename = self._model.GetModelFilename(False) or "Untitled"
        print(f"Connected to SAP2000 v{version} | {filename}")

        # Automatically place the log file next to the active model.
        model_path = self._model.GetModelFilepath()
        if model_path:
            log_file = os.path.join(model_path, "pysap2000.log")
            setup_logger(level="INFO", log_file=log_file)
            _logger.info(f"Log file: {log_file}")
    
    def __enter__(self):
        """Context manager entry point."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit handler.

        Ensures that:
        1. modification mode is finished
        2. COM handles are released
        3. owned SAP2000 instances are closed
        """
        self.disconnect()
        return False
    
    def disconnect(self):
        """
        Explicitly disconnect and release COM resources.

        This can be called manually when not using a context manager.
        Repeated calls are safe and idempotent.
        """
        # 1. Finish modification mode
        if self._in_modification and self._model is not None:
            try:
                self.finish_modification()
            except Exception:
                _logger.debug("finish_modification failed during disconnect", exc_info=True)
        
        # 2. Release the model reference
        self._model = None
        
        # 3. Close the SAP2000 instance if this object started it
        if self._owns_instance and self._sap_object is not None:
            try:
                self._sap_object.ApplicationExit(False)
                _logger.info("SAP2000 application exited (owned instance)")
            except Exception:
                _logger.debug("ApplicationExit failed during disconnect", exc_info=True)
        
        # 4. Release COM object references
        self._sap_object = None
        
        # 5. Force GC to release COM reference counts
        gc.collect()
    
    @property
    def model(self):
        """Return the raw `SapModel` object for advanced or legacy usage."""
        self._ensure_connected()
        return self._model

    # ==================== Modification Mode ====================
    
    def begin_modification(self):
        """
        Begin batch modification mode.

        View refreshing is disabled to improve performance.
        """
        self._ensure_connected()
        if not self._in_modification:
            self._model.View.RefreshView(0, False)
            self._in_modification = True
    
    def finish_modification(self):
        """
        Finish batch modification mode and refresh the view.
        """
        self._ensure_connected()
        if self._in_modification:
            self._model.View.RefreshView(0, True)
            self._in_modification = False
    
    # ==================== Unified CRUD Interface ====================
    
    @staticmethod
    def _obj_desc(obj) -> str:
        """Build a short object description for log messages."""
        from PySap2000.structure_core.point import Point
        from PySap2000.structure_core.frame import Frame
        from PySap2000.structure_core.area import Area
        from PySap2000.structure_core.cable import Cable
        from PySap2000.structure_core.link import Link

        type_name = type(obj).__name__
        no = getattr(obj, 'no', None) or getattr(obj, 'name', None)
        if isinstance(obj, Point):
            x = getattr(obj, 'x', 0)
            y = getattr(obj, 'y', 0)
            z = getattr(obj, 'z', 0)
            return f"Point({no}, x={x}, y={y}, z={z})"
        elif isinstance(obj, Frame):
            sp = getattr(obj, 'start_point', '')
            ep = getattr(obj, 'end_point', '')
            sec = getattr(obj, 'section', '')
            return f"Frame({no}, {sp}->{ep}, sec={sec})"
        elif isinstance(obj, Area):
            return f"Area({no})"
        elif isinstance(obj, Cable):
            return f"Cable({no})"
        elif isinstance(obj, Link):
            return f"Link({no})"
        elif no is not None:
            return f"{type_name}({no})"
        return type_name

    def create_object(self, obj: 'Creatable') -> int:
        """
        Create a single object.

        Args:
            obj: Object to create, such as `Point`, `Frame`, or `Material`

        Returns:
            `0` on success

        Raises:
            SAPConnectionError: The COM connection is no longer valid
            ObjectError: The object does not support create operations

        Example:
            app.create_object(Point(no=1, x=0, y=0, z=0))
            app.create_object(Frame(no=1, start_point=1, end_point=2))
        """
        self._ensure_connected()
        if hasattr(obj, '_create'):
            ret = obj._create(self._model)
            desc = self._obj_desc(obj)
            if ret == 0:
                _logger.info(f"Created {desc}")
            elif ret == -1:
                pass  # already exists, skipped
            else:
                _logger.warning(f"Failed to create {desc}, ret={ret}")
            return ret
        raise ObjectError(f"{type(obj).__name__} does not support create")
    
    def create_object_list(self, objs: List) -> int:
        """
        Create multiple objects in batch mode.
        
        Args:
            objs: List of objects to create
            
        Returns:
            `0` on success
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        self.begin_modification()
        try:
            success = 0
            for obj in objs:
                if self.create_object(obj) == 0:
                    success += 1
            _logger.info(f"Batch created {success}/{len(objs)} objects")
        finally:
            self.finish_modification()
        return 0
    
    def get_object(self, obj: 'Gettable') -> T:
        """
        Retrieve a single object.
        
        Args:
            obj: Object with a `no` attribute identifying the target item
            
        Returns:
            The same object populated with data
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
            ObjectError: The object does not support get operations
            
        Example:
            point = app.get_object(Point(no=1))
            print(point.x, point.y, point.z)
        """
        self._ensure_connected()
        if hasattr(obj, '_get'):
            result = obj._get(self._model)
            desc = self._obj_desc(result)
            _logger.info(f"Retrieved {desc}")
            return result
        raise ObjectError(f"{type(obj).__name__} does not support get")
    
    def get_object_list(self, obj_type: Type[T], nos: List[Union[int, str]] = None) -> List[T]:
        """
        Retrieve multiple objects.
        
        Args:
            obj_type: Object class
            nos: Optional list of object identifiers; `None` means fetch all
            
        Returns:
            A list of objects
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
            ObjectError: The object type does not support bulk retrieval
        """
        self._ensure_connected()

        bulk_getters = [
            candidate
            for attr_name in ("get_all", "_get_all")
            if callable(candidate := getattr(obj_type, attr_name, None))
        ]

        if nos is not None:
            for bulk_getter in bulk_getters:
                if self._supports_name_filtered_bulk_get(bulk_getter):
                    return bulk_getter(self._model, nos)
            if bulk_getters:
                raise ObjectError(
                    f"{obj_type.__name__} does not support filtered bulk retrieval"
                )
        elif bulk_getters:
            return bulk_getters[0](self._model)

        raise ObjectError(f"{obj_type.__name__} does not support get_all")

    @staticmethod
    def _supports_name_filtered_bulk_get(bulk_getter) -> bool:
        """Return whether a bulk getter accepts a list of object identifiers."""
        try:
            parameters = list(inspect.signature(bulk_getter).parameters.values())
        except (TypeError, ValueError):
            return False

        if any(
            p.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
            for p in parameters
        ):
            return True

        named_parameters = [
            p for p in parameters
            if p.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            )
        ]
        if len(named_parameters) < 2:
            return False

        return named_parameters[1].name in {"names", "nos"}
    
    def update_object(self, obj: 'Updatable') -> int:
        """
        Update a single object.
        
        Args:
            obj: Object to update
            
        Returns:
            `0` on success
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
            ObjectError: The object does not support update operations
        """
        self._ensure_connected()
        if hasattr(obj, '_update'):
            ret = obj._update(self._model)
            desc = self._obj_desc(obj)
            if ret == 0:
                _logger.info(f"Updated {desc}")
            else:
                _logger.warning(f"Failed to update {desc}, ret={ret}")
            return ret
        raise ObjectError(f"{type(obj).__name__} does not support update")

    def rename_object(self, obj, new_name: str) -> int:
        """
        Rename an object.
        
        Args:
            obj: Object to rename; it must provide a `change_name` method
            new_name: New object name
            
        Returns:
            `0` on success
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
            ObjectError: The object does not support rename operations
            
        Example:
            app.rename_object(Frame(no="1"), "F1")
        """
        self._ensure_connected()
        if hasattr(obj, 'change_name'):
            old_name = getattr(obj, 'no', '?')
            ret = obj.change_name(self._model, new_name)
            type_name = type(obj).__name__
            if ret == 0:
                _logger.info(f"Renamed {type_name}({old_name}) -> {new_name}")
            else:
                _logger.warning(f"Failed to rename {type_name}({old_name}) -> {new_name}, ret={ret}")
            return ret
        raise ObjectError(f"{type(obj).__name__} does not support rename")
    
    def delete_object(self, obj: 'Deletable') -> int:
        """
        Delete a single object.

        Args:
            obj: Object to delete; it must provide a `no` attribute

        Returns:
            `0` on success

        Raises:
            SAPConnectionError: The COM connection is no longer valid
            ObjectError: The object does not support delete operations
        """
        self._ensure_connected()
        if hasattr(obj, '_delete'):
            ret = obj._delete(self._model)
            desc = self._obj_desc(obj)
            if ret == 0:
                _logger.info(f"Deleted {desc}")
            else:
                _logger.warning(f"Failed to delete {desc}, ret={ret}")
            return ret
        raise ObjectError(f"{type(obj).__name__} does not support delete")

    # ==================== Model Operations ====================
    
    def new_model(self, units: int = 6) -> int:
        """
        Create a new model.
        
        Args:
            units: Unit system code
            
        Returns:
            `0` on success
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        return com_ret(self._model.InitializeNewModel(units))
    
    def open_model(self, path: str) -> int:
        """
        Open a model file.
        
        Args:
            path: Model file path
            
        Returns:
            `0` on success
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        return com_ret(self._model.File.OpenFile(path))
    
    def save_model(self, path: str = "") -> int:
        """
        Save the current model.
        
        Args:
            path: Save path; empty string saves to the current location
            
        Returns:
            `0` on success
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        if path:
            return com_ret(self._model.File.Save(path))
        return com_ret(self._model.File.Save())
    
    def close_model(self, save_changes: bool = False) -> int:
        """
        Close the current model.
        
        Args:
            save_changes: Whether to save changes first
            
        Returns:
            `0` on success
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        if save_changes:
            self.save_model()
        # SAP2000 does not expose a dedicated close-model API, so reset instead.
        return com_ret(self._model.InitializeNewModel(6))
    
    # ==================== Analysis Operations ====================
    
    def calculate(self) -> int:
        """
        Run analysis.

        Returns:
            `0` on success

        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        com_ret(self._model.Analyze.SetRunCaseFlag("", True, True))
        return com_ret(self._model.Analyze.RunAnalysis())
    
    def delete_results(self) -> int:
        """
        Delete analysis results.
        
        Returns:
            `0` on success
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        return com_ret(self._model.Analyze.DeleteResults("", True))
    
    # ==================== Result Retrieval ====================
    
    def get_results(self, result_type: str, load_case: str = "", load_combo: str = ""):
        """
        Retrieve analysis results.
        
        This method is not implemented yet. Use functions from the
        `results` module directly, for example::

            from PySap2000.results import get_joint_displ, deselect_all_cases_and_combos
            deselect_all_cases_and_combos(app.model)
            displ = get_joint_displ(app.model, "1")
        
        Args:
            result_type: Result type such as `'displacement'` or `'reaction'`
            load_case: Load case name
            load_combo: Load combination name
            
        Raises:
            NotImplementedError: Always raised until this method is implemented
        """
        raise NotImplementedError(
            "Application.get_results() is not implemented yet. "
            "Use functions in the PySap2000.results package to retrieve results."
        )
    
    # ==================== Helpers ====================
    
    def set_units(self, units) -> int:
        """
        Set the current unit system.
        
        Args:
            units: A `UnitSystem` enum value or integer code
                
        Returns:
            `0` on success
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        return com_ret(self._model.SetPresentUnits(int(units)))
    
    def get_units(self):
        """
        Return the current unit system.
        
        Returns:
            A `UnitSystem` enum value
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        from PySap2000.global_parameters.units import UnitSystem
        self._ensure_connected()
        return UnitSystem(self._model.GetPresentUnits())
    
    def get_units_name(self) -> str:
        """
        Return a human-readable description of the current unit system.
        
        Returns:
            Description such as `"kN-m-C"` or `"N-mm-C"`
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        from PySap2000.global_parameters.units import Units as _Units
        return _Units.get_unit_description(self.get_units())
    
    def get_database_units(self):
        """
        Return the database unit system.

        All model data is stored internally using database units and converted
        to the active display units when needed.
        
        Returns:
            A `UnitSystem` enum value
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        from PySap2000.global_parameters.units import UnitSystem
        self._ensure_connected()
        return UnitSystem(self._model.GetDatabaseUnits())
    
    def get_database_units_name(self) -> str:
        """
        Return a human-readable description of the database unit system.
        
        Returns:
            Description such as `"kN-m-C"` or `"N-mm-C"`
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        from PySap2000.global_parameters.units import Units as _Units
        return _Units.get_unit_description(self.get_database_units())
    
    def refresh_view(self):
        """
        Refresh the model view.
        
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        self._model.View.RefreshView(0, True)

    # ==================== Model Information ====================
    
    def get_model_filename(self, include_path: bool = True) -> str:
        """
        Return the active model filename.
        
        Args:
            include_path: Whether to include the full path
            
        Returns:
            The model filename
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        return self._model.GetModelFilename(include_path)
    
    def get_model_filepath(self) -> str:
        """
        Return the active model directory path.
        
        Returns:
            Directory containing the model file
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        return self._model.GetModelFilepath()
    
    def get_model_is_locked(self) -> bool:
        """
        Return the model lock state.

        When the model is locked, most definitions and assignments cannot be edited.
        
        Returns:
            `True` if the model is locked
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        return self._model.GetModelIsLocked()
    
    def set_model_is_locked(self, lock_it: bool) -> int:
        """
        Set the model lock state.
        
        Args:
            lock_it: `True` to lock the model, `False` to unlock it
            
        Returns:
            `0` on success
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        return com_ret(self._model.SetModelIsLocked(lock_it))
    
    # ==================== Merge Tolerance ====================
    
    def get_merge_tol(self) -> float:
        """
        Return the automatic merge tolerance.

        Returns:
            Merge tolerance in model length units
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        result = self._model.GetMergeTol()
        return float(com_data(result, 0, default=result))

    
    def set_merge_tol(self, merge_tol: float) -> int:
        """
        Set the automatic merge tolerance.
        
        Args:
            merge_tol: Merge tolerance in model length units
            
        Returns:
            `0` on success
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        return com_ret(self._model.SetMergeTol(merge_tol))
    
    # ==================== Coordinate Systems ====================
    
    def get_present_coord_system(self) -> str:
        """
        Return the current coordinate system name.

        Returns:
            Coordinate system name
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        result = self._model.GetPresentCoordSystem()
        if isinstance(result, str):
            if result.upper() == "GLOBAL":
                return "Global"
        return result

    
    def set_present_coord_system(self, csys: str) -> int:
        """
        Set the current coordinate system.
        
        Args:
            csys: Coordinate system name
            
        Returns:
            `0` on success
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        return com_ret(self._model.SetPresentCoordSystem(csys))
    
    # ==================== Project Information ====================
    
    def get_project_info(self) -> dict:
        """
        Return project information.
        
        Returns:
            Dictionary of project info items: `{item_name: data}`
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        result = self._model.GetProjectInfo()
        if isinstance(result, tuple) and len(result) >= 3:
            num_items = result[0]
            items = result[1]
            data = result[2]
            if num_items > 0 and items and data:
                return dict(zip(items, data))
        return {}
    
    def set_project_info(self, item: str, data: str) -> int:
        """
        Set a project information item.
        
        Args:
            item: Project info item name, for example `"Company Name"`
            data: Project info value
            
        Returns:
            `0` on success
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        return com_ret(self._model.SetProjectInfo(item, data))
    
    # ==================== User Comments ====================
    
    def get_user_comment(self) -> str:
        """
        Return the user comment text.
        
        Returns:
            User comment content
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        result = self._model.GetUserComment()
        if isinstance(result, tuple):
            return result[0]
        return ""
    
    def set_user_comment(
        self, 
        comment: str, 
        num_lines: int = 1, 
        replace: bool = False
    ) -> int:
        """
        Set the user comment text.
        
        Args:
            comment: Comment text
            num_lines: Number of blank lines to insert before the comment
            replace: If `True`, replace existing comments; otherwise append
            
        Returns:
            `0` on success
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        return com_ret(self._model.SetUserComment(comment, num_lines, replace))
    
    # ==================== Version Information ====================
    
    def get_version(self) -> tuple:
        """
        Return SAP2000 version information.
        
        Returns:
            Tuple `(version_string, version_number)`, for example `("26.3.0", 26.3)`
            
        Raises:
            SAPConnectionError: The COM connection is no longer valid
        """
        self._ensure_connected()
        result = self._model.GetVersion()
        version = com_data(result, 0, default="")
        version_number = com_data(result, 1, default=0.0)
        return (version, version_number)
