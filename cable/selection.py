# -*- coding: utf-8 -*-
"""
selection.py - Cable 选择状态

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
    设置 Cable 选择状态
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
        selected: True=选中, False=取消选中
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        # 选中单个 Cable
        set_cable_selected(model, "1", True)
        
        # 选中所有 Cable
        set_cable_selected(model, "ALL", True, CableItemType.GROUP)
    """
    return model.CableObj.SetSelected(str(cable_name), selected, int(item_type))


def get_cable_selected(model, cable_name: str) -> Optional[bool]:
    """
    获取 Cable 选择状态
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
    
    Returns:
        True=选中, False=未选中, None=失败
    
    Example:
        if get_cable_selected(model, "1"):
            print("Cable 1 已选中")
    """
    try:
        result = model.CableObj.GetSelected(str(cable_name), False)
        return com_data(result, 0)
    except Exception:
        pass
    return None


def get_selected_cables(model) -> List[str]:
    """
    获取所有选中的 Cable 名称列表
    
    Args:
        model: SapModel 对象
    
    Returns:
        选中的 Cable 名称列表
    
    Example:
        selected = get_selected_cables(model)
        print(f"选中了 {len(selected)} 个 Cable")
    """
    selected = []
    try:
        # 获取所有 Cable
        result = model.CableObj.GetNameList(0, [])
        names = com_data(result, 1)
        if names:
                for name in names:
                    if get_cable_selected(model, name):
                        selected.append(name)
    except Exception:
        pass
    return selected
