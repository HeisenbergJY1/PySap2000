# -*- coding: utf-8 -*-
"""
point - 节点属性相关类型和函数

为 AI Agent 设计的模块化 API，按功能分类：

1. 支座 (support)
   - set_point_support: 设置支座类型 (固定/铰接/滚动)
   - set_point_restraint: 设置自定义约束
   - get_point_restraint: 获取约束状态
   - delete_point_restraint: 删除约束

2. 弹簧 (spring)
   - set_point_spring: 设置弹簧刚度
   - get_point_spring: 获取弹簧刚度
   - delete_point_spring: 删除弹簧

3. 质量 (mass)
   - set_point_mass: 设置质量
   - get_point_mass: 获取质量
   - delete_point_mass: 删除质量

4. 约束 (constraint)
   - set_point_constraint: 分配到刚性约束 (如隔板)
   - get_point_constraint: 获取约束分配
   - delete_point_constraint: 删除约束分配

5. 局部坐标轴 (local_axes)
   - set_point_local_axes: 设置局部轴角度
   - get_point_local_axes: 获取局部轴角度

6. 节点域 (panel_zone)
   - set_point_panel_zone: 设置节点域
   - get_point_panel_zone: 获取节点域
   - delete_point_panel_zone: 删除节点域

注意: 节点荷载相关函数已移至 loads 模块
"""

# 枚举类型
from .enums import (
    PointSupportType,
    ItemType,
    PanelZonePropType,
    PanelZoneConnectivity,
    PanelZoneLocalAxisFrom,
    SUPPORT_RESTRAINTS,
)

# 数据类
from .data_classes import (
    PointConstraintAssignment,
    PointSpringData,
    PointMassData,
    PanelZoneData,
)

# 支座函数
from .support import (
    set_point_support,
    set_point_restraint,
    get_point_restraint,
    get_point_support_type,
    delete_point_restraint,
    get_points_with_support,
)

# 弹簧函数
from .spring import (
    set_point_spring,
    get_point_spring,
    delete_point_spring,
    set_point_spring_coupled,
    get_point_spring_coupled,
    is_point_spring_coupled,
)

# 质量函数
from .mass import (
    set_point_mass,
    get_point_mass,
    delete_point_mass,
    set_point_mass_by_weight,
    set_point_mass_by_volume,
)

# 约束函数
from .constraint import (
    set_point_constraint,
    get_point_constraint,
    delete_point_constraint,
    get_points_in_constraint,
)

# 局部坐标轴函数
from .local_axes import (
    set_point_local_axes,
    get_point_local_axes,
    set_point_local_axes_advanced,
    get_point_local_axes_advanced,
    get_point_transformation_matrix,
)

# 节点域函数
from .panel_zone import (
    set_point_panel_zone,
    get_point_panel_zone,
    delete_point_panel_zone,
    has_point_panel_zone,
)


# API 分类索引 (供 AI Agent 参考)
POINT_API_CATEGORIES = {
    "支座与边界条件": {
        "description": "设置节点的支座类型和约束条件",
        "functions": [
            "set_point_support",
            "set_point_restraint",
            "get_point_restraint",
            "get_point_support_type",
            "delete_point_restraint",
            "get_points_with_support",
        ]
    },
    "弹簧": {
        "description": "设置节点的弹簧刚度",
        "functions": [
            "set_point_spring",
            "get_point_spring",
            "delete_point_spring",
            "set_point_spring_coupled",
            "get_point_spring_coupled",
            "is_point_spring_coupled",
        ]
    },
    "质量": {
        "description": "设置节点的附加质量",
        "functions": [
            "set_point_mass",
            "get_point_mass",
            "delete_point_mass",
            "set_point_mass_by_weight",
            "set_point_mass_by_volume",
        ]
    },
    "刚性约束": {
        "description": "设置刚性隔板等约束",
        "functions": [
            "set_point_constraint",
            "get_point_constraint",
            "delete_point_constraint",
            "get_points_in_constraint",
        ]
    },
    "局部坐标系": {
        "description": "设置节点的局部坐标轴",
        "functions": [
            "set_point_local_axes",
            "get_point_local_axes",
            "set_point_local_axes_advanced",
            "get_point_local_axes_advanced",
            "get_point_transformation_matrix",
        ]
    },
    "节点域": {
        "description": "设置梁柱节点的节点域",
        "functions": [
            "set_point_panel_zone",
            "get_point_panel_zone",
            "delete_point_panel_zone",
            "has_point_panel_zone",
        ]
    },
}


__all__ = [
    # 枚举
    'PointSupportType',
    'ItemType',
    'PanelZonePropType',
    'PanelZoneConnectivity',
    'PanelZoneLocalAxisFrom',
    'SUPPORT_RESTRAINTS',
    
    # 数据类
    'PointConstraintAssignment',
    'PointSpringData',
    'PointMassData',
    'PanelZoneData',
    
    # 支座函数
    'set_point_support',
    'set_point_restraint',
    'get_point_restraint',
    'get_point_support_type',
    'delete_point_restraint',
    'get_points_with_support',
    
    # 弹簧函数
    'set_point_spring',
    'get_point_spring',
    'delete_point_spring',
    'set_point_spring_coupled',
    'get_point_spring_coupled',
    'is_point_spring_coupled',
    
    # 质量函数
    'set_point_mass',
    'get_point_mass',
    'delete_point_mass',
    'set_point_mass_by_weight',
    'set_point_mass_by_volume',
    
    # 约束函数
    'set_point_constraint',
    'get_point_constraint',
    'delete_point_constraint',
    'get_points_in_constraint',
    
    # 局部坐标轴函数
    'set_point_local_axes',
    'get_point_local_axes',
    'set_point_local_axes_advanced',
    'get_point_local_axes_advanced',
    'get_point_transformation_matrix',
    
    # 节点域函数
    'set_point_panel_zone',
    'get_point_panel_zone',
    'delete_point_panel_zone',
    'has_point_panel_zone',
    
    # API 分类索引
    'POINT_API_CATEGORIES',
]
