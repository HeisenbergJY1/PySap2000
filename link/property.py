# -*- coding: utf-8 -*-
"""
property.py - Link property-assignment helpers.

Helpers for assigning properties at the `LinkObj` level rather than defining
`PropLink` properties.

SAP2000 API:
- LinkObj.SetProperty(Name, PropName, ItemType)
- LinkObj.GetProperty(Name, PropName)
- LinkObj.SetPropertyFD(Name, PropName, ItemType)
- LinkObj.GetPropertyFD(Name, PropName)
"""

from typing import Optional, Tuple
from .enums import LinkItemType
from PySap2000.com_helper import com_data


def set_link_property(
    model,
    link_name: str,
    property_name: str,
    item_type: LinkItemType = LinkItemType.OBJECT
) -> int:
    """
    Assign a link property.
    
    Args:
        model: `SapModel` object
        link_name: Link object name
        property_name: Link property name
        item_type: Item scope
    
    Returns:
        `0` on success
    
    Example:
        set_link_property(model, "1", "Linear1")
    """
    return model.LinkObj.SetProperty(str(link_name), property_name, int(item_type))


def get_link_property(model, link_name: str) -> Optional[str]:
    """
    Return the assigned link property name.
    
    Args:
        model: `SapModel` object
        link_name: Link object name
    
    Returns:
        Property name, or `None` on failure
    """
    try:
        result = model.LinkObj.GetProperty(str(link_name), "")
        return com_data(result, 0)
    except Exception:
        pass
    return None


def set_link_property_fd(
    model,
    link_name: str,
    property_name: Optional[str],
    item_type: LinkItemType = LinkItemType.OBJECT
) -> int:
    """
    Assign a frequency-dependent property to a link.
    
    Args:
        model: `SapModel` object
        link_name: Link object name
        property_name: Frequency-dependent property name; `None` clears it
        item_type: Item scope
    
    Returns:
        `0` on success
    """
    if property_name is None:
        property_name = "None"
    return model.LinkObj.SetPropertyFD(str(link_name), property_name, int(item_type))


def get_link_property_fd(model, link_name: str) -> Optional[str]:
    """
    Return the frequency-dependent property name for a link.
    
    Args:
        model: `SapModel` object
        link_name: Link object name
    
    Returns:
        Frequency-dependent property name, or `None`
    """
    try:
        result = model.LinkObj.GetPropertyFD(str(link_name), "")
        prop_name = com_data(result, 0)
        if prop_name and prop_name != "None":
            return prop_name
    except Exception:
        pass
    return None


def get_link_property_info(model, link_name: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Return both standard and frequency-dependent property information.
    
    Args:
        model: `SapModel` object
        link_name: Link object name
    
    Returns:
        Tuple `(property_name, fd_property_name)`
    """
    prop = get_link_property(model, link_name)
    fd_prop = get_link_property_fd(model, link_name)
    return (prop, fd_prop)
