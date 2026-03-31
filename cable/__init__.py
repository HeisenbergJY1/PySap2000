# -*- coding: utf-8 -*-
"""
cable - Extended helpers for cable objects.

Includes:
- `enums`: cable enums
- `property`: section assignment, material overwrite, material temperature
- `modifier`: cable modifiers
- `mass`: additional mass
- `output_station`: output-station settings
- `group`: group assignment
- `selection`: selection state

Load-related helpers live in `loads/cable_load.py`.
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


# ==================== API Category Index ====================

CABLE_API_CATEGORIES = {
    "section_properties": {
        "description": "Configure section-property assignments for cables",
        "functions": [
            "set_cable_section",
            "get_cable_section",
            "get_cable_section_list",
        ]
    },
    "material": {
        "description": "Configure cable material overwrites and temperatures",
        "functions": [
            "set_cable_material_overwrite",
            "get_cable_material_overwrite",
            "set_cable_material_temp",
            "get_cable_material_temp",
        ]
    },
    "modifiers": {
        "description": "Configure cable modifiers",
        "functions": [
            "set_cable_modifiers",
            "get_cable_modifiers",
            "delete_cable_modifiers",
        ]
    },
    "mass": {
        "description": "Configure additional cable mass",
        "functions": [
            "set_cable_mass",
            "get_cable_mass",
            "delete_cable_mass",
        ]
    },
    "output_stations": {
        "description": "Configure cable output stations",
        "functions": [
            "set_cable_output_stations",
            "get_cable_output_stations",
        ]
    },
    "groups": {
        "description": "Configure cable group assignments",
        "functions": [
            "set_cable_group",
            "get_cable_groups",
        ]
    },
    "selection": {
        "description": "Configure cable selection state",
        "functions": [
            "set_cable_selected",
            "get_cable_selected",
            "get_selected_cables",
        ]
    },
}


__all__ = [
    # Enums
    'CableType',
    'CableDefinitionType',
    'CableItemType',
    'CableOutputStationType',
    # Data classes
    'CableModifiers',
    'CableOutputStations',
    # Section / material properties
    'set_cable_section',
    'get_cable_section',
    'get_cable_section_list',
    'set_cable_material_overwrite',
    'get_cable_material_overwrite',
    'set_cable_material_temp',
    'get_cable_material_temp',
    # Modifiers
    'set_cable_modifiers',
    'get_cable_modifiers',
    'delete_cable_modifiers',
    # Mass
    'set_cable_mass',
    'get_cable_mass',
    'delete_cable_mass',
    # Output stations
    'set_cable_output_stations',
    'get_cable_output_stations',
    # Groups
    'set_cable_group',
    'get_cable_groups',
    # Selection
    'set_cable_selected',
    'get_cable_selected',
    'get_selected_cables',
    # API category index
    'CABLE_API_CATEGORIES',
]
