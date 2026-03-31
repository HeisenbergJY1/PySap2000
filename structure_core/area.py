# -*- coding: utf-8 -*-
"""
area.py - Area element data object.

Maps to SAP2000 `AreaObj`.

API Reference:
    Create:
    - AddByCoord(NumberPoints, x[], y[], z[], Name, PropName="Default", UserName="", CSys="Global")
    - AddByPoint(NumberPoints, Point[], Name, PropName="Default", UserName="")
    
    Get:
    - GetPoints(Name, NumberPoints, Point[])
    - GetProperty(Name, PropName)
    - GetThickness(Name, ThicknessType, ThicknessPattern, ThicknessPatternSF, Thickness[])
    - GetLocalAxes(Name, Ang, Advanced)
    - GetLocalAxesAdvanced(Name, Active, Plane2, PlVectOpt, PlCSys, PlDir[], PlPt[], PlVect[])
    - GetAutoMesh(Name, MeshType, n1, n2, MaxSize1, MaxSize2, ...)
    - GetModifiers(Name, Value[])
    - GetMass(Name, MassOverL2)
    - GetMaterialOverwrite(Name, PropName)
    - GetMatTemp(Name, Temp, PatternName)
    - GetOffsets(Name, OffsetType, OffsetPattern, OffsetPatternSF, Offset[])
    - GetSpring(Name, NumberSprings, MyType[], s[], SimpleSpringType[], ...)
    - GetGroupAssign(Name, NumberGroups, Groups[])
    - GetSelected(Name, Selected)
    - GetGUID(Name, GUID)
    - GetElm(Name, NumberElms, Elm[])
    - GetEdgeConstraint(Name, ConstraintExists)
    - GetTransformationMatrix(Name, Value[], IsGlobal)
    
    Set:
    - SetProperty(Name, PropName, ItemType)
    - SetThickness(Name, ThicknessType, ThicknessPattern, ThicknessPatternSF, Thickness[], ItemType)
    - SetLocalAxes(Name, Ang, ItemType)
    - SetLocalAxesAdvanced(Name, Active, Plane2, PlVectOpt, PlCSys, PlDir[], PlPt[], PlVect[], ItemType)
    - SetAutoMesh(Name, MeshType, n1, n2, MaxSize1, MaxSize2, ...)
    - SetModifiers(Name, Value[], ItemType)
    - SetMass(Name, MassOverL2, Replace, ItemType)
    - SetMaterialOverwrite(Name, PropName, ItemType)
    - SetMatTemp(Name, Temp, PatternName, ItemType)
    - SetOffsets(Name, OffsetType, OffsetPattern, OffsetPatternSF, Offset[], ItemType)
    - SetSpring(Name, MyType, s, SimpleSpringType, LinkProp, Face, ...)
    - SetGroupAssign(Name, GroupName, Remove, ItemType)
    - SetSelected(Name, Selected, ItemType)
    - SetGUID(Name, GUID)
    - SetEdgeConstraint(Name, ConstraintExists, ItemType)
    
    Loads:
    - SetLoadGravity / GetLoadGravity / DeleteLoadGravity
    - SetLoadUniform / GetLoadUniform / DeleteLoadUniform
    - SetLoadSurfacePressure / GetLoadSurfacePressure / DeleteLoadSurfacePressure
    - SetLoadTemperature / GetLoadTemperature / DeleteLoadTemperature
    - SetLoadPorePressure / GetLoadPorePressure / DeleteLoadPorePressure
    - SetLoadStrain / GetLoadStrain / DeleteLoadStrain
    - SetLoadRotate / GetLoadRotate / DeleteLoadRotate
    - SetLoadUniformToFrame / GetLoadUniformToFrame / DeleteLoadUniformToFrame
    - SetLoadWindPressure_1 / GetLoadWindPressure_1 / DeleteLoadWindPressure
"""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Union, ClassVar
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class AreaType(IntEnum):
    """Area element type."""
    SHELL = 1
    PLANE = 2
    ASOLID = 3


class AreaMeshType(IntEnum):
    """Automatic meshing type for area elements."""
    NO_MESH = 0
    MESH_BY_NUMBER = 1
    MESH_BY_MAX_SIZE = 2
    MESH_BY_POINTS_ON_EDGE = 3
    COOKIE_CUT_BY_LINES = 4
    COOKIE_CUT_BY_POINTS = 5
    GENERAL_DIVIDE = 6


class AreaThicknessType(IntEnum):
    """Thickness overwrite type for area elements."""
    NO_OVERWRITE = 0
    BY_JOINT_PATTERN = 1
    BY_POINT = 2


class AreaOffsetType(IntEnum):
    """Offset type for area elements."""
    NO_OFFSET = 0
    BY_JOINT_PATTERN = 1
    BY_POINT = 2


class AreaSpringType(IntEnum):
    """Spring type for area elements."""
    SIMPLE_SPRING = 1
    LINK_PROPERTY = 2


class AreaSimpleSpringType(IntEnum):
    """Simple spring type for area elements."""
    TENSION_COMPRESSION = 1
    COMPRESSION_ONLY = 2
    TENSION_ONLY = 3


class AreaSpringLocalOneType(IntEnum):
    """Local-1-axis direction type for area springs."""
    PARALLEL_TO_LOCAL_AXIS = 1
    NORMAL_TO_FACE = 2
    USER_VECTOR = 3


class AreaFace(IntEnum):
    """Area face."""
    BOTTOM = -1
    TOP = -2


class AreaLoadDir(IntEnum):
    """Area load direction."""
    LOCAL_1 = 1
    LOCAL_2 = 2
    LOCAL_3 = 3
    GLOBAL_X = 4
    GLOBAL_Y = 5
    GLOBAL_Z = 6
    PROJECTED_X = 7
    PROJECTED_Y = 8
    PROJECTED_Z = 9
    GRAVITY = 10
    PROJECTED_GRAVITY = 11


class AreaTempLoadType(IntEnum):
    """Area temperature-load type."""
    TEMPERATURE = 1
    TEMPERATURE_GRADIENT = 3


class AreaStrainComponent(IntEnum):
    """Area strain component."""
    STRAIN_11 = 1
    STRAIN_22 = 2
    STRAIN_12 = 3
    CURVATURE_11 = 4
    CURVATURE_22 = 5
    CURVATURE_12 = 6


class AreaWindPressureType(IntEnum):
    """Area wind-pressure type."""
    FROM_CP = 1
    FROM_CODE = 2


class AreaDistType(IntEnum):
    """Area load distribution type."""
    ONE_WAY = 1
    TWO_WAY = 2


class PlaneRefVectorOption(IntEnum):
    """Plane reference vector option."""
    COORDINATE_DIRECTION = 1
    TWO_JOINTS = 2
    USER_VECTOR = 3


class ItemType(IntEnum):
    """`eItemType` enum."""
    OBJECT = 0
    GROUP = 1
    SELECTED_OBJECTS = 2


@dataclass
class AreaLoadGravity:
    """Gravity load data for area elements."""
    area_name: str
    load_pattern: str
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    csys: str = "Global"


@dataclass
class AreaLoadUniform:
    """Uniform load data for area elements."""
    area_name: str
    load_pattern: str
    value: float = 0.0
    direction: AreaLoadDir = AreaLoadDir.GRAVITY
    csys: str = "Global"


@dataclass
class AreaLoadSurfacePressure:
    """Surface-pressure load data for area elements."""
    area_name: str
    load_pattern: str
    face: int = -1
    value: float = 0.0
    pattern_name: str = ""


@dataclass
class AreaLoadTemperature:
    """Temperature-load data for area elements."""
    area_name: str
    load_pattern: str
    load_type: AreaTempLoadType = AreaTempLoadType.TEMPERATURE
    value: float = 0.0
    pattern_name: str = ""


@dataclass
class AreaSpring:
    """Spring data for area elements."""
    spring_type: AreaSpringType = AreaSpringType.SIMPLE_SPRING
    stiffness: float = 0.0
    simple_spring_type: AreaSimpleSpringType = AreaSimpleSpringType.TENSION_COMPRESSION
    link_prop: str = ""
    face: int = -1
    local_one_type: AreaSpringLocalOneType = AreaSpringLocalOneType.PARALLEL_TO_LOCAL_AXIS
    direction: int = 3
    outward: bool = True
    vector: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    angle: float = 0.0


@dataclass
class AreaAutoMesh:
    """Automatic meshing settings for area elements."""
    mesh_type: AreaMeshType = AreaMeshType.NO_MESH
    n1: int = 2
    n2: int = 2
    max_size1: float = 0.0
    max_size2: float = 0.0
    point_on_edge_from_line: bool = False
    point_on_edge_from_point: bool = False
    extend_cookie_cut_lines: bool = False
    rotation: float = 0.0
    max_size_general: float = 0.0
    local_axes_on_edge: bool = False
    local_axes_on_face: bool = False
    restraints_on_edge: bool = False
    restraints_on_face: bool = False
    group: str = "ALL"
    sub_mesh: bool = False
    sub_mesh_size: float = 0.0


@dataclass
class AreaLocalAxesAdvanced:
    """Advanced local-axis settings for area elements."""
    active: bool = False
    plane2: int = 31  # 31=3-1 plane, 32=3-2 plane
    pl_vect_opt: PlaneRefVectorOption = PlaneRefVectorOption.COORDINATE_DIRECTION
    pl_csys: str = "Global"
    pl_dir: Tuple[int, int] = (1, 2)  # Primary and secondary directions
    pl_pt: Tuple[str, str] = ("", "")  # Two point names
    pl_vect: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # User vector



@dataclass
class Area:
    """
    Area element data object.

    Maps to SAP2000 `AreaObj`.
    """
    
    # Required attribute
    no: Union[int, str] = None
    
    # Definition by points or coordinates (choose one)
    points: Optional[List[str]] = None  # Point name list
    x_coords: Optional[List[float]] = None  # X-coordinate list
    y_coords: Optional[List[float]] = None  # Y-coordinate list
    z_coords: Optional[List[float]] = None  # Z-coordinate list
    
    # Section property
    section: str = "Default"
    
    # Thickness overwrite
    thickness_type: AreaThicknessType = AreaThicknessType.NO_OVERWRITE
    thickness_pattern: str = ""
    thickness_pattern_sf: float = 1.0
    thickness: Optional[List[float]] = None
    
    # Local axes
    local_axis_angle: float = 0.0
    local_axes_advanced: Optional[AreaLocalAxesAdvanced] = None
    
    # Automatic meshing
    auto_mesh: Optional[AreaAutoMesh] = None
    
    # Modifiers (10 values)
    modifiers: Optional[List[float]] = None
    
    # Additional mass
    mass_per_area: float = 0.0
    
    # Material overwrite
    material_overwrite: Optional[str] = None
    
    # Material temperature
    mat_temp: float = 0.0
    mat_temp_pattern: str = ""
    
    # Offsets
    offset_type: AreaOffsetType = AreaOffsetType.NO_OFFSET
    offset_pattern: str = ""
    offset_pattern_sf: float = 1.0
    offsets: Optional[List[float]] = None
    
    # Springs
    springs: Optional[List[AreaSpring]] = None
    
    # Edge constraint
    edge_constraint: bool = False
    
    # Groups
    groups: Optional[List[str]] = None
    
    # Selection state
    selected: bool = False
    
    # Other metadata
    coordinate_system: str = "Global"
    comment: str = ""
    guid: Optional[str] = None
    
    # Class metadata
    _object_type: ClassVar[str] = "AreaObj"

    # ==================== Creation methods ====================
    
    def _create(self, model) -> int:
        """
        Create an area object in SAP2000.
        
        Returns:
            `0` on success, nonzero on failure
        """
        from PySap2000.logger import get_logger
        _log = get_logger("area")

        user_name = str(self.no) if self.no is not None else ""

        # Check whether it already exists
        if user_name:
            try:
                existing = self.get_name_list(model)
                if user_name in existing:
                    _log.warning(f"Area '{user_name}' already exists, skipped")
                    return -1
            except Exception:
                pass

        if self.points is not None:
            return self._create_by_point(model, user_name)
        elif self.x_coords is not None:
            return self._create_by_coord(model, user_name)
        else:
            from PySap2000.exceptions import AreaError
            raise AreaError("Area creation requires points or coordinates")
    
    def _create_by_point(self, model, user_name: str) -> int:
        """Create an area object from point names"""
        num_points = len(self.points)
        result = model.AreaObj.AddByPoint(
            num_points,
            self.points,
            "",
            self.section,
            user_name
        )
        return self._parse_create_result(result)
    
    def _create_by_coord(self, model, user_name: str) -> int:
        """Create an area object from coordinates"""
        num_points = len(self.x_coords)
        result = model.AreaObj.AddByCoord(
            num_points,
            self.x_coords,
            self.y_coords,
            self.z_coords,
            "",
            self.section,
            user_name,
            self.coordinate_system
        )
        return self._parse_create_result(result)
    
    def _parse_create_result(self, result) -> int:
        """Parse creation result"""
        ret = com_ret(result)
        # assigned name: 3if there are 3+ elements it is at the second-to-last index, otherwise the first index
        if com_data(result, 2) is not None:
            assigned_name = com_data(result, -2)
        else:
            assigned_name = com_data(result, 0)
        if isinstance(assigned_name, str) and assigned_name:
            self.no = assigned_name
        return ret

    # ==================== Fetch methods ====================
    
    def _get(self, model) -> 'Area':
        """Fetch area-object data from SAP2000."""
        self._get_points(model)
        self._get_property(model)
        self._get_local_axes(model)
        self._get_auto_mesh(model)
        self._get_modifiers(model)
        self._get_mass(model)
        self._get_group_assign(model)
        self._get_selected(model)
        self._get_guid(model)
        return self
    
    def _get_points(self, model) -> Optional[List[str]]:
        """
        Get area-object point names
        API: GetPoints(Name, NumberPoints, Point[])
        """
        try:
            result = model.AreaObj.GetPoints(str(self.no), 0, [])
            num_points = com_data(result, 0)
            points = com_data(result, 1)
            ret = com_ret(result)
            if ret == 0 and points:
                self.points = list(points)
                return self.points
        except Exception:
            pass
        return None
    
    def _get_property(self, model) -> Optional[str]:
        """Get area section-property name"""
        try:
            result = model.AreaObj.GetProperty(str(self.no), "")
            prop = com_data(result, 0)
            if prop is not None:
                self.section = prop
                return self.section
        except Exception:
            pass
        return None
    
    def _get_local_axes(self, model) -> Optional[float]:
        """Get local-axis angle"""
        try:
            result = model.AreaObj.GetLocalAxes(str(self.no), 0.0, False)
            angle = com_data(result, 0)
            advanced = com_data(result, 1)
            if angle is not None:
                self.local_axis_angle = angle
                if advanced:
                    self._get_local_axes_advanced(model)
                return self.local_axis_angle
        except Exception:
            pass
        return None
    
    def _get_local_axes_advanced(self, model) -> Optional[AreaLocalAxesAdvanced]:
        """
        Get advanced local-axis settings
        API: GetLocalAxesAdvanced(Name, Active, Plane2, PlVectOpt, PlCSys, PlDir[], PlPt[], PlVect[])
        """
        try:
            result = model.AreaObj.GetLocalAxesAdvanced(
                str(self.no), False, 0, 0, "", [], [], []
            )
            if com_data(result, 7) is not None:
                active = com_data(result, 0)
                plane2 = com_data(result, 1)
                pl_vect_opt = com_data(result, 2)
                pl_csys = com_data(result, 3)
                pl_dir = com_data(result, 4)
                pl_pt = com_data(result, 5)
                pl_vect = com_data(result, 6)
                ret = com_ret(result)
                
                if ret == 0 and active:
                    self.local_axes_advanced = AreaLocalAxesAdvanced(
                        active=active,
                        plane2=plane2,
                        pl_vect_opt=PlaneRefVectorOption(pl_vect_opt) if pl_vect_opt else PlaneRefVectorOption.COORDINATE_DIRECTION,
                        pl_csys=pl_csys or "Global",
                        pl_dir=tuple(pl_dir) if pl_dir else (1, 2),
                        pl_pt=tuple(pl_pt) if pl_pt else ("", ""),
                        pl_vect=tuple(pl_vect) if pl_vect else (0.0, 0.0, 0.0)
                    )
                    return self.local_axes_advanced
        except Exception:
            pass
        return None
    
    def _get_auto_mesh(self, model) -> Optional[AreaAutoMesh]:
        """Get automatic meshing settings"""
        try:
            result = model.AreaObj.GetAutoMesh(
                str(self.no), 0, 0, 0, 0.0, 0.0, False, False, False, 0.0, 0.0,
                False, False, False, False, "", False, 0.0
            )
            if com_data(result, 17) is not None:
                self.auto_mesh = AreaAutoMesh(
                    mesh_type=AreaMeshType(com_data(result, 0)) if com_data(result, 0) is not None else AreaMeshType.NO_MESH,
                    n1=com_data(result, 1) or 2,
                    n2=com_data(result, 2) or 2,
                    max_size1=com_data(result, 3) or 0.0,
                    max_size2=com_data(result, 4) or 0.0,
                    point_on_edge_from_line=com_data(result, 5) or False,
                    point_on_edge_from_point=com_data(result, 6) or False,
                    extend_cookie_cut_lines=com_data(result, 7) or False,
                    rotation=com_data(result, 8) or 0.0,
                    max_size_general=com_data(result, 9) or 0.0,
                    local_axes_on_edge=com_data(result, 10) or False,
                    local_axes_on_face=com_data(result, 11) or False,
                    restraints_on_edge=com_data(result, 12) or False,
                    restraints_on_face=com_data(result, 13) or False,
                    group=com_data(result, 14) or "ALL",
                    sub_mesh=com_data(result, 15) or False,
                    sub_mesh_size=com_data(result, 16) or 0.0
                )
                return self.auto_mesh
        except Exception:
            pass
        return None
    
    def _get_modifiers(self, model) -> Optional[List[float]]:
        """Get modifiers"""
        try:
            result = model.AreaObj.GetModifiers(str(self.no), [])
            modifiers = com_data(result, 0)
            ret = com_ret(result)
            if ret == 0 and modifiers:
                    self.modifiers = list(modifiers)
                    return self.modifiers
        except Exception:
            pass
        return None
    
    def _get_mass(self, model) -> Optional[float]:
        """Get added mass"""
        try:
            result = model.AreaObj.GetMass(str(self.no), 0.0)
            mass = com_data(result, 0)
            if mass is not None:
                self.mass_per_area = mass
                return self.mass_per_area
        except Exception:
            pass
        return None
    
    def _get_group_assign(self, model) -> Optional[List[str]]:
        """Get groups containing this area object"""
        try:
            result = model.AreaObj.GetGroupAssign(str(self.no), 0, [])
            num_groups = com_data(result, 0, 0)
            groups = com_data(result, 1)
            if num_groups > 0 and groups:
                    self.groups = list(groups)
                    return self.groups
        except Exception:
            pass
        return None
    
    def _get_selected(self, model) -> bool:
        """Get selection state"""
        try:
            result = model.AreaObj.GetSelected(str(self.no), False)
            selected = com_data(result, 0)
            if selected is not None:
                self.selected = selected
                return self.selected
        except Exception:
            pass
        return False
    
    def _get_guid(self, model):
        """Get area-object GUID"""
        try:
            result = model.AreaObj.GetGUID(str(self.no), "")
            guid = com_data(result, 0)
            if guid is not None:
                self.guid = guid
        except Exception:
            pass


    # ==================== Public query methods ====================
    
    @classmethod
    def get_all(cls, model, names: List[str] = None) -> List['Area']:
        """
        Get all area objects
        
        Args:
            model: SapModel object
            names: Optional list of area-object names. If `None`, gets all area objects
            
        Returns:
            List of `Area` objects with populated data
            
        Example:
            # Get all area objects
            areas = Area.get_all(model)
            for a in areas:
                print(f"{a.no}: section={a.section}, points={a.points}")
            
            # Get specific area objects
            areas = Area.get_all(model, ["1", "2", "3"])
        """
        if names is None:
            names = cls.get_name_list(model)
        
        areas = []
        for name in names:
            area = cls(no=name)
            area._get(model)
            areas.append(area)
        
        return areas
    
    @classmethod
    def get_by_name(cls, model, name: str) -> 'Area':
        """
        Get area object by name
        
        Args:
            model: SapModel object
            name: Area object name
            
        Returns:
            Populated `Area` object
            
        Example:
            area = Area.get_by_name(model, "1")
            print(f"Section: {area.section}, Points: {area.points}")
        """
        area = cls(no=name)
        area._get(model)
        return area
    
    @staticmethod
    def get_count(model) -> int:
        """
        Get total number of area objects
        
        Args:
            model: SapModel object
            
        Returns:
            Area-object count
        """
        return model.AreaObj.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """
        Get all area-object names
        
        Args:
            model: SapModel object
            
        Returns:
            List of area-object names
        """
        result = model.AreaObj.GetNameList(0, [])
        
        names = com_data(result, 1)
        if names is not None:
            return list(names)
        return []
    
    @staticmethod
    def get_section_name_list(model) -> List[str]:
        """
        Get all area section-property names
        
        Args:
            model: SapModel object
            
        Returns:
            List of section-property names
        """
        result = model.PropArea.GetNameList(0, [])
        
        names = com_data(result, 1)
        if names is not None:
            return list(names)
        return []

    # ==================== Delete and update methods ====================
    
    def _delete(self, model) -> int:
        """
        Delete area object from SAP2000.
        
        Returns:
            `0` on success, nonzero on failure
        """
        return model.AreaObj.Delete(str(self.no), ItemType.OBJECT)
    
    def _update(self, model) -> int:
        """Update area-object properties to SAP2000"""
        from PySap2000.logger import get_logger
        _log = get_logger("area")
        ret = 0
        if self.section:
            try:
                existing = self.get_section_name_list(model)
                if self.section not in existing:
                    _log.warning(f"AreaSection '{self.section}' not found")
            except Exception:
                pass
            ret = model.AreaObj.SetProperty(str(self.no), self.section, ItemType.OBJECT)
        return ret

    # ==================== Section-property methods ====================
    
    def set_property(
        self,
        model,
        prop_name: str,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area section property
        
        Args:
            model: SapModel object
            prop_name: Section-property name
            item_type: Item type
            
        Returns:
            `0` on success
        """
        self.section = prop_name
        return model.AreaObj.SetProperty(str(self.no), prop_name, item_type)
    
    def get_property(self, model) -> Optional[str]:
        """Get area section-property name"""
        return self._get_property(model)

    # ==================== Thickness methods ====================
    
    def set_thickness(
        self,
        model,
        thickness_type: AreaThicknessType,
        thickness_pattern: str,
        thickness_pattern_sf: float,
        thickness: List[float],
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area thickness override
        
        Args:
            model: SapModel object
            thickness_type: Thickness type
            thickness_pattern: Thickness-pattern name
            thickness_pattern_sf: Thickness-pattern scale factor
            thickness: Thickness values (one value per point)
            item_type: Item type
            
        Returns:
            `0` on success
        """
        self.thickness_type = thickness_type
        self.thickness_pattern = thickness_pattern
        self.thickness_pattern_sf = thickness_pattern_sf
        self.thickness = thickness
        
        return model.AreaObj.SetThickness(
            str(self.no), thickness_type, thickness_pattern,
            thickness_pattern_sf, thickness, item_type
        )
    
    def get_thickness(self, model) -> Optional[dict]:
        """
        Get area thickness override
        
        Returns:
            Dictionary with thickness info, or `None` on failure
        """
        try:
            result = model.AreaObj.GetThickness(str(self.no), 0, "", 0.0, [])
            if com_data(result, 4) is not None:
                self.thickness_type = AreaThicknessType(com_data(result, 0)) if com_data(result, 0) is not None else AreaThicknessType.NO_OVERWRITE
                self.thickness_pattern = com_data(result, 1) or ""
                self.thickness_pattern_sf = com_data(result, 2) or 1.0
                self.thickness = list(com_data(result, 3)) if com_data(result, 3) else None
                return {
                    "thickness_type": self.thickness_type,
                    "thickness_pattern": self.thickness_pattern,
                    "thickness_pattern_sf": self.thickness_pattern_sf,
                    "thickness": self.thickness
                }
        except Exception:
            pass
        return None

    # ==================== Local-axis methods ====================
    
    def set_local_axes(
        self,
        model,
        angle: float,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area local-axis angle
        
        Args:
            model: SapModel object
            angle: Local-axis angle [deg]
            item_type: Item type
            
        Returns:
            `0` on success
        """
        self.local_axis_angle = angle
        return model.AreaObj.SetLocalAxes(str(self.no), angle, item_type)
    
    def get_local_axes(self, model) -> Optional[Tuple[float, bool]]:
        """
        Get area local-axis angle
        
        Returns:
            (Angle, whether advanced settings exist) tuple, or `None` on failure
        """
        try:
            result = model.AreaObj.GetLocalAxes(str(self.no), 0.0, False)
            angle = com_data(result, 0)
            advanced = com_data(result, 1)
            if angle is not None:
                self.local_axis_angle = angle
                return (self.local_axis_angle, advanced)
        except Exception:
            pass
        return None
    
    def set_local_axes_advanced(
        self,
        model,
        active: bool,
        plane2: int = 31,
        pl_vect_opt: PlaneRefVectorOption = PlaneRefVectorOption.COORDINATE_DIRECTION,
        pl_csys: str = "Global",
        pl_dir: Tuple[int, int] = (1, 2),
        pl_pt: Tuple[str, str] = ("", ""),
        pl_vect: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set advanced area local axes
        
        Args:
            model: SapModel object
            active: Whether advanced local axes are enabled
            plane2: 31=3-1plane, 32=3-2plane
            pl_vect_opt: plane reference-vector option (1=coordinate direction, 2=two points, 3=user vector)
            pl_csys: Coordinate-system name
            pl_dir: primary and secondary directions (used for pl_vect_opt=1)
            pl_pt: two point names (used for pl_vect_opt=2)
            pl_vect: user vector (used for pl_vect_opt=3)
            item_type: Item type
            
        Returns:
            `0` on success
            
        Example:
            # Define by coordinate direction
            area.set_local_axes_advanced(model, True, 31, PlaneRefVectorOption.COORDINATE_DIRECTION,
                                         "Global", (2, 3))
        """
        self.local_axes_advanced = AreaLocalAxesAdvanced(
            active=active,
            plane2=plane2,
            pl_vect_opt=pl_vect_opt,
            pl_csys=pl_csys,
            pl_dir=pl_dir,
            pl_pt=pl_pt,
            pl_vect=pl_vect
        )
        
        return model.AreaObj.SetLocalAxesAdvanced(
            str(self.no), active, plane2, int(pl_vect_opt), pl_csys,
            list(pl_dir), list(pl_pt), list(pl_vect), item_type
        )
    
    def get_local_axes_advanced(self, model) -> Optional[AreaLocalAxesAdvanced]:
        """
        Get advanced area local-axis settings
        
        Returns:
            AreaLocalAxesAdvanced object, or `None` on failure
        """
        return self._get_local_axes_advanced(model)

    # ==================== Transformation-matrix methods ====================
    
    def get_transformation_matrix(self, model, is_global: bool = True) -> Optional[List[float]]:
        """
        Get area transformation matrix
        
        The transformation matrix maps local coordinates to global (or current) coordinates.
        The matrix includes 9 direction-cosine values.
        
        Args:
            model: SapModel object
            is_global: True=global coordinate system, False=current coordinate system
            
        Returns:
            List of 9 direction-cosine values `[c0, c1, c2, c3, c4, c5, c6, c7, c8]`, or `None` on failure
            
        Example:
            matrix = area.get_transformation_matrix(model)
            if matrix:
                # Matrix equation: [GlobalX, GlobalY, GlobalZ] = [c0-c8] * [Local1, Local2, Local3]
                print(f"Transformation matrix: {matrix}")
        """
        try:
            result = model.AreaObj.GetTransformationMatrix(str(self.no), [], is_global)
            matrix = com_data(result, 0)
            ret = com_ret(result)
            if ret == 0 and matrix:
                    return list(matrix)
        except Exception:
            pass
        return None


    # ==================== Auto-mesh methods ====================
    
    def set_auto_mesh(
        self,
        model,
        mesh_type: AreaMeshType,
        n1: int = 2,
        n2: int = 2,
        max_size1: float = 0.0,
        max_size2: float = 0.0,
        point_on_edge_from_line: bool = False,
        point_on_edge_from_point: bool = False,
        extend_cookie_cut_lines: bool = False,
        rotation: float = 0.0,
        max_size_general: float = 0.0,
        local_axes_on_edge: bool = False,
        local_axes_on_face: bool = False,
        restraints_on_edge: bool = False,
        restraints_on_face: bool = False,
        group: str = "ALL",
        sub_mesh: bool = False,
        sub_mesh_size: float = 0.0,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area automatic meshing
        
        Args:
            model: SapModel object
            mesh_type: Mesh type
            n1, n2: Division counts (used for MESH_BY_NUMBER)
            max_size1, max_size2: Maximum size (used for MESH_BY_MAX_SIZE)
            Other parameters: see SAP2000 API documentation
            item_type: Item type
            
        Returns:
            `0` on success
        """
        self.auto_mesh = AreaAutoMesh(
            mesh_type=mesh_type,
            n1=n1, n2=n2,
            max_size1=max_size1, max_size2=max_size2,
            point_on_edge_from_line=point_on_edge_from_line,
            point_on_edge_from_point=point_on_edge_from_point,
            extend_cookie_cut_lines=extend_cookie_cut_lines,
            rotation=rotation,
            max_size_general=max_size_general,
            local_axes_on_edge=local_axes_on_edge,
            local_axes_on_face=local_axes_on_face,
            restraints_on_edge=restraints_on_edge,
            restraints_on_face=restraints_on_face,
            group=group,
            sub_mesh=sub_mesh,
            sub_mesh_size=sub_mesh_size
        )
        
        return model.AreaObj.SetAutoMesh(
            str(self.no), int(mesh_type), n1, n2, max_size1, max_size2,
            point_on_edge_from_line, point_on_edge_from_point,
            extend_cookie_cut_lines, rotation, max_size_general,
            local_axes_on_edge, local_axes_on_face,
            restraints_on_edge, restraints_on_face,
            group, sub_mesh, sub_mesh_size, item_type
        )
    
    def get_auto_mesh(self, model) -> Optional[AreaAutoMesh]:
        """Get area automatic-meshing settings."""
        return self._get_auto_mesh(model)

    # ==================== Modifier methods ====================
    
    def set_modifiers(
        self,
        model,
        modifiers: List[float],
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area modifiers
        
        Args:
            model: SapModel object
            modifiers: 10modifier values
                [f11, f22, f12, m11, m22, m12, v13, v23, mass, weight]
            item_type: Item type
            
        Returns:
            `0` on success
        """
        # Ensure there are10values
        mod_list = list(modifiers)
        while len(mod_list) < 10:
            mod_list.append(1.0)
        
        self.modifiers = mod_list[:10]
        result = model.AreaObj.SetModifiers(str(self.no), mod_list[:10], item_type)
        # Parse return value
        return com_ret(result)
    
    def get_modifiers(self, model) -> Optional[List[float]]:
        """Get area modifiers."""
        return self._get_modifiers(model)
    
    def delete_modifiers(self, model, item_type: ItemType = ItemType.OBJECT) -> int:
        """Delete area modifiers (restore defaults)"""
        self.modifiers = None
        return model.AreaObj.DeleteModifiers(str(self.no), item_type)

    # ==================== Mass methods ====================
    
    def set_mass(
        self,
        model,
        mass_per_area: float,
        replace: bool = True,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set added area mass
        
        Args:
            model: SapModel object
            mass_per_area: Mass per unit area
            replace: Whether to replace existing mass (True=replace, False=add)
            item_type: Item type
            
        Returns:
            `0` on success
        """
        self.mass_per_area = mass_per_area
        return model.AreaObj.SetMass(str(self.no), mass_per_area, replace, item_type)
    
    def get_mass(self, model) -> Optional[float]:
        """Get added area mass"""
        return self._get_mass(model)
    
    def delete_mass(self, model, item_type: ItemType = ItemType.OBJECT) -> int:
        """Delete added area mass"""
        self.mass_per_area = 0.0
        return model.AreaObj.DeleteMass(str(self.no), item_type)

    # ==================== Material-override methods ====================
    
    def set_material_overwrite(
        self,
        model,
        prop_name: str,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area material override
        
        Args:
            model: SapModel object
            prop_name: Material name
            item_type: Item type
            
        Returns:
            `0` on success
        """
        self.material_overwrite = prop_name
        return model.AreaObj.SetMaterialOverwrite(str(self.no), prop_name, item_type)
    
    def get_material_overwrite(self, model) -> Optional[str]:
        """Get area material override"""
        try:
            result = model.AreaObj.GetMaterialOverwrite(str(self.no), "")
            mat = com_data(result, 0)
            if mat is not None:
                self.material_overwrite = mat
                return self.material_overwrite
        except Exception:
            pass
        return None

    # ==================== Material-temperature methods ====================
    
    def set_mat_temp(
        self,
        model,
        temp: float,
        pattern_name: str = "",
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area material temperature
        
        Args:
            model: SapModel object
            temp: Temperature value
            pattern_name: Temperature-pattern name
            item_type: Item type
            
        Returns:
            `0` on success
        """
        self.mat_temp = temp
        self.mat_temp_pattern = pattern_name
        return model.AreaObj.SetMatTemp(str(self.no), temp, pattern_name, item_type)
    
    def get_mat_temp(self, model) -> Optional[Tuple[float, str]]:
        """Get area material temperature"""
        try:
            result = model.AreaObj.GetMatTemp(str(self.no), 0.0, "")
            if com_data(result, 2) is not None:
                self.mat_temp = com_data(result, 0)
                self.mat_temp_pattern = com_data(result, 1)
                return (self.mat_temp, self.mat_temp_pattern)
        except Exception:
            pass
        return None

    # ==================== Offset methods ====================
    
    def set_offsets(
        self,
        model,
        offset_type: AreaOffsetType,
        offset_pattern: str,
        offset_pattern_sf: float,
        offsets: List[float],
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area offsets
        
        Args:
            model: SapModel object
            offset_type: Offset type
            offset_pattern: Offset-pattern name
            offset_pattern_sf: Offset-pattern scale factor
            offsets: Offset values (one value per point)
            item_type: Item type
            
        Returns:
            `0` on success
        """
        self.offset_type = offset_type
        self.offset_pattern = offset_pattern
        self.offset_pattern_sf = offset_pattern_sf
        self.offsets = offsets
        
        return model.AreaObj.SetOffsets(
            str(self.no), int(offset_type), offset_pattern,
            offset_pattern_sf, offsets, item_type
        )
    
    def get_offsets(self, model) -> Optional[dict]:
        """Get area offsets"""
        try:
            result = model.AreaObj.GetOffsets(str(self.no), 0, "", 0.0, [])
            if com_data(result, 4) is not None:
                self.offset_type = AreaOffsetType(com_data(result, 0)) if com_data(result, 0) is not None else AreaOffsetType.NO_OFFSET
                self.offset_pattern = com_data(result, 1) or ""
                self.offset_pattern_sf = com_data(result, 2) or 1.0
                self.offsets = list(com_data(result, 3)) if com_data(result, 3) else None
                return {
                    "offset_type": self.offset_type,
                    "offset_pattern": self.offset_pattern,
                    "offset_pattern_sf": self.offset_pattern_sf,
                    "offsets": self.offsets
                }
        except Exception:
            pass
        return None

    # ==================== Spring methods ====================
    
    def set_spring(
        self,
        model,
        spring_type: AreaSpringType,
        stiffness: float,
        simple_spring_type: AreaSimpleSpringType = AreaSimpleSpringType.TENSION_COMPRESSION,
        link_prop: str = "",
        face: int = -1,
        local_one_type: AreaSpringLocalOneType = AreaSpringLocalOneType.PARALLEL_TO_LOCAL_AXIS,
        direction: int = 3,
        outward: bool = True,
        vector: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        angle: float = 0.0,
        replace: bool = True,
        csys: str = "Local",
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area springs
        
        Args:
            model: SapModel object
            spring_type: Spring type
            stiffness: Spring stiffness
            simple_spring_type: Simple spring type
            link_prop: Link-property name (used for LINK_PROPERTY type)
            face: Face (-1=bottom face, -2=top face)
            local_one_type: local-1 direction type
            direction: Direction
            outward: Whether outward
            vector: user vector
            angle: Angle
            replace: Whether to replace existing springs
            csys: Coordinate system
            item_type: Item type
            
        Returns:
            `0` on success
        """
        return model.AreaObj.SetSpring(
            str(self.no), int(spring_type), stiffness, int(simple_spring_type),
            link_prop, face, int(local_one_type), direction, outward,
            list(vector), angle, replace, csys, item_type
        )
    
    def get_spring(self, model) -> Optional[List[AreaSpring]]:
        """Get area springs."""
        try:
            result = model.AreaObj.GetSpring(
                str(self.no), 0, [], [], [], [], [], [], [], [], [], []
            )
            if com_data(result, 11) is not None:
                num_springs = com_data(result, 0, 0)
                if num_springs > 0:
                    springs = []
                    types = com_data(result, 1)
                    stiffnesses = com_data(result, 2)
                    simple_types = com_data(result, 3)
                    link_props = com_data(result, 4)
                    faces = com_data(result, 5)
                    local_one_types = com_data(result, 6)
                    directions = com_data(result, 7)
                    outwards = com_data(result, 8)
                    vectors = com_data(result, 9)
                    angles = com_data(result, 10)
                    
                    for i in range(num_springs):
                        springs.append(AreaSpring(
                            spring_type=AreaSpringType(types[i]) if types else AreaSpringType.SIMPLE_SPRING,
                            stiffness=stiffnesses[i] if stiffnesses else 0.0,
                            simple_spring_type=AreaSimpleSpringType(simple_types[i]) if simple_types else AreaSimpleSpringType.TENSION_COMPRESSION,
                            link_prop=link_props[i] if link_props else "",
                            face=faces[i] if faces else -1,
                            local_one_type=AreaSpringLocalOneType(local_one_types[i]) if local_one_types else AreaSpringLocalOneType.PARALLEL_TO_LOCAL_AXIS,
                            direction=directions[i] if directions else 3,
                            outward=outwards[i] if outwards else True,
                            vector=tuple(vectors[i]) if vectors and vectors[i] else (0.0, 0.0, 0.0),
                            angle=angles[i] if angles else 0.0
                        ))
                    self.springs = springs
                    return springs
        except Exception:
            pass
        return None
    
    def delete_spring(self, model, item_type: ItemType = ItemType.OBJECT) -> int:
        """Delete area springs."""
        self.springs = None
        return model.AreaObj.DeleteSpring(str(self.no), item_type)


    # ==================== Edge-constraint methods ====================
    
    def set_edge_constraint(
        self,
        model,
        constraint_exists: bool,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area edge constraints
        
        Args:
            model: SapModel object
            constraint_exists: Whether edge constraints exist
            item_type: Item type
            
        Returns:
            `0` on success
        """
        self.edge_constraint = constraint_exists
        return model.AreaObj.SetEdgeConstraint(str(self.no), constraint_exists, item_type)
    
    def get_edge_constraint(self, model) -> bool:
        """Get area edge constraints."""
        try:
            result = model.AreaObj.GetEdgeConstraint(str(self.no), False)
            ec = com_data(result, 0)
            if ec is not None:
                self.edge_constraint = ec
                return self.edge_constraint
        except Exception:
            pass
        return False

    # ==================== Group methods ====================
    
    def set_group_assign(
        self,
        model,
        group_name: str,
        remove: bool = False,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area group assignment
        
        Args:
            model: SapModel object
            group_name: Group name
            remove: Whether to remove from group (True=remove, False=add)
            item_type: Item type
            
        Returns:
            `0` on success
        """
        ret = model.AreaObj.SetGroupAssign(str(self.no), group_name, remove, item_type)
        if ret == 0:
            if self.groups is None:
                self.groups = []
            if remove:
                if group_name in self.groups:
                    self.groups.remove(group_name)
            else:
                if group_name not in self.groups:
                    self.groups.append(group_name)
        return ret
    
    def get_group_assign(self, model) -> Optional[List[str]]:
        """Get groups containing this area object"""
        return self._get_group_assign(model)

    # ==================== Selection methods ====================
    
    def set_selected(
        self,
        model,
        selected: bool = True,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """Set selection state"""
        self.selected = selected
        return model.AreaObj.SetSelected(str(self.no), selected, item_type)
    
    def get_selected(self, model) -> bool:
        """Get selection state"""
        return self._get_selected(model)

    # ==================== GUID methods ====================
    
    def set_guid(self, model, guid: str = "") -> int:
        """
        Set area GUID
        
        Args:
            model: SapModel object
            guid: GUID string. If empty, SAP2000 creates a new GUID
            
        Returns:
            `0` on success
        """
        ret = model.AreaObj.SetGUID(str(self.no), guid)
        if ret == 0:
            self._get_guid(model)
        return ret
    
    def get_guid(self, model) -> Optional[str]:
        """Get area-object GUID"""
        self._get_guid(model)
        return self.guid

    # ==================== Element methods ====================
    
    def get_elements(self, model) -> Optional[List[str]]:
        """
        Get analysis-element names corresponding to this area object
        
        Returns:
            List of analysis-element names, or `None` on failure
        """
        try:
            result = model.AreaObj.GetElm(str(self.no), 0, [])
            num_elms = com_data(result, 0, 0)
            elms = com_data(result, 1)
            if num_elms > 0 and elms:
                    return list(elms)
        except Exception:
            pass
        return None

    # ==================== Other methods ====================
    
    def change_name(self, model, new_name: str) -> int:
        """
        Change area-object name
        
        Args:
            model: SapModel object
            new_name: New name
            
        Returns:
            `0` on success
        """
        ret = model.AreaObj.ChangeName(str(self.no), new_name)
        if ret == 0:
            self.no = new_name
        return ret

    # ==================== Load methods ====================
    
    def set_load_gravity(
        self,
        model,
        load_pattern: str,
        x: float = 0.0,
        y: float = 0.0,
        z: float = -1.0,
        replace: bool = True,
        csys: str = "Global",
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area gravity load
        
        Args:
            model: SapModel object
            load_pattern: Load-pattern name
            x, y, z: gravity acceleration components (typically z=-1 indicates downward)
            replace: Whether to replace existing loads
            csys: Coordinate-system name
            item_type: Item type
            
        Returns:
            `0` on success
        """
        return model.AreaObj.SetLoadGravity(
            str(self.no), load_pattern, x, y, z, replace, csys, item_type
        )
    
    def get_load_gravity(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[AreaLoadGravity]:
        """Get area gravity loads"""
        loads = []
        try:
            result = model.AreaObj.GetLoadGravity(
                str(self.no), 0, [], [], [], [], [], [], item_type
            )
            if com_data(result, 7) is not None:
                num_items = com_data(result, 0, 0)
                area_names = com_data(result, 1)
                load_pats = com_data(result, 2)
                csys_list = com_data(result, 3)
                x_list = com_data(result, 4)
                y_list = com_data(result, 5)
                z_list = com_data(result, 6)
                
                for i in range(num_items):
                    loads.append(AreaLoadGravity(
                        area_name=area_names[i] if area_names else str(self.no),
                        load_pattern=load_pats[i] if load_pats else "",
                        x=x_list[i] if x_list else 0.0,
                        y=y_list[i] if y_list else 0.0,
                        z=z_list[i] if z_list else 0.0,
                        csys=csys_list[i] if csys_list else "Global"
                    ))
        except Exception:
            pass
        return loads
    
    def delete_load_gravity(
        self,
        model,
        load_pattern: str,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """Delete area gravity load"""
        return model.AreaObj.DeleteLoadGravity(str(self.no), load_pattern, item_type)
    
    def set_load_uniform(
        self,
        model,
        load_pattern: str,
        value: float,
        direction: AreaLoadDir = AreaLoadDir.GRAVITY,
        replace: bool = True,
        csys: str = "Global",
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area uniform load
        
        Args:
            model: SapModel object
            load_pattern: Load-pattern name
            value: Load value (force per area)
            direction: Load direction
            replace: Whether to replace existing loads
            csys: Coordinate-system name
            item_type: Item type
            
        Returns:
            `0` on success
        """
        return model.AreaObj.SetLoadUniform(
            str(self.no), load_pattern, value, int(direction), replace, csys, item_type
        )
    
    def get_load_uniform(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[AreaLoadUniform]:
        """Get area uniform loads"""
        loads = []
        try:
            result = model.AreaObj.GetLoadUniform(
                str(self.no), 0, [], [], [], [], [], item_type
            )
            if com_data(result, 6) is not None:
                num_items = com_data(result, 0, 0)
                area_names = com_data(result, 1)
                load_pats = com_data(result, 2)
                csys_list = com_data(result, 3)
                dir_list = com_data(result, 4)
                value_list = com_data(result, 5)
                
                for i in range(num_items):
                    loads.append(AreaLoadUniform(
                        area_name=area_names[i] if area_names else str(self.no),
                        load_pattern=load_pats[i] if load_pats else "",
                        value=value_list[i] if value_list else 0.0,
                        direction=AreaLoadDir(dir_list[i]) if dir_list else AreaLoadDir.GRAVITY,
                        csys=csys_list[i] if csys_list else "Global"
                    ))
        except Exception:
            pass
        return loads
    
    def delete_load_uniform(
        self,
        model,
        load_pattern: str,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """Delete area uniform load"""
        return model.AreaObj.DeleteLoadUniform(str(self.no), load_pattern, item_type)
    
    def set_load_surface_pressure(
        self,
        model,
        load_pattern: str,
        face: int,
        value: float,
        pattern_name: str = "",
        replace: bool = True,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area surface-pressure load
        
        Args:
            model: SapModel object
            load_pattern: Load-pattern name
            face: Face (-1=bottom face, -2=top face)
            value: Pressure value
            pattern_name: Pattern name
            replace: Whether to replace existing loads
            item_type: Item type
            
        Returns:
            `0` on success
        """
        return model.AreaObj.SetLoadSurfacePressure(
            str(self.no), load_pattern, face, value, pattern_name, replace, item_type
        )
    
    def get_load_surface_pressure(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[AreaLoadSurfacePressure]:
        """Get area surface-pressure loads"""
        loads = []
        try:
            result = model.AreaObj.GetLoadSurfacePressure(
                str(self.no), 0, [], [], [], [], [], item_type
            )
            if com_data(result, 6) is not None:
                num_items = com_data(result, 0, 0)
                area_names = com_data(result, 1)
                load_pats = com_data(result, 2)
                faces = com_data(result, 3)
                values = com_data(result, 4)
                patterns = com_data(result, 5)
                
                for i in range(num_items):
                    loads.append(AreaLoadSurfacePressure(
                        area_name=area_names[i] if area_names else str(self.no),
                        load_pattern=load_pats[i] if load_pats else "",
                        face=faces[i] if faces else -1,
                        value=values[i] if values else 0.0,
                        pattern_name=patterns[i] if patterns else ""
                    ))
        except Exception:
            pass
        return loads
    
    def delete_load_surface_pressure(
        self,
        model,
        load_pattern: str,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """Delete area surface-pressure load"""
        return model.AreaObj.DeleteLoadSurfacePressure(str(self.no), load_pattern, item_type)


    def set_load_temperature(
        self,
        model,
        load_pattern: str,
        load_type: AreaTempLoadType,
        value: float,
        pattern_name: str = "",
        replace: bool = True,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area temperature load
        
        Args:
            model: SapModel object
            load_pattern: Load-pattern name
            load_type: Temperature-load type (1=temperature, 3=temperature gradient)
            value: Temperature value
            pattern_name: Pattern name
            replace: Whether to replace existing loads
            item_type: Item type
            
        Returns:
            `0` on success
        """
        return model.AreaObj.SetLoadTemperature(
            str(self.no), load_pattern, int(load_type), value, pattern_name, replace, item_type
        )
    
    def get_load_temperature(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[AreaLoadTemperature]:
        """Get area temperature loads"""
        loads = []
        try:
            result = model.AreaObj.GetLoadTemperature(
                str(self.no), 0, [], [], [], [], [], item_type
            )
            if com_data(result, 6) is not None:
                num_items = com_data(result, 0, 0)
                area_names = com_data(result, 1)
                load_pats = com_data(result, 2)
                load_types = com_data(result, 3)
                values = com_data(result, 4)
                patterns = com_data(result, 5)
                
                for i in range(num_items):
                    loads.append(AreaLoadTemperature(
                        area_name=area_names[i] if area_names else str(self.no),
                        load_pattern=load_pats[i] if load_pats else "",
                        load_type=AreaTempLoadType(load_types[i]) if load_types else AreaTempLoadType.TEMPERATURE,
                        value=values[i] if values else 0.0,
                        pattern_name=patterns[i] if patterns else ""
                    ))
        except Exception:
            pass
        return loads
    
    def delete_load_temperature(
        self,
        model,
        load_pattern: str,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """Delete area temperature load"""
        return model.AreaObj.DeleteLoadTemperature(str(self.no), load_pattern, item_type)
    
    def set_load_pore_pressure(
        self,
        model,
        load_pattern: str,
        value: float,
        pattern_name: str = "",
        replace: bool = True,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area pore-pressure load
        
        Args:
            model: SapModel object
            load_pattern: Load-pattern name
            value: Pore-pressure value
            pattern_name: Pattern name
            replace: Whether to replace existing loads
            item_type: Item type
            
        Returns:
            `0` on success
        """
        return model.AreaObj.SetLoadPorePressure(
            str(self.no), load_pattern, value, pattern_name, replace, item_type
        )
    
    def get_load_pore_pressure(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[dict]:
        """Get area pore-pressure loads"""
        loads = []
        try:
            result = model.AreaObj.GetLoadPorePressure(
                str(self.no), 0, [], [], [], [], item_type
            )
            if com_data(result, 5) is not None:
                num_items = com_data(result, 0, 0)
                area_names = com_data(result, 1)
                load_pats = com_data(result, 2)
                values = com_data(result, 3)
                patterns = com_data(result, 4)
                
                for i in range(num_items):
                    loads.append({
                        "area_name": area_names[i] if area_names else str(self.no),
                        "load_pattern": load_pats[i] if load_pats else "",
                        "value": values[i] if values else 0.0,
                        "pattern_name": patterns[i] if patterns else ""
                    })
        except Exception:
            pass
        return loads
    
    def delete_load_pore_pressure(
        self,
        model,
        load_pattern: str,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """Delete area pore-pressure load"""
        return model.AreaObj.DeleteLoadPorePressure(str(self.no), load_pattern, item_type)
    
    def set_load_strain(
        self,
        model,
        load_pattern: str,
        component: AreaStrainComponent,
        value: float,
        replace: bool = True,
        pattern_name: str = "",
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area strain load
        
        Args:
            model: SapModel object
            load_pattern: Load-pattern name
            component: Strain component
            value: Strain value
            replace: Whether to replace existing loads
            pattern_name: Pattern name
            item_type: Item type
            
        Returns:
            `0` on success
        """
        return model.AreaObj.SetLoadStrain(
            str(self.no), load_pattern, int(component), value, replace, pattern_name, item_type
        )
    
    def get_load_strain(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[dict]:
        """Get area strain loads"""
        loads = []
        try:
            result = model.AreaObj.GetLoadStrain(
                str(self.no), 0, [], [], [], [], [], item_type
            )
            if com_data(result, 6) is not None:
                num_items = com_data(result, 0, 0)
                area_names = com_data(result, 1)
                load_pats = com_data(result, 2)
                components = com_data(result, 3)
                values = com_data(result, 4)
                patterns = com_data(result, 5)
                
                for i in range(num_items):
                    loads.append({
                        "area_name": area_names[i] if area_names else str(self.no),
                        "load_pattern": load_pats[i] if load_pats else "",
                        "component": AreaStrainComponent(components[i]) if components else AreaStrainComponent.STRAIN_11,
                        "value": values[i] if values else 0.0,
                        "pattern_name": patterns[i] if patterns else ""
                    })
        except Exception:
            pass
        return loads
    
    def delete_load_strain(
        self,
        model,
        load_pattern: str,
        component: AreaStrainComponent,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """Delete area strain load"""
        return model.AreaObj.DeleteLoadStrain(str(self.no), load_pattern, int(component), item_type)
    
    def set_load_rotate(
        self,
        model,
        load_pattern: str,
        value: float,
        replace: bool = True,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area rotation load
        
        Args:
            model: SapModel object
            load_pattern: Load-pattern name
            value: rotation speed (rad/s)
            replace: Whether to replace existing loads
            item_type: Item type
            
        Returns:
            `0` on success
        """
        return model.AreaObj.SetLoadRotate(
            str(self.no), load_pattern, value, replace, item_type
        )
    
    def get_load_rotate(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[dict]:
        """Get area rotation loads"""
        loads = []
        try:
            result = model.AreaObj.GetLoadRotate(
                str(self.no), 0, [], [], [], item_type
            )
            if com_data(result, 4) is not None:
                num_items = com_data(result, 0, 0)
                area_names = com_data(result, 1)
                load_pats = com_data(result, 2)
                values = com_data(result, 3)
                
                for i in range(num_items):
                    loads.append({
                        "area_name": area_names[i] if area_names else str(self.no),
                        "load_pattern": load_pats[i] if load_pats else "",
                        "value": values[i] if values else 0.0
                    })
        except Exception:
            pass
        return loads
    
    def delete_load_rotate(
        self,
        model,
        load_pattern: str,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """Delete area rotation load"""
        return model.AreaObj.DeleteLoadRotate(str(self.no), load_pattern, item_type)
    
    def set_load_uniform_to_frame(
        self,
        model,
        load_pattern: str,
        value: float,
        direction: AreaLoadDir = AreaLoadDir.GRAVITY,
        dist_type: AreaDistType = AreaDistType.TWO_WAY,
        replace: bool = True,
        csys: str = "Global",
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area uniform load transferred to frame
        
        Args:
            model: SapModel object
            load_pattern: Load-pattern name
            value: Load value (force per area)
            direction: Load direction
            dist_type: distribution type (one-way / two-way)
            replace: Whether to replace existing loads
            csys: Coordinate-system name
            item_type: Item type
            
        Returns:
            `0` on success
        """
        return model.AreaObj.SetLoadUniformToFrame(
            str(self.no), load_pattern, value, int(direction), int(dist_type),
            replace, csys, item_type
        )
    
    def get_load_uniform_to_frame(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[dict]:
        """Get area uniform loads transferred to frame."""
        loads = []
        try:
            result = model.AreaObj.GetLoadUniformToFrame(
                str(self.no), 0, [], [], [], [], [], [], item_type
            )
            if com_data(result, 7) is not None:
                num_items = com_data(result, 0, 0)
                area_names = com_data(result, 1)
                load_pats = com_data(result, 2)
                csys_list = com_data(result, 3)
                dir_list = com_data(result, 4)
                value_list = com_data(result, 5)
                dist_types = com_data(result, 6)
                
                for i in range(num_items):
                    loads.append({
                        "area_name": area_names[i] if area_names else str(self.no),
                        "load_pattern": load_pats[i] if load_pats else "",
                        "value": value_list[i] if value_list else 0.0,
                        "direction": AreaLoadDir(dir_list[i]) if dir_list else AreaLoadDir.GRAVITY,
                        "dist_type": AreaDistType(dist_types[i]) if dist_types else AreaDistType.TWO_WAY,
                        "csys": csys_list[i] if csys_list else "Global"
                    })
        except Exception:
            pass
        return loads
    
    def delete_load_uniform_to_frame(
        self,
        model,
        load_pattern: str,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """Delete area uniform load transferred to frame."""
        return model.AreaObj.DeleteLoadUniformToFrame(str(self.no), load_pattern, item_type)
    
    def set_load_wind_pressure(
        self,
        model,
        load_pattern: str,
        wind_pressure_type: AreaWindPressureType,
        cp: float = 0.0,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        Set area wind-pressure load
        
        Args:
            model: SapModel object
            load_pattern: Load-pattern name
            wind_pressure_type: Wind-pressure type
            cp: Wind-pressure coefficient (used for `FROM_CP`)
            item_type: Item type
            
        Returns:
            `0` on success
        """
        return model.AreaObj.SetLoadWindPressure_1(
            str(self.no), load_pattern, int(wind_pressure_type), cp, item_type
        )
    
    def get_load_wind_pressure(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[dict]:
        """Get area wind-pressure loads"""
        loads = []
        try:
            result = model.AreaObj.GetLoadWindPressure_1(
                str(self.no), 0, [], [], [], [], item_type
            )
            if com_data(result, 5) is not None:
                num_items = com_data(result, 0, 0)
                area_names = com_data(result, 1)
                load_pats = com_data(result, 2)
                wind_types = com_data(result, 3)
                cps = com_data(result, 4)
                
                for i in range(num_items):
                    loads.append({
                        "area_name": area_names[i] if area_names else str(self.no),
                        "load_pattern": load_pats[i] if load_pats else "",
                        "wind_pressure_type": AreaWindPressureType(wind_types[i]) if wind_types else AreaWindPressureType.FROM_CP,
                        "cp": cps[i] if cps else 0.0
                    })
        except Exception:
            pass
        return loads
    
    def delete_load_wind_pressure(
        self,
        model,
        load_pattern: str,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """Delete area wind-pressure load"""
        return model.AreaObj.DeleteLoadWindPressure(str(self.no), load_pattern, item_type)
