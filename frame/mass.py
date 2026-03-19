# -*- coding: utf-8 -*-
"""
mass.py - 杆件质量相关函数

用于设置杆件的附加质量

SAP2000 API:
- FrameObj.SetMass(Name, MassOverL, Replace, ItemType)
- FrameObj.GetMass(Name, MassOverL)
- FrameObj.DeleteMass(Name, ItemType)
"""

from typing import Optional
from .enums import ItemType
from .data_classes import FrameMassData
from PySap2000.com_helper import com_ret, com_data


def set_frame_mass(
    model,
    frame_name: str,
    mass_per_length: float,
    replace: bool = True,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置杆件单位长度质量
    
    用于添加非结构质量（如管道、设备等）。
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        mass_per_length: 单位长度质量 [M/L]
        replace: True=替换现有质量, False=叠加
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        # 设置杆件附加质量 100 kg/m
        set_frame_mass(model, "1", 100)
        
        # 叠加质量
        set_frame_mass(model, "1", 50, replace=False)
    """
    return model.FrameObj.SetMass(str(frame_name), mass_per_length, replace, int(item_type))


def get_frame_mass(
    model,
    frame_name: str
) -> Optional[float]:
    """
    获取杆件单位长度质量
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        单位长度质量 [M/L]，失败返回 None
    
    Example:
        mass = get_frame_mass(model, "1")
        if mass:
            print(f"单位长度质量: {mass}")
    """
    try:
        result = model.FrameObj.GetMass(str(frame_name), 0.0)
        val = com_data(result, 0)
        if val is not None:
            return val
    except Exception:
        pass
    return None


def get_frame_mass_data(
    model,
    frame_name: str
) -> Optional[FrameMassData]:
    """
    获取杆件质量数据对象
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        FrameMassData 对象，失败返回 None
    
    Example:
        mass_data = get_frame_mass_data(model, "1")
        if mass_data:
            print(f"质量: {mass_data.mass_per_length}")
    """
    mass = get_frame_mass(model, frame_name)
    if mass is not None:
        return FrameMassData(frame_name=str(frame_name), mass_per_length=mass)
    return None


def delete_frame_mass(
    model,
    frame_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    删除杆件附加质量
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        delete_frame_mass(model, "1")
    """
    return model.FrameObj.DeleteMass(str(frame_name), int(item_type))


def has_frame_mass(
    model,
    frame_name: str
) -> bool:
    """
    检查杆件是否有附加质量
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        True=有附加质量, False=无附加质量
    
    Example:
        if has_frame_mass(model, "1"):
            print("杆件有附加质量")
    """
    mass = get_frame_mass(model, frame_name)
    return mass is not None and mass > 0
