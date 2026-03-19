# -*- coding: utf-8 -*-
"""
group.py - 杆件组分配相关函数

用于设置杆件的组分配

SAP2000 API:
- FrameObj.SetGroupAssign(Name, GroupName, Remove, ItemType)
- FrameObj.GetGroupAssign(Name, NumberGroups, Groups[])
"""

from typing import List, Optional
from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


def set_frame_group(
    model,
    frame_name: str,
    group_name: str,
    remove: bool = False,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置杆件组分配
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        group_name: 组名称 (必须已存在)
        remove: False=添加到组, True=从组移除
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        # 将杆件添加到组
        set_frame_group(model, "1", "Beams")
        
        # 从组移除杆件
        set_frame_group(model, "1", "Beams", remove=True)
    """
    return model.FrameObj.SetGroupAssign(str(frame_name), group_name, remove, int(item_type))


def add_frame_to_group(
    model,
    frame_name: str,
    group_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    将杆件添加到组
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        group_name: 组名称 (必须已存在)
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        add_frame_to_group(model, "1", "Beams")
    """
    return set_frame_group(model, frame_name, group_name, False, item_type)


def remove_frame_from_group(
    model,
    frame_name: str,
    group_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    从组移除杆件
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        group_name: 组名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        remove_frame_from_group(model, "1", "Beams")
    """
    return set_frame_group(model, frame_name, group_name, True, item_type)


def get_frame_groups(
    model,
    frame_name: str
) -> Optional[List[str]]:
    """
    获取杆件所属组
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        组名称列表，失败返回 None
    
    Example:
        groups = get_frame_groups(model, "1")
        if groups:
            print(f"杆件所属组: {groups}")
    """
    try:
        result = model.FrameObj.GetGroupAssign(str(frame_name), 0, [])
        num_groups = com_data(result, 0, 0)
        groups = com_data(result, 1)
        if num_groups > 0 and groups:
            return list(groups)
    except Exception:
        pass
    return None


def is_frame_in_group(
    model,
    frame_name: str,
    group_name: str
) -> bool:
    """
    检查杆件是否在指定组中
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        group_name: 组名称
    
    Returns:
        True=在组中, False=不在组中
    
    Example:
        if is_frame_in_group(model, "1", "Beams"):
            print("杆件在 Beams 组中")
    """
    groups = get_frame_groups(model, frame_name)
    if groups:
        return group_name in groups
    return False


def add_frames_to_group(
    model,
    frame_names: List[str],
    group_name: str
) -> int:
    """
    批量将杆件添加到组
    
    Args:
        model: SapModel 对象
        frame_names: 杆件名称列表
        group_name: 组名称 (必须已存在)
    
    Returns:
        0 表示全部成功
    
    Example:
        add_frames_to_group(model, ["1", "2", "3"], "Beams")
    """
    ret = 0
    for name in frame_names:
        result = add_frame_to_group(model, name, group_name)
        if result != 0:
            ret = result
    return ret


def remove_frames_from_group(
    model,
    frame_names: List[str],
    group_name: str
) -> int:
    """
    批量从组移除杆件
    
    Args:
        model: SapModel 对象
        frame_names: 杆件名称列表
        group_name: 组名称
    
    Returns:
        0 表示全部成功
    
    Example:
        remove_frames_from_group(model, ["1", "2", "3"], "Beams")
    """
    ret = 0
    for name in frame_names:
        result = remove_frame_from_group(model, name, group_name)
        if result != 0:
            ret = result
    return ret
