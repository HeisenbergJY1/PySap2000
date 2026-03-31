# -*- coding: utf-8 -*-
"""
group.py - Frame group-assignment helpers.

Provides functions to assign frames to groups and query existing assignments.

SAP2000 API:
- FrameObj.SetGroupAssign(Name, GroupName, Remove, ItemType)
- FrameObj.GetGroupAssign(Name, NumberGroups, Groups[])
"""

from typing import List, Optional
from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


def set_frame_group(
    model,
    frame_name: str,
    group_name: str,
    remove: bool = False,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Assign or remove a frame from a group.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        group_name: Group name, which must already exist
        remove: `False` to add the frame, `True` to remove it
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        # Add the frame to a group
        set_frame_group(model, "1", "Beams")
        
        # Remove the frame from a group
        set_frame_group(model, "1", "Beams", remove=True)
    """
    return model.FrameObj.SetGroupAssign(str(frame_name), group_name, remove, int(item_type))


def add_frame_to_group(
    model,
    frame_name: str,
    group_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Add a frame to a group.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        group_name: Group name, which must already exist
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        add_frame_to_group(model, "1", "Beams")
    """
    return set_frame_group(model, frame_name, group_name, False, item_type)


def remove_frame_from_group(
    model,
    frame_name: str,
    group_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Remove a frame from a group.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        group_name: Group name
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        remove_frame_from_group(model, "1", "Beams")
    """
    return set_frame_group(model, frame_name, group_name, True, item_type)


def get_frame_groups(
    model,
    frame_name: str
) -> Optional[List[str]]:
    """
    Get the groups assigned to a frame.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
    
    Returns:
        List of group names, or `None` if the query fails.
    
    Example:
        groups = get_frame_groups(model, "1")
        if groups:
            print(f"Assigned groups: {groups}")
    """
    try:
        result = model.FrameObj.GetGroupAssign(str(frame_name), 0, [])
        num_groups = com_data(result, 0, 0)
        groups = com_data(result, 1)
        if num_groups > 0 and groups:
            return list(groups)
    except Exception:
        pass
    return None


def is_frame_in_group(
    model,
    frame_name: str,
    group_name: str
) -> bool:
    """
    Check whether a frame belongs to a specific group.
    
    Args:
        model: SAP2000 SapModel object
        frame_name: Frame object name
        group_name: Group name
    
    Returns:
        `True` if the frame belongs to the group, otherwise `False`.
    
    Example:
        if is_frame_in_group(model, "1", "Beams"):
            print("The frame belongs to the Beams group")
    """
    groups = get_frame_groups(model, frame_name)
    if groups:
        return group_name in groups
    return False


def add_frames_to_group(
    model,
    frame_names: List[str],
    group_name: str
) -> int:
    """
    Add multiple frames to a group.
    
    Args:
        model: SAP2000 SapModel object
        frame_names: List of frame object names
        group_name: Group name, which must already exist
    
    Returns:
        `0` if all operations succeed.
    
    Example:
        add_frames_to_group(model, ["1", "2", "3"], "Beams")
    """
    ret = 0
    for name in frame_names:
        result = add_frame_to_group(model, name, group_name)
        if result != 0:
            ret = result
    return ret


def remove_frames_from_group(
    model,
    frame_names: List[str],
    group_name: str
) -> int:
    """
    Remove multiple frames from a group.
    
    Args:
        model: SAP2000 SapModel object
        frame_names: List of frame object names
        group_name: Group name
    
    Returns:
        `0` if all operations succeed.
    
    Example:
        remove_frames_from_group(model, ["1", "2", "3"], "Beams")
    """
    ret = 0
    for name in frame_names:
        result = remove_frame_from_group(model, name, group_name)
        if result != 0:
            ret = result
    return ret
