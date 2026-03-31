# -*- coding: utf-8 -*-
"""
local_axes.py - Link local-axis helpers.

Provides functions to assign and query link local-axis orientation.

SAP2000 API:
- LinkObj.SetLocalAxes(Name, Ang, ItemType)
- LinkObj.GetLocalAxes(Name, Ang, Advanced)
- LinkObj.SetLocalAxesAdvanced(Name, Active, AxVectOpt, AxCSys, AxDir[], AxPt[], AxVect[],
                                Plane2, PlVectOpt, PlCSys, PlDir[], PlPt[], PlVect[], ItemType)
- LinkObj.GetLocalAxesAdvanced(Name, Active, AxVectOpt, AxCSys, AxDir[], AxPt[], AxVect[],
                                Plane2, PlVectOpt, PlCSys, PlDir[], PlPt[], PlVect[])
- LinkObj.GetTransformationMatrix(Name, Value[], IsGlobal)
"""

from typing import Optional, List
from .enums import LinkItemType
from .data_classes import LinkLocalAxesData, LinkLocalAxesAdvancedData
from PySap2000.com_helper import com_data


def set_link_local_axes(
    model,
    link_name: str,
    angle: float,
    item_type: LinkItemType = LinkItemType.OBJECT
) -> int:
    """
    Set the local-axis rotation angle of a link object.

    The local 2 and 3 axes rotate about the positive local 1 axis. A positive
    angle is counterclockwise when viewed looking in the positive local-1 direction.
    
    Args:
        model: SAP2000 SapModel object
        link_name: Link object name
        angle: Rotation angle [deg]
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        set_link_local_axes(model, "1", 30)
    """
    return model.LinkObj.SetLocalAxes(str(link_name), angle, int(item_type))


def get_link_local_axes(
    model,
    link_name: str
) -> Optional[LinkLocalAxesData]:
    """
    Get the local-axis rotation angle of a link object.
    
    Args:
        model: SAP2000 SapModel object
        link_name: Link object name
    
    Returns:
        `LinkLocalAxesData`, or `None` if the query fails.
    
    Example:
        axes = get_link_local_axes(model, "1")
        if axes:
            print(f"Local-axis angle: {axes.angle} deg")
    """
    try:
        result = model.LinkObj.GetLocalAxes(str(link_name), 0.0, False)
        angle = com_data(result, 0)
        if angle is not None:
            return LinkLocalAxesData(
                link_name=str(link_name),
                angle=angle,
                advanced=com_data(result, 1, False)
            )
    except Exception:
        pass
    return None



def set_link_local_axes_advanced(
    model,
    link_name: str,
    active: bool,
    ax_vect_opt: int = 1,
    ax_csys: str = "Global",
    ax_dir: List[int] = None,
    ax_pt: List[str] = None,
    ax_vect: List[float] = None,
    plane2: int = 12,
    pl_vect_opt: int = 1,
    pl_csys: str = "Global",
    pl_dir: List[int] = None,
    pl_pt: List[str] = None,
    pl_vect: List[float] = None,
    item_type: LinkItemType = LinkItemType.OBJECT
) -> int:
    """
    Set advanced local-axis options for a link object.
    
    Args:
        model: SAP2000 SapModel object
        link_name: Link object name
        active: Whether advanced local axes are enabled
        ax_vect_opt: Axis vector option (`1`=coordinate direction,
            `2`=two points, `3`=user vector)
        ax_csys: Axis coordinate system
        ax_dir: Axis direction array `[primary, secondary]`
        ax_pt: Axis reference point array `[pt1, pt2]`
        ax_vect: Axis vector `[x, y, z]`
        plane2: Plane-2 definition (`12` or `13`)
        pl_vect_opt: Plane vector option
        pl_csys: Plane coordinate system
        pl_dir: Plane direction array `[primary, secondary]`
        pl_pt: Plane reference point array `[pt1, pt2]`
        pl_vect: Plane vector `[x, y, z]`
        item_type: Target scope for the operation
        
    Returns:
        `0` if successful.
    
    Example:
        set_link_local_axes_advanced(model, "1", True, ax_vect_opt=3, ax_vect=[1, 0, 0])
    """
    if ax_dir is None:
        ax_dir = [0, 0]
    if ax_pt is None:
        ax_pt = ["", ""]
    if ax_vect is None:
        ax_vect = [0.0, 0.0, 0.0]
    if pl_dir is None:
        pl_dir = [0, 0]
    if pl_pt is None:
        pl_pt = ["", ""]
    if pl_vect is None:
        pl_vect = [0.0, 0.0, 0.0]
    
    return model.LinkObj.SetLocalAxesAdvanced(
        str(link_name), active, ax_vect_opt, ax_csys, ax_dir, ax_pt, ax_vect,
        plane2, pl_vect_opt, pl_csys, pl_dir, pl_pt, pl_vect, int(item_type)
    )


def get_link_local_axes_advanced(
    model,
    link_name: str
) -> Optional[LinkLocalAxesAdvancedData]:
    """
    Get advanced local-axis settings for a link object.
    
    Args:
        model: SAP2000 SapModel object
        link_name: Link object name
    
    Returns:
        `LinkLocalAxesAdvancedData`, or `None` if the query fails.
    
    Example:
        axes = get_link_local_axes_advanced(model, "1")
        if axes and axes.active:
            print(f"Advanced local axes enabled, axis vector option: {axes.ax_vect_opt}")
    """
    try:
        result = model.LinkObj.GetLocalAxesAdvanced(
            str(link_name), False, 0, "", [], [], [], 0, 0, "", [], [], []
        )
        
        active = com_data(result, 0)
        if active is not None:
            return LinkLocalAxesAdvancedData(
                link_name=str(link_name),
                active=com_data(result, 0, False),
                ax_vect_opt=com_data(result, 1, 0),
                ax_csys=com_data(result, 2) or "Global",
                ax_dir=list(com_data(result, 3)) if com_data(result, 3) else [0, 0],
                ax_pt=list(com_data(result, 4)) if com_data(result, 4) else ["", ""],
                ax_vect=list(com_data(result, 5)) if com_data(result, 5) else [0.0, 0.0, 0.0],
                plane2=com_data(result, 6, 0),
                pl_vect_opt=com_data(result, 7, 0),
                pl_csys=com_data(result, 8) or "Global",
                pl_dir=list(com_data(result, 9)) if com_data(result, 9) else [0, 0],
                pl_pt=list(com_data(result, 10)) if com_data(result, 10) else ["", ""],
                pl_vect=list(com_data(result, 11)) if com_data(result, 11) else [0.0, 0.0, 0.0]
            )
    except Exception:
        pass
    return None


def get_link_transformation_matrix(
    model,
    link_name: str,
    is_global: bool = True
) -> Optional[List[float]]:
    """
    Get the transformation matrix of a link object.

    Returns a 3x3 matrix with 9 values for converting between local and global coordinates.
    
    Args:
        model: SAP2000 SapModel object
        link_name: Link object name
        is_global: `True` for the global coordinate system, `False` for the current system
    
    Returns:
        List of 9 floats in row-major order, or `None` if the query fails.
    
    Example:
        matrix = get_link_transformation_matrix(model, "1")
        if matrix:
            print(f"Local-1 axis direction: {matrix[0:3]}")
    """
    try:
        result = model.LinkObj.GetTransformationMatrix(str(link_name), [], is_global)
        values = com_data(result, 0)
        if values:
            return list(values)[:9]
    except Exception:
        pass
    return None
