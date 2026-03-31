# -*- coding: utf-8 -*-
"""
cable.py - Cable element data object.

Maps to SAP2000 `CableObj`.

API Reference:
    - AddByPoint(Point1, Point2, Name, PropName="Default", UserName="") -> Long
    - AddByCoord(xi, yi, zi, xj, yj, zj, Name, PropName="Default", UserName="", CSys="Global") -> Long
    - GetPoints(Name, Point1, Point2) -> Long
    - GetProperty(Name, PropName) -> Long
    - GetCableData(Name, CableType, NumSegs, Weight, ProjectedLoad, UseDeformedGeom, ModelUsingFrames, Parameter[]) -> Long
    - SetCableData(Name, CableType, NumSegs, Weight, ProjectedLoad, Value, UseDeformedGeom, ModelUsingFrames) -> Long
    - GetCableGeometry(Name, NumberPoints, x[], y[], z[], Sag[], Dist[], RD[], CSys) -> Long
    - Count() -> Long
    - GetNameList() -> (NumberNames, MyName[], ret)

Usage:
    from PySap2000 import Application
    from PySap2000.structure_core import Cable, CableType
    
    with Application() as app:
        # Create a cable by point names
        app.create_object(Cable(no=1, start_point="1", end_point="2", section="CAB1"))
        
        # Set cable data
        cable.set_cable_data(model, CableType.LOW_POINT_VERTICAL_SAG, value=24)
        
        # Get cable geometry
        geometry = cable.get_cable_geometry(model)
"""

import math
from dataclasses import dataclass, field
from typing import Optional, List, Union, ClassVar, Tuple

from PySap2000.cable.enums import CableType
from PySap2000.com_helper import com_ret, com_data


@dataclass
class CableGeometry:
    """
    Cable geometry data returned by `GetCableGeometry`.
    """
    number_points: int = 0
    x: Tuple[float, ...] = ()  # X coordinates [L]
    y: Tuple[float, ...] = ()  # Y coordinates [L]
    z: Tuple[float, ...] = ()  # Z coordinates [L]
    sag: Tuple[float, ...] = ()  # Sag values [L]
    distance: Tuple[float, ...] = ()  # Distance along cable [L]
    relative_distance: Tuple[float, ...] = ()  # Relative distance values


@dataclass
class CableParameters:
    """
    Cable parameter data returned by `GetCableData`.
    """
    tension_i_end: float = 0.0           # Parameter(0): I-end tension [F]
    tension_j_end: float = 0.0           # Parameter(1): J-end tension [F]
    horizontal_tension: float = 0.0      # Parameter(2): Horizontal tension component [F]
    max_deformed_sag: float = 0.0        # Parameter(3): Maximum deformed sag [L]
    deformed_low_point_sag: float = 0.0  # Parameter(4): Deformed low-point sag [L]
    deformed_length: float = 0.0         # Parameter(5): Deformed length [L]
    deformed_relative_length: float = 0.0  # Parameter(6): Deformed relative length
    max_undeformed_sag: float = 0.0      # Parameter(7): Maximum undeformed sag [L]
    undeformed_low_point_sag: float = 0.0  # Parameter(8): Undeformed low-point sag [L]
    undeformed_length: float = 0.0       # Parameter(9): Undeformed length [L]
    undeformed_relative_length: float = 0.0  # Parameter(10): Undeformed relative length


@dataclass
class Cable:
    """
    Cable element data object.

    Maps to SAP2000 `CableObj`.
    
    Attributes:
        no: Cable identifier or name
        start_point: Start point name (I-End)
        end_point: End point name (J-End)
        section: Section name
        cable_type: Cable definition type
        tension: Tension-related value depending on `cable_type`
    """
    
    # Required fields
    no: Union[int, str] = None
    
    # Defined by point names
    start_point: Optional[Union[int, str]] = None
    end_point: Optional[Union[int, str]] = None
    
    # Defined by coordinates
    start_x: Optional[float] = None
    start_y: Optional[float] = None
    start_z: Optional[float] = None
    end_x: Optional[float] = None
    end_y: Optional[float] = None
    end_z: Optional[float] = None
    
    # Section
    section: str = ""
    
    # Cable properties (API: GetCableData/SetCableData)
    cable_type: CableType = CableType.MINIMUM_TENSION_AT_I_END
    num_segs: int = 1  # Internal segment count
    added_weight: float = 0.0  # Added weight [F/L]
    projected_load: float = 0.0  # Projected uniform load [F/L]
    cable_value: float = 0.0  # Definition parameter value (depends on `cable_type`)
    use_deformed_geom: bool = False  # Whether to use deformed geometry
    model_using_frames: bool = False  # Whether to model using frame elements
    
    # Cable parameters (read-only, from `GetCableData`)
    parameters: Optional[CableParameters] = None
    
    # Optional fields
    coordinate_system: str = "Global"
    comment: str = ""
    guid: Optional[str] = None
    
    # Read-only fields
    length: Optional[float] = field(default=None, repr=False)
    
    # Class attributes
    _object_type: ClassVar[str] = "CableObj"
    
    def _create(self, model) -> int:
        """
        Create cable object in SAP2000.
        
        API (point names): AddByPoint(Point1, Point2, Name, PropName, UserName)
        API (coordinates): AddByCoord(xi, yi, zi, xj, yj, zj, Name, PropName, UserName, CSys)
        
        Returns:
            `0` on success
        """
        user_name = str(self.no) if self.no is not None else ""
        section = self.section if self.section else "Default"

        # Check whether cable object already exists
        if user_name:
            from PySap2000.logger import get_logger
            _log = get_logger("cable")
            try:
                existing = self.get_name_list(model)
                if user_name in existing:
                    _log.warning(f"Cable '{user_name}' already exists, skipped")
                    return -1
            except Exception:
                pass

        # Create by coordinates
        if self.start_x is not None and self.end_x is not None:
            result = model.CableObj.AddByCoord(
                self.start_x, self.start_y or 0, self.start_z or 0,
                self.end_x, self.end_y or 0, self.end_z or 0,
                "",  # Name - returned by SAP2000
                section,  # PropName
                user_name,  # UserName
                self.coordinate_system  # CSys
            )
            
            assigned_name = com_data(result, 0)
            if assigned_name:
                self.no = assigned_name
            return com_ret(result)
        
        # Create by point names
        if self.start_point is not None and self.end_point is not None:
            # API: AddByPoint(Point1, Point2, Name, PropName, UserName)
            result = model.CableObj.AddByPoint(
                str(self.start_point),  # Point1
                str(self.end_point),    # Point2
                "",                      # Name - returned by SAP2000
                section,                 # PropName
                user_name                # UserName
            )
            
            assigned_name = com_data(result, 0)
            if assigned_name:
                self.no = assigned_name
            return com_ret(result)
        
        from PySap2000.exceptions import CableError
        raise CableError("Cable creation requires points or coordinates")
    
    def _get(self, model) -> 'Cable':
        """
        Fetch cable-object data from SAP2000.
        
        API: GetPoints(Name, Point1, Point2) -> (Point1, Point2, ret)
        API: GetProperty(Name, PropName) -> (PropName, ret)
        """
        no_str = str(self.no)
        
        # Get endpoints
        # API: GetPoints(Name, Point1, Point2) -> (Point1, Point2, ret)
        result = model.CableObj.GetPoints(no_str)
        self.start_point = com_data(result, 0)
        self.end_point = com_data(result, 1)
        ret = com_ret(result)
        
        if ret != 0:
            from PySap2000.exceptions import CableError
            raise CableError(f"Failed to get endpoints for Cable '{no_str}', ret={ret}")
        
        # Get section
        result = model.CableObj.GetProperty(no_str)
        section = com_data(result, 0)
        if section is not None:
            self.section = section
        
        # Get cable data
        self._get_cable_data(model)
        
        # Get GUID
        self._get_guid(model)
        
        # Compute length
        self._calculate_length(model)
        
        return self
    
    def _get_cable_data(self, model):
        """
        Get cable data
        
        API: GetCableData(Name, CableType, NumSegs, Weight, ProjectedLoad, 
                          UseDeformedGeom, ModelUsingFrames, Parameter[])
        Returns: (CableType, NumSegs, Weight, ProjectedLoad, UseDeformedGeom, 
               ModelUsingFrames, Parameter[], ret)
        """
        try:
            result = model.CableObj.GetCableData(str(self.no))
            if com_data(result, 0) is not None:
                self.cable_type = CableType(com_data(result, 0))
                self.num_segs = com_data(result, 1)
                self.added_weight = com_data(result, 2)
                self.projected_load = com_data(result, 3)
                self.use_deformed_geom = com_data(result, 4)
                self.model_using_frames = com_data(result, 5)
                
                # Parse parameter array
                params = com_data(result, 6)
                if params and len(params) >= 11:
                    self.parameters = CableParameters(
                        tension_i_end=params[0],
                        tension_j_end=params[1],
                        horizontal_tension=params[2],
                        max_deformed_sag=params[3],
                        deformed_low_point_sag=params[4],
                        deformed_length=params[5],
                        deformed_relative_length=params[6],
                        max_undeformed_sag=params[7],
                        undeformed_low_point_sag=params[8],
                        undeformed_length=params[9],
                        undeformed_relative_length=params[10]
                    )
        except Exception:
            pass
    
    def _get_guid(self, model):
        """Get GUID"""
        try:
            result = model.CableObj.GetGUID(str(self.no))
            guid = com_data(result, 0)
            if guid is not None:
                self.guid = guid
        except Exception:
            pass
    
    def _calculate_length(self, model):
        """Compute cable length."""
        try:
            from PySap2000.structure_core.point import Point
            p1 = Point(no=self.start_point)._get(model)
            p2 = Point(no=self.end_point)._get(model)
            self.length = round(
                math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2 + (p2.z - p1.z)**2),
                3
            )
        except Exception:
            self.length = None
    
    @classmethod
    def _get_all(cls, model, nos: List = None) -> List['Cable']:
        """Get all cable objects or specified cable objects"""
        if nos is None:
            nos = cls.get_name_list(model)
        
        cables = []
        for no in nos:
            cable = cls(no=no)
            cable._get(model)
            cables.append(cable)
        
        return cables
    
    def _delete(self, model) -> int:
        """Delete cable object from SAP2000"""
        return model.CableObj.Delete(str(self.no))

    def change_name(self, model, new_name: str) -> int:
        """
        Change cable-object name

        Args:
            model: SapModel object
            new_name: New name

        Returns:
            `0` on success
        """
        ret = model.CableObj.ChangeName(str(self.no), new_name)
        if ret == 0:
            self.no = new_name
        return ret
    
    def _update(self, model) -> int:
        """Update cable-object properties"""
        from PySap2000.logger import get_logger
        _log = get_logger("cable")
        no_str = str(self.no)
        ret = 0
        if self.section:
            try:
                existing = self.get_section_name_list(model)
                if self.section not in existing:
                    _log.warning(f"CableSection '{self.section}' not found")
            except Exception:
                pass
            ret = model.CableObj.SetProperty(no_str, self.section)
        return ret
    
    # ==================== Static methods ====================
    
    @staticmethod
    def get_count(model) -> int:
        """
        Get total number of cable objects
        
        API: Count() -> Long
        """
        return model.CableObj.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """
        Get all cable-object names
        
        API: GetNameList() -> (NumberNames, MyName[], ret)
        """
        result = model.CableObj.GetNameList(0, [])
        count = com_data(result, 0, 0)
        names = com_data(result, 1)
        if count > 0 and names:
            return list(names)
        return []
    
    @staticmethod
    def get_section_name_list(model) -> List[str]:
        """Get all cable section names."""
        result = model.PropCable.GetNameList(0, [])
        count = com_data(result, 0, 0)
        names = com_data(result, 1)
        if count > 0 and names:
            return list(names)
        return []
    
    # ==================== Instance methods ====================
    
    def set_section(self, model, section_name: str) -> int:
        """Set section."""
        self.section = section_name
        return model.CableObj.SetProperty(str(self.no), section_name)
    
    def set_guid(self, model, guid: str) -> int:
        """Set GUID"""
        self.guid = guid
        return model.CableObj.SetGUID(str(self.no), guid)
    
    def set_cable_data(
        self,
        model,
        cable_type: CableType = None,
        num_segs: int = None,
        weight: float = None,
        projected_load: float = None,
        value: float = None,
        use_deformed_geom: bool = None,
        model_using_frames: bool = None
    ) -> int:
        """
        Set cable data
        
        API: SetCableData(Name, CableType, NumSegs, Weight, ProjectedLoad, 
                          Value, UseDeformedGeom, ModelUsingFrames) -> Long
        
        Args:
            model: SapModel object
            cable_type: Cable definition type
            num_segs: Internal segment count
            weight: Added weight [F/L]
            projected_load: Projected uniform load [F/L]
            value: Definition parameter value; meaning depends on `cable_type`:
                   - CableType 1,2: unused
                   - CableType 3: I-end tension [F]
                   - CableType 4: J-end tension [F]
                   - CableType 5: horizontal tension component [F]
                   - CableType 6: maximum vertical sag [L]
                   - CableType 7: lowest-point vertical sag [L]
                   - CableType 8: undeformed length [L]
                   - CableType 9: Relative undeformed length
            use_deformed_geom: Whether to use deformed geometry
            model_using_frames: Whether to model using frame elements
            
        Returns:
            `0` on success
        """
        # Use current value or default
        if cable_type is not None:
            self.cable_type = cable_type
        if num_segs is not None:
            self.num_segs = num_segs
        if weight is not None:
            self.added_weight = weight
        if projected_load is not None:
            self.projected_load = projected_load
        if value is not None:
            self.cable_value = value
        if use_deformed_geom is not None:
            self.use_deformed_geom = use_deformed_geom
        if model_using_frames is not None:
            self.model_using_frames = model_using_frames
        
        return model.CableObj.SetCableData(
            str(self.no),
            int(self.cable_type),
            self.num_segs,
            self.added_weight,
            self.projected_load,
            self.cable_value,
            self.use_deformed_geom,
            self.model_using_frames
        )
    
    def get_cable_data(self, model) -> Optional[CableParameters]:
        """
        Get cable data
        
        Returns:
            `CableParameters` object containing all cable parameters
        """
        self._get_cable_data(model)
        return self.parameters
    
    def get_cable_geometry(
        self, 
        model, 
        csys: str = "Global"
    ) -> Optional[CableGeometry]:
        """
        Get cable geometry data
        
        API: GetCableGeometry(Name, NumberPoints, x[], y[], z[], 
                              Sag[], Dist[], RD[], CSys) -> Long
        
        Args:
            model: SapModel object
            csys: Coordinate-system name
            
        Returns:
            `CableGeometry` object
        """
        try:
            result = model.CableObj.GetCableGeometry(str(self.no), csys)
            if com_data(result, 0) is not None:
                return CableGeometry(
                    number_points=com_data(result, 0, 0),
                    x=tuple(com_data(result, 1, ())),
                    y=tuple(com_data(result, 2, ())),
                    z=tuple(com_data(result, 3, ())),
                    sag=tuple(com_data(result, 4, ())),
                    distance=tuple(com_data(result, 5, ())),
                    relative_distance=tuple(com_data(result, 6, ()))
                )
        except Exception:
            pass
        return None
