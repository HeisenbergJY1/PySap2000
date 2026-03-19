# -*- coding: utf-8 -*-
"""
link - Link 对象类型定义和扩展函数模块

对应 SAP2000 的 LinkObj 相关设置

注意: 荷载相关函数在 loads/link_load.py
注意: 属性定义（PropLink）在 section/link_section.py

用法:
    # AI Agent 可以通过分类索引发现功能
    from link import LINK_API_CATEGORIES
    
    # 查看局部轴相关函数
    print(LINK_API_CATEGORIES["局部坐标轴"]["functions"])
    
    # 调用函数
    from link import set_link_local_axes
    set_link_local_axes(model, "1", 30)
"""

# ==================== 枚举类型 ====================
from .enums import (
    LinkType,
    LinkDirectionalType,
    LinkItemType,
    AxisVectorOption,
)

# ==================== 数据类 ====================
from .data_classes import (
    LinkLocalAxesData,
    LinkLocalAxesAdvancedData,
)

# ==================== 局部坐标轴函数 ====================
from .local_axes import (
    set_link_local_axes,
    get_link_local_axes,
    set_link_local_axes_advanced,
    get_link_local_axes_advanced,
    get_link_transformation_matrix,
)

# ==================== 选择函数 ====================
from .selection import (
    set_link_selected,
    get_link_selected,
    select_link,
    deselect_link,
    select_links,
    deselect_links,
    is_link_selected,
)


# ==================== 组分配函数 ====================
from .group import (
    set_link_group,
    add_link_to_group,
    remove_link_from_group,
    get_link_groups,
    is_link_in_group,
    add_links_to_group,
    remove_links_from_group,
)

# ==================== 属性分配函数 ====================
from .property import (
    set_link_property,
    get_link_property,
    set_link_property_fd,
    get_link_property_fd,
    get_link_property_info,
)


# ==================== API 分类索引 (供 AI Agent 发现功能) ====================

LINK_API_CATEGORIES = {
    "局部坐标轴": {
        "description": "设置连接单元的局部坐标轴方向",
        "functions": [
            "set_link_local_axes",           # 设置局部轴角度
            "get_link_local_axes",           # 获取局部轴角度
            "set_link_local_axes_advanced",  # 设置高级局部轴
            "get_link_local_axes_advanced",  # 获取高级局部轴
            "get_link_transformation_matrix", # 获取变换矩阵
        ]
    },
    "选择": {
        "description": "设置连接单元的选择状态",
        "functions": [
            "set_link_selected",   # 设置选择状态
            "get_link_selected",   # 获取选择状态
            "select_link",         # 选中连接单元
            "deselect_link",       # 取消选中连接单元
            "select_links",        # 批量选中连接单元
            "deselect_links",      # 批量取消选中连接单元
            "is_link_selected",    # 检查是否选中
        ]
    },
    "组分配": {
        "description": "设置连接单元的组分配",
        "functions": [
            "set_link_group",           # 设置组分配
            "add_link_to_group",        # 添加到组
            "remove_link_from_group",   # 从组移除
            "get_link_groups",          # 获取所属组
            "is_link_in_group",         # 检查是否在组中
            "add_links_to_group",       # 批量添加到组
            "remove_links_from_group",  # 批量从组移除
        ]
    },
    "属性分配": {
        "description": "设置连接单元的属性分配",
        "functions": [
            "set_link_property",      # 设置连接属性
            "get_link_property",      # 获取连接属性名称
            "set_link_property_fd",   # 设置频率相关属性
            "get_link_property_fd",   # 获取频率相关属性
            "get_link_property_info", # 获取属性信息（含频率相关）
        ]
    },
}


# ==================== 导出列表 ====================

__all__ = [
    # 枚举类型
    'LinkType',
    'LinkDirectionalType',
    'LinkItemType',
    'AxisVectorOption',
    
    # 数据类
    'LinkLocalAxesData',
    'LinkLocalAxesAdvancedData',
    
    # 局部坐标轴函数
    'set_link_local_axes',
    'get_link_local_axes',
    'set_link_local_axes_advanced',
    'get_link_local_axes_advanced',
    'get_link_transformation_matrix',
    
    # 选择函数
    'set_link_selected',
    'get_link_selected',
    'select_link',
    'deselect_link',
    'select_links',
    'deselect_links',
    'is_link_selected',
    
    # 组分配函数
    'set_link_group',
    'add_link_to_group',
    'remove_link_from_group',
    'get_link_groups',
    'is_link_in_group',
    'add_links_to_group',
    'remove_links_from_group',
    
    # 属性分配函数
    'set_link_property',
    'get_link_property',
    'set_link_property_fd',
    'get_link_property_fd',
    'get_link_property_info',
    
    # API 分类索引
    'LINK_API_CATEGORIES',
]
