# -*- coding: utf-8 -*-
"""
enums.py - Point 相关枚举类型
"""

from enum import IntEnum


class PointSupportType(IntEnum):
    """
    节点支座类型
    
    用于快速设置常见支座条件，对应 set_point_support() 函数
    """
    FIXED = 0           # 固定支座 (U1,U2,U3,R1,R2,R3 全约束)
    HINGED = 1          # 铰接支座 (U1,U2,U3 约束, R1,R2,R3 自由)
    ROLLER = 2          # 滚动支座 (仅 U3 约束)
    ROLLER_IN_X = 3     # X向滚动 (U2,U3 约束)
    ROLLER_IN_Y = 4     # Y向滚动 (U1,U3 约束)
    ROLLER_IN_Z = 5     # Z向滚动 (U1,U2 约束)
    FREE = 6            # 自由 (无约束)


class ItemType(IntEnum):
    """
    项目类型枚举
    
    用于指定 API 操作的对象范围
    """
    OBJECT = 0              # 单个对象
    GROUP = 1               # 组内所有对象
    SELECTED_OBJECTS = 2    # 当前选中的对象


class PanelZonePropType(IntEnum):
    """节点域属性类型"""
    ELASTIC_FROM_COLUMN = 0         # 从柱计算弹性刚度
    ELASTIC_FROM_COLUMN_DOUBLER = 1 # 从柱+加劲板计算弹性刚度
    FROM_SPRING_STIFFNESS = 2       # 指定弹簧刚度
    FROM_LINK_PROPERTY = 3          # 使用连接单元属性


class PanelZoneConnectivity(IntEnum):
    """节点域连接类型"""
    BEAMS_TO_OTHER = 0      # 梁连接到其他
    BRACES_TO_OTHER = 1     # 支撑连接到其他


class PanelZoneLocalAxisFrom(IntEnum):
    """节点域局部轴来源"""
    FROM_COLUMN = 0         # 从柱
    USER_DEFINED = 1        # 用户定义


# 支座类型对应的约束值 (U1, U2, U3, R1, R2, R3)
SUPPORT_RESTRAINTS = {
    PointSupportType.FIXED: (True, True, True, True, True, True),
    PointSupportType.HINGED: (True, True, True, False, False, False),
    PointSupportType.ROLLER: (False, False, True, False, False, False),
    PointSupportType.ROLLER_IN_X: (False, True, True, False, False, False),
    PointSupportType.ROLLER_IN_Y: (True, False, True, False, False, False),
    PointSupportType.ROLLER_IN_Z: (True, True, False, False, False, False),
    PointSupportType.FREE: (False, False, False, False, False, False),
}
