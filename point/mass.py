# -*- coding: utf-8 -*-
"""
mass.py - 节点质量相关函数

用于设置节点的附加质量

SAP2000 API:
- PointObj.SetMass / GetMass / DeleteMass
- PointObj.SetMassByVolume
- PointObj.SetMassByWeight
"""

from typing import Tuple, Optional
from .enums import ItemType
from .data_classes import PointMassData
from PySap2000.com_helper import com_ret, com_data


def set_point_mass(
    model,
    point_name: str,
    mass: Tuple[float, float, float, float, float, float],
    item_type: ItemType = ItemType.OBJECT,
    is_local_csys: bool = True,
    replace: bool = True
) -> int:
    """
    设置节点质量
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        mass: 质量 (M1, M2, M3, MR1, MR2, MR3)
            - M1, M2, M3: 平动质量 [M]
            - MR1, MR2, MR3: 转动惯量 [ML²]
        item_type: 项目类型
        is_local_csys: True=使用局部坐标系, False=使用全局坐标系
        replace: True=替换, False=叠加
    
    Returns:
        0 表示成功
    
    Example:
        # 设置 1000kg 的集中质量 (各方向相同)
        set_point_mass(model, "1", (1000, 1000, 1000, 0, 0, 0))
        
        # 设置不同方向的质量
        set_point_mass(model, "2", (500, 500, 1000, 100, 100, 50))
    """
    m_list = list(mass)
    while len(m_list) < 6:
        m_list.append(0.0)
    
    result = model.PointObj.SetMass(
        str(point_name), m_list[:6], item_type, is_local_csys, replace
    )
    return com_ret(result)


def get_point_mass(
    model,
    point_name: str
) -> Optional[PointMassData]:
    """
    获取节点质量
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
    
    Returns:
        PointMassData 对象，失败返回 None
    
    Example:
        mass = get_point_mass(model, "1")
        if mass:
            print(f"质量: {mass.m1}, {mass.m2}, {mass.m3}")
    """
    try:
        result = model.PointObj.GetMass(str(point_name))
        m_values = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and m_values and len(m_values) >= 6:
            return PointMassData(
                point_name=str(point_name),
                m1=m_values[0],
                m2=m_values[1],
                m3=m_values[2],
                mr1=m_values[3],
                mr2=m_values[4],
                mr3=m_values[5]
            )
    except Exception:
        pass
    return None


def delete_point_mass(
    model,
    point_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    删除节点质量
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        item_type: 项目类型
    
    Returns:
        0 表示成功
    """
    return model.PointObj.DeleteMass(str(point_name), item_type)


def set_point_mass_by_weight(
    model,
    point_name: str,
    weight: float,
    item_type: ItemType = ItemType.OBJECT,
    is_local_csys: bool = True,
    replace: bool = True
) -> int:
    """
    通过重量设置节点质量
    
    程序会自动将重量转换为质量 (除以重力加速度)。
    质量在三个平动方向相同，转动惯量为零。
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        weight: 重量 [F]
        item_type: 项目类型
        is_local_csys: 是否使用局部坐标系
        replace: 是否替换
    
    Returns:
        0 表示成功
    
    Example:
        # 设置 10kN 的重量 (程序自动转换为质量)
        set_point_mass_by_weight(model, "1", 10.0)
    """
    return model.PointObj.SetMassByWeight(
        str(point_name), weight, item_type, is_local_csys, replace
    )


def set_point_mass_by_volume(
    model,
    point_name: str,
    volume: float,
    material_name: str,
    item_type: ItemType = ItemType.OBJECT,
    is_local_csys: bool = True,
    replace: bool = True
) -> int:
    """
    通过体积和材料设置节点质量
    
    程序会根据材料密度和体积计算质量。
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        volume: 体积 [L³]
        material_name: 材料名称 (必须已定义)
        item_type: 项目类型
        is_local_csys: 是否使用局部坐标系
        replace: 是否替换
    
    Returns:
        0 表示成功
    
    Example:
        # 设置 1m³ 混凝土的质量
        set_point_mass_by_volume(model, "1", 1.0, "C30")
    """
    return model.PointObj.SetMassByVolume(
        str(point_name), volume, material_name, item_type, is_local_csys, replace
    )
