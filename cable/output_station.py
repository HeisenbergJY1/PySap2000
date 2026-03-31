# -*- coding: utf-8 -*-
"""
output_station.py - Cable output-station helpers.

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
    """Cable output-station control type."""
    MAX_SEGMENT_SIZE = 1    # Maximum segment size
    MIN_SECTIONS = 2        # Minimum number of segments


@dataclass
class CableOutputStations:
    """Cable output-station settings."""
    cable_name: str = ""
    station_type: CableOutputStationType = CableOutputStationType.MAX_SEGMENT_SIZE
    max_seg_size: float = 0.0       # Maximum segment size [L]
    min_sections: int = 0           # Minimum number of segments
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
    Set output-station controls for a cable object.
    
    Args:
        model: SAP2000 SapModel object
        cable_name: Cable object name
        station_type: Output-station control type
            (`1` for maximum segment size, `2` for minimum sections)
        max_seg_size: Maximum segment size [L]. Used when `station_type=1`.
        min_sections: Minimum number of segments. Used when `station_type=2`.
        no_output_at_element_ends: Whether to suppress output at element ends
        no_output_at_point_loads: Whether to suppress output at point-load locations
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        # Control by maximum segment size
        set_cable_output_stations(model, "1", CableOutputStationType.MAX_SEGMENT_SIZE, max_seg_size=10.0)
        
        # Control by minimum number of segments
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
    Get output-station settings for a cable object.
    
    Args:
        model: SAP2000 SapModel object
        cable_name: Cable object name
    
    Returns:
        `CableOutputStations`, or `None` if the query fails.
    
    Example:
        stations = get_cable_output_stations(model, "1")
        if stations:
            print(f"Type: {stations.station_type}, max size: {stations.max_seg_size}")
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
