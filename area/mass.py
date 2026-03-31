# -*- coding: utf-8 -*-
"""
mass.py - Area mass helpers.

Wraps SAP2000 `AreaObj` mass APIs.
"""

from typing import Optional

from .enums import ItemType
from .data_classes import AreaMassData
from PySap2000.com_helper import com_ret, com_data


def set_area_mass(
    model,
    area_name: str,
    mass_per_area: float,
    replace: bool = True,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set additional mass for an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        mass_per_area: Mass per unit area
        replace: Whether to replace existing mass (`True`) or add to it (`False`)
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        # Set the additional mass of area "1" to 100 kg/m^2
        set_area_mass(model, "1", 100.0)
    """
    return model.AreaObj.SetMass(str(area_name), mass_per_area, replace, int(item_type))


def get_area_mass(
    model,
    area_name: str
) -> Optional[float]:
    """
    Get the additional mass assigned to an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        Mass per unit area, or `None` if the query fails.
        
    Example:
        mass = get_area_mass(model, "1")
        if mass is not None:
            print(f"Additional mass: {mass} kg/m^2")
    """
    try:
        result = model.AreaObj.GetMass(str(area_name), 0.0)
        mass = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0:
            return mass
    except Exception:
        pass
    return None


def get_area_mass_data(
    model,
    area_name: str
) -> Optional[AreaMassData]:
    """
    Get area mass as a structured data object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `AreaMassData`, or `None` if the query fails.
    """
    mass = get_area_mass(model, area_name)
    if mass is not None:
        return AreaMassData(area_name=area_name, mass_per_area=mass)
    return None


def delete_area_mass(
    model,
    area_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Delete additional mass assigned to an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
    """
    return model.AreaObj.DeleteMass(str(area_name), int(item_type))


def has_area_mass(
    model,
    area_name: str
) -> bool:
    """
    Check whether an area object has additional mass assigned.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `True` if additional mass is assigned, otherwise `False`.
    """
    mass = get_area_mass(model, area_name)
    return mass is not None and mass > 0.0
