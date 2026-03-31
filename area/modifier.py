# -*- coding: utf-8 -*-
"""
modifier.py - Area modifier helpers.

Wraps SAP2000 `AreaObj` modifier APIs.
"""

from typing import Optional, List, Tuple

from .enums import ItemType
from .data_classes import AreaModifierData
from PySap2000.com_helper import com_ret, com_data


def set_area_modifiers(
    model,
    area_name: str,
    modifiers: List[float],
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set modifier values for an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        modifiers: 10 modifier values
            [f11, f22, f12, m11, m22, m12, v13, v23, mass, weight]
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        # Set modifiers for area "1" with bending stiffness reduced to 0.7
        modifiers = [1.0, 1.0, 1.0, 0.7, 0.7, 0.7, 1.0, 1.0, 1.0, 1.0]
        set_area_modifiers(model, "1", modifiers)
    """
    # Ensure the API always receives 10 modifier values.
    mod_list = list(modifiers)
    while len(mod_list) < 10:
        mod_list.append(1.0)
    
    result = model.AreaObj.SetModifiers(str(area_name), mod_list[:10], int(item_type))
    return com_ret(result)


def set_area_modifiers_tuple(
    model,
    area_name: str,
    modifiers: Tuple[float, ...],
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set area modifiers from a tuple.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        modifiers: Tuple of 10 modifier values
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
    """
    return set_area_modifiers(model, area_name, list(modifiers), item_type)


def set_area_modifiers_data(
    model,
    area_name: str,
    data: AreaModifierData,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set area modifiers from a data object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        data: `AreaModifierData` instance
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        data = AreaModifierData(m11=0.7, m22=0.7, m12=0.7)
        set_area_modifiers_data(model, "1", data)
    """
    return model.AreaObj.SetModifiers(str(area_name), data.to_list(), int(item_type))


def get_area_modifiers(
    model,
    area_name: str
) -> Optional[AreaModifierData]:
    """
    Get area modifiers as a structured data object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `AreaModifierData`, or `None` if the query fails.
        
    Example:
        data = get_area_modifiers(model, "1")
        if data:
            print(f"Bending stiffness m11: {data.m11}")
    """
    modifiers = get_area_modifiers_tuple(model, area_name)
    if modifiers:
        return AreaModifierData.from_list(list(modifiers))
    return None


def get_area_modifiers_tuple(
    model,
    area_name: str
) -> Optional[Tuple[float, ...]]:
    """
    Get area modifiers as a tuple.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        Tuple of 10 modifier values, or `None` if the query fails.
        
    Example:
        modifiers = get_area_modifiers_tuple(model, "1")
        if modifiers:
            print(f"Membrane stiffness f11: {modifiers[0]}")
            print(f"Bending stiffness m11: {modifiers[3]}")
    """
    try:
        result = model.AreaObj.GetModifiers(str(area_name), [])
        modifiers = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and modifiers:
            return tuple(modifiers)
    except Exception:
        pass
    return None


def delete_area_modifiers(
    model,
    area_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Delete area modifiers and restore default values.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
    """
    return model.AreaObj.DeleteModifiers(str(area_name), int(item_type))
