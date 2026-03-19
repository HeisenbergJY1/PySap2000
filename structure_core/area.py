# -*- coding: utf-8 -*-
"""
area.py - 面单元数据对象
对应 SAP2000 的 AreaObj

API Reference:
    创建:
    - AddByCoord(NumberPoints, x[], y[], z[], Name, PropName="Default", UserName="", CSys="Global")
    - AddByPoint(NumberPoints, Point[], Name, PropName="Default", UserName="")
    
    获取:
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
    
    设置:
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
    
    荷载:
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
    """面单元类型"""
    SHELL = 1
    PLANE = 2
    ASOLID = 3


class AreaMeshType(IntEnum):
    """面单元自动网格划分类型"""
    NO_MESH = 0
    MESH_BY_NUMBER = 1
    MESH_BY_MAX_SIZE = 2
    MESH_BY_POINTS_ON_EDGE = 3
    COOKIE_CUT_BY_LINES = 4
    COOKIE_CUT_BY_POINTS = 5
    GENERAL_DIVIDE = 6


class AreaThicknessType(IntEnum):
    """面单元厚度覆盖类型"""
    NO_OVERWRITE = 0
    BY_JOINT_PATTERN = 1
    BY_POINT = 2


class AreaOffsetType(IntEnum):
    """面单元偏移类型"""
    NO_OFFSET = 0
    BY_JOINT_PATTERN = 1
    BY_POINT = 2


class AreaSpringType(IntEnum):
    """面单元弹簧类型"""
    SIMPLE_SPRING = 1
    LINK_PROPERTY = 2


class AreaSimpleSpringType(IntEnum):
    """面单元简单弹簧类型"""
    TENSION_COMPRESSION = 1
    COMPRESSION_ONLY = 2
    TENSION_ONLY = 3


class AreaSpringLocalOneType(IntEnum):
    """面单元弹簧局部1轴方向类型"""
    PARALLEL_TO_LOCAL_AXIS = 1
    NORMAL_TO_FACE = 2
    USER_VECTOR = 3


class AreaFace(IntEnum):
    """面单元面"""
    BOTTOM = -1
    TOP = -2


class AreaLoadDir(IntEnum):
    """面单元荷载方向"""
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
    """面单元温度荷载类型"""
    TEMPERATURE = 1
    TEMPERATURE_GRADIENT = 3


class AreaStrainComponent(IntEnum):
    """面单元应变分量"""
    STRAIN_11 = 1
    STRAIN_22 = 2
    STRAIN_12 = 3
    CURVATURE_11 = 4
    CURVATURE_22 = 5
    CURVATURE_12 = 6


class AreaWindPressureType(IntEnum):
    """面单元风压类型"""
    FROM_CP = 1
    FROM_CODE = 2


class AreaDistType(IntEnum):
    """面单元荷载分布类型"""
    ONE_WAY = 1
    TWO_WAY = 2


class PlaneRefVectorOption(IntEnum):
    """平面参考向量选项"""
    COORDINATE_DIRECTION = 1
    TWO_JOINTS = 2
    USER_VECTOR = 3


class ItemType(IntEnum):
    """eItemType 枚举"""
    OBJECT = 0
    GROUP = 1
    SELECTED_OBJECTS = 2


@dataclass
class AreaLoadGravity:
    """面单元重力荷载数据"""
    area_name: str
    load_pattern: str
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    csys: str = "Global"


@dataclass
class AreaLoadUniform:
    """面单元均布荷载数据"""
    area_name: str
    load_pattern: str
    value: float = 0.0
    direction: AreaLoadDir = AreaLoadDir.GRAVITY
    csys: str = "Global"


@dataclass
class AreaLoadSurfacePressure:
    """面单元表面压力荷载数据"""
    area_name: str
    load_pattern: str
    face: int = -1
    value: float = 0.0
    pattern_name: str = ""


@dataclass
class AreaLoadTemperature:
    """面单元温度荷载数据"""
    area_name: str
    load_pattern: str
    load_type: AreaTempLoadType = AreaTempLoadType.TEMPERATURE
    value: float = 0.0
    pattern_name: str = ""


@dataclass
class AreaSpring:
    """面单元弹簧数据"""
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
    """面单元自动网格划分设置"""
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
    """面单元高级局部坐标轴设置"""
    active: bool = False
    plane2: int = 31  # 31=3-1平面, 32=3-2平面
    pl_vect_opt: PlaneRefVectorOption = PlaneRefVectorOption.COORDINATE_DIRECTION
    pl_csys: str = "Global"
    pl_dir: Tuple[int, int] = (1, 2)  # 主方向和次方向
    pl_pt: Tuple[str, str] = ("", "")  # 两个节点名称
    pl_vect: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # 用户向量



@dataclass
class Area:
    """
    面单元数据对象
    对应 SAP2000 的 AreaObj
    """
    
    # 必填属性
    no: Union[int, str] = None
    
    # 节点定义 (二选一)
    points: Optional[List[str]] = None  # 节点名称列表
    x_coords: Optional[List[float]] = None  # X 坐标列表
    y_coords: Optional[List[float]] = None  # Y 坐标列表
    z_coords: Optional[List[float]] = None  # Z 坐标列表
    
    # 截面属性
    section: str = "Default"
    
    # 厚度覆盖
    thickness_type: AreaThicknessType = AreaThicknessType.NO_OVERWRITE
    thickness_pattern: str = ""
    thickness_pattern_sf: float = 1.0
    thickness: Optional[List[float]] = None
    
    # 局部坐标轴
    local_axis_angle: float = 0.0
    local_axes_advanced: Optional[AreaLocalAxesAdvanced] = None
    
    # 自动网格划分
    auto_mesh: Optional[AreaAutoMesh] = None
    
    # 修改系数 (10个值)
    modifiers: Optional[List[float]] = None
    
    # 附加质量
    mass_per_area: float = 0.0
    
    # 材料覆盖
    material_overwrite: Optional[str] = None
    
    # 材料温度
    mat_temp: float = 0.0
    mat_temp_pattern: str = ""
    
    # 偏移
    offset_type: AreaOffsetType = AreaOffsetType.NO_OFFSET
    offset_pattern: str = ""
    offset_pattern_sf: float = 1.0
    offsets: Optional[List[float]] = None
    
    # 弹簧
    springs: Optional[List[AreaSpring]] = None
    
    # 边缘约束
    edge_constraint: bool = False
    
    # 组
    groups: Optional[List[str]] = None
    
    # 选择状态
    selected: bool = False
    
    # 其他
    coordinate_system: str = "Global"
    comment: str = ""
    guid: Optional[str] = None
    
    # 类属性
    _object_type: ClassVar[str] = "AreaObj"

    # ==================== 创建方法 ====================
    
    def _create(self, model) -> int:
        """
        在 SAP2000 中创建面单元
        
        Returns:
            0 表示成功，非 0 表示失败
        """
        from PySap2000.logger import get_logger
        _log = get_logger("area")

        user_name = str(self.no) if self.no is not None else ""

        # 检查是否已存在
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
        """通过节点名称创建面单元"""
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
        """通过坐标创建面单元"""
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
        """解析创建结果"""
        ret = com_ret(result)
        # assigned name: 3个以上元素时在倒数第二个位置，否则在第一个位置
        if com_data(result, 2) is not None:
            assigned_name = com_data(result, -2)
        else:
            assigned_name = com_data(result, 0)
        if isinstance(assigned_name, str) and assigned_name:
            self.no = assigned_name
        return ret

    # ==================== 获取方法 ====================
    
    def _get(self, model) -> 'Area':
        """从 SAP2000 获取面单元数据"""
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
        获取面单元的节点
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
        """获取面单元截面属性名称"""
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
        """获取局部坐标轴角度"""
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
        获取高级局部坐标轴设置
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
        """获取自动网格划分设置"""
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
        """获取修改系数"""
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
        """获取附加质量"""
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
        """获取面单元所属组"""
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
        """获取选择状态"""
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
        """获取面单元 GUID"""
        try:
            result = model.AreaObj.GetGUID(str(self.no), "")
            guid = com_data(result, 0)
            if guid is not None:
                self.guid = guid
        except Exception:
            pass


    # ==================== 公开查询方法 ====================
    
    @classmethod
    def get_all(cls, model, names: List[str] = None) -> List['Area']:
        """
        获取所有面单元
        
        Args:
            model: SapModel 对象
            names: 可选，指定面单元名称列表。如果为 None，获取所有面单元
            
        Returns:
            Area 对象列表，每个对象已填充完整数据
            
        Example:
            # 获取所有面单元
            areas = Area.get_all(model)
            for a in areas:
                print(f"{a.no}: section={a.section}, points={a.points}")
            
            # 获取指定面单元
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
        获取指定名称的面单元
        
        Args:
            model: SapModel 对象
            name: 面单元名称
            
        Returns:
            填充了数据的 Area 对象
            
        Example:
            area = Area.get_by_name(model, "1")
            print(f"截面: {area.section}, 节点: {area.points}")
        """
        area = cls(no=name)
        area._get(model)
        return area
    
    @staticmethod
    def get_count(model) -> int:
        """
        获取面单元总数
        
        Args:
            model: SapModel 对象
            
        Returns:
            面单元数量
        """
        return model.AreaObj.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """
        获取所有面单元名称列表
        
        Args:
            model: SapModel 对象
            
        Returns:
            面单元名称列表
        """
        result = model.AreaObj.GetNameList(0, [])
        
        names = com_data(result, 1)
        if names is not None:
            return list(names)
        return []
    
    @staticmethod
    def get_section_name_list(model) -> List[str]:
        """
        获取所有面截面属性名称列表
        
        Args:
            model: SapModel 对象
            
        Returns:
            截面属性名称列表
        """
        result = model.PropArea.GetNameList(0, [])
        
        names = com_data(result, 1)
        if names is not None:
            return list(names)
        return []

    # ==================== 删除和更新方法 ====================
    
    def _delete(self, model) -> int:
        """
        从 SAP2000 删除面单元
        
        Returns:
            0 表示成功，非 0 表示失败
        """
        return model.AreaObj.Delete(str(self.no), ItemType.OBJECT)
    
    def _update(self, model) -> int:
        """更新面单元属性到 SAP2000"""
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

    # ==================== 截面属性方法 ====================
    
    def set_property(
        self,
        model,
        prop_name: str,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        设置面单元截面属性
        
        Args:
            model: SapModel 对象
            prop_name: 截面属性名称
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        self.section = prop_name
        return model.AreaObj.SetProperty(str(self.no), prop_name, item_type)
    
    def get_property(self, model) -> Optional[str]:
        """获取面单元截面属性名称"""
        return self._get_property(model)

    # ==================== 厚度方法 ====================
    
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
        设置面单元厚度覆盖
        
        Args:
            model: SapModel 对象
            thickness_type: 厚度类型
            thickness_pattern: 厚度模式名称
            thickness_pattern_sf: 厚度模式比例因子
            thickness: 厚度值列表 (每个节点一个值)
            item_type: 项目类型
            
        Returns:
            0 表示成功
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
        获取面单元厚度覆盖
        
        Returns:
            包含厚度信息的字典，失败返回 None
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

    # ==================== 局部坐标轴方法 ====================
    
    def set_local_axes(
        self,
        model,
        angle: float,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        设置面单元局部坐标轴角度
        
        Args:
            model: SapModel 对象
            angle: 局部坐标轴角度 [deg]
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        self.local_axis_angle = angle
        return model.AreaObj.SetLocalAxes(str(self.no), angle, item_type)
    
    def get_local_axes(self, model) -> Optional[Tuple[float, bool]]:
        """
        获取面单元局部坐标轴角度
        
        Returns:
            (角度, 是否有高级设置) 元组，失败返回 None
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
        设置面单元高级局部坐标轴
        
        Args:
            model: SapModel 对象
            active: 是否启用高级局部坐标轴
            plane2: 31=3-1平面, 32=3-2平面
            pl_vect_opt: 平面参考向量选项 (1=坐标方向, 2=两节点, 3=用户向量)
            pl_csys: 坐标系名称
            pl_dir: 主方向和次方向 (用于 pl_vect_opt=1)
            pl_pt: 两个节点名称 (用于 pl_vect_opt=2)
            pl_vect: 用户向量 (用于 pl_vect_opt=3)
            item_type: 项目类型
            
        Returns:
            0 表示成功
            
        Example:
            # 使用坐标方向定义
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
        获取面单元高级局部坐标轴设置
        
        Returns:
            AreaLocalAxesAdvanced 对象，失败返回 None
        """
        return self._get_local_axes_advanced(model)

    # ==================== 变换矩阵方法 ====================
    
    def get_transformation_matrix(self, model, is_global: bool = True) -> Optional[List[float]]:
        """
        获取面单元变换矩阵
        
        变换矩阵用于将局部坐标系转换为全局坐标系（或当前坐标系）。
        矩阵包含9个方向余弦值。
        
        Args:
            model: SapModel 对象
            is_global: True=全局坐标系, False=当前坐标系
            
        Returns:
            9个方向余弦值的列表 [c0, c1, c2, c3, c4, c5, c6, c7, c8]，失败返回 None
            
        Example:
            matrix = area.get_transformation_matrix(model)
            if matrix:
                # 矩阵方程: [GlobalX, GlobalY, GlobalZ] = [c0-c8] * [Local1, Local2, Local3]
                print(f"变换矩阵: {matrix}")
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


    # ==================== 自动网格划分方法 ====================
    
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
        设置面单元自动网格划分
        
        Args:
            model: SapModel 对象
            mesh_type: 网格划分类型
            n1, n2: 划分数量 (用于 MESH_BY_NUMBER)
            max_size1, max_size2: 最大尺寸 (用于 MESH_BY_MAX_SIZE)
            其他参数: 参见 SAP2000 API 文档
            item_type: 项目类型
            
        Returns:
            0 表示成功
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
        """获取面单元自动网格划分设置"""
        return self._get_auto_mesh(model)

    # ==================== 修改系数方法 ====================
    
    def set_modifiers(
        self,
        model,
        modifiers: List[float],
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        设置面单元修改系数
        
        Args:
            model: SapModel 对象
            modifiers: 10个修改系数值
                [f11, f22, f12, m11, m22, m12, v13, v23, mass, weight]
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        # 确保有10个值
        mod_list = list(modifiers)
        while len(mod_list) < 10:
            mod_list.append(1.0)
        
        self.modifiers = mod_list[:10]
        result = model.AreaObj.SetModifiers(str(self.no), mod_list[:10], item_type)
        # 解析返回值
        return com_ret(result)
    
    def get_modifiers(self, model) -> Optional[List[float]]:
        """获取面单元修改系数"""
        return self._get_modifiers(model)
    
    def delete_modifiers(self, model, item_type: ItemType = ItemType.OBJECT) -> int:
        """删除面单元修改系数 (恢复默认值)"""
        self.modifiers = None
        return model.AreaObj.DeleteModifiers(str(self.no), item_type)

    # ==================== 质量方法 ====================
    
    def set_mass(
        self,
        model,
        mass_per_area: float,
        replace: bool = True,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        设置面单元附加质量
        
        Args:
            model: SapModel 对象
            mass_per_area: 单位面积质量
            replace: 是否替换现有质量 (True=替换, False=叠加)
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        self.mass_per_area = mass_per_area
        return model.AreaObj.SetMass(str(self.no), mass_per_area, replace, item_type)
    
    def get_mass(self, model) -> Optional[float]:
        """获取面单元附加质量"""
        return self._get_mass(model)
    
    def delete_mass(self, model, item_type: ItemType = ItemType.OBJECT) -> int:
        """删除面单元附加质量"""
        self.mass_per_area = 0.0
        return model.AreaObj.DeleteMass(str(self.no), item_type)

    # ==================== 材料覆盖方法 ====================
    
    def set_material_overwrite(
        self,
        model,
        prop_name: str,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        设置面单元材料覆盖
        
        Args:
            model: SapModel 对象
            prop_name: 材料名称
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        self.material_overwrite = prop_name
        return model.AreaObj.SetMaterialOverwrite(str(self.no), prop_name, item_type)
    
    def get_material_overwrite(self, model) -> Optional[str]:
        """获取面单元材料覆盖"""
        try:
            result = model.AreaObj.GetMaterialOverwrite(str(self.no), "")
            mat = com_data(result, 0)
            if mat is not None:
                self.material_overwrite = mat
                return self.material_overwrite
        except Exception:
            pass
        return None

    # ==================== 材料温度方法 ====================
    
    def set_mat_temp(
        self,
        model,
        temp: float,
        pattern_name: str = "",
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        设置面单元材料温度
        
        Args:
            model: SapModel 对象
            temp: 温度值
            pattern_name: 温度模式名称
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        self.mat_temp = temp
        self.mat_temp_pattern = pattern_name
        return model.AreaObj.SetMatTemp(str(self.no), temp, pattern_name, item_type)
    
    def get_mat_temp(self, model) -> Optional[Tuple[float, str]]:
        """获取面单元材料温度"""
        try:
            result = model.AreaObj.GetMatTemp(str(self.no), 0.0, "")
            if com_data(result, 2) is not None:
                self.mat_temp = com_data(result, 0)
                self.mat_temp_pattern = com_data(result, 1)
                return (self.mat_temp, self.mat_temp_pattern)
        except Exception:
            pass
        return None

    # ==================== 偏移方法 ====================
    
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
        设置面单元偏移
        
        Args:
            model: SapModel 对象
            offset_type: 偏移类型
            offset_pattern: 偏移模式名称
            offset_pattern_sf: 偏移模式比例因子
            offsets: 偏移值列表 (每个节点一个值)
            item_type: 项目类型
            
        Returns:
            0 表示成功
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
        """获取面单元偏移"""
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

    # ==================== 弹簧方法 ====================
    
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
        设置面单元弹簧
        
        Args:
            model: SapModel 对象
            spring_type: 弹簧类型
            stiffness: 弹簧刚度
            simple_spring_type: 简单弹簧类型
            link_prop: 连接属性名称 (用于 LINK_PROPERTY 类型)
            face: 面 (-1=底面, -2=顶面)
            local_one_type: 局部1轴方向类型
            direction: 方向
            outward: 是否向外
            vector: 用户向量
            angle: 角度
            replace: 是否替换现有弹簧
            csys: 坐标系
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        return model.AreaObj.SetSpring(
            str(self.no), int(spring_type), stiffness, int(simple_spring_type),
            link_prop, face, int(local_one_type), direction, outward,
            list(vector), angle, replace, csys, item_type
        )
    
    def get_spring(self, model) -> Optional[List[AreaSpring]]:
        """获取面单元弹簧"""
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
        """删除面单元弹簧"""
        self.springs = None
        return model.AreaObj.DeleteSpring(str(self.no), item_type)


    # ==================== 边缘约束方法 ====================
    
    def set_edge_constraint(
        self,
        model,
        constraint_exists: bool,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        设置面单元边缘约束
        
        Args:
            model: SapModel 对象
            constraint_exists: 是否存在边缘约束
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        self.edge_constraint = constraint_exists
        return model.AreaObj.SetEdgeConstraint(str(self.no), constraint_exists, item_type)
    
    def get_edge_constraint(self, model) -> bool:
        """获取面单元边缘约束"""
        try:
            result = model.AreaObj.GetEdgeConstraint(str(self.no), False)
            ec = com_data(result, 0)
            if ec is not None:
                self.edge_constraint = ec
                return self.edge_constraint
        except Exception:
            pass
        return False

    # ==================== 组方法 ====================
    
    def set_group_assign(
        self,
        model,
        group_name: str,
        remove: bool = False,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """
        设置面单元组分配
        
        Args:
            model: SapModel 对象
            group_name: 组名称
            remove: 是否从组中移除 (True=移除, False=添加)
            item_type: 项目类型
            
        Returns:
            0 表示成功
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
        """获取面单元所属组"""
        return self._get_group_assign(model)

    # ==================== 选择方法 ====================
    
    def set_selected(
        self,
        model,
        selected: bool = True,
        item_type: ItemType = ItemType.OBJECT
    ) -> int:
        """设置选择状态"""
        self.selected = selected
        return model.AreaObj.SetSelected(str(self.no), selected, item_type)
    
    def get_selected(self, model) -> bool:
        """获取选择状态"""
        return self._get_selected(model)

    # ==================== GUID 方法 ====================
    
    def set_guid(self, model, guid: str = "") -> int:
        """
        设置面单元 GUID
        
        Args:
            model: SapModel 对象
            guid: GUID 字符串。如果为空字符串，程序将自动创建新的 GUID
            
        Returns:
            0 表示成功
        """
        ret = model.AreaObj.SetGUID(str(self.no), guid)
        if ret == 0:
            self._get_guid(model)
        return ret
    
    def get_guid(self, model) -> Optional[str]:
        """获取面单元 GUID"""
        self._get_guid(model)
        return self.guid

    # ==================== 单元方法 ====================
    
    def get_elements(self, model) -> Optional[List[str]]:
        """
        获取面单元对应的分析单元名称列表
        
        Returns:
            分析单元名称列表，失败返回 None
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

    # ==================== 其他方法 ====================
    
    def change_name(self, model, new_name: str) -> int:
        """
        更改面单元名称
        
        Args:
            model: SapModel 对象
            new_name: 新名称
            
        Returns:
            0 表示成功
        """
        ret = model.AreaObj.ChangeName(str(self.no), new_name)
        if ret == 0:
            self.no = new_name
        return ret

    # ==================== 荷载方法 ====================
    
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
        设置面单元重力荷载
        
        Args:
            model: SapModel 对象
            load_pattern: 荷载模式名称
            x, y, z: 重力加速度分量 (通常 z=-1 表示向下)
            replace: 是否替换现有荷载
            csys: 坐标系名称
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        return model.AreaObj.SetLoadGravity(
            str(self.no), load_pattern, x, y, z, replace, csys, item_type
        )
    
    def get_load_gravity(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[AreaLoadGravity]:
        """获取面单元重力荷载"""
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
        """删除面单元重力荷载"""
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
        设置面单元均布荷载
        
        Args:
            model: SapModel 对象
            load_pattern: 荷载模式名称
            value: 荷载值 (力/面积)
            direction: 荷载方向
            replace: 是否替换现有荷载
            csys: 坐标系名称
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        return model.AreaObj.SetLoadUniform(
            str(self.no), load_pattern, value, int(direction), replace, csys, item_type
        )
    
    def get_load_uniform(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[AreaLoadUniform]:
        """获取面单元均布荷载"""
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
        """删除面单元均布荷载"""
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
        设置面单元表面压力荷载
        
        Args:
            model: SapModel 对象
            load_pattern: 荷载模式名称
            face: 面 (-1=底面, -2=顶面)
            value: 压力值
            pattern_name: 模式名称
            replace: 是否替换现有荷载
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        return model.AreaObj.SetLoadSurfacePressure(
            str(self.no), load_pattern, face, value, pattern_name, replace, item_type
        )
    
    def get_load_surface_pressure(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[AreaLoadSurfacePressure]:
        """获取面单元表面压力荷载"""
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
        """删除面单元表面压力荷载"""
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
        设置面单元温度荷载
        
        Args:
            model: SapModel 对象
            load_pattern: 荷载模式名称
            load_type: 温度荷载类型 (1=温度, 3=温度梯度)
            value: 温度值
            pattern_name: 模式名称
            replace: 是否替换现有荷载
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        return model.AreaObj.SetLoadTemperature(
            str(self.no), load_pattern, int(load_type), value, pattern_name, replace, item_type
        )
    
    def get_load_temperature(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[AreaLoadTemperature]:
        """获取面单元温度荷载"""
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
        """删除面单元温度荷载"""
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
        设置面单元孔隙压力荷载
        
        Args:
            model: SapModel 对象
            load_pattern: 荷载模式名称
            value: 孔隙压力值
            pattern_name: 模式名称
            replace: 是否替换现有荷载
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        return model.AreaObj.SetLoadPorePressure(
            str(self.no), load_pattern, value, pattern_name, replace, item_type
        )
    
    def get_load_pore_pressure(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[dict]:
        """获取面单元孔隙压力荷载"""
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
        """删除面单元孔隙压力荷载"""
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
        设置面单元应变荷载
        
        Args:
            model: SapModel 对象
            load_pattern: 荷载模式名称
            component: 应变分量
            value: 应变值
            replace: 是否替换现有荷载
            pattern_name: 模式名称
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        return model.AreaObj.SetLoadStrain(
            str(self.no), load_pattern, int(component), value, replace, pattern_name, item_type
        )
    
    def get_load_strain(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[dict]:
        """获取面单元应变荷载"""
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
        """删除面单元应变荷载"""
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
        设置面单元旋转荷载
        
        Args:
            model: SapModel 对象
            load_pattern: 荷载模式名称
            value: 旋转速度 (rad/s)
            replace: 是否替换现有荷载
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        return model.AreaObj.SetLoadRotate(
            str(self.no), load_pattern, value, replace, item_type
        )
    
    def get_load_rotate(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[dict]:
        """获取面单元旋转荷载"""
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
        """删除面单元旋转荷载"""
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
        设置面单元均布荷载传递到框架
        
        Args:
            model: SapModel 对象
            load_pattern: 荷载模式名称
            value: 荷载值 (力/面积)
            direction: 荷载方向
            dist_type: 分布类型 (单向/双向)
            replace: 是否替换现有荷载
            csys: 坐标系名称
            item_type: 项目类型
            
        Returns:
            0 表示成功
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
        """获取面单元均布荷载传递到框架"""
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
        """删除面单元均布荷载传递到框架"""
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
        设置面单元风压荷载
        
        Args:
            model: SapModel 对象
            load_pattern: 荷载模式名称
            wind_pressure_type: 风压类型
            cp: 风压系数 (用于 FROM_CP 类型)
            item_type: 项目类型
            
        Returns:
            0 表示成功
        """
        return model.AreaObj.SetLoadWindPressure_1(
            str(self.no), load_pattern, int(wind_pressure_type), cp, item_type
        )
    
    def get_load_wind_pressure(
        self,
        model,
        item_type: ItemType = ItemType.OBJECT
    ) -> List[dict]:
        """获取面单元风压荷载"""
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
        """删除面单元风压荷载"""
        return model.AreaObj.DeleteLoadWindPressure(str(self.no), load_pattern, item_type)
