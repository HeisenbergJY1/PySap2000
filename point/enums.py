# -*- coding: utf-8 -*-
"""
enums.py - Point-related enums.
"""

from enum import IntEnum


class PointSupportType(IntEnum):
    """
    Point support presets.

    Used by `set_point_support()` for common restraint patterns.
    """
    FIXED = 0           # Fully restrained
    HINGED = 1          # Translations restrained, rotations released
    ROLLER = 2          # Only U3 restrained
    ROLLER_IN_X = 3     # Rolling in X, so U2 and U3 restrained
    ROLLER_IN_Y = 4     # Rolling in Y, so U1 and U3 restrained
    ROLLER_IN_Z = 5     # Rolling in Z, so U1 and U2 restrained
    FREE = 6            # Unrestrained


class ItemType(IntEnum):
    """
    Item-scope enum.

    Used to specify the target scope for SAP2000 API calls.
    """
    OBJECT = 0              # Single object
    GROUP = 1               # All objects in a group
    SELECTED_OBJECTS = 2    # Currently selected objects


class PanelZonePropType(IntEnum):
    """Panel-zone property type."""
    ELASTIC_FROM_COLUMN = 0         # Derive elastic stiffness from the column
    ELASTIC_FROM_COLUMN_DOUBLER = 1 # Derive from column plus doubler plate
    FROM_SPRING_STIFFNESS = 2       # Use explicitly specified spring stiffness
    FROM_LINK_PROPERTY = 3          # Use a link property


class PanelZoneConnectivity(IntEnum):
    """Panel-zone connectivity type."""
    BEAMS_TO_OTHER = 0      # Beams connect to other members
    BRACES_TO_OTHER = 1     # Braces connect to other members


class PanelZoneLocalAxisFrom(IntEnum):
    """Source of panel-zone local axes."""
    FROM_COLUMN = 0         # Use the column
    USER_DEFINED = 1        # User-defined


# Restraint tuples for each support preset: (U1, U2, U3, R1, R2, R3)
SUPPORT_RESTRAINTS = {
    PointSupportType.FIXED: (True, True, True, True, True, True),
    PointSupportType.HINGED: (True, True, True, False, False, False),
    PointSupportType.ROLLER: (False, False, True, False, False, False),
    PointSupportType.ROLLER_IN_X: (False, True, True, False, False, False),
    PointSupportType.ROLLER_IN_Y: (True, False, True, False, False, False),
    PointSupportType.ROLLER_IN_Z: (True, True, False, False, False, False),
    PointSupportType.FREE: (False, False, False, False, False, False),
}
