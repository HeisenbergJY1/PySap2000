# -*- coding: utf-8 -*-
"""
modifier.py - 面单元修改器函数
对应 SAP2000 的 AreaObj 修改器相关 API
"""

from typing import Optional, List, Tuple

from .enums import ItemType
from .data_classes import AreaModifierData
from PySap2000.com_helper import com_ret, com_data


def set_area_modifiers(
    model,
    area_name: str,
    modifiers: List[float],
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置面单元修改系数
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        modifiers: 10个修改系数值
            [f11, f22, f12, m11, m22, m12, v13, v23, mass, weight]
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
        
    Example:
        # 设置面单元 "1" 的修改系数 (弯曲刚度折减为 0.7)
        modifiers = [1.0, 1.0, 1.0, 0.7, 0.7, 0.7, 1.0, 1.0, 1.0, 1.0]
        set_area_modifiers(model, "1", modifiers)
    """
    # 确保有10个值
    mod_list = list(modifiers)
    while len(mod_list) < 10:
        mod_list.append(1.0)
    
    result = model.AreaObj.SetModifiers(str(area_name), mod_list[:10], int(item_type))
    return com_ret(result)


def set_area_modifiers_tuple(
    model,
    area_name: str,
    modifiers: Tuple[float, ...],
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    使用元组设置面单元修改系数
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        modifiers: 10个修改系数值的元组
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    return set_area_modifiers(model, area_name, list(modifiers), item_type)


def set_area_modifiers_data(
    model,
    area_name: str,
    data: AreaModifierData,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    使用数据对象设置面单元修改系数
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        data: AreaModifierData 对象
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
        
    Example:
        data = AreaModifierData(m11=0.7, m22=0.7, m12=0.7)
        set_area_modifiers_data(model, "1", data)
    """
    return model.AreaObj.SetModifiers(str(area_name), data.to_list(), int(item_type))


def get_area_modifiers(
    model,
    area_name: str
) -> Optional[AreaModifierData]:
    """
    获取面单元修改系数数据对象
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        AreaModifierData 对象，失败返回 None
        
    Example:
        data = get_area_modifiers(model, "1")
        if data:
            print(f"弯曲刚度 m11: {data.m11}")
    """
    modifiers = get_area_modifiers_tuple(model, area_name)
    if modifiers:
        return AreaModifierData.from_list(list(modifiers))
    return None


def get_area_modifiers_tuple(
    model,
    area_name: str
) -> Optional[Tuple[float, ...]]:
    """
    获取面单元修改系数元组
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        10个修改系数值的元组，失败返回 None
        
    Example:
        modifiers = get_area_modifiers_tuple(model, "1")
        if modifiers:
            print(f"膜刚度 f11: {modifiers[0]}")
            print(f"弯曲刚度 m11: {modifiers[3]}")
    """
    try:
        result = model.AreaObj.GetModifiers(str(area_name), [])
        modifiers = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and modifiers:
            return tuple(modifiers)
    except Exception:
        pass
    return None


def delete_area_modifiers(
    model,
    area_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    删除面单元修改系数 (恢复默认值)
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    return model.AreaObj.DeleteModifiers(str(area_name), int(item_type))
