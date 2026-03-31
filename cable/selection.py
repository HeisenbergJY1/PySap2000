# -*- coding: utf-8 -*-
"""
selection.py - Cable selection helpers.

SAP2000 API:
- CableObj.SetSelected(Name, Selected, ItemType)
- CableObj.GetSelected(Name, Selected)
"""

from typing import Optional, List
from .modifier import CableItemType
from PySap2000.com_helper import com_data


def set_cable_selected(
    model,
    cable_name: str,
    selected: bool = True,
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    Set the selection state of a cable object.
    
    Args:
        model: SAP2000 SapModel object
        cable_name: Cable object name
        selected: `True` to select, `False` to deselect
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        # Select a single cable
        set_cable_selected(model, "1", True)
        
        # Select all cables in the target scope
        set_cable_selected(model, "ALL", True, CableItemType.GROUP)
    """
    return model.CableObj.SetSelected(str(cable_name), selected, int(item_type))


def get_cable_selected(model, cable_name: str) -> Optional[bool]:
    """
    Get the selection state of a cable object.
    
    Args:
        model: SAP2000 SapModel object
        cable_name: Cable object name
    
    Returns:
        `True` if selected, `False` if not selected, or `None` if the query fails.
    
    Example:
        if get_cable_selected(model, "1"):
            print("Cable 1 is selected")
    """
    try:
        result = model.CableObj.GetSelected(str(cable_name), False)
        return com_data(result, 0)
    except Exception:
        pass
    return None


def get_selected_cables(model) -> List[str]:
    """
    Get the names of all selected cable objects.
    
    Args:
        model: SAP2000 SapModel object
    
    Returns:
        List of selected cable names.
    
    Example:
        selected = get_selected_cables(model)
        print(f"Selected {len(selected)} cable objects")
    """
    selected = []
    try:
        # Get all cable object names first, then filter by selection state.
        result = model.CableObj.GetNameList(0, [])
        names = com_data(result, 1)
        if names:
                for name in names:
                    if get_cable_selected(model, name):
                        selected.append(name)
    except Exception:
        pass
    return selected
