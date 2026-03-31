# -*- coding: utf-8 -*-
"""
enums.py - Link-related enums.

Contains enums used by the SAP2000 `LinkObj` API.
"""

from enum import IntEnum


class LinkType(IntEnum):
    """
    Link property type.

    Matches the types used by SAP2000 `PropLink`.
    """
    LINEAR = 1
    DAMPER = 2
    GAP = 3
    HOOK = 4
    PLASTIC_WEN = 5
    RUBBER_ISOLATOR = 6
    FRICTION_ISOLATOR = 7
    MULTI_LINEAR_ELASTIC = 8
    MULTI_LINEAR_PLASTIC = 9
    TENSION_COMPRESSION_FRICTION_ISOLATOR = 10


class LinkDirectionalType(IntEnum):
    """Link directional type."""
    TWO_JOINT = 1       # Two-joint link
    ONE_JOINT = 2       # One-joint grounded link


class LinkItemType(IntEnum):
    """
    `eItemType` enum.

    Used by methods such as `SetLocalAxes` and `SetPropertyFD`.
    """
    OBJECT = 0           # Single object
    GROUP = 1            # All objects in a group
    SELECTED_OBJECTS = 2 # All selected objects


class AxisVectorOption(IntEnum):
    """Axis or plane reference-vector option."""
    COORDINATE_DIRECTION = 1  # Coordinate direction
    TWO_JOINTS = 2            # Two joints
    USER_VECTOR = 3           # User-defined vector
