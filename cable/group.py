# -*- coding: utf-8 -*-
"""
group.py - Cable group-assignment helpers.

SAP2000 API:
- CableObj.SetGroupAssign(Name, GroupName, Remove, ItemType)
- CableObj.GetGroupAssign(Name, NumberGroups, Groups)
"""

from typing import List, Optional
from .modifier import CableItemType
from PySap2000.com_helper import com_data


def set_cable_group(
    model,
    cable_name: str,
    group_name: str,
    remove: bool = False,
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    Add a cable to a group or remove it from one.
    
    Args:
        model: SAP2000 SapModel object
        cable_name: Cable object name
        group_name: Group name
        remove: `False` to add the cable, `True` to remove it
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        # Add the cable to a group
        set_cable_group(model, "1", "CableGroup")
        
        # Remove the cable from a group
        set_cable_group(model, "1", "CableGroup", remove=True)
    """
    return model.CableObj.SetGroupAssign(str(cable_name), group_name, remove, int(item_type))


def get_cable_groups(model, cable_name: str) -> List[str]:
    """
    Get the list of groups assigned to a cable object.
    
    Args:
        model: SAP2000 SapModel object
        cable_name: Cable object name
    
    Returns:
        List of assigned group names.
    
    Example:
        groups = get_cable_groups(model, "1")
        print(f"Cable 1 belongs to: {groups}")
    """
    try:
        result = model.CableObj.GetGroupAssign(str(cable_name), 0, [])
        count = com_data(result, 0, 0)
        groups = com_data(result, 1)
        if count > 0 and groups:
            return list(groups)
    except Exception:
        pass
    return []
