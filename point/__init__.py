# -*- coding: utf-8 -*-
"""
point - Point-related types and helper functions.

This package provides a modular API organized by feature:

1. Supports (`support`)
   - `set_point_support`: assign a support preset
   - `set_point_restraint`: assign custom restraints
   - `get_point_restraint`: fetch restraint state
   - `delete_point_restraint`: remove restraints

2. Springs (`spring`)
   - `set_point_spring`: assign spring stiffness
   - `get_point_spring`: fetch spring stiffness
   - `delete_point_spring`: remove spring assignments

3. Mass (`mass`)
   - `set_point_mass`: assign mass
   - `get_point_mass`: fetch mass
   - `delete_point_mass`: remove mass

4. Constraints (`constraint`)
   - `set_point_constraint`: assign a rigid constraint such as a diaphragm
   - `get_point_constraint`: fetch constraint assignments
   - `delete_point_constraint`: remove constraint assignments

5. Local axes (`local_axes`)
   - `set_point_local_axes`: set local-axis rotation
   - `get_point_local_axes`: fetch local-axis rotation

6. Panel zone (`panel_zone`)
   - `set_point_panel_zone`: assign panel-zone data
   - `get_point_panel_zone`: fetch panel-zone data
   - `delete_point_panel_zone`: remove panel-zone data

Note:
    Point load helpers live in the `loads` package.
"""

# Enums
from .enums import (
    PointSupportType,
    ItemType,
    PanelZonePropType,
    PanelZoneConnectivity,
    PanelZoneLocalAxisFrom,
    SUPPORT_RESTRAINTS,
)

# Data classes
from .data_classes import (
    PointConstraintAssignment,
    PointSpringData,
    PointMassData,
    PanelZoneData,
)

# Support helpers
from .support import (
    set_point_support,
    set_point_restraint,
    get_point_restraint,
    get_point_support_type,
    delete_point_restraint,
    get_points_with_support,
)

# Spring helpers
from .spring import (
    set_point_spring,
    get_point_spring,
    delete_point_spring,
    set_point_spring_coupled,
    get_point_spring_coupled,
    is_point_spring_coupled,
)

# Mass helpers
from .mass import (
    set_point_mass,
    get_point_mass,
    delete_point_mass,
    set_point_mass_by_weight,
    set_point_mass_by_volume,
)

# Constraint helpers
from .constraint import (
    set_point_constraint,
    get_point_constraint,
    delete_point_constraint,
    get_points_in_constraint,
)

# Local-axis helpers
from .local_axes import (
    set_point_local_axes,
    get_point_local_axes,
    set_point_local_axes_advanced,
    get_point_local_axes_advanced,
    get_point_transformation_matrix,
)

# Panel-zone helpers
from .panel_zone import (
    set_point_panel_zone,
    get_point_panel_zone,
    delete_point_panel_zone,
    has_point_panel_zone,
)


# API category index
POINT_API_CATEGORIES = {
    "supports_and_boundary_conditions": {
        "description": "Assign support presets and restraint conditions to points",
        "functions": [
            "set_point_support",
            "set_point_restraint",
            "get_point_restraint",
            "get_point_support_type",
            "delete_point_restraint",
            "get_points_with_support",
        ]
    },
    "springs": {
        "description": "Assign spring stiffness to points",
        "functions": [
            "set_point_spring",
            "get_point_spring",
            "delete_point_spring",
            "set_point_spring_coupled",
            "get_point_spring_coupled",
            "is_point_spring_coupled",
        ]
    },
    "mass": {
        "description": "Assign additional point mass",
        "functions": [
            "set_point_mass",
            "get_point_mass",
            "delete_point_mass",
            "set_point_mass_by_weight",
            "set_point_mass_by_volume",
        ]
    },
    "constraints": {
        "description": "Assign rigid constraints such as diaphragms",
        "functions": [
            "set_point_constraint",
            "get_point_constraint",
            "delete_point_constraint",
            "get_points_in_constraint",
        ]
    },
    "local_axes": {
        "description": "Configure point local axes",
        "functions": [
            "set_point_local_axes",
            "get_point_local_axes",
            "set_point_local_axes_advanced",
            "get_point_local_axes_advanced",
            "get_point_transformation_matrix",
        ]
    },
    "panel_zone": {
        "description": "Configure beam-column joint panel-zone data",
        "functions": [
            "set_point_panel_zone",
            "get_point_panel_zone",
            "delete_point_panel_zone",
            "has_point_panel_zone",
        ]
    },
}


__all__ = [
    # Enums
    'PointSupportType',
    'ItemType',
    'PanelZonePropType',
    'PanelZoneConnectivity',
    'PanelZoneLocalAxisFrom',
    'SUPPORT_RESTRAINTS',
    
    # Data classes
    'PointConstraintAssignment',
    'PointSpringData',
    'PointMassData',
    'PanelZoneData',
    
    # Support helpers
    'set_point_support',
    'set_point_restraint',
    'get_point_restraint',
    'get_point_support_type',
    'delete_point_restraint',
    'get_points_with_support',
    
    # Spring helpers
    'set_point_spring',
    'get_point_spring',
    'delete_point_spring',
    'set_point_spring_coupled',
    'get_point_spring_coupled',
    'is_point_spring_coupled',
    
    # Mass helpers
    'set_point_mass',
    'get_point_mass',
    'delete_point_mass',
    'set_point_mass_by_weight',
    'set_point_mass_by_volume',
    
    # Constraint helpers
    'set_point_constraint',
    'get_point_constraint',
    'delete_point_constraint',
    'get_points_in_constraint',
    
    # Local-axis helpers
    'set_point_local_axes',
    'get_point_local_axes',
    'set_point_local_axes_advanced',
    'get_point_local_axes_advanced',
    'get_point_transformation_matrix',
    
    # Panel-zone helpers
    'set_point_panel_zone',
    'get_point_panel_zone',
    'delete_point_panel_zone',
    'has_point_panel_zone',
    
    # API category index
    'POINT_API_CATEGORIES',
]
