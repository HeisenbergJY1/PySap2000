# -*- coding: utf-8 -*-
"""
point_load.py - 节点荷载

包含:
- 数据类: PointLoadForceData, PointLoadDisplData, PointLoad, PointDisplLoad
- 函数: set_point_load_force, get_point_load_force, delete_point_load_force, ...

SAP2000 API:
- PointObj.SetLoadForce / GetLoadForce / DeleteLoadForce
- PointObj.SetLoadDispl / GetLoadDispl / DeleteLoadDispl
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Union, ClassVar
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


# ==================== 枚举 ====================

class PointLoadItemType(IntEnum):
    """荷载应用对象类型"""
    OBJECT = 0              # 单个对象
    GROUP = 1               # 组
    SELECTED_OBJECTS = 2    # 选中对象


# ==================== 数据类 ====================

@dataclass
class PointLoadForceData:
    """节点力荷载数据 (用于 get 函数返回)"""
    point_name: str = ""
    load_pattern: str = ""
    f1: float = 0.0
    f2: float = 0.0
    f3: float = 0.0
    m1: float = 0.0
    m2: float = 0.0
    m3: float = 0.0
    csys: str = "Global"
    lc_step: int = 0


@dataclass
class PointLoadDisplData:
    """节点位移荷载数据 (用于 get 函数返回)"""
    point_name: str = ""
    load_pattern: str = ""
    u1: float = 0.0
    u2: float = 0.0
    u3: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0
    csys: str = "Global"
    lc_step: int = 0


# ==================== 函数式 API ====================

def set_point_load_force(
    model,
    point_name: str,
    load_pattern: str,
    forces: Tuple[float, float, float, float, float, float],
    replace: bool = False,
    csys: str = "Global",
    item_type: PointLoadItemType = PointLoadItemType.OBJECT
) -> int:
    """
    设置节点力荷载
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        load_pattern: 荷载模式名称 (必须已存在)
        forces: 力和力矩 (F1, F2, F3, M1, M2, M3)
            - F1, F2, F3: 力 [F]
            - M1, M2, M3: 力矩 [FL]
        replace: True=替换现有荷载, False=叠加
        csys: 坐标系名称
        item_type: 项目类型
    
    Returns:
        0 表示成功
    
    Example:
        set_point_load_force(model, "1", "Dead", (0, 0, -100, 0, 0, 0))
    """
    f_list = list(forces)
    while len(f_list) < 6:
        f_list.append(0.0)
    
    result = model.PointObj.SetLoadForce(
        str(point_name), load_pattern, f_list[:6], replace, csys, int(item_type)
    )
    # 解析返回值
    return com_ret(result)


def get_point_load_force(
    model,
    point_name: str,
    item_type: PointLoadItemType = PointLoadItemType.OBJECT
) -> List[PointLoadForceData]:
    """
    获取节点力荷载
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        item_type: 项目类型
    
    Returns:
        PointLoadForceData 对象列表
    
    Example:
        loads = get_point_load_force(model, "1")
        for load in loads:
            print(f"{load.load_pattern}: F3={load.f3}")
    """
    loads = []
    try:
        result = model.PointObj.GetLoadForce(
            str(point_name), 0, [], [], [], [], [], [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            point_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            lc_steps = com_data(result, 3)
            csys_list = com_data(result, 4)
            f1_list = com_data(result, 5)
            f2_list = com_data(result, 6)
            f3_list = com_data(result, 7)
            m1_list = com_data(result, 8)
            m2_list = com_data(result, 9)
            m3_list = com_data(result, 10)
            
            for i in range(num_items):
                loads.append(PointLoadForceData(
                    point_name=point_names[i] if point_names else str(point_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    f1=f1_list[i] if f1_list else 0.0,
                    f2=f2_list[i] if f2_list else 0.0,
                    f3=f3_list[i] if f3_list else 0.0,
                    m1=m1_list[i] if m1_list else 0.0,
                    m2=m2_list[i] if m2_list else 0.0,
                    m3=m3_list[i] if m3_list else 0.0,
                    csys=csys_list[i] if csys_list else "Global",
                    lc_step=lc_steps[i] if lc_steps else 0
                ))
    except Exception:
        pass
    return loads


def delete_point_load_force(
    model,
    point_name: str,
    load_pattern: str,
    item_type: PointLoadItemType = PointLoadItemType.OBJECT
) -> int:
    """
    删除节点力荷载
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        load_pattern: 荷载模式名称
        item_type: 项目类型
    
    Returns:
        0 表示成功
    """
    return model.PointObj.DeleteLoadForce(str(point_name), load_pattern, int(item_type))


def set_point_load_displ(
    model,
    point_name: str,
    load_pattern: str,
    displacements: Tuple[float, float, float, float, float, float],
    replace: bool = False,
    csys: str = "Global",
    item_type: PointLoadItemType = PointLoadItemType.OBJECT
) -> int:
    """
    设置节点位移荷载 (地面位移/支座沉降)
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        load_pattern: 荷载模式名称
        displacements: 位移和转角 (U1, U2, U3, R1, R2, R3)
            - U1, U2, U3: 位移 [L]
            - R1, R2, R3: 转角 [rad]
        replace: True=替换, False=叠加
        csys: 坐标系名称
        item_type: 项目类型
    
    Returns:
        0 表示成功
    
    Example:
        set_point_load_displ(model, "1", "Settlement", (0, 0, -0.01, 0, 0, 0))
    """
    d_list = list(displacements)
    while len(d_list) < 6:
        d_list.append(0.0)
    
    result = model.PointObj.SetLoadDispl(
        str(point_name), load_pattern, d_list[:6], replace, csys, int(item_type)
    )
    # 解析返回值
    return com_ret(result)


def get_point_load_displ(
    model,
    point_name: str,
    item_type: PointLoadItemType = PointLoadItemType.OBJECT
) -> List[PointLoadDisplData]:
    """
    获取节点位移荷载
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        item_type: 项目类型
    
    Returns:
        PointLoadDisplData 对象列表
    """
    loads = []
    try:
        result = model.PointObj.GetLoadDispl(
            str(point_name), 0, [], [], [], [], [], [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            point_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            lc_steps = com_data(result, 3)
            csys_list = com_data(result, 4)
            u1_list = com_data(result, 5)
            u2_list = com_data(result, 6)
            u3_list = com_data(result, 7)
            r1_list = com_data(result, 8)
            r2_list = com_data(result, 9)
            r3_list = com_data(result, 10)
            
            for i in range(num_items):
                loads.append(PointLoadDisplData(
                    point_name=point_names[i] if point_names else str(point_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    u1=u1_list[i] if u1_list else 0.0,
                    u2=u2_list[i] if u2_list else 0.0,
                    u3=u3_list[i] if u3_list else 0.0,
                    r1=r1_list[i] if r1_list else 0.0,
                    r2=r2_list[i] if r2_list else 0.0,
                    r3=r3_list[i] if r3_list else 0.0,
                    csys=csys_list[i] if csys_list else "Global",
                    lc_step=lc_steps[i] if lc_steps else 0
                ))
    except Exception:
        pass
    return loads


def delete_point_load_displ(
    model,
    point_name: str,
    load_pattern: str,
    item_type: PointLoadItemType = PointLoadItemType.OBJECT
) -> int:
    """
    删除节点位移荷载
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        load_pattern: 荷载模式名称
        item_type: 项目类型
    
    Returns:
        0 表示成功
    """
    return model.PointObj.DeleteLoadDispl(str(point_name), load_pattern, int(item_type))
