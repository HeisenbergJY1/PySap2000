# -*- coding: utf-8 -*-
"""
property.py - Cable property-assignment helpers.

Wraps `CableObj.SetProperty` / `GetProperty`.

This module assigns properties to cable objects; it does not define the
properties themselves.

Includes:
- Section assignment: `set/get_cable_section`
- Material override: `set/get_cable_material_overwrite`
- Material temperature: `set/get_cable_material_temp`

Usage:
    from cable import set_cable_section, get_cable_section
    
    # Assign a section to a cable
    set_cable_section(model, "1", "Cable1")
    
    # Get the cable section
    section_name = get_cable_section(model, "1")
"""

from typing import Tuple
from .modifier import CableItemType
from PySap2000.com_helper import com_ret, com_data


# =============================================================================
# Section assignment
# =============================================================================

def set_cable_section(
    model,
    cable_name: str,
    section_name: str,
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    Assign a section property to a cable.
    
    Args:
        model: `SapModel` object
        cable_name: Cable name
        section_name: Section name (must already exist in `PropCable`)
        item_type: Item scope
            - `OBJECT (0)`: single object
            - `GROUP (1)`: all objects in a group
            - `SELECTED_OBJECTS (2)`: all selected objects
    
    Returns:
        `0` on success, non-zero on failure
    
    Example:
        # Set cable "1" to section "Cable1"
        set_cable_section(model, "1", "Cable1")
        
        # Set the section for all cables in group "Cables"
        set_cable_section(model, "Cables", "Cable1", CableItemType.GROUP)
    """
    return model.CableObj.SetProperty(
        str(cable_name),
        section_name,
        int(item_type)
    )


def get_cable_section(model, cable_name: str) -> str:
    """
    Return the assigned section name for a cable.
    
    Args:
        model: `SapModel` object
        cable_name: Cable name
    
    Returns:
        Section name
    """
    result = model.CableObj.GetProperty(str(cable_name))
    return com_data(result, 0, "") or ""



def get_cable_section_list(model) -> list:
    """
    Return the list of all cable section names.
    
    Args:
        model: `SapModel` object
    
    Returns:
        List of section names
    
    Example:
        sections = get_cable_section_list(model)
        for name in sections:
            print(name)
    """
    result = model.PropCable.GetNameList(0, [])
    ret = com_ret(result)
    if ret == 0:
        names = com_data(result, 1)
        return list(names) if names else []
    return []


# =============================================================================
# Material overwrite
# =============================================================================

def set_cable_material_overwrite(
    model,
    cable_name: str,
    material_name: str,
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    Assign a material overwrite to a cable.

    This overrides the material defined in the assigned section property.
    
    Args:
        model: `SapModel` object
        cable_name: Cable name
        material_name: Material name; empty string restores the section material
        item_type: Item scope
    
    Returns:
        `0` on success, non-zero on failure
    
    Example:
        # Override the material on cable "1"
        set_cable_material_overwrite(model, "1", "A416Gr270")
        
        # Clear the overwrite and use the section material
        set_cable_material_overwrite(model, "1", "")
    """
    return model.CableObj.SetMaterialOverwrite(
        str(cable_name),
        material_name,
        int(item_type)
    )


def get_cable_material_overwrite(model, cable_name: str) -> str:
    """
    Return the material overwrite assigned to a cable.
    
    Args:
        model: `SapModel` object
        cable_name: Cable name
    
    Returns:
        Material name, or an empty string if no overwrite is assigned
    
    Example:
        mat = get_cable_material_overwrite(model, "1")
        if mat:
            print(f"Material overwrite: {mat}")
        else:
            print("Using the material defined by the section")
    """
    result = model.CableObj.GetMaterialOverwrite(str(cable_name))
    return com_data(result, 0, "") or ""


# =============================================================================
# Material temperature
# =============================================================================

def set_cable_material_temp(
    model,
    cable_name: str,
    temperature: float,
    pattern_name: str = "",
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    Set the material temperature for a cable.
    
    Args:
        model: `SapModel` object
        cable_name: Cable name
        temperature: Temperature value [T]
        pattern_name: Load pattern name; empty string means no pattern
        item_type: Item scope
    
    Returns:
        `0` on success, non-zero on failure
    
    Example:
        # Set the material temperature of cable "1" to 20 degrees
        set_cable_material_temp(model, "1", 20.0)
    """
    return model.CableObj.SetMatTemp(
        str(cable_name),
        temperature,
        pattern_name,
        int(item_type)
    )


def get_cable_material_temp(model, cable_name: str) -> Tuple[float, str]:
    """
    Return the material temperature assigned to a cable.
    
    Args:
        model: `SapModel` object
        cable_name: Cable name
    
    Returns:
        Tuple `(temperature, pattern_name)`
    
    Example:
        temp, pattern = get_cable_material_temp(model, "1")
        print(f"Temperature: {temp}, Pattern: {pattern}")
    """
    result = model.CableObj.GetMatTemp(str(cable_name))
    temp = com_data(result, 0)
    pattern = com_data(result, 1)
    if temp is not None:
        return (temp, pattern or "")
    return (0.0, "")
