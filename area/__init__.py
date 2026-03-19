# -*- coding: utf-8 -*-
"""
area - Area 对象类型定义和独立函数模块

对应 SAP2000 的 AreaObj 相关设置 (不包含荷载)

荷载相关内容请使用 loads/area_load.py

用法:
    from area import AREA_API_CATEGORIES
    print(AREA_API_CATEGORIES["弹簧"]["functions"])
"""

# ==================== 枚举类型 ====================
from .enums import (
    ItemType,
    AreaType,
    AreaMeshType,
    AreaThicknessType,
    AreaOffsetType,
    AreaSpringType,
    AreaSimpleSpringType,
    AreaSpringLocalOneType,
    AreaFace,
    PlaneRefVectorOption,
)

# ==================== 数据类 ====================
from .data_classes import (
    AreaSpringData,
    AreaAutoMeshData,
    AreaLocalAxesData,
    AreaLocalAxesAdvancedData,
    AreaThicknessData,
    AreaOffsetData,
    AreaModifierData,
    AreaMassData,
)

# ==================== 弹簧函数 ====================
from .spring import (
    set_area_spring,
    get_area_spring,
    delete_area_spring,
    has_area_spring,
)

# ==================== 局部坐标轴函数 ====================
from .local_axes import (
    set_area_local_axes,
    get_area_local_axes,
    set_area_local_axes_advanced,
    get_area_local_axes_advanced,
    get_area_transformation_matrix,
)

# ==================== 修改器函数 ====================
from .modifier import (
    set_area_modifiers,
    set_area_modifiers_tuple,
    get_area_modifiers,
    get_area_modifiers_tuple,
    delete_area_modifiers,
)

# ==================== 质量函数 ====================
from .mass import (
    set_area_mass,
    get_area_mass,
    get_area_mass_data,
    delete_area_mass,
    has_area_mass,
)

# ==================== 厚度函数 ====================
from .thickness import (
    set_area_thickness,
    get_area_thickness,
    has_area_thickness,
)

# ==================== 偏移函数 ====================
from .offset import (
    set_area_offset,
    get_area_offset,
    has_area_offset,
)

# ==================== 自动网格函数 ====================
from .auto_mesh import (
    set_area_auto_mesh,
    get_area_auto_mesh,
    is_area_meshed,
)

# ==================== 边缘约束函数 ====================
from .edge_constraint import (
    set_area_edge_constraint,
    get_area_edge_constraint,
    enable_area_edge_constraint,
    disable_area_edge_constraint,
    has_area_edge_constraint,
)

# ==================== 选择函数 ====================
from .selection import (
    set_area_selected,
    get_area_selected,
    select_area,
    deselect_area,
    select_areas,
    deselect_areas,
    is_area_selected,
)

# ==================== 组分配函数 ====================
from .group import (
    set_area_group,
    add_area_to_group,
    remove_area_from_group,
    get_area_groups,
    is_area_in_group,
    add_areas_to_group,
    remove_areas_from_group,
)

# ==================== 属性分配函数 ====================
from .property import (
    set_area_property,
    get_area_property,
    get_area_property_type,
    set_area_material_overwrite,
    get_area_material_overwrite,
    set_area_material_temperature,
    get_area_material_temperature,
)


# ==================== API 分类索引 (供 AI Agent 发现功能) ====================

AREA_API_CATEGORIES = {
    "弹簧": {
        "description": "设置面单元的弹簧支撑",
        "functions": [
            "set_area_spring",
            "get_area_spring",
            "delete_area_spring",
            "has_area_spring",
        ]
    },
    "局部坐标轴": {
        "description": "设置面单元的局部坐标轴方向",
        "functions": [
            "set_area_local_axes",
            "get_area_local_axes",
            "set_area_local_axes_advanced",
            "get_area_local_axes_advanced",
            "get_area_transformation_matrix",
        ]
    },
    "截面修改器": {
        "description": "设置面单元的截面属性修改器（刚度折减等）",
        "functions": [
            "set_area_modifiers",
            "set_area_modifiers_tuple",
            "get_area_modifiers",
            "get_area_modifiers_tuple",
            "delete_area_modifiers",
        ]
    },
    "质量": {
        "description": "设置面单元的附加质量",
        "functions": [
            "set_area_mass",
            "get_area_mass",
            "get_area_mass_data",
            "delete_area_mass",
            "has_area_mass",
        ]
    },
    "厚度": {
        "description": "设置面单元的厚度覆盖",
        "functions": [
            "set_area_thickness",
            "get_area_thickness",
            "has_area_thickness",
        ]
    },
    "偏移": {
        "description": "设置面单元的偏移",
        "functions": [
            "set_area_offset",
            "get_area_offset",
            "has_area_offset",
        ]
    },
    "自动网格": {
        "description": "设置面单元的自动网格划分",
        "functions": [
            "set_area_auto_mesh",
            "get_area_auto_mesh",
            "is_area_meshed",
        ]
    },
    "边缘约束": {
        "description": "设置面单元的边缘约束",
        "functions": [
            "set_area_edge_constraint",
            "get_area_edge_constraint",
            "enable_area_edge_constraint",
            "disable_area_edge_constraint",
            "has_area_edge_constraint",
        ]
    },
    "选择": {
        "description": "设置面单元的选择状态",
        "functions": [
            "set_area_selected",
            "get_area_selected",
            "select_area",
            "deselect_area",
            "select_areas",
            "deselect_areas",
            "is_area_selected",
        ]
    },
    "组分配": {
        "description": "设置面单元的组分配",
        "functions": [
            "set_area_group",
            "add_area_to_group",
            "remove_area_from_group",
            "get_area_groups",
            "is_area_in_group",
            "add_areas_to_group",
            "remove_areas_from_group",
        ]
    },
    "属性分配": {
        "description": "设置面单元的截面属性和材料",
        "functions": [
            "set_area_property",
            "get_area_property",
            "get_area_property_type",
            "set_area_material_overwrite",
            "get_area_material_overwrite",
            "set_area_material_temperature",
            "get_area_material_temperature",
        ]
    },
}


# ==================== 导出列表 ====================

__all__ = [
    # 枚举类型
    'ItemType',
    'AreaType',
    'AreaMeshType',
    'AreaThicknessType',
    'AreaOffsetType',
    'AreaSpringType',
    'AreaSimpleSpringType',
    'AreaSpringLocalOneType',
    'AreaFace',
    'PlaneRefVectorOption',
    
    # 数据类
    'AreaSpringData',
    'AreaAutoMeshData',
    'AreaLocalAxesData',
    'AreaLocalAxesAdvancedData',
    'AreaThicknessData',
    'AreaOffsetData',
    'AreaModifierData',
    'AreaMassData',
    
    # 弹簧函数
    'set_area_spring',
    'get_area_spring',
    'delete_area_spring',
    'has_area_spring',
    
    # 局部坐标轴函数
    'set_area_local_axes',
    'get_area_local_axes',
    'set_area_local_axes_advanced',
    'get_area_local_axes_advanced',
    'get_area_transformation_matrix',
    
    # 修改器函数
    'set_area_modifiers',
    'set_area_modifiers_tuple',
    'get_area_modifiers',
    'get_area_modifiers_tuple',
    'delete_area_modifiers',
    
    # 质量函数
    'set_area_mass',
    'get_area_mass',
    'get_area_mass_data',
    'delete_area_mass',
    'has_area_mass',
    
    # 厚度函数
    'set_area_thickness',
    'get_area_thickness',
    'has_area_thickness',
    
    # 偏移函数
    'set_area_offset',
    'get_area_offset',
    'has_area_offset',
    
    # 自动网格函数
    'set_area_auto_mesh',
    'get_area_auto_mesh',
    'is_area_meshed',
    
    # 边缘约束函数
    'set_area_edge_constraint',
    'get_area_edge_constraint',
    'enable_area_edge_constraint',
    'disable_area_edge_constraint',
    'has_area_edge_constraint',
    
    # 选择函数
    'set_area_selected',
    'get_area_selected',
    'select_area',
    'deselect_area',
    'select_areas',
    'deselect_areas',
    'is_area_selected',
    
    # 组分配函数
    'set_area_group',
    'add_area_to_group',
    'remove_area_from_group',
    'get_area_groups',
    'is_area_in_group',
    'add_areas_to_group',
    'remove_areas_from_group',
    
    # 属性分配函数
    'set_area_property',
    'get_area_property',
    'get_area_property_type',
    'set_area_material_overwrite',
    'get_area_material_overwrite',
    'set_area_material_temperature',
    'get_area_material_temperature',
    
    # API 分类索引
    'AREA_API_CATEGORIES',
]
