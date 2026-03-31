# -*- coding: utf-8 -*-
"""
link - Link-related types and helper functions.

This package wraps settings related to SAP2000 `LinkObj`.

Notes:
- Load helpers live in `loads/link_load.py`
- Link property definitions (`PropLink`) live in `section/link_section.py`

Example:
    from link import LINK_API_CATEGORIES
    print(LINK_API_CATEGORIES["local_axes"]["functions"])

    from link import set_link_local_axes
    set_link_local_axes(model, "1", 30)
"""

# ==================== Enums ====================
from .enums import (
    LinkType,
    LinkDirectionalType,
    LinkItemType,
    AxisVectorOption,
)

# ==================== Data Classes ====================
from .data_classes import (
    LinkLocalAxesData,
    LinkLocalAxesAdvancedData,
)

# ==================== Local-Axis Helpers ====================
from .local_axes import (
    set_link_local_axes,
    get_link_local_axes,
    set_link_local_axes_advanced,
    get_link_local_axes_advanced,
    get_link_transformation_matrix,
)

# ==================== Selection Helpers ====================
from .selection import (
    set_link_selected,
    get_link_selected,
    select_link,
    deselect_link,
    select_links,
    deselect_links,
    is_link_selected,
)


# ==================== Group Helpers ====================
from .group import (
    set_link_group,
    add_link_to_group,
    remove_link_from_group,
    get_link_groups,
    is_link_in_group,
    add_links_to_group,
    remove_links_from_group,
)

# ==================== Property Helpers ====================
from .property import (
    set_link_property,
    get_link_property,
    set_link_property_fd,
    get_link_property_fd,
    get_link_property_info,
)


# ==================== API Category Index ====================

LINK_API_CATEGORIES = {
    "local_axes": {
        "description": "Configure local-axis orientation for link elements",
        "functions": [
            "set_link_local_axes",            # Set local-axis rotation
            "get_link_local_axes",            # Get local-axis rotation
            "set_link_local_axes_advanced",   # Set advanced local-axis data
            "get_link_local_axes_advanced",   # Get advanced local-axis data
            "get_link_transformation_matrix", # Get the transformation matrix
        ]
    },
    "selection": {
        "description": "Configure link selection state",
        "functions": [
            "set_link_selected",   # Set selection state
            "get_link_selected",   # Get selection state
            "select_link",         # Select one link
            "deselect_link",       # Deselect one link
            "select_links",        # Select multiple links
            "deselect_links",      # Deselect multiple links
            "is_link_selected",    # Check whether a link is selected
        ]
    },
    "groups": {
        "description": "Configure link group assignments",
        "functions": [
            "set_link_group",           # Set group assignment
            "add_link_to_group",        # Add to a group
            "remove_link_from_group",   # Remove from a group
            "get_link_groups",          # Get assigned groups
            "is_link_in_group",         # Check whether it belongs to a group
            "add_links_to_group",       # Add multiple links to a group
            "remove_links_from_group",  # Remove multiple links from a group
        ]
    },
    "properties": {
        "description": "Configure link property assignments",
        "functions": [
            "set_link_property",      # Set link property
            "get_link_property",      # Get link property name
            "set_link_property_fd",   # Set frequency-dependent property
            "get_link_property_fd",   # Get frequency-dependent property
            "get_link_property_info", # Get property info including FD data
        ]
    },
}


# ==================== Exports ====================

__all__ = [
    # Enums
    'LinkType',
    'LinkDirectionalType',
    'LinkItemType',
    'AxisVectorOption',
    
    # Data classes
    'LinkLocalAxesData',
    'LinkLocalAxesAdvancedData',
    
    # Local-axis helpers
    'set_link_local_axes',
    'get_link_local_axes',
    'set_link_local_axes_advanced',
    'get_link_local_axes_advanced',
    'get_link_transformation_matrix',
    
    # Selection helpers
    'set_link_selected',
    'get_link_selected',
    'select_link',
    'deselect_link',
    'select_links',
    'deselect_links',
    'is_link_selected',
    
    # Group helpers
    'set_link_group',
    'add_link_to_group',
    'remove_link_from_group',
    'get_link_groups',
    'is_link_in_group',
    'add_links_to_group',
    'remove_links_from_group',
    
    # Property helpers
    'set_link_property',
    'get_link_property',
    'set_link_property_fd',
    'get_link_property_fd',
    'get_link_property_info',
    
    # API category index
    'LINK_API_CATEGORIES',
]
