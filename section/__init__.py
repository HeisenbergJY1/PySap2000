# -*- coding: utf-8 -*-
"""
section - Section property definitions (`PropXxx` APIs).

This package defines section properties themselves, rather than assigning
those properties to objects. Use the corresponding functional modules
(`frame/`, `area/`, `cable/`, `link/`) for assignments.

Includes section definitions for SAP2000 objects:
- `FrameSection`: frame/member sections (`PropFrame`)
- `CableSection`: cable sections (`PropCable`)
- `AreaSection`: area sections (`PropArea`)
- `LinkSection`: link properties (`PropLink`)

Material definitions live in `structure_core/material.py`.

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
