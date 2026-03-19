# -*- coding: utf-8 -*-
"""
named_assigns - 命名赋值定义

SAP2000 的 NamedAssign API，用于创建可复用的属性修改器和端部释放定义。

与 types_for_xxx 的区别：
- types_for_xxx: 直接对对象设置属性 (如 FrameObj.SetModifiers)
- named_assigns: 创建命名定义，可被多个对象引用 (如 NamedAssign.ModifierFrame)

SAP2000 API 结构:
- NamedAssign.ModifierArea - 面单元刚度修改器定义
- NamedAssign.ModifierCable - 索单元修改器定义
- NamedAssign.ModifierFrame - 杆件修改器定义
- NamedAssign.ReleaseFrame - 杆件端部释放定义

Usage:
    from PySap2000.named_assigns import (
        NamedAreaModifier,
        NamedFrameModifier,
        NamedCableModifier,
        NamedFrameRelease,
    )
    
    # 创建命名修改器
    mod = NamedFrameModifier(name="BeamMod", inertia_33=0.5)
    mod._create(model)
    
    # 获取所有定义
    all_mods = NamedFrameModifier.get_all(model)
"""

from .area_modifier import NamedAreaModifier
from .frame_modifier import NamedFrameModifier
from .cable_modifier import NamedCableModifier
from .frame_release import NamedFrameRelease

__all__ = [
    "NamedAreaModifier",
    "NamedFrameModifier",
    "NamedCableModifier",
    "NamedFrameRelease",
]

# AI Agent 友好的 API 分类
NAMED_ASSIGNS_API_CATEGORIES = {
    "area_modifier": {
        "description": "面单元刚度修改器定义",
        "classes": ["NamedAreaModifier"],
        "api_path": "NamedAssign.ModifierArea",
    },
    "frame_modifier": {
        "description": "杆件修改器定义",
        "classes": ["NamedFrameModifier"],
        "api_path": "NamedAssign.ModifierFrame",
    },
    "cable_modifier": {
        "description": "索单元修改器定义",
        "classes": ["NamedCableModifier"],
        "api_path": "NamedAssign.ModifierCable",
    },
    "frame_release": {
        "description": "杆件端部释放定义",
        "classes": ["NamedFrameRelease"],
        "api_path": "NamedAssign.ReleaseFrame",
    },
}
