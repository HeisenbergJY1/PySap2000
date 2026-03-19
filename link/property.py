# -*- coding: utf-8 -*-
"""
property.py - 连接单元属性分配相关函数

用于设置连接单元的属性分配（LinkObj 级别，非 PropLink）

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
    设置连接单元属性
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        property_name: 连接属性名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        set_link_property(model, "1", "Linear1")
    """
    return model.LinkObj.SetProperty(str(link_name), property_name, int(item_type))


def get_link_property(model, link_name: str) -> Optional[str]:
    """
    获取连接单元属性名称
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
    
    Returns:
        属性名称，失败返回 None
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
    设置连接单元频率相关属性
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        property_name: 频率相关属性名称，None 或 "None" 表示清除
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    if property_name is None:
        property_name = "None"
    return model.LinkObj.SetPropertyFD(str(link_name), property_name, int(item_type))


def get_link_property_fd(model, link_name: str) -> Optional[str]:
    """
    获取连接单元频率相关属性名称
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
    
    Returns:
        频率相关属性名称，无则返回 None
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
    获取连接单元属性信息（包括频率相关属性）
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
    
    Returns:
        (property_name, fd_property_name) 元组
    """
    prop = get_link_property(model, link_name)
    fd_prop = get_link_property_fd(model, link_name)
    return (prop, fd_prop)
