# -*- coding: utf-8 -*-
"""
enums.py - Cable-related enums.

Contains enums used by the SAP2000 `CableObj` API.
"""

from enum import IntEnum


class CableType(IntEnum):
    """
    Cable definition type for tension/sag input.

    Matches the `CableType` argument of `CableObj.SetCableData`.
    """
    MINIMUM_TENSION_AT_I_END = 1    # Minimum tension at the I-end
    MINIMUM_TENSION_AT_J_END = 2    # Minimum tension at the J-end
    TENSION_AT_I_END = 3            # Tension at the I-end [F]
    TENSION_AT_J_END = 4            # Tension at the J-end [F]
    HORIZONTAL_TENSION = 5          # Horizontal tension component [F]
    MAXIMUM_VERTICAL_SAG = 6        # Maximum vertical sag [L]
    LOW_POINT_VERTICAL_SAG = 7      # Vertical sag at the lowest point [L]
    UNDEFORMED_LENGTH = 8           # Undeformed length [L]
    RELATIVE_UNDEFORMED_LENGTH = 9  # Relative undeformed length


class CableDefinitionType(IntEnum):
    """
    Cable geometry definition type.

    Describes how the cable object is defined in the SAP2000 API.
    """
    BY_POINTS = 1       # Defined by points
    BY_COORDINATES = 2  # Defined by coordinates
