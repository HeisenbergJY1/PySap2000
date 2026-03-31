# -*- coding: utf-8 -*-
"""
offset.py - Area offset helpers.

Wraps SAP2000 `AreaObj` offset APIs.
"""

from typing import Optional, List

from .enums import AreaOffsetType, ItemType
from .data_classes import AreaOffsetData
from PySap2000.com_helper import com_ret, com_data


def set_area_offset(
    model,
    area_name: str,
    offset_type: AreaOffsetType,
    offset_pattern: str,
    offset_pattern_sf: float,
    offsets: List[float],
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set offsets for an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        offset_type: Offset type
            - `NO_OFFSET`: no offset
            - `BY_JOINT_PATTERN`: by joint pattern
            - `BY_POINT`: by point
        offset_pattern: Offset pattern name for `BY_JOINT_PATTERN`
        offset_pattern_sf: Offset pattern scale factor
        offsets: List of offsets, one per point, for `BY_POINT`
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        # Set offsets by point
        set_area_offset(model, "1", AreaOffsetType.BY_POINT, "", 1.0, [0.1, 0.1, 0.1, 0.1])
    """
    result = model.AreaObj.SetOffsets(
        str(area_name), int(offset_type), offset_pattern,
        offset_pattern_sf, offsets, int(item_type)
    )
    return com_ret(result)


def set_area_offset_data(
    model,
    area_name: str,
    data: AreaOffsetData,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set area offsets from a data object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        data: `AreaOffsetData` instance
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        data = AreaOffsetData(
            offset_type=AreaOffsetType.BY_POINT,
            offsets=[0.1, 0.1, 0.1, 0.1]
        )
        set_area_offset_data(model, "1", data)
    """
    return model.AreaObj.SetOffsets(
        str(area_name), int(data.offset_type), data.offset_pattern,
        data.offset_pattern_sf, data.offsets or [], int(item_type)
    )


def get_area_offset(
    model,
    area_name: str
) -> Optional[AreaOffsetData]:
    """
    Get offsets assigned to an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `AreaOffsetData`, or `None` if the query fails.
        
    Example:
        data = get_area_offset(model, "1")
        if data:
            print(f"Offset type: {data.offset_type}")
            print(f"Offset values: {data.offsets}")
    """
    try:
        result = model.AreaObj.GetOffsets(str(area_name), 0, "", 0.0, [])
        ret = com_ret(result)
        if ret == 0:
            offset_type_val = com_data(result, 0)
            offset_type = AreaOffsetType(offset_type_val) if offset_type_val is not None else AreaOffsetType.NO_OFFSET
            offset_pattern = com_data(result, 1, "") or ""
            offset_pattern_sf = com_data(result, 2, 1.0) or 1.0
            offsets_raw = com_data(result, 3)
            offsets = list(offsets_raw) if offsets_raw else None
            if True:
                return AreaOffsetData(
                    offset_type=offset_type,
                    offset_pattern=offset_pattern,
                    offset_pattern_sf=offset_pattern_sf,
                    offsets=offsets
                )
    except Exception:
        pass
    return None


def has_area_offset(
    model,
    area_name: str
) -> bool:
    """
    Check whether an area object has offsets assigned.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `True` if offsets are assigned, otherwise `False`.
    """
    data = get_area_offset(model, area_name)
    if data:
        return data.offset_type != AreaOffsetType.NO_OFFSET
    return False
