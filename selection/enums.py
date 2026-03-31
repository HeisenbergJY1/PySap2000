# -*- coding: utf-8 -*-
"""
enums.py - Selection-related enums.

Defines selection enums used by the SAP2000 API.
"""

from enum import IntEnum


class SelectObjectType(IntEnum):
    """
    Selected object type.

    Used for the `ObjectType` values returned by `GetSelected`.

    SAP2000 API:
        1 = Point object
        2 = Frame object
        3 = Cable object
        4 = Tendon object
        5 = Area object
        6 = Solid object
        7 = Link object
    """
    POINT = 1
    FRAME = 2
    CABLE = 3
    TENDON = 4
    AREA = 5
    SOLID = 6
    LINK = 7
