# -*- coding: utf-8 -*-
"""
enums.py - Constraint-related enums.
"""

from enum import IntEnum


class ConstraintType(IntEnum):
    """
    Constraint type enum (`eConstraintType`).
    """
    BODY = 1        # Body constraint
    DIAPHRAGM = 2   # Diaphragm constraint
    PLATE = 3       # Plate constraint
    ROD = 4         # Rod constraint
    BEAM = 5        # Beam constraint
    EQUAL = 6       # Equal displacement constraint
    LOCAL = 7       # Local constraint
    WELD = 8        # Welded constraint
    LINE = 13       # Line constraint


class ConstraintAxis(IntEnum):
    """
    Constraint axis enum (`eConstraintAxis`).

    Used by constraint types such as `Diaphragm`, `Beam`, `Plate`, and `Rod`.
    """
    X = 1           # X axis
    Y = 2           # Y axis
    Z = 3           # Z axis
    AUTO = 4        # Automatically determined
