# -*- coding: utf-8 -*-
"""
select.py - Global selection operation helpers

Wraps the SAP2000 `SelectObj` API.

This module provides global helpers for batch object selection.
For per-object selection state, use each module's `selection.py` (for example `frame/selection.py`).

SAP2000 API:
- `SelectObj.All(DeSelect)` - Select or deselect all objects
- `SelectObj.ClearSelection()` - Clear the current selection
- `SelectObj.InvertSelection()` - Invert the current selection
- `SelectObj.PreviousSelection()` - Restore the previous selection
- `SelectObj.GetSelected(NumberItems, ObjectType[], ObjectName[])` - Get selected objects
- `SelectObj.Group(Name, DeSelect)` - Select by group
- `SelectObj.Constraint(Name, DeSelect)` - Select by constraint
- `SelectObj.CoordinateRange(...)` - Select by coordinate range
- `SelectObj.PlaneXY/XZ/YZ(Name, DeSelect)` - Select by plane
- `SelectObj.LinesParallelToCoordAxis(ParallelTo[], ...)` - Select lines parallel to a coordinate axis
- `SelectObj.LinesParallelToLine(Name, DeSelect)` - Select lines parallel to a reference line
- `SelectObj.PropertyFrame/Area/Link/...(Name, DeSelect)` - Select by property
- `SelectObj.SupportedPoints(DOF[], ...)` - Select supported points

Usage:
    from PySap2000.selection import select_all, get_selected, select_by_group
    
    # Select all
    select_all(model)
    
    # Get selected objects
    for obj_type, obj_name in get_selected(model):
        print(f"{obj_type}: {obj_name}")
"""

from typing import List, Tuple, Optional

from .enums import SelectObjectType
from PySap2000.com_helper import com_ret, com_data


# ==================== Basic selection operations ====================

def select_all(model) -> int:
    """
    Select all objects
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `0` on success
        
    Example:
        select_all(model)
    """
    return model.SelectObj.All(False)


def deselect_all(model) -> int:
    """
    Deselect all objects
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `0` on success
        
    Example:
        deselect_all(model)
    """
    return model.SelectObj.All(True)


def clear_selection(model) -> int:
    """
    Clear the current selection
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `0` on success
        
    Example:
        clear_selection(model)
    """
    return model.SelectObj.ClearSelection()


def invert_selection(model) -> int:
    """
    Invert the current selection
    
    Deselect currently selected objects and select the unselected ones.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `0` on success
        
    Example:
        invert_selection(model)
    """
    return model.SelectObj.InvertSelection()


def previous_selection(model) -> int:
    """
    Restore the previous selection
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `0` on success
        
    Example:
        previous_selection(model)
    """
    return model.SelectObj.PreviousSelection()


def get_selected(model) -> List[Tuple[SelectObjectType, str]]:
    """
    Get the list of selected objects
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        List of `(object_type, object_name)` tuples
        
    Example:
        selected = get_selected(model)
        for obj_type, obj_name in selected:
            print(f"{obj_type.name}: {obj_name}")
    """
    result = model.SelectObj.GetSelected(0, [], [])
    
    num_items = com_data(result, 0, default=0)
    if num_items > 0:
        obj_types = com_data(result, 1)
        obj_names = com_data(result, 2)
        if obj_types and obj_names:
            return [
                (SelectObjectType(obj_types[i]), obj_names[i])
                for i in range(num_items)
            ]
    
    return []


def get_selected_raw(model) -> List[Tuple[int, str]]:
    """
    Get the selected object list in raw form
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        List of `(object_type_int, object_name)` tuples
        
    Example:
        selected = get_selected_raw(model)
        for obj_type, obj_name in selected:
            print(f"Type {obj_type}: {obj_name}")
    """
    result = model.SelectObj.GetSelected(0, [], [])
    
    num_items = com_data(result, 0, default=0)
    if num_items > 0:
        obj_types = com_data(result, 1)
        obj_names = com_data(result, 2)
        if obj_types and obj_names:
            return [(obj_types[i], obj_names[i]) for i in range(num_items)]
    
    return []


def get_selected_count(model) -> int:
    """
    Get the number of selected objects
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Number of selected objects
    """
    result = model.SelectObj.GetSelected(0, [], [])
    
    return com_data(result, 0, default=0)


def get_selected_by_type(model, object_type: SelectObjectType) -> List[str]:
    """
    Get selected objects of a given type
    
    Args:
        model: SAP2000 SapModel object
        object_type: Object type
        
    Returns:
        List of object names
        
    Example:
        frames = get_selected_by_type(model, SelectObjectType.FRAME)
    """
    selected = get_selected_raw(model)
    return [name for obj_type, name in selected if obj_type == int(object_type)]


# ==================== Group / constraint selection ====================

def select_by_group(model, group_name: str) -> int:
    """
    Select objects by group
    
    Args:
        model: SAP2000 SapModel object
        group_name: Group name
        
    Returns:
        `0` on success
        
    Example:
        select_by_group(model, "Beams")
    """
    return model.SelectObj.Group(group_name, False)


def deselect_by_group(model, group_name: str) -> int:
    """
    Deselect objects by group
    
    Args:
        model: SAP2000 SapModel object
        group_name: Group name
        
    Returns:
        `0` on success
        
    Example:
        deselect_by_group(model, "Beams")
    """
    return model.SelectObj.Group(group_name, True)


def select_by_constraint(model, constraint_name: str) -> int:
    """
    Select points by constraint
    
    Select all points assigned to the specified constraint.
    
    Args:
        model: SAP2000 SapModel object
        constraint_name: Constraint name
        
    Returns:
        `0` on success
        
    Example:
        select_by_constraint(model, "Diaph1")
    """
    return model.SelectObj.Constraint(constraint_name, False)


def deselect_by_constraint(model, constraint_name: str) -> int:
    """
    Deselect points by constraint
    
    Args:
        model: SAP2000 SapModel object
        constraint_name: Constraint name
        
    Returns:
        `0` on success
        
    Example:
        deselect_by_constraint(model, "Diaph1")
    """
    return model.SelectObj.Constraint(constraint_name, True)


# ==================== Geometric selection ====================

def select_by_coordinate_range(
    model,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    z_min: float,
    z_max: float,
    deselect: bool = False,
    csys: str = "Global",
    include_intersections: bool = False,
    point: bool = True,
    line: bool = True,
    area: bool = True,
    solid: bool = True,
    link: bool = True
) -> int:
    """
    Select objects by coordinate range
    
    Args:
        model: SAP2000 SapModel object
        x_min, x_max: X-coordinate range
        y_min, y_max: Y-coordinate range
        z_min, z_max: Z-coordinate range
        deselect: `False` to select, `True` to deselect
        csys: Coordinate system name
        include_intersections: `True` to include intersecting objects, `False` for only fully contained objects
        point: Whether to include points
        line: Whether to include line objects
        area: Whether to include area objects
        solid: Whether to include solid objects
        link: Whether to include link objects
        
    Returns:
        `0` on success
        
    Example:
        # Select all objects within X:0-10, Y:0-10, Z:0-5
        select_by_coordinate_range(model, 0, 10, 0, 10, 0, 5)
        
        # Select only frame/line objects
        select_by_coordinate_range(model, 0, 10, 0, 10, 0, 5, 
                                   point=False, area=False, solid=False, link=False)
    """
    return model.SelectObj.CoordinateRange(
        x_min, x_max, y_min, y_max, z_min, z_max,
        deselect, csys, include_intersections,
        point, line, area, solid, link
    )


def select_by_plane_xy(model, point_name: str, deselect: bool = False) -> int:
    """
    Select objects in the same XY plane as a point
    
    Args:
        model: SAP2000 SapModel object
        point_name: Point name
        deselect: `False` to select, `True` to deselect
        
    Returns:
        `0` on success
        
    Example:
        select_by_plane_xy(model, "3")
    """
    return model.SelectObj.PlaneXY(str(point_name), deselect)


def select_by_plane_xz(model, point_name: str, deselect: bool = False) -> int:
    """
    Select objects in the same XZ plane as a point
    
    Args:
        model: SAP2000 SapModel object
        point_name: Point name
        deselect: `False` to select, `True` to deselect
        
    Returns:
        `0` on success
        
    Example:
        select_by_plane_xz(model, "3")
    """
    return model.SelectObj.PlaneXZ(str(point_name), deselect)


def select_by_plane_yz(model, point_name: str, deselect: bool = False) -> int:
    """
    Select objects in the same YZ plane as a point
    
    Args:
        model: SAP2000 SapModel object
        point_name: Point name
        deselect: `False` to select, `True` to deselect
        
    Returns:
        `0` on success
        
    Example:
        select_by_plane_yz(model, "3")
    """
    return model.SelectObj.PlaneYZ(str(point_name), deselect)


def select_lines_parallel_to_coord_axis(
    model,
    parallel_to: List[bool],
    csys: str = "Global",
    tolerance: float = 0.057,
    deselect: bool = False
) -> int:
    """
    Select line objects parallel to a coordinate axis or plane
    
    Args:
        model: SAP2000 SapModel object
        parallel_to: List of 6 booleans
            [0] = X axis
            [1] = Y axis
            [2] = Z axis
            [3] = XY plane
            [4] = XZ plane
            [5] = YZ plane
        csys: Coordinate system name
        tolerance: Angular tolerance [deg]
        deselect: `False` to select, `True` to deselect
        
    Returns:
        `0` on success
        
    Example:
        # Select lines parallel to the Z axis
        select_lines_parallel_to_coord_axis(model, [False, False, True, False, False, False])
        
        # Select lines parallel to the XY plane
        select_lines_parallel_to_coord_axis(model, [False, False, False, True, False, False])
    """
    # Ensure the list has length 6
    if len(parallel_to) < 6:
        parallel_to = parallel_to + [False] * (6 - len(parallel_to))
    
    return model.SelectObj.LinesParallelToCoordAxis(parallel_to, csys, tolerance, deselect)


def select_lines_parallel_to_line(model, line_name: str, deselect: bool = False) -> int:
    """
    Select all line objects parallel to a reference line
    
    Args:
        model: SAP2000 SapModel object
        line_name: Line object name
        deselect: `False` to select, `True` to deselect
        
    Returns:
        `0` on success
        
    Example:
        select_lines_parallel_to_line(model, "1")
    """
    return model.SelectObj.LinesParallelToLine(str(line_name), deselect)


# ==================== Property-based selection ====================

def select_by_property_frame(model, section_name: str, deselect: bool = False) -> int:
    """
    Select by frame section property
    
    Args:
        model: SAP2000 SapModel object
        section_name: Section name
        deselect: `False` to select, `True` to deselect
        
    Returns:
        `0` on success
        
    Example:
        select_by_property_frame(model, "FSEC1")
    """
    return model.SelectObj.PropertyFrame(section_name, deselect)


def select_by_property_area(model, section_name: str, deselect: bool = False) -> int:
    """
    Select by area section property
    
    Args:
        model: SAP2000 SapModel object
        section_name: Section name
        deselect: `False` to select, `True` to deselect
        
    Returns:
        `0` on success
        
    Example:
        select_by_property_area(model, "ASEC1")
    """
    return model.SelectObj.PropertyArea(section_name, deselect)


def select_by_property_cable(model, section_name: str, deselect: bool = False) -> int:
    """
    Select by cable property
    
    Args:
        model: SAP2000 SapModel object
        section_name: Property name
        deselect: `False` to select, `True` to deselect
        
    Returns:
        `0` on success
        
    Example:
        select_by_property_cable(model, "Cable1")
    """
    return model.SelectObj.PropertyCable(section_name, deselect)


def select_by_property_tendon(model, section_name: str, deselect: bool = False) -> int:
    """
    Select by tendon property
    
    Args:
        model: SAP2000 SapModel object
        section_name: Property name
        deselect: `False` to select, `True` to deselect
        
    Returns:
        `0` on success
        
    Example:
        select_by_property_tendon(model, "Tendon1")
    """
    return model.SelectObj.PropertyTendon(section_name, deselect)


def select_by_property_link(model, property_name: str, deselect: bool = False) -> int:
    """
    Select by link property
    
    Args:
        model: SAP2000 SapModel object
        property_name: Property name
        deselect: `False` to select, `True` to deselect
        
    Returns:
        `0` on success
        
    Example:
        select_by_property_link(model, "GAP1")
    """
    return model.SelectObj.PropertyLink(property_name, deselect)


def select_by_property_link_fd(model, property_name: str, deselect: bool = False) -> int:
    """
    Select by frequency-dependent link property
    
    Args:
        model: SAP2000 SapModel object
        property_name: Property name
        deselect: `False` to select, `True` to deselect
        
    Returns:
        `0` on success
        
    Example:
        select_by_property_link_fd(model, "FDLink1")
    """
    return model.SelectObj.PropertyLinkFD(property_name, deselect)


def select_by_property_solid(model, property_name: str, deselect: bool = False) -> int:
    """
    Select by solid property
    
    Args:
        model: SAP2000 SapModel object
        property_name: Property name
        deselect: `False` to select, `True` to deselect
        
    Returns:
        `0` on success
        
    Example:
        select_by_property_solid(model, "Solid1")
    """
    return model.SelectObj.PropertySolid(property_name, deselect)


def select_by_property_material(model, material_name: str, deselect: bool = False) -> int:
    """
    Select by material property
    
    Select all objects that use the specified material.
    
    Args:
        model: SAP2000 SapModel object
        material_name: Material name
        deselect: `False` to select, `True` to deselect
        
    Returns:
        `0` on success
        
    Example:
        select_by_property_material(model, "A992Fy50")
    """
    return model.SelectObj.PropertyMaterial(material_name, deselect)


# ==================== Support-based selection ====================

def select_supported_points(
    model,
    dof: List[bool],
    csys: str = "Local",
    deselect: bool = False,
    select_restraints: bool = True,
    select_joint_springs: bool = True,
    select_line_springs: bool = True,
    select_area_springs: bool = True,
    select_solid_springs: bool = True,
    select_one_joint_links: bool = True
) -> int:
    """
    Select supported points
    
    Args:
        model: SAP2000 SapModel object
        dof: List of 6 booleans representing the DOFs
            [0] = U1
            [1] = U2
            [2] = U3
            [3] = R1
            [4] = R2
            [5] = R3
        csys: Coordinate system name (`"Local"` or a defined coordinate system)
        deselect: `False` to select, `True` to deselect
        select_restraints: Whether to include restrained points
        select_joint_springs: Whether to include points with joint springs
        select_line_springs: Whether to include points with line spring contribution
        select_area_springs: Whether to include points with area spring contribution
        select_solid_springs: Whether to include points with solid spring contribution
        select_one_joint_links: Whether to include points with one-joint links
        
    Returns:
        `0` on success
        
    Example:
        # Select points supported in the Z direction
        select_supported_points(model, [False, False, True, False, False, False])
        
        # Select points restrained in all directions
        select_supported_points(model, [True, True, True, True, True, True])
    """
    # Ensure the list has length 6
    if len(dof) < 6:
        dof = dof + [False] * (6 - len(dof))
    
    result = model.SelectObj.SupportedPoints(
        dof, csys, deselect,
        select_restraints, select_joint_springs, select_line_springs,
        select_area_springs, select_solid_springs, select_one_joint_links
    )
    return com_ret(result)


def get_selected_objects(model) -> dict:
    """
    Get the currently selected objects grouped by type
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Dictionary grouped by type:
        {
            "points": [],   # Points
            "frames": [],   # Frames
            "cables": [],   # Cables
            "tendons": [],  # Tendons
            "areas": [],    # Areas
            "solids": [],   # Solids
            "links": []     # Links
        }
        
    Example:
        selected = get_selected_objects(model)
        print(f"Selected {len(selected['frames'])} frames")
        print(f"Selected {len(selected['areas'])} areas")
        
        # Iterate over selected areas
        for area_name in selected["areas"]:
            print(area_name)
    """
    result = model.SelectObj.GetSelected(0, [], [])
    
    classified = {
        "points": [],
        "frames": [],
        "cables": [],
        "tendons": [],
        "areas": [],
        "solids": [],
        "links": []
    }
    
    obj_types = com_data(result, 1)
    obj_names = com_data(result, 2)
    
    if not obj_types or not obj_names:
        return classified
    
    # Object types: 1=Point, 2=Frame, 3=Cable, 4=Tendon, 5=Area, 6=Solid, 7=Link
    type_map = {
        1: "points",
        2: "frames",
        3: "cables",
        4: "tendons",
        5: "areas",
        6: "solids",
        7: "links"
    }
    
    for obj_type, obj_name in zip(obj_types, obj_names):
        key = type_map.get(obj_type)
        if key:
            classified[key].append(obj_name)
    
    return classified
