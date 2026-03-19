# -*- coding: utf-8 -*-
"""
panel_zone.py - 节点域相关函数

用于设置梁柱节点的节点域 (Panel Zone)

SAP2000 API:
- PointObj.SetPanelZone / GetPanelZone / DeletePanelZone
"""

from typing import Optional
from .enums import (
    ItemType, 
    PanelZonePropType, 
    PanelZoneConnectivity, 
    PanelZoneLocalAxisFrom
)
from .data_classes import PanelZoneData
from PySap2000.com_helper import com_ret, com_data


def set_point_panel_zone(
    model,
    point_name: str,
    prop_type: PanelZonePropType = PanelZonePropType.ELASTIC_FROM_COLUMN,
    thickness: float = 0.0,
    k1: float = 0.0,
    k2: float = 0.0,
    link_prop: str = "",
    connectivity: PanelZoneConnectivity = PanelZoneConnectivity.BEAMS_TO_OTHER,
    local_axis_from: PanelZoneLocalAxisFrom = PanelZoneLocalAxisFrom.FROM_COLUMN,
    local_axis_angle: float = 0.0,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置节点域
    
    节点域用于模拟梁柱节点区域的剪切变形。
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        prop_type: 属性类型
            - ELASTIC_FROM_COLUMN: 从柱截面计算弹性刚度
            - ELASTIC_FROM_COLUMN_DOUBLER: 从柱截面+加劲板计算
            - FROM_SPRING_STIFFNESS: 指定弹簧刚度
            - FROM_LINK_PROPERTY: 使用连接单元属性
        thickness: 加劲板厚度 [L] (仅 ELASTIC_FROM_COLUMN_DOUBLER 使用)
        k1: 弹簧刚度1 (仅 FROM_SPRING_STIFFNESS 使用)
        k2: 弹簧刚度2 (仅 FROM_SPRING_STIFFNESS 使用)
        link_prop: 连接单元属性名称 (仅 FROM_LINK_PROPERTY 使用)
        connectivity: 连接类型
        local_axis_from: 局部轴来源
        local_axis_angle: 局部轴角度 [deg]
        item_type: 项目类型
    
    Returns:
        0 表示成功
    
    Example:
        # 使用柱截面计算节点域刚度
        set_point_panel_zone(model, "5", PanelZonePropType.ELASTIC_FROM_COLUMN)
        
        # 使用加劲板
        set_point_panel_zone(
            model, "5", 
            PanelZonePropType.ELASTIC_FROM_COLUMN_DOUBLER,
            thickness=0.01  # 10mm 加劲板
        )
    """
    return model.PointObj.SetPanelZone(
        str(point_name),
        prop_type,
        thickness,
        k1,
        k2,
        link_prop,
        connectivity,
        local_axis_from,
        local_axis_angle,
        item_type
    )


def get_point_panel_zone(
    model,
    point_name: str
) -> Optional[PanelZoneData]:
    """
    获取节点域设置
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
    
    Returns:
        PanelZoneData 对象，失败或无节点域返回 None
    
    Example:
        pz = get_point_panel_zone(model, "5")
        if pz:
            print(f"节点域类型: {pz.prop_type}")
    """
    try:
        result = model.PointObj.GetPanelZone(str(point_name))
        ret = com_ret(result)
        if ret == 0:
            return PanelZoneData(
                prop_type=PanelZonePropType(com_data(result, 0)),
                thickness=com_data(result, 1, 0.0),
                k1=com_data(result, 2, 0.0),
                k2=com_data(result, 3, 0.0),
                link_prop=com_data(result, 4, ""),
                connectivity=PanelZoneConnectivity(com_data(result, 5)),
                local_axis_from=PanelZoneLocalAxisFrom(com_data(result, 6)),
                local_axis_angle=com_data(result, 7, 0.0)
            )
    except Exception:
        pass
    return None


def delete_point_panel_zone(
    model,
    point_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    删除节点域
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        item_type: 项目类型
    
    Returns:
        0 表示成功
    
    Example:
        delete_point_panel_zone(model, "5")
    """
    return model.PointObj.DeletePanelZone(str(point_name), item_type)


def has_point_panel_zone(
    model,
    point_name: str
) -> bool:
    """
    检查节点是否有节点域
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
    
    Returns:
        True=有节点域, False=没有
    """
    return get_point_panel_zone(model, point_name) is not None
