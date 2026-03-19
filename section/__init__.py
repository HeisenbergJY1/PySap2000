# -*- coding: utf-8 -*-
"""
section - 截面定义模块 (PropXxx API)

本模块用于定义截面属性（是什么），而非分配属性到对象（怎么用）。
属性分配功能请使用 types_for_xxx 模块。

包含 SAP2000 中各种对象的截面定义：
- FrameSection: 杆件截面 (PropFrame)
- CableSection: 缆索截面 (PropCable)
- AreaSection: 面截面 (PropArea)
- LinkSection: 连接截面 (PropLink)

材料定义在 structure_core/material.py

Usage:
    from section import FrameSection, AreaSection, LinkSection
    from structure_core import Material
"""

from .frame_section import FrameSection, FrameSectionType, SECTION_TYPE_NAMES
from .cable_section import CableSection
from .area_section import AreaSection, AreaSectionType, ShellType, PlaneType, AreaModifiers
from .link_section import LinkSection, LinkSectionType

__all__ = [
    # Frame
    'FrameSection',
    'FrameSectionType',
    'SECTION_TYPE_NAMES',
    # Cable
    'CableSection',
    # Area
    'AreaSection',
    'AreaSectionType',
    'ShellType',
    'PlaneType',
    'AreaModifiers',
    # Link
    'LinkSection',
    'LinkSectionType',
]
