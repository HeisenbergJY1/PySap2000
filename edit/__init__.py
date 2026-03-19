# -*- coding: utf-8 -*-
"""
edit - 编辑操作模块

SAP2000 Edit API 封装

子模块:
- edit_area: 面单元编辑
- edit_frame: 框架编辑
- edit_point: 点编辑
- edit_solid: 实体编辑
- edit_general: 通用编辑
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
    # 面单元编辑
    "divide_area",
    "expand_shrink_area",
    "merge_area",
    "add_point_to_area",
    "remove_point_from_area",
    "change_area_connectivity",
    # 框架编辑
    "divide_frame_at_distance",
    "divide_frame_at_intersections",
    "divide_frame_by_ratio",
    "extend_frame",
    "join_frame",
    "trim_frame",
    "change_frame_connectivity",
    # 点编辑
    "align_point",
    "connect_point",
    "disconnect_point",
    "merge_point",
    "change_point_coordinates",
    # 实体编辑
    "divide_solid",
    # 通用编辑
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
