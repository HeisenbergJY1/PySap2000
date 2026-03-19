# -*- coding: utf-8 -*-
"""
modifier.py - 杆件截面修改器相关函数

用于设置杆件的截面属性修改器（刚度折减等）

SAP2000 API:
- FrameObj.SetModifiers(Name, Value[], ItemType)
- FrameObj.GetModifiers(Name, Value[])
- FrameObj.DeleteModifiers(Name, ItemType)
"""

from typing import Tuple, Optional
from .enums import ItemType
from .data_classes import FrameModifierData
from PySap2000.com_helper import com_ret, com_data


def set_frame_modifiers(
    model,
    frame_name: str,
    area: float = 1.0,
    shear_2: float = 1.0,
    shear_3: float = 1.0,
    torsion: float = 1.0,
    inertia_22: float = 1.0,
    inertia_33: float = 1.0,
    mass: float = 1.0,
    weight: float = 1.0,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置杆件截面修改器
    
    修改器用于调整截面属性，常用于刚度折减。
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        area: 截面面积修改器 (A)
        shear_2: 局部2方向剪切面积修改器 (As2)
        shear_3: 局部3方向剪切面积修改器 (As3)
        torsion: 扭转常数修改器 (J)
        inertia_22: 局部2轴惯性矩修改器 (I22)
        inertia_33: 局部3轴惯性矩修改器 (I33)
        mass: 质量修改器
        weight: 重量修改器
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        # 设置 I33 修改器为 0.5 (刚度折减50%)
        set_frame_modifiers(model, "1", inertia_33=0.5)
        
        # 梁刚度折减 (I22=0.4, I33=0.4)
        set_frame_modifiers(model, "1", inertia_22=0.4, inertia_33=0.4)
        
        # 柱刚度折减 (A=0.7, I22=0.7, I33=0.7)
        set_frame_modifiers(model, "1", area=0.7, inertia_22=0.7, inertia_33=0.7)
    """
    modifiers = [area, shear_2, shear_3, torsion, inertia_22, inertia_33, mass, weight]
    result = model.FrameObj.SetModifiers(str(frame_name), modifiers, int(item_type))
    return com_ret(result)


def set_frame_modifiers_tuple(
    model,
    frame_name: str,
    modifiers: Tuple[float, ...],
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置杆件截面修改器（元组格式）
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        modifiers: 8个修改器值的元组
            (A, As2, As3, J, I22, I33, Mass, Weight)
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        set_frame_modifiers_tuple(model, "1", (1, 1, 1, 1, 1, 0.5, 1, 1))
    """
    m_list = list(modifiers)
    while len(m_list) < 8:
        m_list.append(1.0)
    return model.FrameObj.SetModifiers(str(frame_name), m_list[:8], int(item_type))


def get_frame_modifiers(
    model,
    frame_name: str
) -> Optional[FrameModifierData]:
    """
    获取杆件截面修改器
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        FrameModifierData 对象，失败返回 None
    
    Example:
        modifiers = get_frame_modifiers(model, "1")
        if modifiers:
            print(f"I33修改器: {modifiers.inertia_33}")
    """
    try:
        result = model.FrameObj.GetModifiers(str(frame_name), [0.0] * 8)
        values = com_data(result, 0)
        if values and len(values) >= 8:
            return FrameModifierData.from_tuple(str(frame_name), tuple(values))
    except Exception:
        pass
    return None


def get_frame_modifiers_tuple(
    model,
    frame_name: str
) -> Optional[Tuple[float, ...]]:
    """
    获取杆件截面修改器（元组格式）
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        8个修改器值的元组，失败返回 None
    
    Example:
        modifiers = get_frame_modifiers_tuple(model, "1")
        if modifiers:
            print(f"修改器: {modifiers}")
    """
    try:
        result = model.FrameObj.GetModifiers(str(frame_name), [0.0] * 8)
        values = com_data(result, 0)
        if values:
            return tuple(values)
    except Exception:
        pass
    return None


def delete_frame_modifiers(
    model,
    frame_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    删除杆件修改器（恢复默认值1.0）
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        delete_frame_modifiers(model, "1")
    """
    return model.FrameObj.DeleteModifiers(str(frame_name), int(item_type))
