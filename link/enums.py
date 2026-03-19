# -*- coding: utf-8 -*-
"""
enums.py - Link 对象相关枚举类型
对应 SAP2000 的 LinkObj 相关枚举
"""

from enum import IntEnum


class LinkType(IntEnum):
    """
    连接单元类型
    
    对应 SAP2000 PropLink 的类型
    """
    LINEAR = 1
    DAMPER = 2
    GAP = 3
    HOOK = 4
    PLASTIC_WEN = 5
    RUBBER_ISOLATOR = 6
    FRICTION_ISOLATOR = 7
    MULTI_LINEAR_ELASTIC = 8
    MULTI_LINEAR_PLASTIC = 9
    TENSION_COMPRESSION_FRICTION_ISOLATOR = 10


class LinkDirectionalType(IntEnum):
    """连接单元方向类型"""
    TWO_JOINT = 1       # 两节点连接
    ONE_JOINT = 2       # 单节点连接（接地）


class LinkItemType(IntEnum):
    """
    eItemType 枚举
    用于 SetLocalAxes, SetPropertyFD 等方法
    """
    OBJECT = 0           # 单个对象
    GROUP = 1            # 组内所有对象
    SELECTED_OBJECTS = 2 # 所有选中的对象


class AxisVectorOption(IntEnum):
    """轴/平面参考向量选项"""
    COORDINATE_DIRECTION = 1  # 坐标方向
    TWO_JOINTS = 2            # 两节点
    USER_VECTOR = 3           # 用户向量
