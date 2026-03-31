# -*- coding: utf-8 -*-
"""
named_assigns - Named assignment definitions

Wraps the SAP2000 `NamedAssign` API for reusable modifier and end-release definitions.

Compared with the functional modules:
- `frame/modifier.py` and similar modules set properties directly on objects (for example `FrameObj.SetModifiers`)
- `named_assigns`: creates named reusable definitions that can be referenced by multiple objects (for example `NamedAssign.ModifierFrame`)

SAP2000 API structure:
- `NamedAssign.ModifierArea` - Area stiffness modifier definitions
- `NamedAssign.ModifierCable` - Cable modifier definitions
- `NamedAssign.ModifierFrame` - Frame modifier definitions
- `NamedAssign.ReleaseFrame` - Frame end-release definitions

Usage:
    from PySap2000.named_assigns import (
        NamedAreaModifier,
        NamedFrameModifier,
        NamedCableModifier,
        NamedFrameRelease,
    )
    
    # Create a named modifier
    mod = NamedFrameModifier(name="BeamMod", inertia_33=0.5)
    mod._create(model)
    
    # Get all definitions
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

# API categories for discoverability
NAMED_ASSIGNS_API_CATEGORIES = {
    "area_modifier": {
        "description": "Area stiffness modifier definitions",
        "classes": ["NamedAreaModifier"],
        "api_path": "NamedAssign.ModifierArea",
    },
    "frame_modifier": {
        "description": "Frame modifier definitions",
        "classes": ["NamedFrameModifier"],
        "api_path": "NamedAssign.ModifierFrame",
    },
    "cable_modifier": {
        "description": "Cable modifier definitions",
        "classes": ["NamedCableModifier"],
        "api_path": "NamedAssign.ModifierCable",
    },
    "frame_release": {
        "description": "Frame end-release definitions",
        "classes": ["NamedFrameRelease"],
        "api_path": "NamedAssign.ReleaseFrame",
    },
}
