# -*- coding: utf-8 -*-
"""
mass.py - Frame mass helpers.

Provides functions to assign and query additional frame mass.

SAP2000 API:
- FrameObj.SetMass(Name, MassOverL, Replace, ItemType)
- FrameObj.GetMass(Name, MassOverL)
- FrameObj.DeleteMass(Name, ItemType)
"""

from typing import Optional
from .enums import ItemType
from .data_classes import FrameMassData
from PySap2000.com_helper import com_ret, com_data


def set_frame_mass(
    model,
    frame_name: str,
    mass_per_length: float,
    replace: bool = True,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set the additional mass per unit length for a frame.

    This is typically used for non-structural mass such as piping or equipment.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        mass_per_length: Mass per unit length [M/L]
        replace: `True` to replace existing mass, `False` to add to it
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        # Assign 100 kg/m of additional mass
        set_frame_mass(model, "1", 100)
        
        # Add to the existing mass
        set_frame_mass(model, "1", 50, replace=False)
    """
    return model.FrameObj.SetMass(str(frame_name), mass_per_length, replace, int(item_type))


def get_frame_mass(
    model,
    frame_name: str
) -> Optional[float]:
    """
    Get the additional mass per unit length of a frame.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
    
    Returns:
        Mass per unit length [M/L], or `None` if the query fails.
    
    Example:
        mass = get_frame_mass(model, "1")
        if mass:
            print(f"Mass per unit length: {mass}")
    """
    try:
        result = model.FrameObj.GetMass(str(frame_name), 0.0)
        val = com_data(result, 0)
        if val is not None:
            return val
    except Exception:
        pass
    return None


def get_frame_mass_data(
    model,
    frame_name: str
) -> Optional[FrameMassData]:
    """
    Get frame mass data as a structured object.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
    
    Returns:
        A `FrameMassData` instance, or `None` if unavailable.
    
    Example:
        mass_data = get_frame_mass_data(model, "1")
        if mass_data:
            print(f"Mass: {mass_data.mass_per_length}")
    """
    mass = get_frame_mass(model, frame_name)
    if mass is not None:
        return FrameMassData(frame_name=str(frame_name), mass_per_length=mass)
    return None


def delete_frame_mass(
    model,
    frame_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Delete additional frame mass.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        delete_frame_mass(model, "1")
    """
    return model.FrameObj.DeleteMass(str(frame_name), int(item_type))


def has_frame_mass(
    model,
    frame_name: str
) -> bool:
    """
    Check whether a frame has additional assigned mass.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
    
    Returns:
        `True` if additional mass exists, otherwise `False`.
    
    Example:
        if has_frame_mass(model, "1"):
            print("The frame has additional mass")
    """
    mass = get_frame_mass(model, frame_name)
    return mass is not None and mass > 0
