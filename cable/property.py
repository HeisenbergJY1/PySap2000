# -*- coding: utf-8 -*-
"""
property.py - Cable 属性分配函数
对应 SAP2000 的 CableObj.SetProperty / GetProperty

本模块用于分配属性到 Cable（怎么用），而非定义属性（是什么）。
属性定义请使用 properties 模块。

包含:
- 截面分配: set/get_cable_section
- 材料覆盖: set/get_cable_material_overwrite
- 材料温度: set/get_cable_material_temp

Usage:
    from cable import set_cable_section, get_cable_section
    
    # 分配截面到 Cable
    set_cable_section(model, "1", "Cable1")
    
    # 获取 Cable 的截面
    section_name = get_cable_section(model, "1")
"""

from typing import Tuple
from .modifier import CableItemType
from PySap2000.com_helper import com_ret, com_data


# =============================================================================
# 截面分配
# =============================================================================

def set_cable_section(
    model,
    cable_name: str,
    section_name: str,
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    设置 Cable 的截面属性
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
        section_name: 截面名称 (必须已在 PropCable 中定义)
        item_type: 项目类型
            - OBJECT (0): 单个对象
            - GROUP (1): 组内所有对象
            - SELECTED_OBJECTS (2): 所有选中对象
    
    Returns:
        0 表示成功，非 0 表示失败
    
    Example:
        # 设置 Cable "1" 的截面为 "Cable1"
        set_cable_section(model, "1", "Cable1")
        
        # 设置组 "Cables" 内所有 Cable 的截面
        set_cable_section(model, "Cables", "Cable1", CableItemType.GROUP)
    """
    return model.CableObj.SetProperty(
        str(cable_name),
        section_name,
        int(item_type)
    )


def get_cable_section(model, cable_name: str) -> str:
    """
    获取 Cable 的截面属性名称
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
    
    Returns:
        截面名称
    """
    result = model.CableObj.GetProperty(str(cable_name))
    return com_data(result, 0, "") or ""



def get_cable_section_list(model) -> list:
    """
    获取所有 Cable 截面名称列表
    
    Args:
        model: SapModel 对象
    
    Returns:
        截面名称列表
    
    Example:
        sections = get_cable_section_list(model)
        for name in sections:
            print(name)
    """
    result = model.PropCable.GetNameList(0, [])
    ret = com_ret(result)
    if ret == 0:
        names = com_data(result, 1)
        return list(names) if names else []
    return []


# =============================================================================
# 材料覆盖
# =============================================================================

def set_cable_material_overwrite(
    model,
    cable_name: str,
    material_name: str,
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    设置 Cable 的材料覆盖
    
    覆盖截面属性中定义的材料。
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
        material_name: 材料名称，空字符串表示使用截面属性中的材料
        item_type: 项目类型
    
    Returns:
        0 表示成功，非 0 表示失败
    
    Example:
        # 覆盖 Cable "1" 的材料为 "A416Gr270"
        set_cable_material_overwrite(model, "1", "A416Gr270")
        
        # 清除材料覆盖，使用截面属性中的材料
        set_cable_material_overwrite(model, "1", "")
    """
    return model.CableObj.SetMaterialOverwrite(
        str(cable_name),
        material_name,
        int(item_type)
    )


def get_cable_material_overwrite(model, cable_name: str) -> str:
    """
    获取 Cable 的材料覆盖
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
    
    Returns:
        材料名称，空字符串表示未覆盖
    
    Example:
        mat = get_cable_material_overwrite(model, "1")
        if mat:
            print(f"材料覆盖: {mat}")
        else:
            print("使用截面属性中的材料")
    """
    result = model.CableObj.GetMaterialOverwrite(str(cable_name))
    return com_data(result, 0, "") or ""


# =============================================================================
# 材料温度
# =============================================================================

def set_cable_material_temp(
    model,
    cable_name: str,
    temperature: float,
    pattern_name: str = "",
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    设置 Cable 的材料温度
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
        temperature: 温度值 [T]
        pattern_name: 荷载模式名称，空字符串表示无模式
        item_type: 项目类型
    
    Returns:
        0 表示成功，非 0 表示失败
    
    Example:
        # 设置 Cable "1" 的材料温度为 20°C
        set_cable_material_temp(model, "1", 20.0)
    """
    return model.CableObj.SetMatTemp(
        str(cable_name),
        temperature,
        pattern_name,
        int(item_type)
    )


def get_cable_material_temp(model, cable_name: str) -> Tuple[float, str]:
    """
    获取 Cable 的材料温度
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
    
    Returns:
        (temperature, pattern_name) 元组
    
    Example:
        temp, pattern = get_cable_material_temp(model, "1")
        print(f"温度: {temp}, 模式: {pattern}")
    """
    result = model.CableObj.GetMatTemp(str(cable_name))
    temp = com_data(result, 0)
    pattern = com_data(result, 1)
    if temp is not None:
        return (temp, pattern or "")
    return (0.0, "")
