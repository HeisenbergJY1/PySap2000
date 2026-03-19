# -*- coding: utf-8 -*-
"""
property.py - 面单元属性分配函数
对应 SAP2000 的 AreaObj.SetProperty / GetProperty

本模块用于分配属性到面单元（怎么用），而非定义属性（是什么）。
属性定义请使用 properties 模块。

Usage:
    from area import set_area_property, get_area_property
    
    # 分配属性到面单元
    set_area_property(model, "1", "SLAB1")
    
    # 获取面单元的属性
    prop_name = get_area_property(model, "1")
"""

from typing import Optional
from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


def set_area_property(
    model,
    area_name: str,
    property_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置面单元的截面属性
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        property_name: 属性名称 (必须已在 PropArea 中定义)
        item_type: 项目类型
            - OBJECT (0): 单个对象
            - GROUP (1): 组内所有对象
            - SELECTED (2): 所有选中对象
    
    Returns:
        0 表示成功，非 0 表示失败
    
    Example:
        # 设置面单元 "1" 的属性为 "SLAB1"
        set_area_property(model, "1", "SLAB1")
        
        # 设置组 "Floor" 内所有面单元的属性
        set_area_property(model, "Floor", "SLAB1", ItemType.GROUP)
        
        # 设置所有选中面单元的属性
        set_area_property(model, "", "SLAB1", ItemType.SELECTED)
    """
    return model.AreaObj.SetProperty(
        str(area_name),
        property_name,
        item_type.value
    )


def get_area_property(model, area_name: str) -> str:
    """
    获取面单元的截面属性名称
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
    
    Returns:
        属性名称
    
    Example:
        prop_name = get_area_property(model, "1")
        print(f"面单元 1 的属性: {prop_name}")
    """
    result = model.AreaObj.GetProperty(str(area_name))
    return com_data(result, 0, "") or ""


def get_area_property_type(model, area_name: str) -> int:
    """
    获取面单元的属性类型
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
    
    Returns:
        属性类型:
            1 = Shell (壳)
            2 = Plane (平面)
            3 = Asolid (轴对称实体)
    
    Example:
        prop_type = get_area_property_type(model, "1")
        if prop_type == 1:
            print("这是壳单元")
    """
    result = model.AreaObj.GetProperty(str(area_name))
    return com_data(result, 1, 0)


def set_area_material_overwrite(
    model,
    area_name: str,
    material_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置面单元的材料覆盖
    
    覆盖截面属性中定义的材料。
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        material_name: 材料名称，空字符串表示使用截面属性中的材料
        item_type: 项目类型
    
    Returns:
        0 表示成功，非 0 表示失败
    
    Example:
        # 覆盖面单元 "1" 的材料为 "C30"
        set_area_material_overwrite(model, "1", "C30")
        
        # 清除材料覆盖，使用截面属性中的材料
        set_area_material_overwrite(model, "1", "")
    """
    return model.AreaObj.SetMaterialOverwrite(
        str(area_name),
        material_name,
        item_type.value
    )


def get_area_material_overwrite(model, area_name: str) -> str:
    """
    获取面单元的材料覆盖
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
    
    Returns:
        材料名称，空字符串表示未覆盖
    
    Example:
        mat = get_area_material_overwrite(model, "1")
        if mat:
            print(f"材料覆盖: {mat}")
        else:
            print("使用截面属性中的材料")
    """
    result = model.AreaObj.GetMaterialOverwrite(str(area_name))
    return com_data(result, 0, "") or ""


def set_area_material_temperature(
    model,
    area_name: str,
    temperature: float,
    pattern_name: str = "",
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置面单元的材料温度
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        temperature: 温度值 [T]
        pattern_name: 荷载模式名称，空字符串表示无模式
        item_type: 项目类型
    
    Returns:
        0 表示成功，非 0 表示失败
    
    Example:
        # 设置面单元 "1" 的材料温度为 20°C
        set_area_material_temperature(model, "1", 20.0)
    """
    return model.AreaObj.SetMatTemp(
        str(area_name),
        temperature,
        pattern_name,
        item_type.value
    )


def get_area_material_temperature(model, area_name: str) -> tuple:
    """
    获取面单元的材料温度
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
    
    Returns:
        (temperature, pattern_name) 元组
    
    Example:
        temp, pattern = get_area_material_temperature(model, "1")
        print(f"温度: {temp}, 模式: {pattern}")
    """
    result = model.AreaObj.GetMatTemp(str(area_name))
    return (com_data(result, 0, 0.0), com_data(result, 1, "") or "")
