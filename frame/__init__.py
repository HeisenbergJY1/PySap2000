# -*- coding: utf-8 -*-
"""
frame - Frame-related types and helper functions.

This package provides a modular API organized by feature:

1. End releases (`release`)
   - `set_frame_release`: assign a release preset
   - `set_frame_release_custom`: assign custom releases for 6 DOFs
   - `get_frame_release`: fetch release state
   - `get_frame_release_type`: fetch release preset type
   - `is_frame_hinged`: check whether the frame is hinged

2. Local axes (`local_axes`)
   - `set_frame_local_axes`: set local-axis rotation
   - `get_frame_local_axes`: fetch local-axis rotation
   - `set_frame_local_axes_advanced`: configure advanced local axes
   - `get_frame_local_axes_advanced`: fetch advanced local-axis data
   - `get_frame_transformation_matrix`: fetch the transformation matrix

3. Section modifiers (`modifier`)
   - `set_frame_modifiers`: assign modifiers
   - `get_frame_modifiers`: fetch modifiers
   - `delete_frame_modifiers`: remove modifiers

4. Mass (`mass`)
   - `set_frame_mass`: assign mass per unit length
   - `get_frame_mass`: fetch mass per unit length
   - `delete_frame_mass`: remove additional mass

5. Selection (`selection`)
   - `set_frame_selected`: set selection state
   - `select_frame` / `deselect_frame`: select or deselect a frame

6. Group assignment (`group`)
   - `add_frame_to_group`: add to a group
   - `remove_frame_from_group`: remove from a group
   - `get_frame_groups`: fetch assigned groups

7. Property assignment (`property`)
   - `set_frame_section`: assign section properties
   - `get_frame_section`: fetch assigned section
   - `get_frame_section_nonprismatic`: fetch nonprismatic section data

Note:
    Frame load helpers live in the `loads` package.
"""

# ==================== Enums ====================
from .enums import (
    FrameType,
    FrameSectionType,
    FrameReleaseType,
    ItemType,
    SECTION_TYPE_NAMES,
    RELEASE_PRESETS,
)

# ==================== Data Classes ====================
from .data_classes import (
    FrameReleaseData,
    FrameModifierData,
    FrameLocalAxesData,
    FrameLocalAxesAdvancedData,
    FrameMassData,
    FrameSectionNonPrismaticData,
)

# ==================== Release Helpers ====================
from .release import (
    set_frame_release,
    set_frame_release_custom,
    get_frame_release,
    get_frame_release_type,
    is_frame_hinged,
)

# ==================== Local-Axis Helpers ====================
from .local_axes import (
    set_frame_local_axes,
    get_frame_local_axes,
    set_frame_local_axes_advanced,
    get_frame_local_axes_advanced,
    get_frame_transformation_matrix,
)

# ==================== Modifier Helpers ====================
from .modifier import (
    set_frame_modifiers,
    set_frame_modifiers_tuple,
    get_frame_modifiers,
    get_frame_modifiers_tuple,
    delete_frame_modifiers,
)

# ==================== Mass Helpers ====================
from .mass import (
    set_frame_mass,
    get_frame_mass,
    get_frame_mass_data,
    delete_frame_mass,
    has_frame_mass,
)

# ==================== Selection Helpers ====================
from .selection import (
    set_frame_selected,
    get_frame_selected,
    select_frame,
    deselect_frame,
    select_frames,
    deselect_frames,
    is_frame_selected,
)

# ==================== Group Helpers ====================
from .group import (
    set_frame_group,
    add_frame_to_group,
    remove_frame_from_group,
    get_frame_groups,
    is_frame_in_group,
    add_frames_to_group,
    remove_frames_from_group,
)

# ==================== Property Helpers ====================
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

# ==================== Hinge Data ====================
from .hinge import (
    FrameHinge,
    FrameHingeType,
    HINGE_RELEASES,
)


# ==================== API Category Index ====================

FRAME_API_CATEGORIES = {
    "releases": {
        "description": "Configure end releases for frame elements",
        "functions": [
            "set_frame_release",
            "set_frame_release_custom",
            "get_frame_release",
            "get_frame_release_type",
            "is_frame_hinged",
        ]
    },
    "local_axes": {
        "description": "Configure local-axis orientation for frame elements",
        "functions": [
            "set_frame_local_axes",
            "get_frame_local_axes",
            "set_frame_local_axes_advanced",
            "get_frame_local_axes_advanced",
            "get_frame_transformation_matrix",
        ]
    },
    "modifiers": {
        "description": "Configure frame section modifiers such as stiffness reductions",
        "functions": [
            "set_frame_modifiers",
            "set_frame_modifiers_tuple",
            "get_frame_modifiers",
            "get_frame_modifiers_tuple",
            "delete_frame_modifiers",
        ]
    },
    "mass": {
        "description": "Configure additional frame mass",
        "functions": [
            "set_frame_mass",
            "get_frame_mass",
            "get_frame_mass_data",
            "delete_frame_mass",
            "has_frame_mass",
        ]
    },
    "selection": {
        "description": "Configure frame selection state",
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
    "groups": {
        "description": "Configure frame group assignments",
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
    "properties": {
        "description": "Configure frame section and material-related assignments",
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


# ==================== Exports ====================

__all__ = [
    # Enums
    'FrameType',
    'FrameSectionType',
    'FrameReleaseType',
    'ItemType',
    'SECTION_TYPE_NAMES',
    'RELEASE_PRESETS',
    
    # Data classes
    'FrameReleaseData',
    'FrameModifierData',
    'FrameLocalAxesData',
    'FrameLocalAxesAdvancedData',
    'FrameMassData',
    'FrameSectionNonPrismaticData',
    'FrameHinge',
    'FrameHingeType',
    'HINGE_RELEASES',
    
    # Release helpers
    'set_frame_release',
    'set_frame_release_custom',
    'get_frame_release',
    'get_frame_release_type',
    'is_frame_hinged',
    
    # Local-axis helpers
    'set_frame_local_axes',
    'get_frame_local_axes',
    'set_frame_local_axes_advanced',
    'get_frame_local_axes_advanced',
    'get_frame_transformation_matrix',
    
    # Modifier helpers
    'set_frame_modifiers',
    'set_frame_modifiers_tuple',
    'get_frame_modifiers',
    'get_frame_modifiers_tuple',
    'delete_frame_modifiers',
    
    # Mass helpers
    'set_frame_mass',
    'get_frame_mass',
    'get_frame_mass_data',
    'delete_frame_mass',
    'has_frame_mass',
    
    # Selection helpers
    'set_frame_selected',
    'get_frame_selected',
    'select_frame',
    'deselect_frame',
    'select_frames',
    'deselect_frames',
    'is_frame_selected',
    
    # Group helpers
    'set_frame_group',
    'add_frame_to_group',
    'remove_frame_from_group',
    'get_frame_groups',
    'is_frame_in_group',
    'add_frames_to_group',
    'remove_frames_from_group',
    
    # Property helpers
    'set_frame_section',
    'get_frame_section',
    'get_frame_section_info',
    'get_frame_section_nonprismatic',
    'set_frame_material_overwrite',
    'get_frame_material_overwrite',
    'set_frame_material_temperature',
    'get_frame_material_temperature',
    
    # API category index
    'FRAME_API_CATEGORIES',
]
