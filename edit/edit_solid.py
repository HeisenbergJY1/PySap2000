# -*- coding: utf-8 -*-
"""
edit_solid.py - Solid editing

Wrappers for the SAP2000 `EditSolid` API.

SAP2000 API:
- `EditSolid.Divide` - Divide solids
"""

from typing import List
from PySap2000.com_helper import com_ret, com_data


def divide_solid(
    model,
    name: str,
    num_1: int = 2,
    num_2: int = 2,
    num_3: int = 2
) -> List[str]:
    """
    Divide solid objects
    
    Args:
        model: SAP2000 SapModel object
        name: Solid object name
        num_1: Number of divisions along local-1
        num_2: Number of divisions along local-2
        num_3: Number of divisions along local-3
        
    Returns:
        List of newly created solid names
    """
    result = model.EditSolid.Divide(name, num_1, num_2, num_3, 0, [])
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []
