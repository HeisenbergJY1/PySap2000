# -*- coding: utf-8 -*-
"""
data_classes.py - Point 属性相关数据类
"""

from dataclasses import dataclass
from typing import Optional
from .enums import PanelZonePropType, PanelZoneConnectivity, PanelZoneLocalAxisFrom


@dataclass
class PointConstraintAssignment:
    """节点约束分配数据"""
    point_name: str
    constraint_name: str


@dataclass
class PointSpringData:
    """
    节点弹簧数据
    
    Attributes:
        point_name: 节点名称
        u1, u2, u3: 平动刚度 [F/L]
        r1, r2, r3: 转动刚度 [FL/rad]
        is_local_csys: 是否使用局部坐标系
    """
    point_name: str
    u1: float = 0.0
    u2: float = 0.0
    u3: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0
    is_local_csys: bool = False


@dataclass
class PointMassData:
    """
    节点质量数据
    
    Attributes:
        point_name: 节点名称
        m1, m2, m3: 平动质量
        mr1, mr2, mr3: 转动惯量
        is_local_csys: 是否使用局部坐标系
    """
    point_name: str
    m1: float = 0.0
    m2: float = 0.0
    m3: float = 0.0
    mr1: float = 0.0
    mr2: float = 0.0
    mr3: float = 0.0
    is_local_csys: bool = True


@dataclass
class PanelZoneData:
    """
    节点域数据
    
    Attributes:
        prop_type: 属性类型
        thickness: 加劲板厚度
        k1, k2: 弹簧刚度
        link_prop: 连接单元属性名称
        connectivity: 连接类型
        local_axis_from: 局部轴来源
        local_axis_angle: 局部轴角度
    """
    prop_type: PanelZonePropType = PanelZonePropType.ELASTIC_FROM_COLUMN
    thickness: float = 0.0
    k1: float = 0.0
    k2: float = 0.0
    link_prop: str = ""
    connectivity: PanelZoneConnectivity = PanelZoneConnectivity.BEAMS_TO_OTHER
    local_axis_from: PanelZoneLocalAxisFrom = PanelZoneLocalAxisFrom.FROM_COLUMN
    local_axis_angle: float = 0.0
