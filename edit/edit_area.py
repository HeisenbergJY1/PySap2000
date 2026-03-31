# -*- coding: utf-8 -*-
"""
edit_area.py - Area editing

Wrappers for the SAP2000 `EditArea` API.

SAP2000 API:
- `EditArea.Divide` - Divide area objects
- `EditArea.ExpandShrink` - Expand / shrink
- `EditArea.Merge` - Merge
- `EditArea.PointAdd` - Add point
- `EditArea.PointRemove` - Remove point
- `EditArea.ChangeConnectivity` - Change connectivity
"""

from typing import List
from PySap2000.com_helper import com_ret, com_data


def divide_area(
    model,
    name: str,
    mesh_type: int,
    num_1: int = 2,
    num_2: int = 2,
    max_size_1: float = 0.0,
    max_size_2: float = 0.0,
    constrain_points: bool = True,
    delete_original: bool = True
) -> List[str]:
    """
    Divide area objects
    
    Args:
        model: SAP2000 SapModel object
        name: Area object name
        mesh_type: Mesh type
            `0` = Divide by count
            `1` = Divide by max size
            `2` = Divide by points
        num_1: Number of divisions along local-1
        num_2: Number of divisions along local-2
        max_size_1: Maximum size along local-1
        max_size_2: Maximum size along local-2
        constrain_points: Whether to constrain to existing points
        delete_original: Whether to delete original objects
        
    Returns:
        List of newly created area object names
    """
    result = model.EditArea.Divide(
        name, mesh_type, num_1, num_2, max_size_1, max_size_2,
        constrain_points, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def expand_shrink_area(model, name: str, offset: float) -> int:
    """
    Expand or shrink area objects
    
    Args:
        model: SAP2000 SapModel object
        name: Area object name
        offset: Offset value (positive expands, negative shrinks)
        
    Returns:
        `0` on success
    """
    return model.EditArea.ExpandShrink(name, offset)


def merge_area(model, names: List[str], delete_original: bool = True) -> str:
    """
    Merge area objects
    
    Args:
        model: SAP2000 SapModel object
        names: Area object names to merge
        delete_original: Whether to delete original objects
        
    Returns:
        Newly created area object name
    """
    # COM signature: `Merge(NumberAreas, Names)` accepts only count and names.
    # `delete_original` and `NewAreaName` are output params handled by comtypes.
    result = model.EditArea.Merge(len(names), names)
    # Find the new area object name from return values (string elements).
    if isinstance(result, str) and result:
        return result
    # For `comtypes` list/tuple returns, scan for the new string name.
    i = 0
    while True:
        item = com_data(result, i, None)
        if item is None:
            break
        if isinstance(item, str) and item:
            return item
        i += 1
    return ""


def add_point_to_area(model, name: str, point_name: str) -> int:
    """
    Add a point to an area object
    
    Args:
        model: SAP2000 SapModel object
        name: Area object name
        point_name: Point name to add
        
    Returns:
        `0` on success
    """
    return model.EditArea.PointAdd(name, point_name)


def remove_point_from_area(model, name: str, point_name: str) -> int:
    """
    Remove a point from an area object
    
    Args:
        model: SAP2000 SapModel object
        name: Area object name
        point_name: Point name to remove
        
    Returns:
        `0` on success
    """
    return model.EditArea.PointRemove(name, point_name)


def change_area_connectivity(
    model,
    name: str,
    point_names: List[str]
) -> int:
    """
    Change area object connectivity
    
    Args:
        model: SAP2000 SapModel object
        name: Area object name
        point_names: New point-name list
        
    Returns:
        `0` on success
    """
    return model.EditArea.ChangeConnectivity(name, len(point_names), point_names)
