# -*- coding: utf-8 -*-
"""
link_load.py - 连接单元荷载

包含:
- 枚举: LinkLoadItemType
- 数据类: LinkLoadDeformationData, LinkLoadGravityData, LinkLoadTargetForceData
- 函数: set_link_load_xxx, get_link_load_xxx, delete_link_load_xxx

SAP2000 API:
- LinkObj.SetLoadDeformation / GetLoadDeformation / DeleteLoadDeformation
- LinkObj.SetLoadGravity / GetLoadGravity / DeleteLoadGravity
- LinkObj.SetLoadTargetForce / GetLoadTargetForce / DeleteLoadTargetForce
"""

from dataclasses import dataclass, field
from typing import List, Tuple
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


# ==================== 枚举 ====================

class LinkLoadItemType(IntEnum):
    """荷载应用对象类型"""
    OBJECT = 0              # 单个对象
    GROUP = 1               # 组
    SELECTED_OBJECTS = 2    # 选中对象


# ==================== 数据类 ====================

@dataclass
class LinkLoadDeformationData:
    """连接单元变形荷载数据"""
    link_name: str = ""
    load_pattern: str = ""
    dof: Tuple[bool, ...] = field(default_factory=lambda: (False,) * 6)  # U1,U2,U3,R1,R2,R3
    deformation: Tuple[float, ...] = field(default_factory=lambda: (0.0,) * 6)  # [L] or [rad]


@dataclass
class LinkLoadGravityData:
    """连接单元重力荷载数据"""
    link_name: str = ""
    load_pattern: str = ""
    x: float = 0.0
    y: float = 0.0
    z: float = -1.0
    csys: str = "Global"


@dataclass
class LinkLoadTargetForceData:
    """连接单元目标力荷载数据"""
    link_name: str = ""
    load_pattern: str = ""
    dof: Tuple[bool, ...] = field(default_factory=lambda: (False,) * 6)  # P,V2,V3,T,M2,M3
    force: Tuple[float, ...] = field(default_factory=lambda: (0.0,) * 6)  # [F] or [FL]
    relative_dist: Tuple[float, ...] = field(default_factory=lambda: (0.5,) * 6)


# ==================== 变形荷载函数 ====================

def set_link_load_deformation(
    model,
    link_name: str,
    load_pattern: str,
    dof: Tuple[bool, ...],
    deformation: Tuple[float, ...],
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> int:
    """
    设置连接单元变形荷载
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        load_pattern: 荷载模式名称
        dof: 各自由度是否有变形荷载 (U1, U2, U3, R1, R2, R3)
        deformation: 变形值 (U1, U2, U3 [L], R1, R2, R3 [rad])
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        set_link_load_deformation(model, "1", "DEAD", 
            (True, False, False, False, False, False), (0.01, 0, 0, 0, 0, 0))
    """
    dof_list = list(dof) if len(dof) >= 6 else list(dof) + [False] * (6 - len(dof))
    d_list = list(deformation) if len(deformation) >= 6 else list(deformation) + [0.0] * (6 - len(deformation))
    
    return model.LinkObj.SetLoadDeformation(
        str(link_name), load_pattern, dof_list, d_list, int(item_type)
    )


def get_link_load_deformation(
    model,
    link_name: str,
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> List[LinkLoadDeformationData]:
    """
    获取连接单元变形荷载
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        item_type: 操作范围
    
    Returns:
        LinkLoadDeformationData 对象列表
    """
    loads = []
    try:
        result = model.LinkObj.GetLoadDeformation(str(link_name), int(item_type))
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            link_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            dof1 = com_data(result, 3)
            dof2 = com_data(result, 4)
            dof3 = com_data(result, 5)
            dof4 = com_data(result, 6)
            dof5 = com_data(result, 7)
            dof6 = com_data(result, 8)
            u1 = com_data(result, 9)
            u2 = com_data(result, 10)
            u3 = com_data(result, 11)
            r1 = com_data(result, 12)
            r2 = com_data(result, 13)
            r3 = com_data(result, 14)

            for i in range(num_items):
                loads.append(LinkLoadDeformationData(
                    link_name=link_names[i] if link_names else str(link_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    dof=(dof1[i], dof2[i], dof3[i], dof4[i], dof5[i], dof6[i]),
                    deformation=(u1[i], u2[i], u3[i], r1[i], r2[i], r3[i])
                ))
    except Exception:
        pass
    return loads


def delete_link_load_deformation(
    model,
    link_name: str,
    load_pattern: str,
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> int:
    """
    删除连接单元变形荷载
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        load_pattern: 荷载模式名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.LinkObj.DeleteLoadDeformation(str(link_name), load_pattern, int(item_type))


# ==================== 重力荷载函数 ====================

def set_link_load_gravity(
    model,
    link_name: str,
    load_pattern: str,
    x: float = 0.0,
    y: float = 0.0,
    z: float = -1.0,
    replace: bool = True,
    csys: str = "Global",
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> int:
    """
    设置连接单元重力荷载
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        load_pattern: 荷载模式名称
        x: X方向重力系数
        y: Y方向重力系数
        z: Z方向重力系数 (默认-1)
        replace: True=替换现有荷载, False=叠加
        csys: 坐标系名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.LinkObj.SetLoadGravity(
        str(link_name), load_pattern, x, y, z, replace, csys, int(item_type)
    )


def get_link_load_gravity(
    model,
    link_name: str,
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> List[LinkLoadGravityData]:
    """
    获取连接单元重力荷载
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        item_type: 操作范围
    
    Returns:
        LinkLoadGravityData 对象列表
    """
    loads = []
    try:
        result = model.LinkObj.GetLoadGravity(str(link_name), int(item_type))
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            link_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            csys_list = com_data(result, 3)
            x_list = com_data(result, 4)
            y_list = com_data(result, 5)
            z_list = com_data(result, 6)

            for i in range(num_items):
                loads.append(LinkLoadGravityData(
                    link_name=link_names[i] if link_names else str(link_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    x=x_list[i] if x_list else 0.0,
                    y=y_list[i] if y_list else 0.0,
                    z=z_list[i] if z_list else 0.0,
                    csys=csys_list[i] if csys_list else "Global"
                ))
    except Exception:
        pass
    return loads


def delete_link_load_gravity(
    model,
    link_name: str,
    load_pattern: str,
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> int:
    """
    删除连接单元重力荷载
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        load_pattern: 荷载模式名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.LinkObj.DeleteLoadGravity(str(link_name), load_pattern, int(item_type))


# ==================== 目标力荷载函数 ====================

def set_link_load_target_force(
    model,
    link_name: str,
    load_pattern: str,
    dof: Tuple[bool, ...],
    force: Tuple[float, ...],
    relative_dist: Tuple[float, ...],
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> int:
    """
    设置连接单元目标力荷载
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        load_pattern: 荷载模式名称
        dof: 各自由度是否有目标力 (P, V2, V3, T, M2, M3)
        force: 目标力值 (P [F], V2 [F], V3 [F], T [FL], M2 [FL], M3 [FL])
        relative_dist: 相对距离 (0-1)
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    dof_list = list(dof) if len(dof) >= 6 else list(dof) + [False] * (6 - len(dof))
    f_list = list(force) if len(force) >= 6 else list(force) + [0.0] * (6 - len(force))
    rd_list = list(relative_dist) if len(relative_dist) >= 6 else list(relative_dist) + [0.5] * (6 - len(relative_dist))
    
    return model.LinkObj.SetLoadTargetForce(
        str(link_name), load_pattern, dof_list, f_list, rd_list, int(item_type)
    )


def get_link_load_target_force(
    model,
    link_name: str,
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> List[LinkLoadTargetForceData]:
    """
    获取连接单元目标力荷载
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        item_type: 操作范围
    
    Returns:
        LinkLoadTargetForceData 对象列表
    """
    loads = []
    try:
        result = model.LinkObj.GetLoadTargetForce(str(link_name), int(item_type))
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            link_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            dof1 = com_data(result, 3)
            dof2 = com_data(result, 4)
            dof3 = com_data(result, 5)
            dof4 = com_data(result, 6)
            dof5 = com_data(result, 7)
            dof6 = com_data(result, 8)
            p_vals = com_data(result, 9)
            v2_vals = com_data(result, 10)
            v3_vals = com_data(result, 11)
            t_vals = com_data(result, 12)
            m2_vals = com_data(result, 13)
            m3_vals = com_data(result, 14)
            t1_vals = com_data(result, 15)
            t2_vals = com_data(result, 16)
            t3_vals = com_data(result, 17)
            t4_vals = com_data(result, 18)
            t5_vals = com_data(result, 19)
            t6_vals = com_data(result, 20)

            for i in range(num_items):
                loads.append(LinkLoadTargetForceData(
                    link_name=link_names[i] if link_names else str(link_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    dof=(dof1[i], dof2[i], dof3[i], dof4[i], dof5[i], dof6[i]),
                    force=(p_vals[i], v2_vals[i], v3_vals[i], t_vals[i], m2_vals[i], m3_vals[i]),
                    relative_dist=(t1_vals[i], t2_vals[i], t3_vals[i], t4_vals[i], t5_vals[i], t6_vals[i])
                ))
    except Exception:
        pass
    return loads


def delete_link_load_target_force(
    model,
    link_name: str,
    load_pattern: str,
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> int:
    """
    删除连接单元目标力荷载
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        load_pattern: 荷载模式名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.LinkObj.DeleteLoadTargetForce(str(link_name), load_pattern, int(item_type))
