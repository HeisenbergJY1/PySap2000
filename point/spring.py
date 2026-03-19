# -*- coding: utf-8 -*-
"""
spring.py - 节点弹簧相关函数

用于设置节点的弹簧刚度

SAP2000 API:
- PointObj.SetSpring(Name, k, ItemType, IsLocalCSys, Replace)
- PointObj.GetSpring(Name)
- PointObj.DeleteSpring(Name, ItemType)
- PointObj.SetSpringCoupled(Name, k, ItemType, IsLocalCSys, Replace)
- PointObj.GetSpringCoupled(Name)
"""

from typing import Tuple, Optional, List
from .enums import ItemType
from .data_classes import PointSpringData
from PySap2000.com_helper import com_ret, com_data


def set_point_spring(
    model,
    point_name: str,
    k: Tuple[float, float, float, float, float, float],
    item_type: ItemType = ItemType.OBJECT,
    is_local_csys: bool = False,
    replace: bool = True
) -> int:
    """
    设置节点弹簧刚度
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        k: 弹簧刚度 (U1, U2, U3, R1, R2, R3)
            - U1, U2, U3: 平动刚度 [F/L]
            - R1, R2, R3: 转动刚度 [FL/rad]
        item_type: 项目类型
        is_local_csys: True=使用局部坐标系, False=使用全局坐标系
        replace: True=替换现有弹簧, False=叠加到现有弹簧
    
    Returns:
        0 表示成功
    
    Example:
        # 设置竖向弹簧刚度 1000 kN/m
        set_point_spring(model, "1", (0, 0, 1000, 0, 0, 0))
        
        # 设置全部 6 个自由度的弹簧
        set_point_spring(model, "2", (100, 100, 1000, 50, 50, 50))
    """
    k_list = list(k)
    while len(k_list) < 6:
        k_list.append(0.0)
    
    result = model.PointObj.SetSpring(
        str(point_name), k_list[:6], item_type, is_local_csys, replace
    )
    return com_ret(result)


def get_point_spring(
    model,
    point_name: str
) -> Optional[PointSpringData]:
    """
    获取节点弹簧刚度
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
    
    Returns:
        PointSpringData 对象，失败返回 None
    
    Example:
        spring = get_point_spring(model, "1")
        if spring:
            print(f"竖向刚度: {spring.u3}")
    """
    try:
        result = model.PointObj.GetSpring(str(point_name))
        k_values = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and k_values and len(k_values) >= 6:
            return PointSpringData(
                point_name=str(point_name),
                u1=k_values[0],
                u2=k_values[1],
                u3=k_values[2],
                r1=k_values[3],
                r2=k_values[4],
                r3=k_values[5]
            )
    except Exception:
        pass
    return None


def delete_point_spring(
    model,
    point_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    删除节点弹簧
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        item_type: 项目类型
    
    Returns:
        0 表示成功
    
    Example:
        delete_point_spring(model, "1")
    """
    return model.PointObj.DeleteSpring(str(point_name), item_type)


def set_point_spring_coupled(
    model,
    point_name: str,
    k: Tuple[float, ...],
    item_type: ItemType = ItemType.OBJECT,
    is_local_csys: bool = False,
    replace: bool = True
) -> int:
    """
    设置节点耦合弹簧刚度 (21个刚度系数)
    
    耦合弹簧考虑各自由度之间的耦合效应。
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        k: 21个弹簧刚度系数 (对称刚度矩阵的上三角)
            k[0] = U1-U1
            k[1] = U1-U2, k[2] = U2-U2
            k[3] = U1-U3, k[4] = U2-U3, k[5] = U3-U3
            ... (共21个)
        item_type: 项目类型
        is_local_csys: 是否使用局部坐标系
        replace: 是否替换现有弹簧
    
    Returns:
        0 表示成功
    """
    k_list = list(k)
    while len(k_list) < 21:
        k_list.append(0.0)
    
    return model.PointObj.SetSpringCoupled(
        str(point_name), k_list[:21], item_type, is_local_csys, replace
    )


def get_point_spring_coupled(
    model,
    point_name: str
) -> Optional[Tuple[float, ...]]:
    """
    获取节点耦合弹簧刚度
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
    
    Returns:
        21个刚度系数的元组，失败返回 None
    """
    try:
        result = model.PointObj.GetSpringCoupled(str(point_name))
        k_values = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and k_values:
            return tuple(k_values)
    except Exception:
        pass
    return None


def is_point_spring_coupled(
    model,
    point_name: str
) -> bool:
    """
    检查节点是否有耦合弹簧
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
    
    Returns:
        True=有耦合弹簧, False=没有
    """
    try:
        result = model.PointObj.IsSpringCoupled(str(point_name), False)
        value = com_data(result, 0)
        if value is not None:
            return value
    except Exception:
        pass
    return False
