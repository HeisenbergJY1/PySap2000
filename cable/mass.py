# -*- coding: utf-8 -*-
"""
mass.py - Cable 质量指派

SAP2000 API:
- CableObj.SetMass(Name, MassOverL, Replace, ItemType)
- CableObj.GetMass(Name, MassOverL)
- CableObj.DeleteMass(Name, ItemType)
"""

from typing import Optional
from .modifier import CableItemType
from PySap2000.com_helper import com_data


def set_cable_mass(
    model,
    cable_name: str,
    mass_per_length: float,
    replace: bool = False,
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    设置 Cable 附加质量
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
        mass_per_length: 单位长度质量 [M/L]
        replace: True=替换现有质量, False=叠加
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        set_cable_mass(model, "1", 0.001)
    """
    return model.CableObj.SetMass(str(cable_name), mass_per_length, replace, int(item_type))


def get_cable_mass(model, cable_name: str) -> Optional[float]:
    """
    获取 Cable 附加质量
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
    
    Returns:
        单位长度质量 [M/L]，失败返回 None
    
    Example:
        mass = get_cable_mass(model, "1")
    """
    try:
        result = model.CableObj.GetMass(str(cable_name), 0.0)
        return com_data(result, 0)
    except Exception:
        pass
    return None


def delete_cable_mass(
    model,
    cable_name: str,
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    删除 Cable 附加质量
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.CableObj.DeleteMass(str(cable_name), int(item_type))
