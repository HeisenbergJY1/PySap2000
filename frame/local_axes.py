# -*- coding: utf-8 -*-
"""
local_axes.py - Frame local-axis helpers.

Helpers for assigning and querying frame local-axis orientation.

SAP2000 API:
- FrameObj.SetLocalAxes(Name, Ang, ItemType)
- FrameObj.GetLocalAxes(Name, Ang, Advanced)
- FrameObj.GetTransformationMatrix(Name, Value[], IsGlobal)
"""

from typing import Tuple, Optional, List
from .enums import ItemType
from .data_classes import FrameLocalAxesData, FrameLocalAxesAdvancedData
from PySap2000.com_helper import com_ret, com_data


def set_frame_local_axes(
    model,
    frame_name: str,
    angle: float,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set the local-axis rotation angle of a frame.

    The local 2 and 3 axes rotate about the positive local 1 axis.
    Positive angles are counterclockwise when looking in the +1 direction.
    
    Args:
        model: `SapModel` object
        frame_name: Frame name
        angle: Rotation angle in degrees
        item_type: Item scope
    
    Returns:
        `0` on success
    
    Example:
        # Rotate local axes by 30 degrees
        set_frame_local_axes(model, "1", 30)
        
        # Rotate local axes by 90 degrees
        set_frame_local_axes(model, "B1", 90)
    """
    return model.FrameObj.SetLocalAxes(str(frame_name), angle, int(item_type))


def get_frame_local_axes(
    model,
    frame_name: str
) -> Optional[FrameLocalAxesData]:
    """
    Return the frame local-axis rotation angle.
    
    Args:
        model: `SapModel` object
        frame_name: Frame name
    
    Returns:
        `FrameLocalAxesData`, or `None` on failure
    
    Example:
        axes = get_frame_local_axes(model, "1")
        if axes:
            print(f"Local axis angle: {axes.angle}°")
    """
    try:
        result = model.FrameObj.GetLocalAxes(str(frame_name))
        angle = com_data(result, 0)
        if angle is not None:
            return FrameLocalAxesData(
                frame_name=str(frame_name),
                angle=angle,
                advanced=com_data(result, 1, False)
            )
    except Exception:
        pass
    return None


def set_frame_local_axes_advanced(
    model,
    frame_name: str,
    active: bool,
    plane2: int = 12,
    pl_vect_opt: int = 1,
    pl_csys: str = "Global",
    pl_dir: List[int] = None,
    pl_pt: List[str] = None,
    pl_vect: List[float] = None,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Assign advanced local-axis settings to a frame.
    
    Args:
        model: `SapModel` object
        frame_name: Frame name
        active: Whether advanced local axes are active
        plane2: `12` for the 1-2 plane, `13` for the 1-3 plane
        pl_vect_opt: Plane reference option (`1` coord dir, `2` two points, `3` user vector)
        pl_csys: Coordinate system name
        pl_dir: Direction array `[primary, secondary]`
        pl_pt: Reference point array `[pt1, pt2]`
        pl_vect: User vector `[x, y, z]`
        item_type: Item scope
    
    Returns:
        `0` on success
    
    Example:
        # Define the 1-2 plane by coordinate directions
        set_frame_local_axes_advanced(model, "3", True, 12, 1, "Global", [2, 3])
    """
    if pl_dir is None:
        pl_dir = [0, 0]
    if pl_pt is None:
        pl_pt = ["", ""]
    if pl_vect is None:
        pl_vect = [0.0, 0.0, 0.0]
    
    return model.FrameObj.SetLocalAxesAdvanced(
        str(frame_name), active, plane2, pl_vect_opt, pl_csys,
        pl_dir, pl_pt, pl_vect, int(item_type)
    )


def get_frame_local_axes_advanced(
    model,
    frame_name: str
) -> Optional[FrameLocalAxesAdvancedData]:
    """
    Return advanced local-axis settings for a frame.
    
    Args:
        model: `SapModel` object
        frame_name: Frame name
    
    Returns:
        `FrameLocalAxesAdvancedData`, or `None` on failure
    
    Example:
        data = get_frame_local_axes_advanced(model, "3")
        if data and data.active:
            print(f"Plane: {data.plane2}, Option: {data.pl_vect_opt}")
    """
    try:
        result = model.FrameObj.GetLocalAxesAdvanced(
            str(frame_name), False, 0, 0, "", [], [], []
        )
        ret = com_ret(result)
        if ret == 0:
            active = com_data(result, 0, False)
            plane2 = com_data(result, 1, 12)
            pl_vect_opt = com_data(result, 2, 1)
            pl_csys = com_data(result, 3, "Global")
            pl_dir = com_data(result, 4, [1, 2])
            pl_pt = com_data(result, 5, ["", ""])
            pl_vect = com_data(result, 6, [0.0, 0.0, 0.0])
            return FrameLocalAxesAdvancedData(
                active=active,
                plane2=plane2,
                pl_vect_opt=pl_vect_opt if pl_vect_opt else 1,
                pl_csys=pl_csys or "Global",
                pl_dir=tuple(pl_dir) if pl_dir else (1, 2),
                pl_pt=tuple(pl_pt) if pl_pt else ("", ""),
                pl_vect=tuple(pl_vect) if pl_vect else (0.0, 0.0, 0.0)
            )
    except Exception:
        pass
    return None


def get_frame_transformation_matrix(
    model,
    frame_name: str,
    is_global: bool = True
) -> Optional[List[float]]:
    """
    Return the frame transformation matrix.

    The matrix is a 3x3 matrix (9 values) used to transform between local and
    global coordinates.
    
    Args:
        model: `SapModel` object
        frame_name: Frame name
        is_global: `True` for global coordinates, `False` for the current system
    
    Returns:
        List of 9 floats (row-major 3x3 matrix), or `None` on failure
    
    Example:
        matrix = get_frame_transformation_matrix(model, "1")
        if matrix:
            # matrix[0:3] = direction of local axis 1 in global coordinates
            # matrix[3:6] = direction of local axis 2 in global coordinates
            # matrix[6:9] = direction of local axis 3 in global coordinates
            print(f"Local axis 1 direction: {matrix[0:3]}")
    """
    try:
        result = model.FrameObj.GetTransformationMatrix(
            str(frame_name), [0.0] * 12, is_global
        )
        values = com_data(result, 0)
        if values and len(values) >= 9:
            return list(values[:9])
    except Exception:
        pass
    return None
