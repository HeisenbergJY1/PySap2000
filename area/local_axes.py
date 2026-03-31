# -*- coding: utf-8 -*-
"""
local_axes.py - Area local-axis helpers.

Wraps SAP2000 `AreaObj` local-axis APIs.
"""

from typing import Optional, List, Tuple

from .enums import PlaneRefVectorOption, ItemType
from .data_classes import AreaLocalAxesData, AreaLocalAxesAdvancedData
from PySap2000.com_helper import com_ret, com_data


def set_area_local_axes(
    model,
    area_name: str,
    angle: float,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set the local-axis angle of an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        angle: Local-axis angle [deg]
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        # Set the local-axis angle of area "1" to 45 degrees
        set_area_local_axes(model, "1", 45.0)
    """
    return model.AreaObj.SetLocalAxes(str(area_name), angle, int(item_type))


def get_area_local_axes(
    model,
    area_name: str
) -> Optional[AreaLocalAxesData]:
    """
    Get the local-axis angle of an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `AreaLocalAxesData`, or `None` if the query fails.
        
    Example:
        result = get_area_local_axes(model, "1")
        if result:
            print(f"Angle: {result.angle} deg, advanced: {result.advanced}")
    """
    try:
        result = model.AreaObj.GetLocalAxes(str(area_name), 0.0, False)
        angle = com_data(result, 0)
        if angle is not None:
            return AreaLocalAxesData(
                area_name=str(area_name),
                angle=angle,
                advanced=com_data(result, 1, False)
            )
    except Exception:
        pass
    return None


def set_area_local_axes_advanced(
    model,
    area_name: str,
    active: bool,
    plane2: int = 31,
    pl_vect_opt: PlaneRefVectorOption = PlaneRefVectorOption.COORDINATE_DIRECTION,
    pl_csys: str = "Global",
    pl_dir: Tuple[int, int] = (1, 2),
    pl_pt: Tuple[str, str] = ("", ""),
    pl_vect: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set advanced local-axis options for an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        active: Whether advanced local axes are enabled
        plane2: `31` for the 3-1 plane, `32` for the 3-2 plane
        pl_vect_opt: Plane reference-vector option
            - `COORDINATE_DIRECTION (1)`: coordinate direction
            - `TWO_JOINTS (2)`: two joints
            - `USER_VECTOR (3)`: user vector
        pl_csys: Coordinate system name
        pl_dir: Primary and secondary directions, used when `pl_vect_opt=1`
        pl_pt: Two point names, used when `pl_vect_opt=2`
        pl_vect: User vector, used when `pl_vect_opt=3`
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        # Define the plane using a coordinate direction
        set_area_local_axes_advanced(model, "1", True, 31, 
            PlaneRefVectorOption.COORDINATE_DIRECTION, "Global", (2, 3))
    """
    return model.AreaObj.SetLocalAxesAdvanced(
        str(area_name), active, plane2, int(pl_vect_opt), pl_csys,
        list(pl_dir), list(pl_pt), list(pl_vect), int(item_type)
    )


def get_area_local_axes_advanced(
    model,
    area_name: str
) -> Optional[AreaLocalAxesAdvancedData]:
    """
    Get advanced local-axis settings for an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `AreaLocalAxesAdvancedData`, or `None` if the query fails.
        
    Example:
        data = get_area_local_axes_advanced(model, "1")
        if data and data.active:
            print(f"Plane: {data.plane2}, option: {data.pl_vect_opt}")
    """
    try:
        result = model.AreaObj.GetLocalAxesAdvanced(
            str(area_name), False, 0, 0, "", [], [], []
        )
        ret = com_ret(result)
        if ret == 0:
            active = com_data(result, 0, False)
            plane2 = com_data(result, 1, 31)
            pl_vect_opt = com_data(result, 2, 1)
            pl_csys = com_data(result, 3, "Global")
            pl_dir = com_data(result, 4, [1, 2])
            pl_pt = com_data(result, 5, ["", ""])
            pl_vect = com_data(result, 6, [0.0, 0.0, 0.0])
            return AreaLocalAxesAdvancedData(
                active=active,
                plane2=plane2,
                pl_vect_opt=PlaneRefVectorOption(pl_vect_opt) if pl_vect_opt else PlaneRefVectorOption.COORDINATE_DIRECTION,
                pl_csys=pl_csys or "Global",
                pl_dir=tuple(pl_dir) if pl_dir else (1, 2),
                pl_pt=tuple(pl_pt) if pl_pt else ("", ""),
                pl_vect=tuple(pl_vect) if pl_vect else (0.0, 0.0, 0.0)
            )
    except Exception:
        pass
    return None


def get_area_transformation_matrix(
    model,
    area_name: str,
    is_global: bool = True
) -> Optional[List[float]]:
    """
    Get the transformation matrix of an area object.

    The matrix converts local coordinates to global coordinates, or to the
    current coordinate system. It contains 9 direction cosine values.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        is_global: `True` for the global system, `False` for the current system
        
    Returns:
        List of 9 direction-cosine values
        `[c0, c1, c2, c3, c4, c5, c6, c7, c8]`, or `None` if the query fails.
        
    Example:
        matrix = get_area_transformation_matrix(model, "1")
        if matrix:
            # Matrix form: [GlobalX, GlobalY, GlobalZ] = [c0-c8] * [Local1, Local2, Local3]
            print(f"Transformation matrix: {matrix}")
    """
    try:
        result = model.AreaObj.GetTransformationMatrix(str(area_name), [], is_global)
        matrix = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and matrix:
            return list(matrix)
    except Exception:
        pass
    return None
