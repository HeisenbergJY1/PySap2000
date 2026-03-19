# -*- coding: utf-8 -*-
"""
constraint.py - 节点约束相关函数

用于设置节点的刚性约束 (如刚性隔板 Diaphragm)

SAP2000 API:
- PointObj.SetConstraint / GetConstraint / DeleteConstraint

注意: 这里的 Constraint 是指 SAP2000 中的 Joint Constraint (如 Diaphragm, Body 等)，
不是支座约束 (Restraint)。
"""

from typing import List
from .enums import ItemType
from .data_classes import PointConstraintAssignment
from PySap2000.com_helper import com_ret, com_data


def set_point_constraint(
    model,
    point_name: str,
    constraint_name: str,
    item_type: ItemType = ItemType.OBJECT,
    replace: bool = True
) -> int:
    """
    设置节点约束 (如刚性隔板)
    
    将节点分配到已定义的约束中。约束必须先通过 SAP2000 界面或 API 定义。
    
    常见约束类型:
    - Diaphragm: 刚性隔板，约束平面内平动和转动
    - Body: 刚体约束，约束所有自由度
    - Equal: 等位移约束
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        constraint_name: 约束名称 (必须已定义)
        item_type: 项目类型
        replace: True=替换所有现有约束, False=添加到现有约束
    
    Returns:
        0 表示成功
    
    Example:
        # 将节点分配到刚性隔板 "Diaph1"
        set_point_constraint(model, "1", "Diaph1")
        
        # 将多个节点分配到同一隔板
        for name in ["1", "2", "3", "4"]:
            set_point_constraint(model, name, "Diaph1")
    """
    return model.PointObj.SetConstraint(
        str(point_name), constraint_name, item_type, replace
    )


def get_point_constraint(
    model,
    point_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> List[PointConstraintAssignment]:
    """
    获取节点约束分配
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        item_type: 项目类型
    
    Returns:
        PointConstraintAssignment 对象列表
    
    Example:
        constraints = get_point_constraint(model, "1")
        for c in constraints:
            print(f"节点 {c.point_name} 属于约束 {c.constraint_name}")
    """
    assignments = []
    try:
        result = model.PointObj.GetConstraint(
            str(point_name), 0, [], [], item_type
        )
        num_items = com_data(result, 0, 0)
        point_names = com_data(result, 1, [])
        constraint_names = com_data(result, 2, [])
        
        for i in range(num_items):
            assignments.append(PointConstraintAssignment(
                point_name=point_names[i] if point_names else str(point_name),
                constraint_name=constraint_names[i] if constraint_names else ""
            ))
    except Exception:
        pass
    return assignments


def delete_point_constraint(
    model,
    point_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    删除节点的所有约束分配
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        item_type: 项目类型
    
    Returns:
        0 表示成功
    
    Example:
        delete_point_constraint(model, "1")
    """
    return model.PointObj.DeleteConstraint(str(point_name), item_type)


def get_points_in_constraint(
    model,
    constraint_name: str
) -> List[str]:
    """
    获取属于指定约束的所有节点
    
    Args:
        model: SapModel 对象
        constraint_name: 约束名称
    
    Returns:
        节点名称列表
    
    Example:
        points = get_points_in_constraint(model, "Diaph1")
        print(f"隔板 Diaph1 包含 {len(points)} 个节点")
    """
    points_in_constraint = []
    
    # 获取所有节点
    result = model.PointObj.GetNameList(0, [])
    names = com_data(result, 1)
    if not names:
        return points_in_constraint
    
    # 检查每个节点
    for name in names:
        constraints = get_point_constraint(model, name)
        for c in constraints:
            if c.constraint_name == constraint_name:
                points_in_constraint.append(name)
                break
    
    return points_in_constraint
