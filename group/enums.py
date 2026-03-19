# -*- coding: utf-8 -*-
"""
enums.py - 组相关枚举

SAP2000 API 中组相关的枚举定义
"""

from enum import IntEnum


class GroupObjectType(IntEnum):
    """
    组内对象类型
    
    用于 GetAssignments 返回的 ObjectType
    
    SAP2000 API:
        1 = Point object
        2 = Frame object
        3 = Cable object
        4 = Tendon object
        5 = Area object
        6 = Solid object
        7 = Link object
    """
    POINT = 1
    FRAME = 2
    CABLE = 3
    TENDON = 4
    AREA = 5
    SOLID = 6
    LINK = 7
