# -*- coding: utf-8 -*-
"""
auto_mesh.py - Area automatic meshing helpers.

Wraps SAP2000 `AreaObj` automatic meshing APIs.
"""

from typing import Optional

from .enums import AreaMeshType, ItemType
from .data_classes import AreaAutoMeshData
from PySap2000.com_helper import com_ret, com_data


def set_area_auto_mesh(
    model,
    area_name: str,
    mesh_type: AreaMeshType,
    n1: int = 2,
    n2: int = 2,
    max_size1: float = 0.0,
    max_size2: float = 0.0,
    point_on_edge_from_line: bool = False,
    point_on_edge_from_point: bool = False,
    extend_cookie_cut_lines: bool = False,
    rotation: float = 0.0,
    max_size_general: float = 0.0,
    local_axes_on_edge: bool = False,
    local_axes_on_face: bool = False,
    restraints_on_edge: bool = False,
    restraints_on_face: bool = False,
    group: str = "ALL",
    sub_mesh: bool = False,
    sub_mesh_size: float = 0.0,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Configure automatic meshing for an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        mesh_type: Meshing mode
            - `NO_MESH`: no meshing
            - `MESH_BY_NUMBER`: divide by counts
            - `MESH_BY_MAX_SIZE`: divide by maximum size
            - `MESH_BY_POINTS_ON_EDGE`: divide by points on edges
            - `COOKIE_CUT_BY_LINES`: cookie-cut using lines
            - `COOKIE_CUT_BY_POINTS`: cookie-cut using points
            - `GENERAL_DIVIDE`: general division
        n1, n2: Division counts for `MESH_BY_NUMBER`
        max_size1, max_size2: Maximum sizes for `MESH_BY_MAX_SIZE`
        point_on_edge_from_line: Include edge points derived from lines
        point_on_edge_from_point: Include edge points derived from points
        extend_cookie_cut_lines: Whether cookie-cut lines should be extended
        rotation: Rotation angle
        max_size_general: General maximum size
        local_axes_on_edge: Preserve local axes on edges
        local_axes_on_face: Preserve local axes on faces
        restraints_on_edge: Preserve restraints on edges
        restraints_on_face: Preserve restraints on faces
        group: Group name
        sub_mesh: Whether to generate submesh
        sub_mesh_size: Submesh size
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        # Divide by count (4x4)
        set_area_auto_mesh(model, "1", AreaMeshType.MESH_BY_NUMBER, n1=4, n2=4)
        
        # Divide by maximum size
        set_area_auto_mesh(model, "1", AreaMeshType.MESH_BY_MAX_SIZE, max_size1=0.5, max_size2=0.5)
    """
    return model.AreaObj.SetAutoMesh(
        str(area_name), int(mesh_type), n1, n2, max_size1, max_size2,
        point_on_edge_from_line, point_on_edge_from_point,
        extend_cookie_cut_lines, rotation, max_size_general,
        local_axes_on_edge, local_axes_on_face,
        restraints_on_edge, restraints_on_face,
        group, sub_mesh, sub_mesh_size, int(item_type)
    )


def set_area_auto_mesh_data(
    model,
    area_name: str,
    data: AreaAutoMeshData,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Configure area automatic meshing from a data object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        data: `AreaAutoMeshData` instance
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        data = AreaAutoMeshData(mesh_type=AreaMeshType.MESH_BY_NUMBER, n1=4, n2=4)
        set_area_auto_mesh_data(model, "1", data)
    """
    return model.AreaObj.SetAutoMesh(
        str(area_name), int(data.mesh_type), data.n1, data.n2,
        data.max_size1, data.max_size2,
        data.point_on_edge_from_line, data.point_on_edge_from_point,
        data.extend_cookie_cut_lines, data.rotation, data.max_size_general,
        data.local_axes_on_edge, data.local_axes_on_face,
        data.restraints_on_edge, data.restraints_on_face,
        data.group, data.sub_mesh, data.sub_mesh_size, int(item_type)
    )


def get_area_auto_mesh(
    model,
    area_name: str
) -> Optional[AreaAutoMeshData]:
    """
    Get automatic meshing settings for an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `AreaAutoMeshData`, or `None` if the query fails.
        
    Example:
        data = get_area_auto_mesh(model, "1")
        if data:
            print(f"Mesh type: {data.mesh_type}")
            print(f"Divisions: {data.n1} x {data.n2}")
    """
    try:
        result = model.AreaObj.GetAutoMesh(
            str(area_name), 0, 0, 0, 0.0, 0.0, False, False, False, 0.0, 0.0,
            False, False, False, False, "", False, 0.0
        )
        mesh_type_val = com_data(result, 0)
        if mesh_type_val is not None:
            return AreaAutoMeshData(
                mesh_type=AreaMeshType(mesh_type_val) if mesh_type_val is not None else AreaMeshType.NO_MESH,
                n1=com_data(result, 1, 2) or 2,
                n2=com_data(result, 2, 2) or 2,
                max_size1=com_data(result, 3, 0.0) or 0.0,
                max_size2=com_data(result, 4, 0.0) or 0.0,
                point_on_edge_from_line=com_data(result, 5, False) or False,
                point_on_edge_from_point=com_data(result, 6, False) or False,
                extend_cookie_cut_lines=com_data(result, 7, False) or False,
                rotation=com_data(result, 8, 0.0) or 0.0,
                max_size_general=com_data(result, 9, 0.0) or 0.0,
                local_axes_on_edge=com_data(result, 10, False) or False,
                local_axes_on_face=com_data(result, 11, False) or False,
                restraints_on_edge=com_data(result, 12, False) or False,
                restraints_on_face=com_data(result, 13, False) or False,
                group=com_data(result, 14, "ALL") or "ALL",
                sub_mesh=com_data(result, 15, False) or False,
                sub_mesh_size=com_data(result, 16, 0.0) or 0.0
            )
    except Exception:
        pass
    return None


def is_area_meshed(
    model,
    area_name: str
) -> bool:
    """
    Check whether automatic meshing is enabled for an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `True` if automatic meshing is configured, otherwise `False`.
    """
    data = get_area_auto_mesh(model, area_name)
    if data:
        return data.mesh_type != AreaMeshType.NO_MESH
    return False
