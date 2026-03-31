# -*- coding: utf-8 -*-
"""
property.py - Area property-assignment helpers.

Wraps SAP2000 `AreaObj.SetProperty` and `AreaObj.GetProperty`.

This module assigns existing properties to area objects. Property definition
itself belongs to the `section` package.

Usage:
    from area import set_area_property, get_area_property

    # Assign a property to an area
    set_area_property(model, "1", "SLAB1")

    # Get the assigned property
    prop_name = get_area_property(model, "1")
"""

from typing import Optional
from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


def set_area_property(
    model,
    area_name: str,
    property_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Assign a section property to an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        property_name: Property name, which must already exist in `PropArea`
        item_type: Target scope
            - `OBJECT (0)`: single object
            - `GROUP (1)`: all objects in a group
            - `SELECTED_OBJECTS (2)`: all selected objects
    
    Returns:
        `0` on success. Nonzero indicates failure.
    
    Example:
        # Set the property of area "1" to "SLAB1"
        set_area_property(model, "1", "SLAB1")
        
        # Set the property for all areas in group "Floor"
        set_area_property(model, "Floor", "SLAB1", ItemType.GROUP)
        
        # Set the property for all selected areas
        set_area_property(model, "", "SLAB1", ItemType.SELECTED_OBJECTS)
    """
    return model.AreaObj.SetProperty(
        str(area_name),
        property_name,
        item_type.value
    )


def get_area_property(model, area_name: str) -> str:
    """
    Get the assigned section property name of an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
    
    Returns:
        Property name.
    
    Example:
        prop_name = get_area_property(model, "1")
        print(f"Property of area 1: {prop_name}")
    """
    result = model.AreaObj.GetProperty(str(area_name))
    return com_data(result, 0, "") or ""


def get_area_property_type(model, area_name: str) -> int:
    """
    Get the property type of an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
    
    Returns:
        Property type:
            `1` = Shell
            `2` = Plane
            `3` = Asolid
    
    Example:
        prop_type = get_area_property_type(model, "1")
        if prop_type == 1:
            print("This is a shell element")
    """
    result = model.AreaObj.GetProperty(str(area_name))
    return com_data(result, 1, 0)


def set_area_material_overwrite(
    model,
    area_name: str,
    material_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Override the material assigned through the area property.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        material_name: Material name. Use an empty string to fall back to the
            material defined by the area property.
        item_type: Target scope
    
    Returns:
        `0` on success. Nonzero indicates failure.
    
    Example:
        # Override the material of area "1" with "C30"
        set_area_material_overwrite(model, "1", "C30")
        
        # Clear the override and use the property material
        set_area_material_overwrite(model, "1", "")
    """
    return model.AreaObj.SetMaterialOverwrite(
        str(area_name),
        material_name,
        item_type.value
    )


def get_area_material_overwrite(model, area_name: str) -> str:
    """
    Get the material override assigned to an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
    
    Returns:
        Material name, or an empty string if no override exists.
    
    Example:
        mat = get_area_material_overwrite(model, "1")
        if mat:
            print(f"Material override: {mat}")
        else:
            print("Using the property material")
    """
    result = model.AreaObj.GetMaterialOverwrite(str(area_name))
    return com_data(result, 0, "") or ""


def set_area_material_temperature(
    model,
    area_name: str,
    temperature: float,
    pattern_name: str = "",
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set the material temperature assigned to an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        temperature: Temperature value [T]
        pattern_name: Load pattern name. Use an empty string for no pattern.
        item_type: Target scope
    
    Returns:
        `0` on success. Nonzero indicates failure.
    
    Example:
        # Set the material temperature of area "1" to 20 C
        set_area_material_temperature(model, "1", 20.0)
    """
    return model.AreaObj.SetMatTemp(
        str(area_name),
        temperature,
        pattern_name,
        item_type.value
    )


def get_area_material_temperature(model, area_name: str) -> tuple:
    """
    Get the material temperature assigned to an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
    
    Returns:
        Tuple `(temperature, pattern_name)`.
    
    Example:
        temp, pattern = get_area_material_temperature(model, "1")
        print(f"Temperature: {temp}, pattern: {pattern}")
    """
    result = model.AreaObj.GetMatTemp(str(area_name))
    return (com_data(result, 0, 0.0), com_data(result, 1, "") or "")
