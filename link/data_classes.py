# -*- coding: utf-8 -*-
"""
data_classes.py - Link 对象数据类

用于存储 Link 对象的各种属性数据
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class LinkLocalAxesData:
    """连接单元局部轴数据"""
    link_name: str = ""
    angle: float = 0.0
    advanced: bool = False


@dataclass
class LinkLocalAxesAdvancedData:
    """
    连接单元高级局部轴数据
    
    Attributes:
        link_name: 连接单元名称
        active: 是否激活高级局部轴
        ax_vect_opt: 轴向量选项 (1=坐标方向, 2=两节点, 3=用户向量)
        ax_csys: 轴坐标系
        ax_dir: 轴方向数组 [primary, secondary]
        ax_pt: 轴参考点数组 [pt1, pt2]
        ax_vect: 轴向量 [x, y, z]
        plane2: 平面2定义 (12 或 13)
        pl_vect_opt: 平面向量选项
        pl_csys: 平面坐标系
        pl_dir: 平面方向数组 [primary, secondary]
        pl_pt: 平面参考点数组 [pt1, pt2]
        pl_vect: 平面向量 [x, y, z]
    """
    link_name: str = ""
    active: bool = False
    ax_vect_opt: int = 1
    ax_csys: str = "Global"
    ax_dir: List[int] = field(default_factory=lambda: [0, 0])
    ax_pt: List[str] = field(default_factory=lambda: ["", ""])
    ax_vect: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    plane2: int = 12
    pl_vect_opt: int = 1
    pl_csys: str = "Global"
    pl_dir: List[int] = field(default_factory=lambda: [0, 0])
    pl_pt: List[str] = field(default_factory=lambda: ["", ""])
    pl_vect: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
