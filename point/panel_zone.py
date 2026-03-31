# -*- coding: utf-8 -*-
"""
panel_zone.py - Panel-zone helpers.

Helpers for assigning and querying beam-column joint panel zones.

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
    Assign a panel zone to a point.

    Panel zones are used to model shear deformation in beam-column joints.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        prop_type: Property type
            - `ELASTIC_FROM_COLUMN`: derive elastic stiffness from the column section
            - `ELASTIC_FROM_COLUMN_DOUBLER`: derive it from the column plus doubler plate
            - `FROM_SPRING_STIFFNESS`: specify spring stiffness explicitly
            - `FROM_LINK_PROPERTY`: use a link property
        thickness: Doubler-plate thickness [L]
        k1: Spring stiffness 1
        k2: Spring stiffness 2
        link_prop: Link property name
        connectivity: Connectivity type
        local_axis_from: Local-axis source
        local_axis_angle: Local-axis angle [deg]
        item_type: Item scope
    
    Returns:
        `0` on success
    
    Example:
        # Derive panel-zone stiffness from the column section
        set_point_panel_zone(model, "5", PanelZonePropType.ELASTIC_FROM_COLUMN)
        
        # Use a doubler plate
        set_point_panel_zone(
            model, "5", 
            PanelZonePropType.ELASTIC_FROM_COLUMN_DOUBLER,
            thickness=0.01  # 10 mm doubler plate
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
    Return panel-zone settings for a point.
    
    Args:
        model: `SapModel` object
        point_name: Point name
    
    Returns:
        `PanelZoneData`, or `None` when unavailable
    
    Example:
        pz = get_point_panel_zone(model, "5")
        if pz:
            print(f"Panel-zone type: {pz.prop_type}")
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
    Delete the panel-zone assignment from a point.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        item_type: Item scope
    
    Returns:
        `0` on success
    
    Example:
        delete_point_panel_zone(model, "5")
    """
    return model.PointObj.DeletePanelZone(str(point_name), item_type)


def has_point_panel_zone(
    model,
    point_name: str
) -> bool:
    """
    Check whether a point has panel-zone data assigned.
    
    Args:
        model: `SapModel` object
        point_name: Point name
    
    Returns:
        `True` if panel-zone data exists, otherwise `False`
    """
    return get_point_panel_zone(model, point_name) is not None
