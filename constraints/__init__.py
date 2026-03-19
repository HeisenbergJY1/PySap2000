# -*- coding: utf-8 -*-
"""
constraints - 约束定义模块

SAP2000 约束类型:
    Body - 刚体约束 (所有节点保持刚体运动)
    Diaphragm - 刚性隔板 (平面内刚性)
    Plate - 板约束 (平面外刚性)
    Rod - 杆约束 (轴向刚性)
    Beam - 梁约束 (梁截面保持平面)
    Equal - 等位移约束 (指定自由度位移相等)
    Local - 局部约束 (局部坐标系下的约束)
    Weld - 焊接约束 (完全刚性连接)
    Line - 线约束 (沿线刚性)
"""

from .enums import ConstraintType, ConstraintAxis
from .constraints import (
    # 通用函数
    get_constraint_count,
    get_constraint_name_list,
    get_constraint_type,
    change_constraint_name,
    delete_constraint,
    # Diaphragm
    get_diaphragm,
    set_diaphragm,
    # Body
    get_body,
    set_body,
    # Equal
    get_equal,
    set_equal,
    # Local
    get_local,
    set_local,
    # Beam
    get_beam,
    set_beam,
    # Plate
    get_plate,
    set_plate,
    # Rod
    get_rod,
    set_rod,
    # Weld
    get_weld,
    set_weld,
    # Line
    get_line,
    set_line,
    # 特殊函数
    get_special_rigid_diaphragm_list,
)

__all__ = [
    # 枚举
    "ConstraintType",
    "ConstraintAxis",
    # 通用函数
    "get_constraint_count",
    "get_constraint_name_list",
    "get_constraint_type",
    "change_constraint_name",
    "delete_constraint",
    # Diaphragm
    "get_diaphragm",
    "set_diaphragm",
    # Body
    "get_body",
    "set_body",
    # Equal
    "get_equal",
    "set_equal",
    # Local
    "get_local",
    "set_local",
    # Beam
    "get_beam",
    "set_beam",
    # Plate
    "get_plate",
    "set_plate",
    # Rod
    "get_rod",
    "set_rod",
    # Weld
    "get_weld",
    "set_weld",
    # Line
    "get_line",
    "set_line",
    # 特殊函数
    "get_special_rigid_diaphragm_list",
]
