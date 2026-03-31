# -*- coding: utf-8 -*-
"""
property.py - Frame property-assignment helpers.

Wraps SAP2000 `FrameObj.SetSection` and `FrameObj.GetSection`.

This module assigns existing properties to frame objects. Property definition
itself belongs to the `section` package.

Usage:
    from frame import set_frame_section, get_frame_section

    # Assign a section to a frame
    set_frame_section(model, "1", "W14X22")

    # Get the currently assigned section
    section_name = get_frame_section(model, "1")
"""

from typing import Optional, Tuple
from .enums import ItemType
from .data_classes import FrameSectionNonPrismaticData
from PySap2000.com_helper import com_ret, com_data


def set_frame_section(
    model,
    frame_name: str,
    section_name: str,
    item_type: ItemType = ItemType.OBJECT,
    var_total_length: float = 0.0,
    var_rel_start_loc: float = 0.0,
) -> int:
    """
    Assign a section property to a frame object.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        section_name: Section property name, which must already exist in `PropFrame`
        item_type: Target scope
            - `OBJECT (0)`: single object
            - `GROUP (1)`: all objects in a group
            - `SELECTED_OBJECTS (2)`: all selected objects
        var_total_length: Assumed total length for nonprismatic variation.
            Use `0` to match the frame length.
        var_rel_start_loc: Relative distance from the I-end to the nonprismatic
            start location. Only used when `var_total_length > 0`.
    
    Returns:
        `0` on success. Nonzero indicates failure.
    
    Example:
        # Set frame "1" to use section "W14X22"
        set_frame_section(model, "1", "W14X22")
        
        # Set the section for every frame in group "Beams"
        set_frame_section(model, "Beams", "W14X22", ItemType.GROUP)
        
        # Assign a nonprismatic section with total length and start location
        set_frame_section(model, "8", "NP1", var_total_length=360, var_rel_start_loc=0.1)
    """
    return model.FrameObj.SetSection(
        str(frame_name),
        section_name,
        item_type.value,
        var_rel_start_loc,
        var_total_length,
    )


def get_frame_section(model, frame_name: str) -> str:
    """
    Get the assigned section property name of a frame.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
    
    Returns:
        Section property name.
    
    Example:
        section = get_frame_section(model, "1")
        print(f"Section of frame 1: {section}")
    """
    result = model.FrameObj.GetSection(str(frame_name))
    return com_data(result, 0, "") or ""


def get_frame_section_info(model, frame_name: str) -> Tuple[str, str]:
    """
    Get section assignment details for a frame, including auto-select data.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
    
    Returns:
        Tuple `(section_name, auto_select_list)`.
        - `section_name`: current assigned section
        - `auto_select_list`: auto-select list name, if present
    
    Example:
        section, auto_list = get_frame_section_info(model, "1")
        if auto_list:
            print(f"Auto-select list in use: {auto_list}")
    """
    result = model.FrameObj.GetSection(str(frame_name))
    return (com_data(result, 0, "") or "", com_data(result, 1, "") or "")


def set_frame_material_overwrite(
    model,
    frame_name: str,
    material_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Override the material assigned through the frame section property.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        material_name: Material name. Use an empty string to fall back to the
            material defined by the section property.
        item_type: Target scope
    
    Returns:
        `0` on success. Nonzero indicates failure.
    
    Example:
        # Override the material of frame "1" with "A992Fy50"
        set_frame_material_overwrite(model, "1", "A992Fy50")
        
        # Clear the override and use the section material
        set_frame_material_overwrite(model, "1", "")
    """
    return model.FrameObj.SetMaterialOverwrite(
        str(frame_name),
        material_name,
        item_type.value
    )


def get_frame_material_overwrite(model, frame_name: str) -> str:
    """
    Get the material override assigned to a frame.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
    
    Returns:
        Material name, or an empty string if no override is assigned.
    
    Example:
        mat = get_frame_material_overwrite(model, "1")
        if mat:
            print(f"Material override: {mat}")
        else:
            print("Using the section material")
    """
    result = model.FrameObj.GetMaterialOverwrite(str(frame_name))
    material = com_data(result, 0, "") or ""
    # SAP2000 may return the literal string "None" to indicate no override.
    if material == "None":
        return ""
    return material


def set_frame_material_temperature(
    model,
    frame_name: str,
    temperature: float,
    pattern_name: str = "",
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set the material temperature assigned to a frame.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        temperature: Temperature value [T]
        pattern_name: Load pattern name. Use an empty string for no pattern.
        item_type: Target scope
    
    Returns:
        `0` on success. Nonzero indicates failure.
    
    Example:
        # Set the material temperature of frame "1" to 20 C
        set_frame_material_temperature(model, "1", 20.0)
    """
    return model.FrameObj.SetMatTemp(
        str(frame_name),
        temperature,
        pattern_name,
        item_type.value
    )


def get_frame_material_temperature(model, frame_name: str) -> Tuple[float, str]:
    """
    Get the material temperature assigned to a frame.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
    
    Returns:
        Tuple `(temperature, pattern_name)`.
    
    Example:
        temp, pattern = get_frame_material_temperature(model, "1")
        print(f"Temperature: {temp}, pattern: {pattern}")
    """
    result = model.FrameObj.GetMatTemp(str(frame_name))
    return (com_data(result, 0, 0.0), com_data(result, 1, "") or "")


def get_frame_section_nonprismatic(
    model,
    frame_name: str,
) -> FrameSectionNonPrismaticData:
    """
    Get nonprismatic section assignment data for a frame.

    Wraps the `FrameObj.GetSectionNonPrismatic` API. This is only valid when
    the frame has a nonprismatic section assignment.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
    
    Returns:
        `FrameSectionNonPrismaticData` instance.
    
    Raises:
        ValueError: The frame does not have a nonprismatic section assignment.
    
    Example:
        data = get_frame_section_nonprismatic(model, "876")
        print(f"Nonprismatic property: {data.prop_name}, total length: {data.total_length}")
    """
    result = model.FrameObj.GetSectionNonPrismatic(
        str(frame_name), "", 0.0, 0.0
    )
    ret = com_ret(result)
    if ret != 0:
        raise ValueError(
            f"Frame {frame_name} has no nonprismatic section assignment or the query failed"
        )
    return FrameSectionNonPrismaticData(
        frame_name=frame_name,
        prop_name=com_data(result, 0, "") or "",
        total_length=com_data(result, 1, 0.0),
        rel_start_loc=com_data(result, 2, 0.0),
    )
