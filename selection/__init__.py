# -*- coding: utf-8 -*-
"""
select - 全局选择操作模块

用于 SAP2000 中的批量选择操作 (SelectObj API)

注意: 这是全局选择操作模块，用于批量选择对象。
单个对象的选择状态请使用:
- types_for_frames/frame_selection.py
- types_for_links/link_selection.py
- types_for_areas/area_selection.py
- types_for_points/point_selection.py

SAP2000 API:
- SelectObj.All - 选择/取消选择所有对象
- SelectObj.ClearSelection - 清除选择
- SelectObj.InvertSelection - 反转选择
- SelectObj.PreviousSelection - 恢复上一次选择
- SelectObj.GetSelected - 获取已选择对象列表
- SelectObj.Group - 按组选择
- SelectObj.Constraint - 按约束选择
- SelectObj.CoordinateRange - 按坐标范围选择
- SelectObj.PlaneXY/XZ/YZ - 按平面选择
- SelectObj.LinesParallelToCoordAxis - 选择平行于坐标轴的线
- SelectObj.LinesParallelToLine - 选择平行于指定线的线
- SelectObj.PropertyFrame/Area/Link/... - 按属性选择
- SelectObj.SupportedPoints - 选择有支座的节点

Usage:
    from PySap2000.selection import (
        select_all, clear_selection, get_selected,
        select_by_group, select_by_property_frame,
        select_by_coordinate_range
    )
    
    # 选择所有对象
    select_all(model)
    
    # 获取已选择对象
    selected = get_selected(model)
    for obj_type, obj_name in selected:
        print(f"{obj_type}: {obj_name}")
    
    # 按组选择
    select_by_group(model, "Beams")
    
    # 按坐标范围选择
    select_by_coordinate_range(model, 0, 10, 0, 10, 0, 5)
"""

from .select import (
    # 基础选择操作
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
    
    # 按组/约束选择
    select_by_group,
    deselect_by_group,
    select_by_constraint,
    deselect_by_constraint,
    
    # 按几何位置选择
    select_by_coordinate_range,
    select_by_plane_xy,
    select_by_plane_xz,
    select_by_plane_yz,
    select_lines_parallel_to_coord_axis,
    select_lines_parallel_to_line,
    
    # 按属性选择
    select_by_property_frame,
    select_by_property_area,
    select_by_property_cable,
    select_by_property_tendon,
    select_by_property_link,
    select_by_property_link_fd,
    select_by_property_solid,
    select_by_property_material,
    
    # 按支座选择
    select_supported_points,
)

from .enums import SelectObjectType

__all__ = [
    # 基础选择操作
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
    
    # 按组/约束选择
    "select_by_group",
    "deselect_by_group",
    "select_by_constraint",
    "deselect_by_constraint",
    
    # 按几何位置选择
    "select_by_coordinate_range",
    "select_by_plane_xy",
    "select_by_plane_xz",
    "select_by_plane_yz",
    "select_lines_parallel_to_coord_axis",
    "select_lines_parallel_to_line",
    
    # 按属性选择
    "select_by_property_frame",
    "select_by_property_area",
    "select_by_property_cable",
    "select_by_property_tendon",
    "select_by_property_link",
    "select_by_property_link_fd",
    "select_by_property_solid",
    "select_by_property_material",
    
    # 按支座选择
    "select_supported_points",
    
    # 枚举
    "SelectObjectType",
]

# AI Agent 友好的 API 分类
SELECT_API_CATEGORIES = {
    "basic_selection": {
        "description": "基础选择操作",
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
        "description": "按组/约束选择",
        "functions": [
            "select_by_group",
            "deselect_by_group",
            "select_by_constraint",
            "deselect_by_constraint",
        ],
    },
    "geometry_selection": {
        "description": "按几何位置选择",
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
        "description": "按属性选择",
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
        "description": "按支座选择",
        "functions": ["select_supported_points"],
    },
    "enums": {
        "description": "选择相关枚举",
        "items": ["SelectObjectType"],
    },
}
