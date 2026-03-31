# -*- coding: utf-8 -*-
"""
enums.py - Analysis result enums.

Enum definitions for the SAP2000 Analysis Results API.
"""

from enum import IntEnum


class ItemTypeElm(IntEnum):
    """
    Element scope for a result request.

    SAP2000 API: `eItemTypeElm`

    Used to define the scope of a result query:
    - `OBJECT_ELM`: request results for elements associated with the object
    - `ELEMENT`: request results for the specified element
    - `GROUP_ELM`: request results for all elements in a group
    - `SELECTION_ELM`: request results for all selected elements
    """
    OBJECT_ELM = 0      # Elements associated with the object
    ELEMENT = 1         # Specific element
    GROUP_ELM = 2       # Elements in a group
    SELECTION_ELM = 3   # Selected elements
