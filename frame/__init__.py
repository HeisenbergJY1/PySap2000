# -*- coding: utf-8 -*-
"""
frame - 杆件属性相关类型和函数

为 AI Agent 设计的模块化 API，按功能分类：

1. 端部释放 (release)
   - set_frame_release: 设置释放类型 (两端固定/I端铰接/J端铰接/两端铰接)
   - set_frame_release_custom: 设置自定义释放 (6个自由度)
   - get_frame_release: 获取释放状态
   - get_frame_release_type: 获取释放类型
   - is_frame_hinged: 检查是否铰接

2. 局部坐标轴 (local_axes)
   - set_frame_local_axes: 设置局部轴角度
   - get_frame_local_axes: 获取局部轴角度
   - set_frame_local_axes_advanced: 设置高级局部轴
   - get_frame_local_axes_advanced: 获取高级局部轴
   - get_frame_transformation_matrix: 获取变换矩阵

3. 截面修改器 (modifier)
   - set_frame_modifiers: 设置修改器
   - get_frame_modifiers: 获取修改器
   - delete_frame_modifiers: 删除修改器

4. 质量 (mass)
   - set_frame_mass: 设置单位长度质量
   - get_frame_mass: 获取单位长度质量
   - delete_frame_mass: 删除附加质量

5. 选择 (selection)
   - set_frame_selected: 设置选择状态
   - select_frame/deselect_frame: 选中/取消选中

6. 组分配 (group)
   - add_frame_to_group: 添加到组
   - remove_frame_from_group: 从组移除
   - get_frame_groups: 获取所属组

7. 属性分配 (property)
   - set_frame_section: 设置截面属性（支持变截面参数）
   - get_frame_section: 获取截面属性
   - get_frame_section_nonprismatic: 获取变截面分配数据

注意: 杆件荷载相关函数在 loads 模块
"""

# ==================== 枚举类型 ====================
from .enums import (
    FrameType,
    FrameSectionType,
    FrameReleaseType,
    ItemType,
    SECTION_TYPE_NAMES,
    RELEASE_PRESETS,
)

# ==================== 数据类 ====================
from .data_classes import (
    FrameReleaseData,
    FrameModifierData,
    FrameLocalAxesData,
    FrameLocalAxesAdvancedData,
    FrameMassData,
    FrameSectionNonPrismaticData,
)

# ==================== 端部释放函数 ====================
from .release import (
    set_frame_release,
    set_frame_release_custom,
    get_frame_release,
    get_frame_release_type,
    is_frame_hinged,
)

# ==================== 局部坐标轴函数 ====================
from .local_axes import (
    set_frame_local_axes,
    get_frame_local_axes,
    set_frame_local_axes_advanced,
    get_frame_local_axes_advanced,
    get_frame_transformation_matrix,
)

# ==================== 修改器函数 ====================
from .modifier import (
    set_frame_modifiers,
    set_frame_modifiers_tuple,
    get_frame_modifiers,
    get_frame_modifiers_tuple,
    delete_frame_modifiers,
)

# ==================== 质量函数 ====================
from .mass import (
    set_frame_mass,
    get_frame_mass,
    get_frame_mass_data,
    delete_frame_mass,
    has_frame_mass,
)

# ==================== 选择函数 ====================
from .selection import (
    set_frame_selected,
    get_frame_selected,
    select_frame,
    deselect_frame,
    select_frames,
    deselect_frames,
    is_frame_selected,
)

# ==================== 组分配函数 ====================
from .group import (
    set_frame_group,
    add_frame_to_group,
    remove_frame_from_group,
    get_frame_groups,
    is_frame_in_group,
    add_frames_to_group,
    remove_frames_from_group,
)

# ==================== 属性分配函数 ====================
from .property import (
    set_frame_section,
    get_frame_section,
    get_frame_section_info,
    get_frame_section_nonprismatic,
    set_frame_material_overwrite,
    get_frame_material_overwrite,
    set_frame_material_temperature,
    get_frame_material_temperature,
)

# ==================== 铰数据类 ====================
from .hinge import (
    FrameHinge,
    FrameHingeType,
    HINGE_RELEASES,
)


# ==================== API 分类索引 (供 AI Agent 发现功能) ====================

FRAME_API_CATEGORIES = {
    "端部释放": {
        "description": "设置杆件端部的约束释放（铰接）",
        "functions": [
            "set_frame_release",
            "set_frame_release_custom",
            "get_frame_release",
            "get_frame_release_type",
            "is_frame_hinged",
        ]
    },
    "局部坐标轴": {
        "description": "设置杆件的局部坐标轴方向",
        "functions": [
            "set_frame_local_axes",
            "get_frame_local_axes",
            "set_frame_local_axes_advanced",
            "get_frame_local_axes_advanced",
            "get_frame_transformation_matrix",
        ]
    },
    "截面修改器": {
        "description": "设置杆件的截面属性修改器（刚度折减等）",
        "functions": [
            "set_frame_modifiers",
            "set_frame_modifiers_tuple",
            "get_frame_modifiers",
            "get_frame_modifiers_tuple",
            "delete_frame_modifiers",
        ]
    },
    "质量": {
        "description": "设置杆件的附加质量",
        "functions": [
            "set_frame_mass",
            "get_frame_mass",
            "get_frame_mass_data",
            "delete_frame_mass",
            "has_frame_mass",
        ]
    },
    "选择": {
        "description": "设置杆件的选择状态",
        "functions": [
            "set_frame_selected",
            "get_frame_selected",
            "select_frame",
            "deselect_frame",
            "select_frames",
            "deselect_frames",
            "is_frame_selected",
        ]
    },
    "组分配": {
        "description": "设置杆件的组分配",
        "functions": [
            "set_frame_group",
            "add_frame_to_group",
            "remove_frame_from_group",
            "get_frame_groups",
            "is_frame_in_group",
            "add_frames_to_group",
            "remove_frames_from_group",
        ]
    },
    "属性分配": {
        "description": "设置杆件的截面属性和材料",
        "functions": [
            "set_frame_section",
            "get_frame_section",
            "get_frame_section_info",
            "get_frame_section_nonprismatic",
            "set_frame_material_overwrite",
            "get_frame_material_overwrite",
            "set_frame_material_temperature",
            "get_frame_material_temperature",
        ]
    },
}


# ==================== 导出列表 ====================

__all__ = [
    # 枚举类型
    'FrameType',
    'FrameSectionType',
    'FrameReleaseType',
    'ItemType',
    'SECTION_TYPE_NAMES',
    'RELEASE_PRESETS',
    
    # 数据类
    'FrameReleaseData',
    'FrameModifierData',
    'FrameLocalAxesData',
    'FrameLocalAxesAdvancedData',
    'FrameMassData',
    'FrameSectionNonPrismaticData',
    'FrameHinge',
    'FrameHingeType',
    'HINGE_RELEASES',
    
    # 端部释放函数
    'set_frame_release',
    'set_frame_release_custom',
    'get_frame_release',
    'get_frame_release_type',
    'is_frame_hinged',
    
    # 局部坐标轴函数
    'set_frame_local_axes',
    'get_frame_local_axes',
    'set_frame_local_axes_advanced',
    'get_frame_local_axes_advanced',
    'get_frame_transformation_matrix',
    
    # 修改器函数
    'set_frame_modifiers',
    'set_frame_modifiers_tuple',
    'get_frame_modifiers',
    'get_frame_modifiers_tuple',
    'delete_frame_modifiers',
    
    # 质量函数
    'set_frame_mass',
    'get_frame_mass',
    'get_frame_mass_data',
    'delete_frame_mass',
    'has_frame_mass',
    
    # 选择函数
    'set_frame_selected',
    'get_frame_selected',
    'select_frame',
    'deselect_frame',
    'select_frames',
    'deselect_frames',
    'is_frame_selected',
    
    # 组分配函数
    'set_frame_group',
    'add_frame_to_group',
    'remove_frame_from_group',
    'get_frame_groups',
    'is_frame_in_group',
    'add_frames_to_group',
    'remove_frames_from_group',
    
    # 属性分配函数
    'set_frame_section',
    'get_frame_section',
    'get_frame_section_info',
    'get_frame_section_nonprismatic',
    'set_frame_material_overwrite',
    'get_frame_material_overwrite',
    'set_frame_material_temperature',
    'get_frame_material_temperature',
    
    # API 分类索引
    'FRAME_API_CATEGORIES',
]
