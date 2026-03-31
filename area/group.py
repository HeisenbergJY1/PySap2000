# -*- coding: utf-8 -*-
"""
group.py - Area group-assignment helpers.

Wraps SAP2000 `AreaObj` group-assignment APIs.

SAP2000 API:
- AreaObj.SetGroupAssign(Name, GroupName, Remove, ItemType)
- AreaObj.GetGroupAssign(Name, NumberGroups, Groups[])
"""

from typing import List, Optional

from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


def set_area_group(
    model,
    area_name: str,
    group_name: str,
    remove: bool = False,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Assign or remove an area object from a group.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        group_name: Group name, which must already exist
        remove: `False` to add the area, `True` to remove it
        item_type: Target scope
    
    Returns:
        `0` on success. Nonzero indicates failure.
    
    Example:
        # Add the area to a group
        set_area_group(model, "1", "Slabs")
        
        # Remove the area from a group
        set_area_group(model, "1", "Slabs", remove=True)
    """
    return model.AreaObj.SetGroupAssign(str(area_name), group_name, remove, int(item_type))


def add_area_to_group(
    model,
    area_name: str,
    group_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Add an area object to a group.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        group_name: Group name, which must already exist
        item_type: Target scope
    
    Returns:
        `0` on success. Nonzero indicates failure.
    
    Example:
        add_area_to_group(model, "1", "Slabs")
    """
    return set_area_group(model, area_name, group_name, False, item_type)


def remove_area_from_group(
    model,
    area_name: str,
    group_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Remove an area object from a group.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        group_name: Group name
        item_type: Target scope
    
    Returns:
        `0` on success. Nonzero indicates failure.
    
    Example:
        remove_area_from_group(model, "1", "Slabs")
    """
    return set_area_group(model, area_name, group_name, True, item_type)


def get_area_groups(
    model,
    area_name: str
) -> Optional[List[str]]:
    """
    Get the groups assigned to an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
    
    Returns:
        List of group names, or `None` if the query fails.
    
    Example:
        groups = get_area_groups(model, "1")
        if groups:
            print(f"Assigned groups: {groups}")
    """
    try:
        result = model.AreaObj.GetGroupAssign(str(area_name), 0, [])
        num_groups = com_data(result, 0, 0)
        groups = com_data(result, 1)
        if num_groups > 0 and groups:
            return list(groups)
    except Exception:
        pass
    return None


def is_area_in_group(
    model,
    area_name: str,
    group_name: str
) -> bool:
    """
    Check whether an area object belongs to a specific group.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        group_name: Group name
    
    Returns:
        `True` if the area belongs to the group, otherwise `False`.
    
    Example:
        if is_area_in_group(model, "1", "Slabs"):
            print("The area belongs to the Slabs group")
    """
    groups = get_area_groups(model, area_name)
    if groups:
        return group_name in groups
    return False


def add_areas_to_group(
    model,
    area_names: List[str],
    group_name: str
) -> int:
    """
    Add multiple area objects to a group.
    
    Args:
        model: SAP2000 SapModel object
        area_names: List of area object names
        group_name: Group name, which must already exist
    
    Returns:
        `0` if all operations succeed. Nonzero indicates at least one failure.
    
    Example:
        add_areas_to_group(model, ["1", "2", "3"], "Slabs")
    """
    ret = 0
    for name in area_names:
        result = add_area_to_group(model, name, group_name)
        if result != 0:
            ret = result
    return ret


def remove_areas_from_group(
    model,
    area_names: List[str],
    group_name: str
) -> int:
    """
    Remove multiple area objects from a group.
    
    Args:
        model: SAP2000 SapModel object
        area_names: List of area object names
        group_name: Group name
    
    Returns:
        `0` if all operations succeed. Nonzero indicates at least one failure.
    
    Example:
        remove_areas_from_group(model, ["1", "2", "3"], "Slabs")
    """
    ret = 0
    for name in area_names:
        result = remove_area_from_group(model, name, group_name)
        if result != 0:
            ret = result
    return ret
