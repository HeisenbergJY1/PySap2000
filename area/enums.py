# -*- coding: utf-8 -*-
"""
enums.py - Area 对象相关枚举类型
对应 SAP2000 的 AreaObj 相关枚举

注意: 荷载相关枚举已移至 loads/area_load.py
"""

from enum import IntEnum


class AreaType(IntEnum):
    """面单元类型"""
    SHELL = 1      # 壳单元
    PLANE = 2      # 平面单元
    ASOLID = 3     # 轴对称实体


class AreaMeshType(IntEnum):
    """面单元自动网格划分类型"""
    NO_MESH = 0                 # 不划分
    MESH_BY_NUMBER = 1          # 按数量划分
    MESH_BY_MAX_SIZE = 2        # 按最大尺寸划分
    MESH_BY_POINTS_ON_EDGE = 3  # 按边上点划分
    COOKIE_CUT_BY_LINES = 4     # 按线切割
    COOKIE_CUT_BY_POINTS = 5    # 按点切割
    GENERAL_DIVIDE = 6          # 通用划分


class AreaThicknessType(IntEnum):
    """面单元厚度覆盖类型"""
    NO_OVERWRITE = 0     # 不覆盖
    BY_JOINT_PATTERN = 1 # 按节点模式
    BY_POINT = 2         # 按节点


class AreaOffsetType(IntEnum):
    """面单元偏移类型"""
    NO_OFFSET = 0        # 无偏移
    BY_JOINT_PATTERN = 1 # 按节点模式
    BY_POINT = 2         # 按节点


class AreaSpringType(IntEnum):
    """面单元弹簧类型"""
    SIMPLE_SPRING = 1   # 简单弹簧
    LINK_PROPERTY = 2   # 连接属性


class AreaSimpleSpringType(IntEnum):
    """面单元简单弹簧类型"""
    TENSION_COMPRESSION = 1  # 拉压
    COMPRESSION_ONLY = 2     # 仅压
    TENSION_ONLY = 3         # 仅拉


class AreaSpringLocalOneType(IntEnum):
    """面单元弹簧局部1轴方向类型"""
    PARALLEL_TO_LOCAL_AXIS = 1  # 平行于局部轴
    NORMAL_TO_FACE = 2          # 垂直于面
    USER_VECTOR = 3             # 用户向量


class AreaFace(IntEnum):
    """面单元面"""
    BOTTOM = -1  # 底面
    TOP = -2     # 顶面


class PlaneRefVectorOption(IntEnum):
    """平面参考向量选项"""
    COORDINATE_DIRECTION = 1  # 坐标方向
    TWO_JOINTS = 2            # 两节点
    USER_VECTOR = 3           # 用户向量


class ItemType(IntEnum):
    """eItemType 枚举"""
    OBJECT = 0            # 单个对象
    GROUP = 1             # 组
    SELECTED_OBJECTS = 2  # 选中的对象
