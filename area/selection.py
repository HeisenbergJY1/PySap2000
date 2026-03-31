# -*- coding: utf-8 -*-
"""
selection.py - Area selection helpers.

Wraps SAP2000 `AreaObj` selection APIs.
"""

from typing import List

from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


def set_area_selected(
    model,
    area_name: str,
    selected: bool = True,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set the selection state of an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        selected: Whether the area should be selected
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        # Select area "1"
        set_area_selected(model, "1", True)
        
        # Deselect area "1"
        set_area_selected(model, "1", False)
    """
    return model.AreaObj.SetSelected(str(area_name), selected, int(item_type))


def get_area_selected(
    model,
    area_name: str
) -> bool:
    """
    Get the selection state of an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `True` if selected, otherwise `False`.
        
    Example:
        is_selected = get_area_selected(model, "1")
        print(f"Area 1 is {'selected' if is_selected else 'not selected'}")
    """
    try:
        result = model.AreaObj.GetSelected(str(area_name), False)
        val = com_data(result, 0)
        if val is not None:
            return val
    except Exception:
        pass
    return False


def select_area(
    model,
    area_name: str
) -> int:
    """
    Select an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        select_area(model, "1")
    """
    return set_area_selected(model, area_name, True)


def deselect_area(
    model,
    area_name: str
) -> int:
    """
    Deselect an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        deselect_area(model, "1")
    """
    return set_area_selected(model, area_name, False)


def select_areas(
    model,
    area_names: List[str]
) -> int:
    """
    Select multiple area objects.
    
    Args:
        model: SAP2000 SapModel object
        area_names: List of area object names
        
    Returns:
        `0` if all operations succeed. Nonzero indicates at least one failure.
        
    Example:
        select_areas(model, ["1", "2", "3"])
    """
    ret = 0
    for name in area_names:
        result = set_area_selected(model, name, True)
        if result != 0:
            ret = result
    return ret


def deselect_areas(
    model,
    area_names: List[str]
) -> int:
    """
    Deselect multiple area objects.
    
    Args:
        model: SAP2000 SapModel object
        area_names: List of area object names
        
    Returns:
        `0` if all operations succeed. Nonzero indicates at least one failure.
        
    Example:
        deselect_areas(model, ["1", "2", "3"])
    """
    ret = 0
    for name in area_names:
        result = set_area_selected(model, name, False)
        if result != 0:
            ret = result
    return ret


def is_area_selected(
    model,
    area_name: str
) -> bool:
    """
    Check whether an area object is selected.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `True` if selected, otherwise `False`.
    """
    return get_area_selected(model, area_name)
