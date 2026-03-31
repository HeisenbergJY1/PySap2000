# -*- coding: utf-8 -*-
"""
selection.py - Frame selection helpers.

Provides functions to set and query frame selection state.

SAP2000 API:
- FrameObj.SetSelected(Name, Selected, ItemType)
- FrameObj.GetSelected(Name, Selected)
"""

from typing import List
from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


def set_frame_selected(
    model,
    frame_name: str,
    selected: bool = True,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set the selection state of a frame object.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        selected: `True` to select, `False` to deselect
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        # Select a frame
        set_frame_selected(model, "1", True)
        
        # Deselect a frame
        set_frame_selected(model, "1", False)
    """
    return model.FrameObj.SetSelected(str(frame_name), selected, int(item_type))


def get_frame_selected(
    model,
    frame_name: str
) -> bool:
    """
    Get the selection state of a frame object.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
    
    Returns:
        `True` if the frame is selected, otherwise `False`.
    
    Example:
        if get_frame_selected(model, "1"):
            print("The frame is selected")
    """
    try:
        result = model.FrameObj.GetSelected(str(frame_name), False)
        val = com_data(result, 0)
        if val is not None:
            return val
    except Exception:
        pass
    return False


def select_frame(
    model,
    frame_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Select a frame object.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        select_frame(model, "1")
    """
    return set_frame_selected(model, frame_name, True, item_type)


def deselect_frame(
    model,
    frame_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Deselect a frame object.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        deselect_frame(model, "1")
    """
    return set_frame_selected(model, frame_name, False, item_type)


def select_frames(
    model,
    frame_names: List[str]
) -> int:
    """
    Select multiple frame objects.
    
    Args:
        model: SAP2000 SapModel object
        frame_names: List of frame object names
    
    Returns:
        `0` if all operations succeed.
    
    Example:
        select_frames(model, ["1", "2", "3"])
    """
    ret = 0
    for name in frame_names:
        result = set_frame_selected(model, name, True)
        if result != 0:
            ret = result
    return ret


def deselect_frames(
    model,
    frame_names: List[str]
) -> int:
    """
    Deselect multiple frame objects.
    
    Args:
        model: SAP2000 SapModel object
        frame_names: List of frame object names
    
    Returns:
        `0` if all operations succeed.
    
    Example:
        deselect_frames(model, ["1", "2", "3"])
    """
    ret = 0
    for name in frame_names:
        result = set_frame_selected(model, name, False)
        if result != 0:
            ret = result
    return ret


def is_frame_selected(
    model,
    frame_name: str
) -> bool:
    """
    Check whether a frame object is selected.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
    
    Returns:
        `True` if selected, otherwise `False`.
    
    Example:
        if is_frame_selected(model, "1"):
            print("The frame is selected")
    """
    return get_frame_selected(model, frame_name)
