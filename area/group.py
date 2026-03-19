# -*- coding: utf-8 -*-
"""
group.py - 面单元组分配函数
对应 SAP2000 的 AreaObj 组分配相关 API

SAP2000 API:
- AreaObj.SetGroupAssign(Name, GroupName, Remove, ItemType)
- AreaObj.GetGroupAssign(Name, NumberGroups, Groups[])
"""

from typing import List, Optional

from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


def set_area_group(
    model,
    area_name: str,
    group_name: str,
    remove: bool = False,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置面单元组分配
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        group_name: 组名称 (必须已存在)
        remove: False=添加到组, True=从组移除
        item_type: 操作范围
    
    Returns:
        0 表示成功，非 0 表示失败
    
    Example:
        # 将面单元添加到组
        set_area_group(model, "1", "Slabs")
        
        # 从组移除面单元
        set_area_group(model, "1", "Slabs", remove=True)
    """
    return model.AreaObj.SetGroupAssign(str(area_name), group_name, remove, int(item_type))


def add_area_to_group(
    model,
    area_name: str,
    group_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    将面单元添加到组
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        group_name: 组名称 (必须已存在)
        item_type: 操作范围
    
    Returns:
        0 表示成功，非 0 表示失败
    
    Example:
        add_area_to_group(model, "1", "Slabs")
    """
    return set_area_group(model, area_name, group_name, False, item_type)


def remove_area_from_group(
    model,
    area_name: str,
    group_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    从组移除面单元
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        group_name: 组名称
        item_type: 操作范围
    
    Returns:
        0 表示成功，非 0 表示失败
    
    Example:
        remove_area_from_group(model, "1", "Slabs")
    """
    return set_area_group(model, area_name, group_name, True, item_type)


def get_area_groups(
    model,
    area_name: str
) -> Optional[List[str]]:
    """
    获取面单元所属组
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
    
    Returns:
        组名称列表，失败返回 None
    
    Example:
        groups = get_area_groups(model, "1")
        if groups:
            print(f"面单元所属组: {groups}")
    """
    try:
        result = model.AreaObj.GetGroupAssign(str(area_name), 0, [])
        num_groups = com_data(result, 0, 0)
        groups = com_data(result, 1)
        if num_groups > 0 and groups:
            return list(groups)
    except Exception:
        pass
    return None


def is_area_in_group(
    model,
    area_name: str,
    group_name: str
) -> bool:
    """
    检查面单元是否在指定组中
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        group_name: 组名称
    
    Returns:
        True=在组中, False=不在组中
    
    Example:
        if is_area_in_group(model, "1", "Slabs"):
            print("面单元在 Slabs 组中")
    """
    groups = get_area_groups(model, area_name)
    if groups:
        return group_name in groups
    return False


def add_areas_to_group(
    model,
    area_names: List[str],
    group_name: str
) -> int:
    """
    批量将面单元添加到组
    
    Args:
        model: SapModel 对象
        area_names: 面单元名称列表
        group_name: 组名称 (必须已存在)
    
    Returns:
        0 表示全部成功，非 0 表示有失败
    
    Example:
        add_areas_to_group(model, ["1", "2", "3"], "Slabs")
    """
    ret = 0
    for name in area_names:
        result = add_area_to_group(model, name, group_name)
        if result != 0:
            ret = result
    return ret


def remove_areas_from_group(
    model,
    area_names: List[str],
    group_name: str
) -> int:
    """
    批量从组移除面单元
    
    Args:
        model: SapModel 对象
        area_names: 面单元名称列表
        group_name: 组名称
    
    Returns:
        0 表示全部成功，非 0 表示有失败
    
    Example:
        remove_areas_from_group(model, ["1", "2", "3"], "Slabs")
    """
    ret = 0
    for name in area_names:
        result = remove_area_from_group(model, name, group_name)
        if result != 0:
            ret = result
    return ret
