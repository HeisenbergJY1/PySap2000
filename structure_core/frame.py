# -*- coding: utf-8 -*-
"""
frame.py - Frame element data object.

Maps to SAP2000 `FrameObj`.

This is a pure data class that only contains core CRUD behavior.
For extended behavior such as loads, releases, and modifiers, use:
- `loads/frame_load.py` for loads
- the `frame/` package for sections, releases, modifiers, and related helpers

API Reference:
    - AddByCoord(xi, yi, zi, xj, yj, zj, Name, PropName, UserName, CSys) -> Long
    - AddByPoint(Point1, Point2, Name, PropName, UserName) -> Long
    - GetPoints(Name, Point1, Point2) -> Long
    - GetSection(Name, PropName, SAuto) -> Long
    - SetSection(Name, PropName, ItemType) -> Long
    - Count() -> Long
    - GetNameList() -> (NumberNames, MyName[], ret)
    - Delete(Name) -> Long

Usage:
    from PySap2000.structure_core import Frame
    
    # Create a frame by point names
    frame = Frame(no=1, start_point="1", end_point="2", section="W14X30")
    frame._create(model)
    
    # Create a frame by coordinates
    frame = Frame(
        no=2, 
        start_x=0, start_y=0, start_z=0,
        end_x=10, end_y=0, end_z=0,
        section="W14X30"
    )
    frame._create(model)
    
    # Fetch a frame
    frame = Frame.get_by_name(model, "1")
    print(f"Section: {frame.section}")
"""

import math
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Union, ClassVar

# Import enums from the frame package to avoid duplication.
from PySap2000.frame.enums import (
    FrameType,
    FrameSectionType,
    FrameReleaseType,
    ItemType,
    SECTION_TYPE_NAMES,
)
from PySap2000.com_helper import com_ret, com_data


# Map section types to SAP2000 getter methods.
SECTION_TYPE_METHOD_MAP = {
    FrameSectionType.I_SECTION: 'GetISection_1',
    FrameSectionType.PIPE: 'GetPipe',
    FrameSectionType.BOX: 'GetTube_1',
    FrameSectionType.CIRCLE: 'GetCircle',
    FrameSectionType.RECTANGULAR: 'GetRectangle',
}


@dataclass
class Frame:
    """
    Frame element data object.

    Maps to SAP2000 `FrameObj`.
    
    Attributes:
        no: Frame identifier or name
        start_point: Start point name (I-End)
        end_point: End point name (J-End)
        section: Section name
        s_auto: Auto-select list name
        material: Material name
    """
    
    # Required attribute
    no: Union[int, str] = None
    
    # Definition by points
    start_point: Optional[Union[int, str]] = None
    end_point: Optional[Union[int, str]] = None
    
    # Definition by coordinates
    start_x: Optional[float] = None
    start_y: Optional[float] = None
    start_z: Optional[float] = None
    end_x: Optional[float] = None
    end_y: Optional[float] = None
    end_z: Optional[float] = None
    
    # Section and material
    section: str = ""
    s_auto: str = ""
    section_type: Optional[FrameSectionType] = None
    section_type_name: str = ""
    material: Optional[str] = None
    
    # Frame properties
    type: FrameType = FrameType.BEAM
    local_axis_angle: float = 0.0
    advanced_axes: bool = False
    
    # End releases (U1, U2, U3, R1, R2, R3)
    release_i: Tuple[bool, ...] = field(default_factory=lambda: (False,)*6)
    release_j: Tuple[bool, ...] = field(default_factory=lambda: (False,)*6)
    
    # Read-only attributes
    length: Optional[float] = field(default=None, repr=False)
    weight: float = 0.0  # Frame weight [kg]
    guid: Optional[str] = None
    
    # Optional attributes
    coordinate_system: str = "Global"
    comment: str = ""
    
    # Class metadata
    _object_type: ClassVar[str] = "FrameObj"
    
    # ==================== Core CRUD Methods ====================
    
    def _create(self, model) -> int:
        """
        Create the frame in SAP2000.
        
        Returns:
            `0` on success
        """
        from PySap2000.logger import get_logger
        _log = get_logger("frame")

        user_name = str(self.no) if self.no is not None else ""
        section = self.section if self.section else "Default"

        # Check whether the frame name already exists
        if user_name:
            try:
                existing = self.get_name_list(model)
                if user_name in existing:
                    _log.warning(f"Frame '{user_name}' already exists, skipped")
                    return -1
            except Exception:
                pass

        # Create by coordinates
        if self.start_x is not None and self.end_x is not None:
            # Check whether the section exists
            self._check_section_exists(model, section, _log)
            result = model.FrameObj.AddByCoord(
                self.start_x, self.start_y or 0, self.start_z or 0,
                self.end_x, self.end_y or 0, self.end_z or 0,
                "", section, user_name, self.coordinate_system
            )
            assigned_name = com_data(result, index=0)
            if assigned_name:
                self.no = assigned_name
            return com_ret(result)
        
        # Create by points
        if self.start_point is not None and self.end_point is not None:
            # Check whether the points exist
            self._check_points_exist(model, _log)
            # Check whether the section exists
            self._check_section_exists(model, section, _log)

            result = model.FrameObj.AddByPoint(
                str(self.start_point), str(self.end_point),
                "", section, user_name
            )
            assigned_name = com_data(result, index=0)
            if assigned_name:
                self.no = assigned_name
            return com_ret(result)
        
        from PySap2000.exceptions import FrameError
        raise FrameError("Frame creation requires points or coordinates")

    def _check_points_exist(self, model, _log):
        """Warn if end points are missing from the model."""
        try:
            ret = model.PointObj.GetNameList(0, [])
            raw_names = com_data(ret, index=1)
            names = list(raw_names) if raw_names else []
            for pt, label in [(self.start_point, "start_point"), (self.end_point, "end_point")]:
                if str(pt) not in names:
                    _log.warning(f"Point {pt} ({label}) not found")
        except Exception:
            pass

    def _check_section_exists(self, model, section, _log):
        """Warn if the section is missing from the model."""
        if section == "Default":
            return
        try:
            ret = model.PropFrame.GetNameList(0, [])
            raw_names = com_data(ret, index=1)
            names = list(raw_names) if raw_names else []
            if section not in names:
                _log.warning(f"Section '{section}' not found")
        except Exception:
            pass
    
    def _get(self, model) -> 'Frame':
        """Fetch frame data from SAP2000."""
        no_str = str(self.no)
        
        # Get end points
        result = model.FrameObj.GetPoints(no_str)
        self.start_point = com_data(result, index=0)
        self.end_point = com_data(result, index=1)
        if com_ret(result) != 0:
            from PySap2000.exceptions import FrameError
            raise FrameError(f"Failed to get endpoints for Frame '{no_str}'")
        
        # Get section data
        result = model.FrameObj.GetSection(no_str)
        self.section = com_data(result, index=0, default="")
        s_auto_val = com_data(result, index=1)
        self.s_auto = s_auto_val if s_auto_val else ""
        
        # Get section type
        self._get_section_type(model)
        
        # Get local axis data
        self._get_local_axes(model)
        
        # Get end releases
        self._get_releases(model)
        
        # Get GUID
        self._get_guid(model)
        
        # Compute length
        self._calculate_length(model)
        
        # Compute weight
        self._calculate_weight(model)
        
        return self
    
    def _delete(self, model) -> int:
        """Delete the frame from SAP2000."""
        return model.FrameObj.Delete(str(self.no))

    def change_name(self, model, new_name: str) -> int:
        """
        Change the frame name.

        Args:
            model: `SapModel` object
            new_name: New frame name

        Returns:
            `0` on success
        """
        ret = model.FrameObj.ChangeName(str(self.no), new_name)
        if ret == 0:
            self.no = new_name
        return ret
    
    def _update(self, model) -> int:
        """Update the assigned frame section."""
        from PySap2000.logger import get_logger
        _log = get_logger("frame")
        if self.section:
            self._check_section_exists(model, self.section, _log)
            return model.FrameObj.SetSection(str(self.no), self.section, ItemType.OBJECT)
        return 0
    
    # ==================== Internal Helpers ====================
    
    def _get_section_type(self, model):
        """Fetch the section type."""
        if self.section:
            try:
                result = model.PropFrame.GetTypeOAPI(self.section)
                type_val = com_data(result, index=0)
                if type_val is not None:
                    self.section_type = FrameSectionType(type_val)
                    self.section_type_name = SECTION_TYPE_NAMES.get(
                        self.section_type, self.section_type.name
                    )
            except (ValueError, Exception):
                pass
    
    def _get_local_axes(self, model):
        """Fetch local axis information."""
        try:
            result = model.FrameObj.GetLocalAxes(str(self.no))
            self.local_axis_angle = com_data(result, index=0, default=0.0)
            self.advanced_axes = com_data(result, index=1, default=False)
        except Exception:
            pass
    
    def _get_releases(self, model):
        """Fetch end release information."""
        try:
            result = model.FrameObj.GetReleases(str(self.no))
            ri = com_data(result, index=0)
            rj = com_data(result, index=1)
            if ri is not None:
                self.release_i = tuple(ri)
            if rj is not None:
                self.release_j = tuple(rj)
        except Exception:
            pass
    
    def _get_guid(self, model):
        """Fetch the frame GUID."""
        try:
            result = model.FrameObj.GetGUID(str(self.no))
            self.guid = com_data(result, index=0)
        except Exception:
            pass
    
    def _calculate_length(self, model, point_cache: dict = None):
        """
        Compute the frame length.
        
        Args:
            model: `SapModel` object
            point_cache: Optional point-coordinate cache `{name: (x, y, z)}`
        """
        try:
            if point_cache is not None:
                p1 = point_cache.get(str(self.start_point))
                p2 = point_cache.get(str(self.end_point))
                if p1 and p2:
                    self.length = round(
                        math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2),
                        3
                    )
                    return
            # Fall back to per-point queries
            from PySap2000.structure_core.point import Point
            p1 = Point(no=self.start_point)._get(model)
            p2 = Point(no=self.end_point)._get(model)
            self.length = round(
                math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2 + (p2.z - p1.z)**2),
                3
            )
        except Exception:
            self.length = None
    
    def _calculate_weight(self, model, *, _units_context: bool = False) -> float:
        """
        Compute frame weight in kilograms.
        
        weight = weight_per_meter × length
        
        If the current unit system is not `N_M_C`, units are switched
        temporarily. In batch mode, callers can pass `_units_context=True`
        after switching units once to avoid repeated toggles.
        
        Args:
            model: `SapModel` object
            _units_context: `True` when the caller has already switched to `N_M_C`
            
        Returns:
            Frame weight in kilograms, or `0.0` if data is invalid
        """
        if not self.section:
            self.weight = 0.0
            return 0.0
        
        try:
            from PySap2000.section.frame_section import FrameSection
            from PySap2000.global_parameters.units import Units, UnitSystem
            
            # When `_units_context` is True, the caller already switched units.
            need_switch = False
            if not _units_context:
                current_units = Units.get_present_units(model)
                need_switch = current_units != UnitSystem.N_M_C
                if need_switch:
                    Units.set_present_units(model, UnitSystem.N_M_C)
            
            try:
                # Get section weight per unit length (kg/m)
                section = FrameSection.get_by_name(model, self.section)
                weight_per_meter = section.weight_per_meter
                
                if weight_per_meter <= 0:
                    self.weight = 0.0
                    return 0.0
                
                # Compute frame length (m)
                from PySap2000.structure_core.point import Point
                p1 = Point(no=self.start_point)._get(model)
                p2 = Point(no=self.end_point)._get(model)
                length_m = math.sqrt(
                    (p2.x - p1.x)**2 + (p2.y - p1.y)**2 + (p2.z - p1.z)**2
                )
                
                self.weight = weight_per_meter * length_m
            finally:
                if need_switch:
                    Units.set_present_units(model, current_units)
            
        except Exception:
            self.weight = 0.0
        
        return self.weight
    
    # ==================== Static Methods ====================
    
    @staticmethod
    def get_count(model) -> int:
        """Return the total number of frames."""
        return model.FrameObj.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """Return the list of all frame names."""
        result = model.FrameObj.GetNameList(0, [])
        names = com_data(result, index=1)
        if names is not None:
            return list(names)
        return []
    
    @staticmethod
    def get_section_name_list(model) -> List[str]:
        """Return the list of all frame section names."""
        result = model.PropFrame.GetNameList(0, [])
        names = com_data(result, index=1)
        if names is not None:
            return list(names)
        return []
    
    # ==================== Class Methods ====================
    
    @classmethod
    def get_by_name(cls, model, name: str) -> 'Frame':
        """
        Fetch a frame by name.
        
        Example:
            frame = Frame.get_by_name(model, "1")
            print(f"Section: {frame.section}")
        """
        frame = cls(no=name)
        frame._get(model)
        return frame
    
    @classmethod
    def get_all(cls, model, names: List[str] = None) -> List['Frame']:
        """
        Fetch all frames using the Database Tables API.

        Compared with per-object COM calls, this approach dramatically reduces
        call count and is much faster for large models.
        
        Args:
            model: `SapModel` object
            names: Optional frame name list; `None` fetches all frames
            
        Returns:
            List of `Frame` objects
            
        Example:
            frames = Frame.get_all(model)
            for f in frames:
                print(f"{f.no}: {f.section}, L={f.length}")
        """
        from PySap2000.database_tables import DatabaseTables
        
        # 1) Fetch frame connectivity in bulk
        conn_table = DatabaseTables.get_table_for_display(
            model, "Connectivity - Frame"
        )
        if conn_table is None or conn_table.num_records == 0:
            return []
        
        # 2) Fetch section assignments in bulk
        sec_table = DatabaseTables.get_table_for_display(
            model, "Frame Section Assignments"
        )
        section_map = {}  # {frame_name: (section, s_auto)}
        if sec_table and sec_table.num_records > 0:
            for row in sec_table.to_dict_list():
                fname = row.get("Frame", "")
                section_map[fname] = (
                    row.get("AnalSect", ""),
                    row.get("AutoSelect", ""),
                )
        
        # 3) Fetch point coordinates in bulk for length calculation
        coord_table = DatabaseTables.get_table_for_display(
            model, "Joint Coordinates"
        )
        point_cache = {}  # {joint_name: (x, y, z)}
        if coord_table and coord_table.num_records > 0:
            for row in coord_table.to_dict_list():
                jname = row.get("Joint", "")
                try:
                    point_cache[jname] = (
                        float(row.get("XorR", 0)),
                        float(row.get("Y", 0)),
                        float(row.get("Z", 0)),
                    )
                except (ValueError, TypeError):
                    pass
        
        # Build a name filter
        name_filter = set(str(n) for n in names) if names else None
        
        frames = []
        for row in conn_table.to_dict_list():
            frame_name = row.get("Frame", "")
            if name_filter and frame_name not in name_filter:
                continue
            
            start_pt = row.get("JointI", "")
            end_pt = row.get("JointJ", "")
            sec_info = section_map.get(frame_name, ("", ""))
            
            frame = cls(
                no=frame_name,
                start_point=start_pt,
                end_point=end_pt,
                section=sec_info[0],
                s_auto=sec_info[1] if sec_info[1] else "",
            )
            
            # Compute length from the cache without extra COM calls
            frame._calculate_length(model, point_cache=point_cache)
            
            frames.append(frame)
        
        return frames
    
    # ==================== Batch Methods ====================
    
    @classmethod
    def calculate_weights_batch(
        cls, 
        model, 
        frames: List['Frame'] = None
    ) -> dict:
        """
        Compute frame weights in batch mode.
        
        Args:
            model: `SapModel` object
            frames: Optional frame list; fetch all if `None`
            
        Returns:
            Dict mapping frame name to weight in kilograms
            
        Example:
            weights = Frame.calculate_weights_batch(model)
            total = sum(weights.values())
            print(f"Total weight: {total:.2f} kg")
        """
        from PySap2000.global_parameters.units import Units, UnitSystem
        from PySap2000.section.frame_section import FrameSection
        from PySap2000.database_tables import DatabaseTables
        
        if frames is None:
            frames = cls.get_all(model)
        
        if not frames:
            return {}
        
        # Save the current unit system
        current_units = Units.get_present_units(model)
        need_switch = current_units != UnitSystem.N_M_C
        
        if need_switch:
            Units.set_present_units(model, UnitSystem.N_M_C)
        
        weights = {}
        section_cache = {}  # Section data cache
        
        try:
            # Fetch all point coordinates once via Database Tables
            point_cache = {}
            coord_table = DatabaseTables.get_table_for_display(
                model, "Joint Coordinates"
            )
            if coord_table and coord_table.num_records > 0:
                for row in coord_table.to_dict_list():
                    jname = row.get("Joint", "")
                    try:
                        point_cache[jname] = (
                            float(row.get("XorR", 0)),
                            float(row.get("Y", 0)),
                            float(row.get("Z", 0)),
                        )
                    except (ValueError, TypeError):
                        pass
            
            for frame in frames:
                try:
                    # Get section weight with caching
                    if frame.section not in section_cache:
                        section = FrameSection.get_by_name(model, frame.section)
                        section_cache[frame.section] = section.weight_per_meter
                    
                    weight_per_meter = section_cache[frame.section]
                    if weight_per_meter <= 0:
                        weights[str(frame.no)] = 0.0
                        continue
                    
                    p1 = point_cache.get(str(frame.start_point))
                    p2 = point_cache.get(str(frame.end_point))
                    
                    if not p1 or not p2:
                        weights[str(frame.no)] = 0.0
                        continue
                    
                    # Compute length and weight
                    length = math.sqrt(
                        (p2[0] - p1[0])**2 + 
                        (p2[1] - p1[1])**2 + 
                        (p2[2] - p1[2])**2
                    )
                    weights[str(frame.no)] = weight_per_meter * length
                    
                except Exception:
                    weights[str(frame.no)] = 0.0
        finally:
            if need_switch:
                Units.set_present_units(model, current_units)
        
        return weights
    
    @classmethod
    def create_batch(
        cls, 
        model, 
        frames: List['Frame']
    ) -> Tuple[List['Frame'], List[Tuple[str, str]]]:
        """
        Create frames in batch mode.
        
        Args:
            model: `SapModel` object
            frames: Frames to create
            
        Returns:
            Tuple of successful frames and failed `(name, error)` pairs
            
        Example:
            frames = [
                Frame(no="F1", start_point="1", end_point="2", section="W14X30"),
                Frame(no="F2", start_point="2", end_point="3", section="W14X30"),
            ]
            succeeded, failed = Frame.create_batch(model, frames)
            print(f"Succeeded: {len(succeeded)}, Failed: {len(failed)}")
        """
        succeeded = []
        failed = []
        
        for frame in frames:
            try:
                ret = frame._create(model)
                if ret == 0:
                    succeeded.append(frame)
                else:
                    failed.append((str(frame.no), f"Return code: {ret}"))
            except Exception as e:
                failed.append((str(frame.no), str(e)))
        
        return succeeded, failed
    
    @classmethod
    def delete_batch(
        cls, 
        model, 
        names: List[str]
    ) -> Tuple[List[str], List[Tuple[str, str]]]:
        """
        Delete frames in batch mode.
        
        Args:
            model: `SapModel` object
            names: Names of frames to delete
            
        Returns:
            Tuple of successful names and failed `(name, error)` pairs
            
        Example:
            succeeded, failed = Frame.delete_batch(model, ["F1", "F2", "F3"])
        """
        succeeded = []
        failed = []
        
        for name in names:
            try:
                ret = model.FrameObj.Delete(str(name))
                if ret == 0:
                    succeeded.append(name)
                else:
                    failed.append((name, f"Return code: {ret}"))
            except Exception as e:
                failed.append((name, str(e)))
        
        return succeeded, failed
    
    @classmethod
    def set_section_batch(
        cls, 
        model, 
        names: List[str], 
        section: str
    ) -> Tuple[List[str], List[Tuple[str, str]]]:
        """
        Assign a section to multiple frames.
        
        Args:
            model: `SapModel` object
            names: Frame name list
            section: Section name
            
        Returns:
            Tuple of successful names and failed `(name, error)` pairs
            
        Example:
            succeeded, failed = Frame.set_section_batch(
                model, 
                ["F1", "F2", "F3"], 
                "W21X44"
            )
        """
        succeeded = []
        failed = []
        
        for name in names:
            try:
                ret = model.FrameObj.SetSection(str(name), section, ItemType.OBJECT)
                if ret == 0:
                    succeeded.append(name)
                else:
                    failed.append((name, f"Return code: {ret}"))
            except Exception as e:
                failed.append((name, str(e)))
        
        return succeeded, failed
