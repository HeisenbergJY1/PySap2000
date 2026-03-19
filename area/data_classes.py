# -*- coding: utf-8 -*-
"""
data_classes.py - Area 对象相关数据类
对应 SAP2000 的 AreaObj 相关数据结构

注意: 荷载相关数据类已移至 loads/area_load.py
"""

from dataclasses import dataclass
from typing import Optional, List, Tuple

from .enums import (
    AreaSpringType, AreaSimpleSpringType, AreaSpringLocalOneType,
    AreaMeshType, AreaThicknessType, AreaOffsetType, PlaneRefVectorOption
)


# ==================== 属性数据类 ====================

@dataclass
class AreaSpringData:
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
class AreaAutoMeshData:
    """面单元自动网格划分设置"""
    mesh_type: AreaMeshType = AreaMeshType.NO_MESH
    n1: int = 2                          # 方向1划分数量
    n2: int = 2                          # 方向2划分数量
    max_size1: float = 0.0               # 方向1最大尺寸
    max_size2: float = 0.0               # 方向2最大尺寸
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
class AreaLocalAxesData:
    """面单元局部坐标轴数据"""
    area_name: str = ""
    angle: float = 0.0       # 局部坐标轴旋转角度 [deg]
    advanced: bool = False    # 是否有高级设置


@dataclass
class AreaLocalAxesAdvancedData:
    """面单元高级局部坐标轴设置"""
    active: bool = False
    plane2: int = 31  # 31=3-1平面, 32=3-2平面
    pl_vect_opt: PlaneRefVectorOption = PlaneRefVectorOption.COORDINATE_DIRECTION
    pl_csys: str = "Global"
    pl_dir: Tuple[int, int] = (1, 2)  # 主方向和次方向
    pl_pt: Tuple[str, str] = ("", "")  # 两个节点名称
    pl_vect: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # 用户向量


@dataclass
class AreaThicknessData:
    """面单元厚度覆盖数据"""
    thickness_type: AreaThicknessType = AreaThicknessType.NO_OVERWRITE
    thickness_pattern: str = ""
    thickness_pattern_sf: float = 1.0
    thickness: Optional[List[float]] = None


@dataclass
class AreaOffsetData:
    """面单元偏移数据"""
    offset_type: AreaOffsetType = AreaOffsetType.NO_OFFSET
    offset_pattern: str = ""
    offset_pattern_sf: float = 1.0
    offsets: Optional[List[float]] = None


@dataclass
class AreaModifierData:
    """面单元修改器数据 (10个值)"""
    f11: float = 1.0    # 膜刚度 f11
    f22: float = 1.0    # 膜刚度 f22
    f12: float = 1.0    # 膜刚度 f12
    m11: float = 1.0    # 弯曲刚度 m11
    m22: float = 1.0    # 弯曲刚度 m22
    m12: float = 1.0    # 弯曲刚度 m12
    v13: float = 1.0    # 剪切刚度 v13
    v23: float = 1.0    # 剪切刚度 v23
    mass: float = 1.0   # 质量修改器
    weight: float = 1.0 # 重量修改器
    
    def to_list(self) -> List[float]:
        """转换为列表"""
        return [self.f11, self.f22, self.f12, self.m11, self.m22,
                self.m12, self.v13, self.v23, self.mass, self.weight]
    
    @classmethod
    def from_list(cls, values: List[float]) -> 'AreaModifierData':
        """从列表创建"""
        if len(values) >= 10:
            return cls(
                f11=values[0], f22=values[1], f12=values[2],
                m11=values[3], m22=values[4], m12=values[5],
                v13=values[6], v23=values[7],
                mass=values[8], weight=values[9]
            )
        return cls()


@dataclass
class AreaMassData:
    """面单元质量数据"""
    area_name: str           # 面单元名称
    mass_per_area: float     # 单位面积质量
