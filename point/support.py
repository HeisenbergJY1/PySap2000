# -*- coding: utf-8 -*-
"""
support.py - 节点支座相关函数

用于设置节点的边界条件（约束）

SAP2000 API:
- PointObj.SetRestraint(Name, Value, ItemType)
- PointObj.GetRestraint(Name)
- PointObj.DeleteRestraint(Name, ItemType)
"""

from typing import Tuple, Optional, List
from .enums import PointSupportType, ItemType, SUPPORT_RESTRAINTS
from PySap2000.com_helper import com_ret, com_data


def set_point_support(
    model,
    point_name: str,
    support_type: PointSupportType,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置节点支座类型
    
    这是设置支座的便捷方法，使用预定义的支座类型。
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        support_type: 支座类型
            - FIXED: 固定支座 (全约束)
            - HINGED: 铰接支座 (约束平动，释放转动)
            - ROLLER: 滚动支座 (仅约束 Z 方向)
            - FREE: 自由 (无约束)
        item_type: 项目类型
    
    Returns:
        0 表示成功，非 0 表示失败
    
    Example:
        # 设置节点 "1" 为固定支座
        set_point_support(model, "1", PointSupportType.FIXED)
        
        # 设置节点 "2" 为铰接支座
        set_point_support(model, "2", PointSupportType.HINGED)
    """
    restraints = list(SUPPORT_RESTRAINTS.get(support_type, (False,) * 6))
    result = model.PointObj.SetRestraint(str(point_name), restraints, item_type)
    return com_ret(result)


def set_point_restraint(
    model,
    point_name: str,
    restraints: Tuple[bool, bool, bool, bool, bool, bool],
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置节点自定义约束
    
    可以自由组合 6 个自由度的约束状态。
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        restraints: 约束状态 (U1, U2, U3, R1, R2, R3)
            - True: 约束该自由度
            - False: 释放该自由度
        item_type: 项目类型
    
    Returns:
        0 表示成功
    
    Example:
        # 约束 X, Y 平动，释放其他
        set_point_restraint(model, "1", (True, True, False, False, False, False))
        
        # 约束所有平动，释放所有转动
        set_point_restraint(model, "2", (True, True, True, False, False, False))
    """
    result = model.PointObj.SetRestraint(str(point_name), list(restraints), item_type)
    return com_ret(result)


def get_point_restraint(
    model,
    point_name: str
) -> Optional[Tuple[bool, bool, bool, bool, bool, bool]]:
    """
    获取节点约束状态
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
    
    Returns:
        约束状态元组 (U1, U2, U3, R1, R2, R3)，失败返回 None
    
    Example:
        restraints = get_point_restraint(model, "1")
        if restraints:
            print(f"U1约束: {restraints[0]}, U2约束: {restraints[1]}")
    """
    try:
        result = model.PointObj.GetRestraint(str(point_name))
        restraints = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and restraints:
            return tuple(restraints)
    except Exception:
        pass
    return None


def get_point_support_type(
    model,
    point_name: str
) -> Optional[PointSupportType]:
    """
    获取节点支座类型
    
    根据约束状态推断支座类型。
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
    
    Returns:
        支座类型，如果不匹配预定义类型则返回 None
    
    Example:
        support_type = get_point_support_type(model, "1")
        if support_type == PointSupportType.FIXED:
            print("这是固定支座")
    """
    restraints = get_point_restraint(model, point_name)
    if restraints:
        for support_type, expected in SUPPORT_RESTRAINTS.items():
            if restraints == expected:
                return support_type
    return None


def delete_point_restraint(
    model,
    point_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    删除节点约束（释放所有自由度）
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        item_type: 项目类型
    
    Returns:
        0 表示成功
    
    Example:
        delete_point_restraint(model, "1")
    """
    return model.PointObj.DeleteRestraint(str(point_name), item_type)


def get_points_with_support(model) -> List[str]:
    """
    获取所有有支座的节点名称列表（使用 Database Tables API 批量获取）
    
    原实现: N 个节点 = N 次 COM 调用逐个检查约束
    新实现: 1 次 DB Tables 调用获取所有约束数据
    
    Args:
        model: SapModel 对象
    
    Returns:
        有支座的节点名称列表
    
    Example:
        supported_points = get_points_with_support(model)
        print(f"共有 {len(supported_points)} 个支座节点")
    """
    from PySap2000.database_tables import DatabaseTables
    
    # 一次 COM 调用获取所有约束分配
    table_data = DatabaseTables.get_table_for_display(
        model, "Joint Restraint Assignments"
    )
    
    if table_data is None or table_data.num_records == 0:
        return []
    
    supported = []
    restraint_fields = ["U1", "U2", "U3", "R1", "R2", "R3"]
    
    for row in table_data.to_dict_list():
        joint_name = row.get("Joint", "")
        # 只要有任意一个自由度被约束（值为 "Yes"），就算有支座
        has_restraint = any(
            row.get(f, "").strip().lower() == "yes"
            for f in restraint_fields
        )
        if has_restraint:
            supported.append(joint_name)
    
    return supported
