# -*- coding: utf-8 -*-
"""
frame_load.py - Frame loads

Includes:
- Enums: FrameLoadType, FrameLoadDirection, FrameLoadItemType
- Dataclasses: FrameLoadDistributedData, FrameLoadPointData
- Functions: set_frame_load_distributed, get_frame_load_distributed, ...

SAP2000 API:
- FrameObj.SetLoadDistributed / GetLoadDistributed / DeleteLoadDistributed
- FrameObj.SetLoadPoint / GetLoadPoint / DeleteLoadPoint
"""

from dataclasses import dataclass
from typing import List, Tuple
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


# ==================== Enums ====================

class FrameLoadType(IntEnum):
    """Frame load type."""
    FORCE = 1   # Force (F/L or F)
    MOMENT = 2  # Moment (FL/L or FL)


class FrameLoadDirection(IntEnum):
    """
    Frame load direction.

    1-3: Local coordinate system (CSys="Local")
    4-6: Global coordinate system direction
    7-9: Projected direction
    10-11: Gravity direction
    """
    LOCAL_1 = 1                 # Local-1 axis (only CSys=Local)
    LOCAL_2 = 2                 # Local-2 axis (only CSys=Local)
    LOCAL_3 = 3                 # Local-3 axis (only CSys=Local)
    GLOBAL_X = 4                # Global-X direction
    GLOBAL_Y = 5                # Global-Y direction
    GLOBAL_Z = 6                # Global-Z direction
    PROJECTED_GLOBAL_X = 7      # Projected global-X direction
    PROJECTED_GLOBAL_Y = 8      # Projected global-Y direction
    PROJECTED_GLOBAL_Z = 9      # Projected global-Z direction
    GRAVITY = 10                # Gravity direction (negative global Z)
    PROJECTED_GRAVITY = 11      # Projected gravity direction


class FrameLoadItemType(IntEnum):
    """Load assignment target type."""
    OBJECT = 0              # Single object
    GROUP = 1               # Group
    SELECTED_OBJECTS = 2    # Selected objects


# ==================== Dataclasses ====================

@dataclass
class FrameLoadDistributedData:
    """Frame distributed load data (returned by getter methods)."""
    frame_name: str = ""
    load_pattern: str = ""
    load_type: int = 1      # 1=Force, 2=Moment
    direction: int = 10     # Default gravity direction
    dist1: float = 0.0
    dist2: float = 1.0
    val1: float = 0.0
    val2: float = 0.0
    csys: str = "Global"
    rel_dist: bool = True


@dataclass
class FrameLoadPointData:
    """Frame point load data (returned by getter methods)."""
    frame_name: str = ""
    load_pattern: str = ""
    load_type: int = 1      # 1=Force, 2=Moment
    direction: int = 10     # Default gravity direction
    dist: float = 0.5
    value: float = 0.0
    csys: str = "Global"
    rel_dist: bool = True


# ==================== Distributed load functions ====================

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
    Set frame distributed load.

    Args:
        model: SapModel object
        frame_name: Frame name
        load_pattern: Load pattern name
        val1: Start load value [F/L] or [FL/L]
        val2: End load value. If `None`, uses `val1` (uniform load).
        load_type: Load type (`FORCE` for force, `MOMENT` for moment)
        direction: Load direction (`GRAVITY`, `GLOBAL_X/Y/Z`, `LOCAL_1/2/3`)
        dist1: Start distance (relative `0-1` or absolute)
        dist2: End distance (relative `0-1` or absolute)
        csys: Coordinate system name
        rel_dist: `True` for relative distance, `False` for absolute distance
        replace: `True` replaces existing loads, `False` adds to existing loads
        item_type: Operation scope

    Returns:
        `0` on success

    Example:
        # Full-length uniform load: 10 kN/m (gravity direction)
        set_frame_load_distributed(model, "1", "DEAD", 10)
        
        # Triangular load: 0-20 kN/m
        set_frame_load_distributed(model, "1", "LIVE", 0, 20)
        
        # Partial uniform load (`0.2-0.8` range)
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
    Get frame distributed loads.

    Args:
        model: SapModel object
        frame_name: Frame name
        item_type: Operation scope
    
    Returns:
        List of `FrameLoadDistributedData` objects
    
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
    Delete frame distributed load.

    Args:
        model: SapModel object
        frame_name: Frame name
        load_pattern: Load pattern name
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.FrameObj.DeleteLoadDistributed(str(frame_name), load_pattern, int(item_type))


# ==================== Point load functions ====================

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
    Set frame point load.

    Args:
        model: SapModel object
        frame_name: Frame name
        load_pattern: Load pattern name
        value: Load value `[F]` or `[FL]`
        load_type: Load type (`FORCE` for force, `MOMENT` for moment)
        direction: Load direction
        dist: Load location distance (relative `0-1` or absolute)
        csys: Coordinate system name
        rel_dist: `True` for relative distance, `False` for absolute distance
        replace: `True` replaces existing loads, `False` adds to existing loads
        item_type: Operation scope
    
    Returns:
        `0` on success
    
    Example:
        # Midspan point load: 100 kN (gravity direction)
        set_frame_load_point(model, "1", "LIVE", 100)
        
        # Point load at one-third span
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
    Get frame point loads.

    Args:
        model: SapModel object
        frame_name: Frame name
        item_type: Operation scope
    
    Returns:
        List of `FrameLoadPointData` objects
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
    Delete frame point load.

    Args:
        model: SapModel object
        frame_name: Frame name
        load_pattern: Load pattern name
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.FrameObj.DeleteLoadPoint(str(frame_name), load_pattern, int(item_type))
