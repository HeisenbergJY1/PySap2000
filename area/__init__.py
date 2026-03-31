# -*- coding: utf-8 -*-
"""
area - Area object types and standalone helper functions.

Provides wrappers around SAP2000 `AreaObj` settings, excluding load assignment.

For load-related APIs, use `loads/area_load.py`.

Usage:
    from area import AREA_API_CATEGORIES
    print(AREA_API_CATEGORIES["spring"]["functions"])
"""

# ==================== Enums ====================
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

# ==================== Data Classes ====================
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

# ==================== Spring Functions ====================
from .spring import (
    set_area_spring,
    get_area_spring,
    delete_area_spring,
    has_area_spring,
)

# ==================== Local-Axis Functions ====================
from .local_axes import (
    set_area_local_axes,
    get_area_local_axes,
    set_area_local_axes_advanced,
    get_area_local_axes_advanced,
    get_area_transformation_matrix,
)

# ==================== Modifier Functions ====================
from .modifier import (
    set_area_modifiers,
    set_area_modifiers_tuple,
    get_area_modifiers,
    get_area_modifiers_tuple,
    delete_area_modifiers,
)

# ==================== Mass Functions ====================
from .mass import (
    set_area_mass,
    get_area_mass,
    get_area_mass_data,
    delete_area_mass,
    has_area_mass,
)

# ==================== Thickness Functions ====================
from .thickness import (
    set_area_thickness,
    get_area_thickness,
    has_area_thickness,
)

# ==================== Offset Functions ====================
from .offset import (
    set_area_offset,
    get_area_offset,
    has_area_offset,
)

# ==================== Auto-Mesh Functions ====================
from .auto_mesh import (
    set_area_auto_mesh,
    get_area_auto_mesh,
    is_area_meshed,
)

# ==================== Edge-Constraint Functions ====================
from .edge_constraint import (
    set_area_edge_constraint,
    get_area_edge_constraint,
    enable_area_edge_constraint,
    disable_area_edge_constraint,
    has_area_edge_constraint,
)

# ==================== Selection Functions ====================
from .selection import (
    set_area_selected,
    get_area_selected,
    select_area,
    deselect_area,
    select_areas,
    deselect_areas,
    is_area_selected,
)

# ==================== Group-Assignment Functions ====================
from .group import (
    set_area_group,
    add_area_to_group,
    remove_area_from_group,
    get_area_groups,
    is_area_in_group,
    add_areas_to_group,
    remove_areas_from_group,
)

# ==================== Property-Assignment Functions ====================
from .property import (
    set_area_property,
    get_area_property,
    get_area_property_type,
    set_area_material_overwrite,
    get_area_material_overwrite,
    set_area_material_temperature,
    get_area_material_temperature,
)


# ==================== API Category Index ====================

AREA_API_CATEGORIES = {
    "spring": {
        "description": "Assign spring supports to area objects",
        "functions": [
            "set_area_spring",
            "get_area_spring",
            "delete_area_spring",
            "has_area_spring",
        ]
    },
    "local_axes": {
        "description": "Assign local-axis orientation to area objects",
        "functions": [
            "set_area_local_axes",
            "get_area_local_axes",
            "set_area_local_axes_advanced",
            "get_area_local_axes_advanced",
            "get_area_transformation_matrix",
        ]
    },
    "modifiers": {
        "description": "Assign area property modifiers such as stiffness reduction factors",
        "functions": [
            "set_area_modifiers",
            "set_area_modifiers_tuple",
            "get_area_modifiers",
            "get_area_modifiers_tuple",
            "delete_area_modifiers",
        ]
    },
    "mass": {
        "description": "Assign additional mass to area objects",
        "functions": [
            "set_area_mass",
            "get_area_mass",
            "get_area_mass_data",
            "delete_area_mass",
            "has_area_mass",
        ]
    },
    "thickness": {
        "description": "Assign thickness overrides to area objects",
        "functions": [
            "set_area_thickness",
            "get_area_thickness",
            "has_area_thickness",
        ]
    },
    "offset": {
        "description": "Assign offsets to area objects",
        "functions": [
            "set_area_offset",
            "get_area_offset",
            "has_area_offset",
        ]
    },
    "auto_mesh": {
        "description": "Configure automatic meshing for area objects",
        "functions": [
            "set_area_auto_mesh",
            "get_area_auto_mesh",
            "is_area_meshed",
        ]
    },
    "edge_constraint": {
        "description": "Configure edge constraints for area objects",
        "functions": [
            "set_area_edge_constraint",
            "get_area_edge_constraint",
            "enable_area_edge_constraint",
            "disable_area_edge_constraint",
            "has_area_edge_constraint",
        ]
    },
    "selection": {
        "description": "Set the selection state of area objects",
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
    "group_assignment": {
        "description": "Assign area objects to groups",
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
    "property_assignment": {
        "description": "Assign section properties and materials to area objects",
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


# ==================== Exports ====================

__all__ = [
    # Enums
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
    
    # Data classes
    'AreaSpringData',
    'AreaAutoMeshData',
    'AreaLocalAxesData',
    'AreaLocalAxesAdvancedData',
    'AreaThicknessData',
    'AreaOffsetData',
    'AreaModifierData',
    'AreaMassData',
    
    # Spring functions
    'set_area_spring',
    'get_area_spring',
    'delete_area_spring',
    'has_area_spring',
    
    # Local-axis functions
    'set_area_local_axes',
    'get_area_local_axes',
    'set_area_local_axes_advanced',
    'get_area_local_axes_advanced',
    'get_area_transformation_matrix',
    
    # Modifier functions
    'set_area_modifiers',
    'set_area_modifiers_tuple',
    'get_area_modifiers',
    'get_area_modifiers_tuple',
    'delete_area_modifiers',
    
    # Mass functions
    'set_area_mass',
    'get_area_mass',
    'get_area_mass_data',
    'delete_area_mass',
    'has_area_mass',
    
    # Thickness functions
    'set_area_thickness',
    'get_area_thickness',
    'has_area_thickness',
    
    # Offset functions
    'set_area_offset',
    'get_area_offset',
    'has_area_offset',
    
    # Auto-mesh functions
    'set_area_auto_mesh',
    'get_area_auto_mesh',
    'is_area_meshed',
    
    # Edge-constraint functions
    'set_area_edge_constraint',
    'get_area_edge_constraint',
    'enable_area_edge_constraint',
    'disable_area_edge_constraint',
    'has_area_edge_constraint',
    
    # Selection functions
    'set_area_selected',
    'get_area_selected',
    'select_area',
    'deselect_area',
    'select_areas',
    'deselect_areas',
    'is_area_selected',
    
    # Group-assignment functions
    'set_area_group',
    'add_area_to_group',
    'remove_area_from_group',
    'get_area_groups',
    'is_area_in_group',
    'add_areas_to_group',
    'remove_areas_from_group',
    
    # Property-assignment functions
    'set_area_property',
    'get_area_property',
    'get_area_property_type',
    'set_area_material_overwrite',
    'get_area_material_overwrite',
    'set_area_material_temperature',
    'get_area_material_temperature',
    
    # API category index
    'AREA_API_CATEGORIES',
]
