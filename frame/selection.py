# -*- coding: utf-8 -*-
"""
selection.py - 杆件选择相关函数

用于设置和获取杆件的选择状态

SAP2000 API:
- FrameObj.SetSelected(Name, Selected, ItemType)
- FrameObj.GetSelected(Name, Selected)
"""

from typing import List
from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


def set_frame_selected(
    model,
    frame_name: str,
    selected: bool = True,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置杆件选择状态
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        selected: True=选中, False=取消选中
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        # 选中杆件
        set_frame_selected(model, "1", True)
        
        # 取消选中
        set_frame_selected(model, "1", False)
    """
    return model.FrameObj.SetSelected(str(frame_name), selected, int(item_type))


def get_frame_selected(
    model,
    frame_name: str
) -> bool:
    """
    获取杆件选择状态
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        True=选中, False=未选中
    
    Example:
        if get_frame_selected(model, "1"):
            print("杆件已选中")
    """
    try:
        result = model.FrameObj.GetSelected(str(frame_name), False)
        val = com_data(result, 0)
        if val is not None:
            return val
    except Exception:
        pass
    return False


def select_frame(
    model,
    frame_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    选中杆件
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        select_frame(model, "1")
    """
    return set_frame_selected(model, frame_name, True, item_type)


def deselect_frame(
    model,
    frame_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    取消选中杆件
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        deselect_frame(model, "1")
    """
    return set_frame_selected(model, frame_name, False, item_type)


def select_frames(
    model,
    frame_names: List[str]
) -> int:
    """
    批量选中杆件
    
    Args:
        model: SapModel 对象
        frame_names: 杆件名称列表
    
    Returns:
        0 表示全部成功
    
    Example:
        select_frames(model, ["1", "2", "3"])
    """
    ret = 0
    for name in frame_names:
        result = set_frame_selected(model, name, True)
        if result != 0:
            ret = result
    return ret


def deselect_frames(
    model,
    frame_names: List[str]
) -> int:
    """
    批量取消选中杆件
    
    Args:
        model: SapModel 对象
        frame_names: 杆件名称列表
    
    Returns:
        0 表示全部成功
    
    Example:
        deselect_frames(model, ["1", "2", "3"])
    """
    ret = 0
    for name in frame_names:
        result = set_frame_selected(model, name, False)
        if result != 0:
            ret = result
    return ret


def is_frame_selected(
    model,
    frame_name: str
) -> bool:
    """
    检查杆件是否被选中
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        True=选中, False=未选中
    
    Example:
        if is_frame_selected(model, "1"):
            print("杆件已选中")
    """
    return get_frame_selected(model, frame_name)
