# -*- coding: utf-8 -*-
"""
cable - Cable 对象扩展功能

包含:
- enums: CableType, CableDefinitionType
- property: 截面分配、材料覆盖、材料温度
- modifier: 修改系数
- mass: 附加质量
- output_station: 输出站点
- group: 组指派
- selection: 选择状态

荷载相关内容在 loads/cable_load.py
"""

from .enums import CableType, CableDefinitionType

from .modifier import (
    CableItemType,
    CableModifiers,
    set_cable_modifiers,
    get_cable_modifiers,
    delete_cable_modifiers,
)

from .property import (
    set_cable_section,
    get_cable_section,
    get_cable_section_list,
    set_cable_material_overwrite,
    get_cable_material_overwrite,
    set_cable_material_temp,
    get_cable_material_temp,
)

from .mass import (
    set_cable_mass,
    get_cable_mass,
    delete_cable_mass,
)

from .output_station import (
    CableOutputStationType,
    CableOutputStations,
    set_cable_output_stations,
    get_cable_output_stations,
)

from .group import (
    set_cable_group,
    get_cable_groups,
)

from .selection import (
    set_cable_selected,
    get_cable_selected,
    get_selected_cables,
)


# ==================== API 分类索引 (供 AI Agent 发现功能) ====================

CABLE_API_CATEGORIES = {
    "截面属性": {
        "description": "设置 Cable 的截面属性分配",
        "functions": [
            "set_cable_section",
            "get_cable_section",
            "get_cable_section_list",
        ]
    },
    "材料": {
        "description": "设置 Cable 的材料覆盖和温度",
        "functions": [
            "set_cable_material_overwrite",
            "get_cable_material_overwrite",
            "set_cable_material_temp",
            "get_cable_material_temp",
        ]
    },
    "修改系数": {
        "description": "设置 Cable 的修改系数",
        "functions": [
            "set_cable_modifiers",
            "get_cable_modifiers",
            "delete_cable_modifiers",
        ]
    },
    "质量": {
        "description": "设置 Cable 的附加质量",
        "functions": [
            "set_cable_mass",
            "get_cable_mass",
            "delete_cable_mass",
        ]
    },
    "输出站点": {
        "description": "设置 Cable 的输出站点",
        "functions": [
            "set_cable_output_stations",
            "get_cable_output_stations",
        ]
    },
    "组": {
        "description": "设置 Cable 的组分配",
        "functions": [
            "set_cable_group",
            "get_cable_groups",
        ]
    },
    "选择": {
        "description": "设置 Cable 的选择状态",
        "functions": [
            "set_cable_selected",
            "get_cable_selected",
            "get_selected_cables",
        ]
    },
}


__all__ = [
    # 枚举
    'CableType',
    'CableDefinitionType',
    'CableItemType',
    'CableOutputStationType',
    # 数据类
    'CableModifiers',
    'CableOutputStations',
    # 截面/材料属性
    'set_cable_section',
    'get_cable_section',
    'get_cable_section_list',
    'set_cable_material_overwrite',
    'get_cable_material_overwrite',
    'set_cable_material_temp',
    'get_cable_material_temp',
    # 修改系数
    'set_cable_modifiers',
    'get_cable_modifiers',
    'delete_cable_modifiers',
    # 质量
    'set_cable_mass',
    'get_cable_mass',
    'delete_cable_mass',
    # 输出站点
    'set_cable_output_stations',
    'get_cable_output_stations',
    # 组
    'set_cable_group',
    'get_cable_groups',
    # 选择
    'set_cable_selected',
    'get_cable_selected',
    'get_selected_cables',
    # API 分类索引
    'CABLE_API_CATEGORIES',
]
