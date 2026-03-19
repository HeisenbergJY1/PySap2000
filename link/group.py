# -*- coding: utf-8 -*-
"""
group.py - 连接单元组分配相关函数

用于设置连接单元的组分配

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
    设置连接单元组分配
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        group_name: 组名称 (必须已存在)
        remove: False=添加到组, True=从组移除
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
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
    """将连接单元添加到组"""
    return set_link_group(model, link_name, group_name, False, item_type)


def remove_link_from_group(
    model,
    link_name: str,
    group_name: str,
    item_type: LinkItemType = LinkItemType.OBJECT
) -> int:
    """从组移除连接单元"""
    return set_link_group(model, link_name, group_name, True, item_type)


def get_link_groups(model, link_name: str) -> Optional[List[str]]:
    """
    获取连接单元所属组
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
    
    Returns:
        组名称列表，失败返回 None
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
    """检查连接单元是否在指定组中"""
    groups = get_link_groups(model, link_name)
    if groups:
        return group_name in groups
    return False


def add_links_to_group(model, link_names: List[str], group_name: str) -> int:
    """批量将连接单元添加到组"""
    ret = 0
    for name in link_names:
        result = add_link_to_group(model, name, group_name)
        if result != 0:
            ret = result
    return ret


def remove_links_from_group(model, link_names: List[str], group_name: str) -> int:
    """批量从组移除连接单元"""
    ret = 0
    for name in link_names:
        result = remove_link_from_group(model, name, group_name)
        if result != 0:
            ret = result
    return ret
