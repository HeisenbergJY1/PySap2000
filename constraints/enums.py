# -*- coding: utf-8 -*-
"""
enums.py - 约束相关枚举类型
"""

from enum import IntEnum


class ConstraintType(IntEnum):
    """
    约束类型枚举 (eConstraintType)
    """
    BODY = 1        # 刚体约束
    DIAPHRAGM = 2   # 刚性隔板
    PLATE = 3       # 板约束
    ROD = 4         # 杆约束
    BEAM = 5        # 梁约束
    EQUAL = 6       # 等位移约束
    LOCAL = 7       # 局部约束
    WELD = 8        # 焊接约束
    LINE = 13       # 线约束


class ConstraintAxis(IntEnum):
    """
    约束轴向枚举 (eConstraintAxis)
    
    用于 Diaphragm, Beam, Plate, Rod 等约束类型
    """
    X = 1           # X轴
    Y = 2           # Y轴
    Z = 3           # Z轴
    AUTO = 4        # 自动确定
