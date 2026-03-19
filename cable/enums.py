# -*- coding: utf-8 -*-
"""
enums.py - Cable 对象相关枚举类型
对应 SAP2000 的 CableObj 相关枚举
"""

from enum import IntEnum


class CableType(IntEnum):
    """
    索类型定义
    
    对应 SAP2000 CableObj.SetCableData 的 CableType 参数
    """
    MINIMUM_TENSION_AT_I_END = 1    # I端最小张力
    MINIMUM_TENSION_AT_J_END = 2    # J端最小张力
    TENSION_AT_I_END = 3            # I端张力 [F]
    TENSION_AT_J_END = 4            # J端张力 [F]
    HORIZONTAL_TENSION = 5          # 水平张力分量 [F]
    MAXIMUM_VERTICAL_SAG = 6        # 最大垂直垂度 [L]
    LOW_POINT_VERTICAL_SAG = 7      # 最低点垂直垂度 [L]
    UNDEFORMED_LENGTH = 8           # 未变形长度 [L]
    RELATIVE_UNDEFORMED_LENGTH = 9  # 相对未变形长度


class CableDefinitionType(IntEnum):
    """
    索定义类型 (用于截面指派)
    
    对应 SAP2000 CableObj 的定义方式
    """
    BY_POINTS = 1       # 通过节点定义
    BY_COORDINATES = 2  # 通过坐标定义
