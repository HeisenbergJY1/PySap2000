# -*- coding: utf-8 -*-
"""
selection.py - 面单元选择函数
对应 SAP2000 的 AreaObj 选择相关 API
"""

from typing import List

from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


def set_area_selected(
    model,
    area_name: str,
    selected: bool = True,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置面单元选择状态
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        selected: 是否选中
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
        
    Example:
        # 选中面单元 "1"
        set_area_selected(model, "1", True)
        
        # 取消选中面单元 "1"
        set_area_selected(model, "1", False)
    """
    return model.AreaObj.SetSelected(str(area_name), selected, int(item_type))


def get_area_selected(
    model,
    area_name: str
) -> bool:
    """
    获取面单元选择状态
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        True 表示选中，False 表示未选中
        
    Example:
        is_selected = get_area_selected(model, "1")
        print(f"面单元 1 {'已选中' if is_selected else '未选中'}")
    """
    try:
        result = model.AreaObj.GetSelected(str(area_name), False)
        val = com_data(result, 0)
        if val is not None:
            return val
    except Exception:
        pass
    return False


def select_area(
    model,
    area_name: str
) -> int:
    """
    选中面单元
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        0 表示成功，非 0 表示失败
        
    Example:
        select_area(model, "1")
    """
    return set_area_selected(model, area_name, True)


def deselect_area(
    model,
    area_name: str
) -> int:
    """
    取消选中面单元
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        0 表示成功，非 0 表示失败
        
    Example:
        deselect_area(model, "1")
    """
    return set_area_selected(model, area_name, False)


def select_areas(
    model,
    area_names: List[str]
) -> int:
    """
    批量选中面单元
    
    Args:
        model: SapModel 对象
        area_names: 面单元名称列表
        
    Returns:
        0 表示全部成功，非 0 表示有失败
        
    Example:
        select_areas(model, ["1", "2", "3"])
    """
    ret = 0
    for name in area_names:
        result = set_area_selected(model, name, True)
        if result != 0:
            ret = result
    return ret


def deselect_areas(
    model,
    area_names: List[str]
) -> int:
    """
    批量取消选中面单元
    
    Args:
        model: SapModel 对象
        area_names: 面单元名称列表
        
    Returns:
        0 表示全部成功，非 0 表示有失败
        
    Example:
        deselect_areas(model, ["1", "2", "3"])
    """
    ret = 0
    for name in area_names:
        result = set_area_selected(model, name, False)
        if result != 0:
            ret = result
    return ret


def is_area_selected(
    model,
    area_name: str
) -> bool:
    """
    检查面单元是否选中
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        True 表示选中，False 表示未选中
    """
    return get_area_selected(model, area_name)
