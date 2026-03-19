# -*- coding: utf-8 -*-
"""
edge_constraint.py - 面单元边缘约束函数
对应 SAP2000 的 AreaObj 边缘约束相关 API
"""

from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


def set_area_edge_constraint(
    model,
    area_name: str,
    constraint_exists: bool,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置面单元边缘约束
    
    边缘约束用于确保相邻面单元在边缘处的位移兼容性。
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        constraint_exists: 是否存在边缘约束
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
        
    Example:
        # 启用边缘约束
        set_area_edge_constraint(model, "1", True)
        
        # 禁用边缘约束
        set_area_edge_constraint(model, "1", False)
    """
    return model.AreaObj.SetEdgeConstraint(str(area_name), constraint_exists, int(item_type))


def get_area_edge_constraint(
    model,
    area_name: str
) -> bool:
    """
    获取面单元边缘约束状态
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        True 表示存在边缘约束，False 表示不存在
        
    Example:
        has_constraint = get_area_edge_constraint(model, "1")
        print(f"边缘约束: {'启用' if has_constraint else '禁用'}")
    """
    try:
        result = model.AreaObj.GetEdgeConstraint(str(area_name), False)
        val = com_data(result, 0)
        if val is not None:
            return val
    except Exception:
        pass
    return False


def enable_area_edge_constraint(
    model,
    area_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    启用面单元边缘约束
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    return set_area_edge_constraint(model, area_name, True, item_type)


def disable_area_edge_constraint(
    model,
    area_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    禁用面单元边缘约束
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    return set_area_edge_constraint(model, area_name, False, item_type)


def has_area_edge_constraint(
    model,
    area_name: str
) -> bool:
    """
    检查面单元是否有边缘约束
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        True 表示有边缘约束，False 表示无
    """
    return get_area_edge_constraint(model, area_name)
