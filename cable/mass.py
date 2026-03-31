# -*- coding: utf-8 -*-
"""
mass.py - Cable mass-assignment helpers.

SAP2000 API:
- CableObj.SetMass(Name, MassOverL, Replace, ItemType)
- CableObj.GetMass(Name, MassOverL)
- CableObj.DeleteMass(Name, ItemType)
"""

from typing import Optional
from .modifier import CableItemType
from PySap2000.com_helper import com_data


def set_cable_mass(
    model,
    cable_name: str,
    mass_per_length: float,
    replace: bool = False,
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    Set additional mass for a cable object.
    
    Args:
        model: SAP2000 SapModel object
        cable_name: Cable object name
        mass_per_length: Mass per unit length [M/L]
        replace: `True` to replace existing mass, `False` to add to it
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        set_cable_mass(model, "1", 0.001)
    """
    return model.CableObj.SetMass(str(cable_name), mass_per_length, replace, int(item_type))


def get_cable_mass(model, cable_name: str) -> Optional[float]:
    """
    Get the additional mass assigned to a cable object.
    
    Args:
        model: SAP2000 SapModel object
        cable_name: Cable object name
    
    Returns:
        Mass per unit length [M/L], or `None` if the query fails.
    
    Example:
        mass = get_cable_mass(model, "1")
    """
    try:
        result = model.CableObj.GetMass(str(cable_name), 0.0)
        return com_data(result, 0)
    except Exception:
        pass
    return None


def delete_cable_mass(
    model,
    cable_name: str,
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    Delete the additional mass assigned to a cable object.
    
    Args:
        model: SAP2000 SapModel object
        cable_name: Cable object name
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    """
    return model.CableObj.DeleteMass(str(cable_name), int(item_type))
