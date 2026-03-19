# -*- coding: utf-8 -*-
"""
frame_load.py - 杆件荷载

包含:
- 枚举: FrameLoadType, FrameLoadDirection, FrameLoadItemType
- 数据类: FrameLoadDistributedData, FrameLoadPointData
- 函数: set_frame_load_distributed, get_frame_load_distributed, ...

SAP2000 API:
- FrameObj.SetLoadDistributed / GetLoadDistributed / DeleteLoadDistributed
- FrameObj.SetLoadPoint / GetLoadPoint / DeleteLoadPoint
"""

from dataclasses import dataclass
from typing import List, Tuple
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


# ==================== 枚举 ====================

class FrameLoadType(IntEnum):
    """杆件荷载类型"""
    FORCE = 1   # 力 (F/L 或 F)
    MOMENT = 2  # 力矩 (FL/L 或 FL)


class FrameLoadDirection(IntEnum):
    """
    杆件荷载方向
    
    1-3: 局部坐标系 (CSys="Local")
    4-6: 全局坐标系方向
    7-9: 投影方向
    10-11: 重力方向
    """
    LOCAL_1 = 1                 # 局部1轴 (仅 CSys=Local)
    LOCAL_2 = 2                 # 局部2轴 (仅 CSys=Local)
    LOCAL_3 = 3                 # 局部3轴 (仅 CSys=Local)
    GLOBAL_X = 4                # 全局X方向
    GLOBAL_Y = 5                # 全局Y方向
    GLOBAL_Z = 6                # 全局Z方向
    PROJECTED_GLOBAL_X = 7      # 投影全局X方向
    PROJECTED_GLOBAL_Y = 8      # 投影全局Y方向
    PROJECTED_GLOBAL_Z = 9      # 投影全局Z方向
    GRAVITY = 10                # 重力方向 (负全局Z)
    PROJECTED_GRAVITY = 11      # 投影重力方向


class FrameLoadItemType(IntEnum):
    """荷载应用对象类型"""
    OBJECT = 0              # 单个对象
    GROUP = 1               # 组
    SELECTED_OBJECTS = 2    # 选中对象


# ==================== 数据类 ====================

@dataclass
class FrameLoadDistributedData:
    """杆件分布荷载数据 (用于 get 函数返回)"""
    frame_name: str = ""
    load_pattern: str = ""
    load_type: int = 1      # 1=Force, 2=Moment
    direction: int = 10     # 默认重力方向
    dist1: float = 0.0
    dist2: float = 1.0
    val1: float = 0.0
    val2: float = 0.0
    csys: str = "Global"
    rel_dist: bool = True


@dataclass
class FrameLoadPointData:
    """杆件集中荷载数据 (用于 get 函数返回)"""
    frame_name: str = ""
    load_pattern: str = ""
    load_type: int = 1      # 1=Force, 2=Moment
    direction: int = 10     # 默认重力方向
    dist: float = 0.5
    value: float = 0.0
    csys: str = "Global"
    rel_dist: bool = True


# ==================== 分布荷载函数 ====================

def set_frame_load_distributed(
    model,
    frame_name: str,
    load_pattern: str,
    val1: float,
    val2: float = None,
    load_type: FrameLoadType = FrameLoadType.FORCE,
    direction: FrameLoadDirection = FrameLoadDirection.GRAVITY,
    dist1: float = 0.0,
    dist2: float = 1.0,
    csys: str = "Global",
    rel_dist: bool = True,
    replace: bool = True,
    item_type: FrameLoadItemType = FrameLoadItemType.OBJECT
) -> int:
    """
    设置杆件分布荷载
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        load_pattern: 荷载模式名称
        val1: 起点荷载值 [F/L] 或 [FL/L]
        val2: 终点荷载值，如果为 None 则等于 val1 (均布荷载)
        load_type: 荷载类型 (FORCE=力, MOMENT=力矩)
        direction: 荷载方向 (GRAVITY=重力方向, GLOBAL_X/Y/Z, LOCAL_1/2/3)
        dist1: 起点距离 (相对0-1或绝对)
        dist2: 终点距离 (相对0-1或绝对)
        csys: 坐标系名称
        rel_dist: True=相对距离, False=绝对距离
        replace: True=替换现有荷载, False=叠加
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        # 全长均布荷载 10 kN/m (重力方向)
        set_frame_load_distributed(model, "1", "DEAD", 10)
        
        # 三角形荷载 0-20 kN/m
        set_frame_load_distributed(model, "1", "LIVE", 0, 20)
        
        # 局部均布荷载 (0.2-0.8 范围)
        set_frame_load_distributed(model, "1", "DEAD", 15, 15, dist1=0.2, dist2=0.8)
    """
    if val2 is None:
        val2 = val1
    
    return model.FrameObj.SetLoadDistributed(
        str(frame_name), load_pattern, int(load_type), int(direction),
        dist1, dist2, val1, val2, csys, rel_dist, replace, int(item_type)
    )


def get_frame_load_distributed(
    model,
    frame_name: str,
    item_type: FrameLoadItemType = FrameLoadItemType.OBJECT
) -> List[FrameLoadDistributedData]:
    """
    获取杆件分布荷载
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        item_type: 操作范围
    
    Returns:
        FrameLoadDistributedData 对象列表
    
    Example:
        loads = get_frame_load_distributed(model, "1")
        for load in loads:
            print(f"{load.load_pattern}: {load.val1} - {load.val2}")
    """
    loads = []
    try:
        result = model.FrameObj.GetLoadDistributed(
            str(frame_name), 0, [], [], [], [], [], [], [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            frame_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            my_types = com_data(result, 3)
            csys_list = com_data(result, 4)
            dirs = com_data(result, 5)
            rd1_list = com_data(result, 6)
            rd2_list = com_data(result, 7)
            dist1_list = com_data(result, 8)
            dist2_list = com_data(result, 9)
            val1_list = com_data(result, 10)
            val2_list = com_data(result, 11)
            
            for i in range(num_items):
                loads.append(FrameLoadDistributedData(
                    frame_name=frame_names[i] if frame_names else str(frame_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    load_type=my_types[i] if my_types else 1,
                    direction=dirs[i] if dirs else 10,
                    dist1=dist1_list[i] if dist1_list else 0.0,
                    dist2=dist2_list[i] if dist2_list else 1.0,
                    val1=val1_list[i] if val1_list else 0.0,
                    val2=val2_list[i] if val2_list else 0.0,
                    csys=csys_list[i] if csys_list else "Global",
                    rel_dist=rd1_list[i] < 1.1 if rd1_list else True
                ))
    except Exception:
        pass
    return loads


def delete_frame_load_distributed(
    model,
    frame_name: str,
    load_pattern: str,
    item_type: FrameLoadItemType = FrameLoadItemType.OBJECT
) -> int:
    """
    删除杆件分布荷载
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        load_pattern: 荷载模式名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.FrameObj.DeleteLoadDistributed(str(frame_name), load_pattern, int(item_type))


# ==================== 集中荷载函数 ====================

def set_frame_load_point(
    model,
    frame_name: str,
    load_pattern: str,
    value: float,
    load_type: FrameLoadType = FrameLoadType.FORCE,
    direction: FrameLoadDirection = FrameLoadDirection.GRAVITY,
    dist: float = 0.5,
    csys: str = "Global",
    rel_dist: bool = True,
    replace: bool = True,
    item_type: FrameLoadItemType = FrameLoadItemType.OBJECT
) -> int:
    """
    设置杆件集中荷载
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        load_pattern: 荷载模式名称
        value: 荷载值 [F] 或 [FL]
        load_type: 荷载类型 (FORCE=力, MOMENT=力矩)
        direction: 荷载方向
        dist: 荷载位置距离 (相对0-1或绝对)
        csys: 坐标系名称
        rel_dist: True=相对距离, False=绝对距离
        replace: True=替换现有荷载, False=叠加
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        # 跨中集中力 100 kN (重力方向)
        set_frame_load_point(model, "1", "LIVE", 100)
        
        # 1/3 点处集中力
        set_frame_load_point(model, "1", "LIVE", 50, dist=0.333)
    """
    return model.FrameObj.SetLoadPoint(
        str(frame_name), load_pattern, int(load_type), int(direction),
        dist, value, csys, rel_dist, replace, int(item_type)
    )


def get_frame_load_point(
    model,
    frame_name: str,
    item_type: FrameLoadItemType = FrameLoadItemType.OBJECT
) -> List[FrameLoadPointData]:
    """
    获取杆件集中荷载
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        item_type: 操作范围
    
    Returns:
        FrameLoadPointData 对象列表
    """
    loads = []
    try:
        result = model.FrameObj.GetLoadPoint(
            str(frame_name), 0, [], [], [], [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            frame_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            my_types = com_data(result, 3)
            csys_list = com_data(result, 4)
            dirs = com_data(result, 5)
            rel_dists = com_data(result, 6)
            dists = com_data(result, 7)
            vals = com_data(result, 8)
            
            for i in range(num_items):
                loads.append(FrameLoadPointData(
                    frame_name=frame_names[i] if frame_names else str(frame_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    load_type=my_types[i] if my_types else 1,
                    direction=dirs[i] if dirs else 10,
                    dist=dists[i] if dists else 0.5,
                    value=vals[i] if vals else 0.0,
                    csys=csys_list[i] if csys_list else "Global",
                    rel_dist=rel_dists[i] if rel_dists else True
                ))
    except Exception:
        pass
    return loads


def delete_frame_load_point(
    model,
    frame_name: str,
    load_pattern: str,
    item_type: FrameLoadItemType = FrameLoadItemType.OBJECT
) -> int:
    """
    删除杆件集中荷载
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        load_pattern: 荷载模式名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.FrameObj.DeleteLoadPoint(str(frame_name), load_pattern, int(item_type))
