# -*- coding: utf-8 -*-
"""
thickness.py - Area thickness helpers.

Wraps SAP2000 `AreaObj` thickness APIs.
"""

from typing import Optional, List

from .enums import AreaThicknessType, ItemType
from .data_classes import AreaThicknessData
from PySap2000.com_helper import com_ret, com_data


def set_area_thickness(
    model,
    area_name: str,
    thickness_type: AreaThicknessType,
    thickness_pattern: str,
    thickness_pattern_sf: float,
    thickness: List[float],
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set thickness overrides for an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        thickness_type: Thickness override type
            - `NO_OVERWRITE`: no override, use section-defined thickness
            - `BY_JOINT_PATTERN`: by joint pattern
            - `BY_POINT`: by point
        thickness_pattern: Thickness pattern name for `BY_JOINT_PATTERN`
        thickness_pattern_sf: Thickness pattern scale factor
        thickness: List of thickness values, one per point, for `BY_POINT`
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        # Set thickness by point
        set_area_thickness(model, "1", AreaThicknessType.BY_POINT, "", 1.0, [0.2, 0.2, 0.25, 0.25])
    """
    result = model.AreaObj.SetThickness(
        str(area_name), int(thickness_type), thickness_pattern,
        thickness_pattern_sf, thickness, int(item_type)
    )
    return com_ret(result)


def set_area_thickness_data(
    model,
    area_name: str,
    data: AreaThicknessData,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set area thickness overrides from a data object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        data: `AreaThicknessData` instance
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        data = AreaThicknessData(
            thickness_type=AreaThicknessType.BY_POINT,
            thickness=[0.2, 0.2, 0.25, 0.25]
        )
        set_area_thickness_data(model, "1", data)
    """
    return model.AreaObj.SetThickness(
        str(area_name), int(data.thickness_type), data.thickness_pattern,
        data.thickness_pattern_sf, data.thickness or [], int(item_type)
    )


def get_area_thickness(
    model,
    area_name: str
) -> Optional[AreaThicknessData]:
    """
    Get thickness overrides assigned to an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `AreaThicknessData`, or `None` if the query fails.
        
    Example:
        data = get_area_thickness(model, "1")
        if data:
            print(f"Thickness type: {data.thickness_type}")
            print(f"Thickness values: {data.thickness}")
    """
    try:
        result = model.AreaObj.GetThickness(str(area_name), 0, "", 0.0, [])
        ret = com_ret(result)
        if ret == 0:
            tt_val = com_data(result, 0)
            thickness_type = AreaThicknessType(tt_val) if tt_val is not None else AreaThicknessType.NO_OVERWRITE
            thickness_pattern = com_data(result, 1, "") or ""
            thickness_pattern_sf = com_data(result, 2, 1.0) or 1.0
            thickness_raw = com_data(result, 3)
            thickness = list(thickness_raw) if thickness_raw else None
            if True:
                return AreaThicknessData(
                    thickness_type=thickness_type,
                    thickness_pattern=thickness_pattern,
                    thickness_pattern_sf=thickness_pattern_sf,
                    thickness=thickness
                )
    except Exception:
        pass
    return None


def has_area_thickness(
    model,
    area_name: str
) -> bool:
    """
    Check whether an area object has thickness overrides.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `True` if thickness overrides exist, otherwise `False`.
    """
    data = get_area_thickness(model, area_name)
    if data:
        return data.thickness_type != AreaThicknessType.NO_OVERWRITE
    return False
