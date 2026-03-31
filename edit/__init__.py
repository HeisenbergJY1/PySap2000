# -*- coding: utf-8 -*-
"""
edit - edit operation helpers

Wrappers for SAP2000 Edit APIs.

Submodules:
- edit_area: Area editing
- edit_frame: Frame editing
- edit_point: Point editing
- edit_solid: Solid editing
- edit_general: General editing
"""

from .edit_area import (
    divide_area,
    expand_shrink_area,
    merge_area,
    add_point_to_area,
    remove_point_from_area,
    change_area_connectivity,
)

from .edit_frame import (
    divide_frame_at_distance,
    divide_frame_at_intersections,
    divide_frame_by_ratio,
    extend_frame,
    join_frame,
    trim_frame,
    change_frame_connectivity,
)

from .edit_point import (
    align_point,
    connect_point,
    disconnect_point,
    merge_point,
    change_point_coordinates,
)

from .edit_solid import (
    divide_solid,
)

from .edit_general import (
    extrude_area_to_solid_linear_normal,
    extrude_area_to_solid_linear_user,
    extrude_area_to_solid_radial,
    extrude_frame_to_area_linear,
    extrude_frame_to_area_radial,
    extrude_point_to_frame_linear,
    extrude_point_to_frame_radial,
    move_selected,
    replicate_linear,
    replicate_mirror,
    replicate_radial,
)

__all__ = [
    # Area editing
    "divide_area",
    "expand_shrink_area",
    "merge_area",
    "add_point_to_area",
    "remove_point_from_area",
    "change_area_connectivity",
    # Frame editing
    "divide_frame_at_distance",
    "divide_frame_at_intersections",
    "divide_frame_by_ratio",
    "extend_frame",
    "join_frame",
    "trim_frame",
    "change_frame_connectivity",
    # Point editing
    "align_point",
    "connect_point",
    "disconnect_point",
    "merge_point",
    "change_point_coordinates",
    # Solid editing
    "divide_solid",
    # General editing
    "extrude_area_to_solid_linear_normal",
    "extrude_area_to_solid_linear_user",
    "extrude_area_to_solid_radial",
    "extrude_frame_to_area_linear",
    "extrude_frame_to_area_radial",
    "extrude_point_to_frame_linear",
    "extrude_point_to_frame_radial",
    "move_selected",
    "replicate_linear",
    "replicate_mirror",
    "replicate_radial",
]
