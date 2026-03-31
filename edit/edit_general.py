# -*- coding: utf-8 -*-
"""
edit_general.py - General editing

Wrappers for the SAP2000 `EditGeneral` API.

SAP2000 API:
- `EditGeneral.ExtrudeAreaToSolidLinearNormal` - Extrude areas to solids (normal)
- `EditGeneral.ExtrudeAreaToSolidLinearUser` - Extrude areas to solids (user vector)
- `EditGeneral.ExtrudeAreaToSolidRadial` - Extrude areas to solids (radial)
- `EditGeneral.ExtrudeFrameToAreaLinear` - Extrude frames to areas (linear)
- `EditGeneral.ExtrudeFrameToAreaRadial` - Extrude frames to areas (radial)
- `EditGeneral.ExtrudePointToFrameLinear` - Extrude points to frames (linear)
- `EditGeneral.ExtrudePointToFrameRadial` - Extrude points to frames (radial)
- `EditGeneral.Move` - Move
- `EditGeneral.ReplicateLinear` - Linear replicate
- `EditGeneral.ReplicateMirror` - Mirror replicate
- `EditGeneral.ReplicateRadial` - Radial replicate
"""

from typing import List
from PySap2000.com_helper import com_ret, com_data


def extrude_area_to_solid_linear_normal(
    model,
    num_solid: int,
    thickness: float,
    delete_original: bool = False
) -> List[str]:
    """
    Extrude selected areas to solids along the normal direction
    
    Args:
        model: SAP2000 SapModel object
        num_solid: Number of solids
        thickness: Total thickness
        delete_original: Whether to delete original areas
        
    Returns:
        List of newly created solid names
    """
    result = model.EditGeneral.ExtrudeAreaToSolidLinearNormal(
        num_solid, thickness, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def extrude_area_to_solid_linear_user(
    model,
    num_solid: int,
    dx: float,
    dy: float,
    dz: float,
    delete_original: bool = False
) -> List[str]:
    """
    Extrude selected areas to solids along a user-defined direction
    
    Args:
        model: SAP2000 SapModel object
        num_solid: Number of solids
        dx: X increment
        dy: Y increment
        dz: Z increment
        delete_original: Whether to delete original areas
        
    Returns:
        List of newly created solid names
    """
    result = model.EditGeneral.ExtrudeAreaToSolidLinearUser(
        num_solid, dx, dy, dz, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def extrude_area_to_solid_radial(
    model,
    num_solid: int,
    total_angle: float,
    x: float,
    y: float,
    z: float,
    rx: float,
    ry: float,
    rz: float,
    delete_original: bool = False
) -> List[str]:
    """
    Extrude selected areas to solids radially
    
    Args:
        model: SAP2000 SapModel object
        num_solid: Number of solids
        total_angle: Total angle [deg]
        x, y, z: A point on the rotation axis
        rx, ry, rz: Rotation-axis direction vector
        delete_original: Whether to delete original areas
        
    Returns:
        List of newly created solid names
    """
    result = model.EditGeneral.ExtrudeAreaToSolidRadial(
        num_solid, total_angle, x, y, z, rx, ry, rz, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def extrude_frame_to_area_linear(
    model,
    num_area: int,
    dx: float,
    dy: float,
    dz: float,
    delete_original: bool = False
) -> List[str]:
    """
    Extrude selected frames to area objects linearly
    
    Args:
        model: SAP2000 SapModel object
        num_area: Number of areas
        dx: X increment
        dy: Y increment
        dz: Z increment
        delete_original: Whether to delete original frames
        
    Returns:
        List of newly created area object names
    """
    result = model.EditGeneral.ExtrudeFrameToAreaLinear(
        num_area, dx, dy, dz, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def extrude_frame_to_area_radial(
    model,
    num_area: int,
    total_angle: float,
    x: float,
    y: float,
    z: float,
    rx: float,
    ry: float,
    rz: float,
    delete_original: bool = False
) -> List[str]:
    """
    Extrude selected frames to area objects radially
    
    Args:
        model: SAP2000 SapModel object
        num_area: Number of areas
        total_angle: Total angle [deg]
        x, y, z: A point on the rotation axis
        rx, ry, rz: Rotation-axis direction vector
        delete_original: Whether to delete original frames
        
    Returns:
        List of newly created area object names
    """
    result = model.EditGeneral.ExtrudeFrameToAreaRadial(
        num_area, total_angle, x, y, z, rx, ry, rz, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def extrude_point_to_frame_linear(
    model,
    num_frame: int,
    dx: float,
    dy: float,
    dz: float,
    delete_original: bool = False
) -> List[str]:
    """
    Extrude selected points to frames linearly
    
    Args:
        model: SAP2000 SapModel object
        num_frame: Number of frames
        dx: X increment
        dy: Y increment
        dz: Z increment
        delete_original: Whether to delete original points
        
    Returns:
        List of newly created frame names
    """
    result = model.EditGeneral.ExtrudePointToFrameLinear(
        num_frame, dx, dy, dz, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def extrude_point_to_frame_radial(
    model,
    num_frame: int,
    total_angle: float,
    x: float,
    y: float,
    z: float,
    rx: float,
    ry: float,
    rz: float,
    delete_original: bool = False
) -> List[str]:
    """
    Extrude selected points to frames radially
    
    Args:
        model: SAP2000 SapModel object
        num_frame: Number of frames
        total_angle: Total angle [deg]
        x, y, z: A point on the rotation axis
        rx, ry, rz: Rotation-axis direction vector
        delete_original: Whether to delete original points
        
    Returns:
        List of newly created frame names
    """
    result = model.EditGeneral.ExtrudePointToFrameRadial(
        num_frame, total_angle, x, y, z, rx, ry, rz, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def move_selected(
    model,
    dx: float,
    dy: float,
    dz: float
) -> int:
    """
    Move selected objects
    
    Args:
        model: SAP2000 SapModel object
        dx: X translation
        dy: Y translation
        dz: Z translation
        
    Returns:
        `0` on success
    """
    return model.EditGeneral.Move(dx, dy, dz)


def replicate_linear(
    model,
    num: int,
    dx: float,
    dy: float,
    dz: float
) -> int:
    """
    Replicate selected objects linearly
    
    Args:
        model: SAP2000 SapModel object
        num: Number of copies
        dx: X increment
        dy: Y increment
        dz: Z increment
        
    Returns:
        `0` on success
    """
    return model.EditGeneral.ReplicateLinear(num, dx, dy, dz)


def replicate_mirror(
    model,
    plane: int,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0
) -> int:
    """
    Replicate selected objects by mirror
    
    Args:
        model: SAP2000 SapModel object
        plane: Mirror plane
            `1` = Plane parallel to YZ
            `2` = Plane parallel to XZ
            `3` = Plane parallel to XY
        x, y, z: A point on the mirror plane
        
    Returns:
        `0` on success
    """
    return model.EditGeneral.ReplicateMirror(plane, x, y, z)


def replicate_radial(
    model,
    num: int,
    total_angle: float,
    x: float,
    y: float,
    z: float,
    rx: float,
    ry: float,
    rz: float
) -> int:
    """
    Replicate selected objects radially
    
    Args:
        model: SAP2000 SapModel object
        num: Number of copies
        total_angle: Total angle [deg]
        x, y, z: A point on the rotation axis
        rx, ry, rz: Rotation-axis direction vector
        
    Returns:
        `0` on success
    """
    return model.EditGeneral.ReplicateRadial(num, total_angle, x, y, z, rx, ry, rz)
