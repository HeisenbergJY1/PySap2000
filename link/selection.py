# -*- coding: utf-8 -*-
"""
selection.py - 连接单元选择相关函数

用于设置和获取连接单元的选择状态

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
    设置连接单元选择状态
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        selected: True=选中, False=取消选中
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        set_link_selected(model, "1", True)
    """
    return model.LinkObj.SetSelected(str(link_name), selected, int(item_type))


def get_link_selected(
    model,
    link_name: str
) -> bool:
    """
    获取连接单元选择状态
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
    
    Returns:
        True=选中, False=未选中
    
    Example:
        if get_link_selected(model, "1"):
            print("连接单元已选中")
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
    """选中连接单元"""
    return set_link_selected(model, link_name, True, item_type)


def deselect_link(
    model,
    link_name: str,
    item_type: LinkItemType = LinkItemType.OBJECT
) -> int:
    """取消选中连接单元"""
    return set_link_selected(model, link_name, False, item_type)


def select_links(model, link_names: List[str]) -> int:
    """批量选中连接单元"""
    ret = 0
    for name in link_names:
        result = set_link_selected(model, name, True)
        if result != 0:
            ret = result
    return ret


def deselect_links(model, link_names: List[str]) -> int:
    """批量取消选中连接单元"""
    ret = 0
    for name in link_names:
        result = set_link_selected(model, name, False)
        if result != 0:
            ret = result
    return ret


def is_link_selected(model, link_name: str) -> bool:
    """检查连接单元是否被选中"""
    return get_link_selected(model, link_name)
