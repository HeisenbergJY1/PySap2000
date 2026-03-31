# -*- coding: utf-8 -*-
"""
local_axes.py - Point local-axis helpers.

Helpers for assigning and querying point local coordinate systems.

SAP2000 API:
- PointObj.SetLocalAxes / GetLocalAxes
- PointObj.SetLocalAxesAdvanced / GetLocalAxesAdvanced
"""

from typing import Tuple, Optional
from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


def set_point_local_axes(
    model,
    point_name: str,
    a: float,
    b: float,
    c: float,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Set point local-axis angles.

    The local coordinate system is defined through sequential rotations:
    1. Start with local axes 1, 2, and 3 aligned with global X, Y, and Z
    2. Rotate about local axis 3 by angle `a`
    3. Rotate about the transformed local axis 2 by angle `b`
    4. Rotate about the transformed local axis 1 by angle `c`
    
    Args:
        model: `SapModel` object
        point_name: Point name
        a: Rotation about axis 3 [deg]
        b: Rotation about axis 2 [deg]
        c: Rotation about axis 1 [deg]
        item_type: Item scope
    
    Returns:
        `0` on success
    
    Example:
        # Rotate 90 degrees about the Z axis
        set_point_local_axes(model, "1", 90, 0, 0)
        
        # Rotate 45 degrees about the Y axis
        set_point_local_axes(model, "2", 0, 45, 0)
    """
    return model.PointObj.SetLocalAxes(str(point_name), a, b, c, item_type)


def get_point_local_axes(
    model,
    point_name: str
) -> Optional[Tuple[float, float, float]]:
    """
    Return point local-axis angles.
    
    Args:
        model: `SapModel` object
        point_name: Point name
    
    Returns:
        Angle tuple `(a, b, c)` in degrees, or `None` on failure
    
    Example:
        angles = get_point_local_axes(model, "1")
        if angles:
            a, b, c = angles
            print(f"Rotation angles: a={a}°, b={b}°, c={c}°")
    """
    try:
        result = model.PointObj.GetLocalAxes(str(point_name), 0.0, 0.0, 0.0, False)
        a = com_data(result, 0)
        b = com_data(result, 1)
        c = com_data(result, 2)
        if a is not None:
            return (a, b, c)
    except Exception:
        pass
    return None


def set_point_local_axes_advanced(
    model,
    point_name: str,
    active: bool,
    axvec_opt: int,
    axcsys: str,
    axdir: Tuple[int, int],
    axpt: Tuple[str, str],
    axvec: Tuple[float, float, float],
    plane2: int,
    plvec_opt: int,
    plcsys: str,
    pldir: Tuple[int, int],
    plpt: Tuple[str, str],
    plvec: Tuple[float, float, float],
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Assign advanced local-axis settings to a point.

    This advanced helper supports multiple axis-definition modes.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        active: `True` to use advanced definition, `False` for simple angles
        axvec_opt: Axis vector option (`1` coord direction, `2` two points, `3` user vector)
        axcsys: Axis coordinate system name
        axdir: Axis directions
        axpt: Axis definition points
        axvec: Axis vector `(x, y, z)`
        plane2: Plane definition option
        plvec_opt: Plane vector option
        plcsys: Plane coordinate system name
        pldir: Plane directions
        plpt: Plane definition points
        plvec: Plane vector
        item_type: Item scope
    
    Returns:
        `0` on success
    
    Note:
        For most cases, prefer the simpler `set_point_local_axes()` helper.
    """
    return model.PointObj.SetLocalAxesAdvanced(
        str(point_name),
        active,
        axvec_opt,
        axcsys,
        axdir[0], axdir[1],
        axpt[0], axpt[1],
        axvec[0], axvec[1], axvec[2],
        plane2,
        plvec_opt,
        plcsys,
        pldir[0], pldir[1],
        plpt[0], plpt[1],
        plvec[0], plvec[1], plvec[2],
        item_type
    )


def get_point_local_axes_advanced(
    model,
    point_name: str
) -> Optional[dict]:
    """
    Return advanced local-axis settings for a point.
    
    Args:
        model: `SapModel` object
        point_name: Point name
    
    Returns:
        Dictionary of advanced settings, or `None` on failure
    """
    try:
        result = model.PointObj.GetLocalAxesAdvanced(str(point_name))
        active = com_data(result, 0)
        if active is not None and com_data(result, 19) is not None:
            return {
                'active': active,
                'axvec_opt': com_data(result, 1),
                'axcsys': com_data(result, 2),
                'axdir': (com_data(result, 3), com_data(result, 4)),
                'axpt': (com_data(result, 5), com_data(result, 6)),
                'axvec': (com_data(result, 7), com_data(result, 8), com_data(result, 9)),
                'plane2': com_data(result, 10),
                'plvec_opt': com_data(result, 11),
                'plcsys': com_data(result, 12),
                'pldir': (com_data(result, 13), com_data(result, 14)),
                'plpt': (com_data(result, 15), com_data(result, 16)),
                'plvec': (com_data(result, 17), com_data(result, 18), com_data(result, 19))
            }
    except Exception:
        pass
    return None


def get_point_transformation_matrix(
    model,
    point_name: str,
    is_global: bool = True
) -> Optional[Tuple[float, ...]]:
    """
    Return the point transformation matrix.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        is_global: `True` for global-to-local, `False` for local-to-global
    
    Returns:
        12-value transformation matrix, or `None` on failure
    """
    try:
        result = model.PointObj.GetTransformationMatrix(
            str(point_name), [0.0] * 12, is_global
        )
        matrix = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and matrix:
            return tuple(matrix)
    except Exception:
        pass
    return None
