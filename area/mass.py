# -*- coding: utf-8 -*-
"""
mass.py - 面单元质量函数
对应 SAP2000 的 AreaObj 质量相关 API
"""

from typing import Optional

from .enums import ItemType
from .data_classes import AreaMassData
from PySap2000.com_helper import com_ret, com_data


def set_area_mass(
    model,
    area_name: str,
    mass_per_area: float,
    replace: bool = True,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置面单元附加质量
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        mass_per_area: 单位面积质量
        replace: 是否替换现有质量 (True=替换, False=叠加)
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
        
    Example:
        # 设置面单元 "1" 的附加质量为 100 kg/m²
        set_area_mass(model, "1", 100.0)
    """
    return model.AreaObj.SetMass(str(area_name), mass_per_area, replace, int(item_type))


def get_area_mass(
    model,
    area_name: str
) -> Optional[float]:
    """
    获取面单元附加质量
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        单位面积质量，失败返回 None
        
    Example:
        mass = get_area_mass(model, "1")
        if mass is not None:
            print(f"附加质量: {mass} kg/m²")
    """
    try:
        result = model.AreaObj.GetMass(str(area_name), 0.0)
        mass = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0:
            return mass
    except Exception:
        pass
    return None


def get_area_mass_data(
    model,
    area_name: str
) -> Optional[AreaMassData]:
    """
    获取面单元质量数据对象
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        AreaMassData 对象，失败返回 None
    """
    mass = get_area_mass(model, area_name)
    if mass is not None:
        return AreaMassData(area_name=area_name, mass_per_area=mass)
    return None


def delete_area_mass(
    model,
    area_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    删除面单元附加质量
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    return model.AreaObj.DeleteMass(str(area_name), int(item_type))


def has_area_mass(
    model,
    area_name: str
) -> bool:
    """
    检查面单元是否有附加质量
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        True 表示有附加质量，False 表示没有
    """
    mass = get_area_mass(model, area_name)
    return mass is not None and mass > 0.0
