# -*- coding: utf-8 -*-
"""
output_station.py - Cable 输出站点设置

SAP2000 API:
- CableObj.SetOutputStations(Name, MyType, MaxSegSize, MinSections, 
                              NoOutPutAndDesignAtElementEnds, 
                              NoOutPutAndDesignAtPointLoads, ItemType)
- CableObj.GetOutputStations(Name, MyType, MaxSegSize, MinSections,
                              NoOutPutAndDesignAtElementEnds,
                              NoOutPutAndDesignAtPointLoads)
"""

from dataclasses import dataclass
from typing import Optional
from enum import IntEnum
from .modifier import CableItemType
from PySap2000.com_helper import com_data


class CableOutputStationType(IntEnum):
    """输出站点类型"""
    MAX_SEGMENT_SIZE = 1    # 最大分段尺寸
    MIN_SECTIONS = 2        # 最小分段数


@dataclass
class CableOutputStations:
    """Cable 输出站点数据"""
    cable_name: str = ""
    station_type: CableOutputStationType = CableOutputStationType.MAX_SEGMENT_SIZE
    max_seg_size: float = 0.0       # 最大分段尺寸 [L]
    min_sections: int = 0           # 最小分段数
    no_output_at_element_ends: bool = False
    no_output_at_point_loads: bool = False



def set_cable_output_stations(
    model,
    cable_name: str,
    station_type: CableOutputStationType = CableOutputStationType.MAX_SEGMENT_SIZE,
    max_seg_size: float = 24.0,
    min_sections: int = 3,
    no_output_at_element_ends: bool = False,
    no_output_at_point_loads: bool = False,
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    设置 Cable 输出站点
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
        station_type: 站点类型 (1=最大分段尺寸, 2=最小分段数)
        max_seg_size: 最大分段尺寸 [L] (station_type=1 时使用)
        min_sections: 最小分段数 (station_type=2 时使用)
        no_output_at_element_ends: 不在单元端点输出
        no_output_at_point_loads: 不在集中荷载位置输出
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        # 按最大分段尺寸
        set_cable_output_stations(model, "1", CableOutputStationType.MAX_SEGMENT_SIZE, max_seg_size=10.0)
        
        # 按最小分段数
        set_cable_output_stations(model, "1", CableOutputStationType.MIN_SECTIONS, min_sections=5)
    """
    return model.CableObj.SetOutputStations(
        str(cable_name),
        int(station_type),
        max_seg_size,
        min_sections,
        no_output_at_element_ends,
        no_output_at_point_loads,
        int(item_type)
    )


def get_cable_output_stations(model, cable_name: str) -> Optional[CableOutputStations]:
    """
    获取 Cable 输出站点设置
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
    
    Returns:
        CableOutputStations 对象，失败返回 None
    
    Example:
        stations = get_cable_output_stations(model, "1")
        if stations:
            print(f"类型: {stations.station_type}, 最大尺寸: {stations.max_seg_size}")
    """
    try:
        result = model.CableObj.GetOutputStations(str(cable_name), 0, 0.0, 0, False, False)
        station_type = com_data(result, 0)
        if station_type is not None:
            return CableOutputStations(
                cable_name=str(cable_name),
                station_type=CableOutputStationType(station_type),
                max_seg_size=com_data(result, 1, 0.0),
                min_sections=com_data(result, 2, 0),
                no_output_at_element_ends=com_data(result, 3, False),
                no_output_at_point_loads=com_data(result, 4, False)
            )
    except Exception:
        pass
    return None
