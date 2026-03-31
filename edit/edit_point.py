# -*- coding: utf-8 -*-
"""
edit_point.py - Point editing

Wrappers for the SAP2000 `EditPoint` API.

SAP2000 API:
- `EditPoint.Align` - Align
- `EditPoint.Connect` - Connect
- `EditPoint.Disconnect` - Disconnect
- `EditPoint.Merge` - Merge
- `EditPoint.ChangeCoordinates_1` - Change coordinates
"""

from typing import List


def align_point(
    model,
    axis: int,
    ordinate: float = 0.0,
    csys: str = "Global"
) -> int:
    """
    Align selected points
    
    Args:
        model: SAP2000 SapModel object
        axis: Alignment axis
            `1` = X axis
            `2` = Y axis
            `3` = Z axis
        ordinate: Target coordinate value
        csys: Coordinate system name
        
    Returns:
        `0` on success
    """
    return model.EditPoint.Align(axis, ordinate, csys)


def connect_point(model) -> int:
    """
    Connect selected points (creates frames)
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `0` on success
    """
    return model.EditPoint.Connect()


def disconnect_point(model, name: str) -> int:
    """
    Disconnect point connections
    
    Args:
        model: SAP2000 SapModel object
        name: Point name
        
    Returns:
        `0` on success
    """
    return model.EditPoint.Disconnect(name)


def merge_point(model, tolerance: float = 0.001) -> int:
    """
    Merge selected points
    
    Args:
        model: SAP2000 SapModel object
        tolerance: Merge tolerance
        
    Returns:
        `0` on success
    """
    return model.EditPoint.Merge(tolerance)


def change_point_coordinates(
    model,
    name: str,
    x: float,
    y: float,
    z: float,
    csys: str = "Global"
) -> int:
    """
    Change point coordinates
    
    Args:
        model: SAP2000 SapModel object
        name: Point name
        x: X coordinate
        y: Y coordinate
        z: Z coordinate
        csys: Coordinate system name
        
    Returns:
        `0` on success
    """
    return model.EditPoint.ChangeCoordinates_1(name, x, y, z, csys)
