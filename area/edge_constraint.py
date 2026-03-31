# -*- coding: utf-8 -*-
"""
edge_constraint.py - Area edge-constraint helpers.

Wraps SAP2000 `AreaObj` edge-constraint APIs.
"""

from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


def set_area_edge_constraint(
    model,
    area_name: str,
    constraint_exists: bool,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set the edge-constraint state of an area object.

    Edge constraints help enforce displacement compatibility between adjacent areas.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        constraint_exists: Whether edge constraints should exist
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        # Enable edge constraints
        set_area_edge_constraint(model, "1", True)
        
        # Disable edge constraints
        set_area_edge_constraint(model, "1", False)
    """
    return model.AreaObj.SetEdgeConstraint(str(area_name), constraint_exists, int(item_type))


def get_area_edge_constraint(
    model,
    area_name: str
) -> bool:
    """
    Get the edge-constraint state of an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `True` if edge constraints exist, otherwise `False`.
        
    Example:
        has_constraint = get_area_edge_constraint(model, "1")
        print(f"Edge constraint: {'enabled' if has_constraint else 'disabled'}")
    """
    try:
        result = model.AreaObj.GetEdgeConstraint(str(area_name), False)
        val = com_data(result, 0)
        if val is not None:
            return val
    except Exception:
        pass
    return False


def enable_area_edge_constraint(
    model,
    area_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Enable edge constraints for an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
    """
    return set_area_edge_constraint(model, area_name, True, item_type)


def disable_area_edge_constraint(
    model,
    area_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Disable edge constraints for an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
    """
    return set_area_edge_constraint(model, area_name, False, item_type)


def has_area_edge_constraint(
    model,
    area_name: str
) -> bool:
    """
    Check whether an area object has edge constraints.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `True` if edge constraints are present, otherwise `False`.
    """
    return get_area_edge_constraint(model, area_name)
