# -*- coding: utf-8 -*-
"""
group.py - Cable 组指派

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
    将 Cable 添加到组或从组中移除
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
        group_name: 组名称
        remove: False=添加到组, True=从组移除
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        # 添加到组
        set_cable_group(model, "1", "CableGroup")
        
        # 从组移除
        set_cable_group(model, "1", "CableGroup", remove=True)
    """
    return model.CableObj.SetGroupAssign(str(cable_name), group_name, remove, int(item_type))


def get_cable_groups(model, cable_name: str) -> List[str]:
    """
    获取 Cable 所属的组列表
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
    
    Returns:
        组名称列表
    
    Example:
        groups = get_cable_groups(model, "1")
        print(f"Cable 1 属于: {groups}")
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
