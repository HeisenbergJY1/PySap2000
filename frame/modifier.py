# -*- coding: utf-8 -*-
"""
modifier.py - Frame section modifier helpers.

Provides functions to assign frame property modifiers such as stiffness reduction factors.

SAP2000 API:
- FrameObj.SetModifiers(Name, Value[], ItemType)
- FrameObj.GetModifiers(Name, Value[])
- FrameObj.DeleteModifiers(Name, ItemType)
"""

from typing import Tuple, Optional
from .enums import ItemType
from .data_classes import FrameModifierData
from PySap2000.com_helper import com_ret, com_data


def set_frame_modifiers(
    model,
    frame_name: str,
    area: float = 1.0,
    shear_2: float = 1.0,
    shear_3: float = 1.0,
    torsion: float = 1.0,
    inertia_22: float = 1.0,
    inertia_33: float = 1.0,
    mass: float = 1.0,
    weight: float = 1.0,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set section property modifiers for a frame.

    Modifiers are commonly used for stiffness reduction.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        area: Area modifier (`A`)
        shear_2: Local-2 shear-area modifier (`As2`)
        shear_3: Local-3 shear-area modifier (`As3`)
        torsion: Torsional constant modifier (`J`)
        inertia_22: Local-2 inertia modifier (`I22`)
        inertia_33: Local-3 inertia modifier (`I33`)
        mass: Mass modifier
        weight: Weight modifier
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        # Set the I33 modifier to 0.5 (50% stiffness reduction)
        set_frame_modifiers(model, "1", inertia_33=0.5)
        
        # Reduce beam stiffness (I22=0.4, I33=0.4)
        set_frame_modifiers(model, "1", inertia_22=0.4, inertia_33=0.4)
        
        # Reduce column stiffness (A=0.7, I22=0.7, I33=0.7)
        set_frame_modifiers(model, "1", area=0.7, inertia_22=0.7, inertia_33=0.7)
    """
    modifiers = [area, shear_2, shear_3, torsion, inertia_22, inertia_33, mass, weight]
    result = model.FrameObj.SetModifiers(str(frame_name), modifiers, int(item_type))
    return com_ret(result)


def set_frame_modifiers_tuple(
    model,
    frame_name: str,
    modifiers: Tuple[float, ...],
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set frame section modifiers from a tuple.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        modifiers: Tuple of 8 modifier values
            `(A, As2, As3, J, I22, I33, Mass, Weight)`
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        set_frame_modifiers_tuple(model, "1", (1, 1, 1, 1, 1, 0.5, 1, 1))
    """
    m_list = list(modifiers)
    while len(m_list) < 8:
        m_list.append(1.0)
    return model.FrameObj.SetModifiers(str(frame_name), m_list[:8], int(item_type))


def get_frame_modifiers(
    model,
    frame_name: str
) -> Optional[FrameModifierData]:
    """
    Get frame section modifiers as a structured object.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
    
    Returns:
        A `FrameModifierData` instance, or `None` if unavailable.
    
    Example:
        modifiers = get_frame_modifiers(model, "1")
        if modifiers:
            print(f"I33 modifier: {modifiers.inertia_33}")
    """
    try:
        result = model.FrameObj.GetModifiers(str(frame_name), [0.0] * 8)
        values = com_data(result, 0)
        if values and len(values) >= 8:
            return FrameModifierData.from_tuple(str(frame_name), tuple(values))
    except Exception:
        pass
    return None


def get_frame_modifiers_tuple(
    model,
    frame_name: str
) -> Optional[Tuple[float, ...]]:
    """
    Get frame section modifiers as a tuple.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
    
    Returns:
        Tuple of 8 modifier values, or `None` if unavailable.
    
    Example:
        modifiers = get_frame_modifiers_tuple(model, "1")
        if modifiers:
            print(f"Modifiers: {modifiers}")
    """
    try:
        result = model.FrameObj.GetModifiers(str(frame_name), [0.0] * 8)
        values = com_data(result, 0)
        if values:
            return tuple(values)
    except Exception:
        pass
    return None


def delete_frame_modifiers(
    model,
    frame_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Delete frame modifiers and restore defaults of `1.0`.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        delete_frame_modifiers(model, "1")
    """
    return model.FrameObj.DeleteModifiers(str(frame_name), int(item_type))
