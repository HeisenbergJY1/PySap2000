# -*- coding: utf-8 -*-
"""
selection - Global selection operations.

Provides batch selection helpers for SAP2000 through the `SelectObj` API.

Note:
    This package handles global selection operations across many objects.
    For per-object selection state, use each module's `selection.py`:
    - `frame/selection.py`
    - `link/selection.py`
    - `area/selection.py`
    - `point/` (via `Point.set_selected`)

SAP2000 API:
- `SelectObj.All` - Select or deselect all objects
- `SelectObj.ClearSelection` - Clear the current selection
- `SelectObj.InvertSelection` - Invert the current selection
- `SelectObj.PreviousSelection` - Restore the previous selection
- `SelectObj.GetSelected` - Get the selected object list
- `SelectObj.Group` - Select by group
- `SelectObj.Constraint` - Select by constraint
- `SelectObj.CoordinateRange` - Select by coordinate range
- `SelectObj.PlaneXY/XZ/YZ` - Select by plane
- `SelectObj.LinesParallelToCoordAxis` - Select lines parallel to an axis
- `SelectObj.LinesParallelToLine` - Select lines parallel to a reference line
- `SelectObj.PropertyFrame/Area/Link/...` - Select by property
- `SelectObj.SupportedPoints` - Select supported points

Usage:
    from PySap2000.selection import (
        select_all, clear_selection, get_selected,
        select_by_group, select_by_property_frame,
        select_by_coordinate_range
    )
    
    # Select all objects
    select_all(model)
    
    # Get selected objects
    selected = get_selected(model)
    for obj_type, obj_name in selected:
        print(f"{obj_type}: {obj_name}")
    
    # Select by group
    select_by_group(model, "Beams")
    
    # Select by coordinate range
    select_by_coordinate_range(model, 0, 10, 0, 10, 0, 5)
"""

from .select import (
    # Basic selection operations
    select_all,
    deselect_all,
    clear_selection,
    invert_selection,
    previous_selection,
    get_selected,
    get_selected_raw,
    get_selected_count,
    get_selected_by_type,
    get_selected_objects,
    
    # Group / constraint selection
    select_by_group,
    deselect_by_group,
    select_by_constraint,
    deselect_by_constraint,
    
    # Geometric selection
    select_by_coordinate_range,
    select_by_plane_xy,
    select_by_plane_xz,
    select_by_plane_yz,
    select_lines_parallel_to_coord_axis,
    select_lines_parallel_to_line,
    
    # Property-based selection
    select_by_property_frame,
    select_by_property_area,
    select_by_property_cable,
    select_by_property_tendon,
    select_by_property_link,
    select_by_property_link_fd,
    select_by_property_solid,
    select_by_property_material,
    
    # Support-based selection
    select_supported_points,
)

from .enums import SelectObjectType

__all__ = [
    # Basic selection operations
    "select_all",
    "deselect_all",
    "clear_selection",
    "invert_selection",
    "previous_selection",
    "get_selected",
    "get_selected_raw",
    "get_selected_count",
    "get_selected_by_type",
    "get_selected_objects",
    
    # Group / constraint selection
    "select_by_group",
    "deselect_by_group",
    "select_by_constraint",
    "deselect_by_constraint",
    
    # Geometric selection
    "select_by_coordinate_range",
    "select_by_plane_xy",
    "select_by_plane_xz",
    "select_by_plane_yz",
    "select_lines_parallel_to_coord_axis",
    "select_lines_parallel_to_line",
    
    # Property-based selection
    "select_by_property_frame",
    "select_by_property_area",
    "select_by_property_cable",
    "select_by_property_tendon",
    "select_by_property_link",
    "select_by_property_link_fd",
    "select_by_property_solid",
    "select_by_property_material",
    
    # Support-based selection
    "select_supported_points",
    
    # Enums
    "SelectObjectType",
]

# API categories for discoverability
SELECT_API_CATEGORIES = {
    "basic_selection": {
        "description": "Basic selection operations",
        "functions": [
            "select_all",
            "deselect_all", 
            "clear_selection",
            "invert_selection",
            "previous_selection",
            "get_selected",
            "get_selected_raw",
            "get_selected_count",
            "get_selected_by_type",
            "get_selected_objects",
        ],
    },
    "group_constraint_selection": {
        "description": "Selection by group or constraint",
        "functions": [
            "select_by_group",
            "deselect_by_group",
            "select_by_constraint",
            "deselect_by_constraint",
        ],
    },
    "geometry_selection": {
        "description": "Selection by geometric location",
        "functions": [
            "select_by_coordinate_range",
            "select_by_plane_xy",
            "select_by_plane_xz",
            "select_by_plane_yz",
            "select_lines_parallel_to_coord_axis",
            "select_lines_parallel_to_line",
        ],
    },
    "property_selection": {
        "description": "Selection by property",
        "functions": [
            "select_by_property_frame",
            "select_by_property_area",
            "select_by_property_cable",
            "select_by_property_tendon",
            "select_by_property_link",
            "select_by_property_link_fd",
            "select_by_property_solid",
            "select_by_property_material",
        ],
    },
    "support_selection": {
        "description": "Selection by support condition",
        "functions": ["select_supported_points"],
    },
    "enums": {
        "description": "Selection-related enums",
        "items": ["SelectObjectType"],
    },
}
