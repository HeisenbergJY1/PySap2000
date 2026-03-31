# -*- coding: utf-8 -*-
"""
group.py - Link group-assignment helpers.

Provides functions to assign link objects to groups and query those assignments.

SAP2000 API:
- LinkObj.SetGroupAssign(Name, GroupName, Remove, ItemType)
- LinkObj.GetGroupAssign(Name, NumberGroups, Groups[])
"""

from typing import List, Optional
from .enums import LinkItemType
from PySap2000.com_helper import com_data


def set_link_group(
    model,
    link_name: str,
    group_name: str,
    remove: bool = False,
    item_type: LinkItemType = LinkItemType.OBJECT
) -> int:
    """
    Assign or remove a link object from a group.
    
    Args:
        model: SAP2000 SapModel object
        link_name: Link object name
        group_name: Group name, which must already exist
        remove: `False` to add the link, `True` to remove it
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        set_link_group(model, "1", "Isolators")
    """
    return model.LinkObj.SetGroupAssign(str(link_name), group_name, remove, int(item_type))


def add_link_to_group(
    model,
    link_name: str,
    group_name: str,
    item_type: LinkItemType = LinkItemType.OBJECT
) -> int:
    """Add a link object to a group."""
    return set_link_group(model, link_name, group_name, False, item_type)


def remove_link_from_group(
    model,
    link_name: str,
    group_name: str,
    item_type: LinkItemType = LinkItemType.OBJECT
) -> int:
    """Remove a link object from a group."""
    return set_link_group(model, link_name, group_name, True, item_type)


def get_link_groups(model, link_name: str) -> Optional[List[str]]:
    """
    Get the groups assigned to a link object.
    
    Args:
        model: SAP2000 SapModel object
        link_name: Link object name
    
    Returns:
        List of group names, or `None` if the query fails.
    """
    try:
        result = model.LinkObj.GetGroupAssign(str(link_name), 0, [])
        num_groups = com_data(result, 0, 0)
        groups = com_data(result, 1)
        if num_groups > 0 and groups:
            return list(groups)
    except Exception:
        pass
    return None


def is_link_in_group(model, link_name: str, group_name: str) -> bool:
    """Check whether a link object belongs to a specific group."""
    groups = get_link_groups(model, link_name)
    if groups:
        return group_name in groups
    return False


def add_links_to_group(model, link_names: List[str], group_name: str) -> int:
    """Add multiple link objects to a group."""
    ret = 0
    for name in link_names:
        result = add_link_to_group(model, name, group_name)
        if result != 0:
            ret = result
    return ret


def remove_links_from_group(model, link_names: List[str], group_name: str) -> int:
    """Remove multiple link objects from a group."""
    ret = 0
    for name in link_names:
        result = remove_link_from_group(model, name, group_name)
        if result != 0:
            ret = result
    return ret
