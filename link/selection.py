# -*- coding: utf-8 -*-
"""
selection.py - Link selection helpers.

Provides functions to set and query the selection state of link objects.

SAP2000 API:
- LinkObj.SetSelected(Name, Selected, ItemType)
- LinkObj.GetSelected(Name, Selected)
"""

from typing import List
from .enums import LinkItemType
from PySap2000.com_helper import com_data


def set_link_selected(
    model,
    link_name: str,
    selected: bool = True,
    item_type: LinkItemType = LinkItemType.OBJECT
) -> int:
    """
    Set the selection state of a link object.
    
    Args:
        model: SAP2000 SapModel object
        link_name: Link object name
        selected: `True` to select, `False` to deselect
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        set_link_selected(model, "1", True)
    """
    return model.LinkObj.SetSelected(str(link_name), selected, int(item_type))


def get_link_selected(
    model,
    link_name: str
) -> bool:
    """
    Get the selection state of a link object.
    
    Args:
        model: SAP2000 SapModel object
        link_name: Link object name
    
    Returns:
        `True` if selected, otherwise `False`.
    
    Example:
        if get_link_selected(model, "1"):
            print("The link is selected")
    """
    try:
        result = model.LinkObj.GetSelected(str(link_name), False)
        return com_data(result, 0, False)
    except Exception:
        pass
    return False


def select_link(
    model,
    link_name: str,
    item_type: LinkItemType = LinkItemType.OBJECT
) -> int:
    """Select a link object."""
    return set_link_selected(model, link_name, True, item_type)


def deselect_link(
    model,
    link_name: str,
    item_type: LinkItemType = LinkItemType.OBJECT
) -> int:
    """Deselect a link object."""
    return set_link_selected(model, link_name, False, item_type)


def select_links(model, link_names: List[str]) -> int:
    """Select multiple link objects."""
    ret = 0
    for name in link_names:
        result = set_link_selected(model, name, True)
        if result != 0:
            ret = result
    return ret


def deselect_links(model, link_names: List[str]) -> int:
    """Deselect multiple link objects."""
    ret = 0
    for name in link_names:
        result = set_link_selected(model, name, False)
        if result != 0:
            ret = result
    return ret


def is_link_selected(model, link_name: str) -> bool:
    """Check whether a link object is selected."""
    return get_link_selected(model, link_name)
