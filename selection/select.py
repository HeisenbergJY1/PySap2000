# -*- coding: utf-8 -*-
"""
select.py - 全局选择操作函数

对应 SAP2000 的 SelectObj API

这是全局选择操作模块，用于批量选择对象。
单个对象的选择状态请使用 types_for_xxx/xx_selection.py

SAP2000 API:
- SelectObj.All(DeSelect) - 选择/取消选择所有对象
- SelectObj.ClearSelection() - 清除选择
- SelectObj.InvertSelection() - 反转选择
- SelectObj.PreviousSelection() - 恢复上一次选择
- SelectObj.GetSelected(NumberItems, ObjectType[], ObjectName[]) - 获取已选择对象
- SelectObj.Group(Name, DeSelect) - 按组选择
- SelectObj.Constraint(Name, DeSelect) - 按约束选择
- SelectObj.CoordinateRange(...) - 按坐标范围选择
- SelectObj.PlaneXY/XZ/YZ(Name, DeSelect) - 按平面选择
- SelectObj.LinesParallelToCoordAxis(ParallelTo[], ...) - 选择平行于坐标轴的线
- SelectObj.LinesParallelToLine(Name, DeSelect) - 选择平行于指定线的线
- SelectObj.PropertyFrame/Area/Link/...(Name, DeSelect) - 按属性选择
- SelectObj.SupportedPoints(DOF[], ...) - 选择有支座的节点

Usage:
    from PySap2000.selection import select_all, get_selected, select_by_group
    
    # 选择所有
    select_all(model)
    
    # 获取已选择对象
    for obj_type, obj_name in get_selected(model):
        print(f"{obj_type}: {obj_name}")
"""

from typing import List, Tuple, Optional

from .enums import SelectObjectType
from PySap2000.com_helper import com_ret, com_data


# ==================== 基础选择操作 ====================

def select_all(model) -> int:
    """
    选择所有对象
    
    Args:
        model: SapModel 对象
        
    Returns:
        0 表示成功
        
    Example:
        select_all(model)
    """
    return model.SelectObj.All(False)


def deselect_all(model) -> int:
    """
    取消选择所有对象
    
    Args:
        model: SapModel 对象
        
    Returns:
        0 表示成功
        
    Example:
        deselect_all(model)
    """
    return model.SelectObj.All(True)


def clear_selection(model) -> int:
    """
    清除选择
    
    Args:
        model: SapModel 对象
        
    Returns:
        0 表示成功
        
    Example:
        clear_selection(model)
    """
    return model.SelectObj.ClearSelection()


def invert_selection(model) -> int:
    """
    反转选择
    
    取消选择已选对象，选择未选对象
    
    Args:
        model: SapModel 对象
        
    Returns:
        0 表示成功
        
    Example:
        invert_selection(model)
    """
    return model.SelectObj.InvertSelection()


def previous_selection(model) -> int:
    """
    恢复上一次选择
    
    Args:
        model: SapModel 对象
        
    Returns:
        0 表示成功
        
    Example:
        previous_selection(model)
    """
    return model.SelectObj.PreviousSelection()


def get_selected(model) -> List[Tuple[SelectObjectType, str]]:
    """
    获取已选择对象列表
    
    Args:
        model: SapModel 对象
        
    Returns:
        (对象类型, 对象名称) 元组列表
        
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
    获取已选择对象列表 (原始格式)
    
    Args:
        model: SapModel 对象
        
    Returns:
        (对象类型整数, 对象名称) 元组列表
        
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
    获取已选择对象数量
    
    Args:
        model: SapModel 对象
        
    Returns:
        已选择对象数量
    """
    result = model.SelectObj.GetSelected(0, [], [])
    
    return com_data(result, 0, default=0)


def get_selected_by_type(model, object_type: SelectObjectType) -> List[str]:
    """
    获取指定类型的已选择对象
    
    Args:
        model: SapModel 对象
        object_type: 对象类型
        
    Returns:
        对象名称列表
        
    Example:
        frames = get_selected_by_type(model, SelectObjectType.FRAME)
    """
    selected = get_selected_raw(model)
    return [name for obj_type, name in selected if obj_type == int(object_type)]


# ==================== 按组/约束选择 ====================

def select_by_group(model, group_name: str) -> int:
    """
    按组选择对象
    
    Args:
        model: SapModel 对象
        group_name: 组名称
        
    Returns:
        0 表示成功
        
    Example:
        select_by_group(model, "Beams")
    """
    return model.SelectObj.Group(group_name, False)


def deselect_by_group(model, group_name: str) -> int:
    """
    按组取消选择对象
    
    Args:
        model: SapModel 对象
        group_name: 组名称
        
    Returns:
        0 表示成功
        
    Example:
        deselect_by_group(model, "Beams")
    """
    return model.SelectObj.Group(group_name, True)


def select_by_constraint(model, constraint_name: str) -> int:
    """
    按约束选择节点
    
    选择分配了指定约束的所有节点
    
    Args:
        model: SapModel 对象
        constraint_name: 约束名称
        
    Returns:
        0 表示成功
        
    Example:
        select_by_constraint(model, "Diaph1")
    """
    return model.SelectObj.Constraint(constraint_name, False)


def deselect_by_constraint(model, constraint_name: str) -> int:
    """
    按约束取消选择节点
    
    Args:
        model: SapModel 对象
        constraint_name: 约束名称
        
    Returns:
        0 表示成功
        
    Example:
        deselect_by_constraint(model, "Diaph1")
    """
    return model.SelectObj.Constraint(constraint_name, True)


# ==================== 按几何位置选择 ====================

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
    按坐标范围选择对象
    
    Args:
        model: SapModel 对象
        x_min, x_max: X坐标范围
        y_min, y_max: Y坐标范围
        z_min, z_max: Z坐标范围
        deselect: False=选择, True=取消选择
        csys: 坐标系名称
        include_intersections: True=包含相交对象, False=仅完全在范围内的对象
        point: 是否选择节点
        line: 是否选择线对象
        area: 是否选择面对象
        solid: 是否选择实体对象
        link: 是否选择连接单元
        
    Returns:
        0 表示成功
        
    Example:
        # 选择 X:0-10, Y:0-10, Z:0-5 范围内的所有对象
        select_by_coordinate_range(model, 0, 10, 0, 10, 0, 5)
        
        # 仅选择杆件
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
    选择与指定节点同一XY平面的对象
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        deselect: False=选择, True=取消选择
        
    Returns:
        0 表示成功
        
    Example:
        select_by_plane_xy(model, "3")
    """
    return model.SelectObj.PlaneXY(str(point_name), deselect)


def select_by_plane_xz(model, point_name: str, deselect: bool = False) -> int:
    """
    选择与指定节点同一XZ平面的对象
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        deselect: False=选择, True=取消选择
        
    Returns:
        0 表示成功
        
    Example:
        select_by_plane_xz(model, "3")
    """
    return model.SelectObj.PlaneXZ(str(point_name), deselect)


def select_by_plane_yz(model, point_name: str, deselect: bool = False) -> int:
    """
    选择与指定节点同一YZ平面的对象
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        deselect: False=选择, True=取消选择
        
    Returns:
        0 表示成功
        
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
    选择平行于坐标轴或平面的线对象
    
    Args:
        model: SapModel 对象
        parallel_to: 6个布尔值的列表
            [0] = X轴
            [1] = Y轴
            [2] = Z轴
            [3] = XY平面
            [4] = XZ平面
            [5] = YZ平面
        csys: 坐标系名称
        tolerance: 角度容差 [deg]
        deselect: False=选择, True=取消选择
        
    Returns:
        0 表示成功
        
    Example:
        # 选择平行于Z轴的线
        select_lines_parallel_to_coord_axis(model, [False, False, True, False, False, False])
        
        # 选择平行于XY平面的线
        select_lines_parallel_to_coord_axis(model, [False, False, False, True, False, False])
    """
    # 确保列表长度为6
    if len(parallel_to) < 6:
        parallel_to = parallel_to + [False] * (6 - len(parallel_to))
    
    return model.SelectObj.LinesParallelToCoordAxis(parallel_to, csys, tolerance, deselect)


def select_lines_parallel_to_line(model, line_name: str, deselect: bool = False) -> int:
    """
    选择平行于指定线的所有线对象
    
    Args:
        model: SapModel 对象
        line_name: 线对象名称
        deselect: False=选择, True=取消选择
        
    Returns:
        0 表示成功
        
    Example:
        select_lines_parallel_to_line(model, "1")
    """
    return model.SelectObj.LinesParallelToLine(str(line_name), deselect)


# ==================== 按属性选择 ====================

def select_by_property_frame(model, section_name: str, deselect: bool = False) -> int:
    """
    按杆件截面属性选择
    
    Args:
        model: SapModel 对象
        section_name: 截面名称
        deselect: False=选择, True=取消选择
        
    Returns:
        0 表示成功
        
    Example:
        select_by_property_frame(model, "FSEC1")
    """
    return model.SelectObj.PropertyFrame(section_name, deselect)


def select_by_property_area(model, section_name: str, deselect: bool = False) -> int:
    """
    按面截面属性选择
    
    Args:
        model: SapModel 对象
        section_name: 截面名称
        deselect: False=选择, True=取消选择
        
    Returns:
        0 表示成功
        
    Example:
        select_by_property_area(model, "ASEC1")
    """
    return model.SelectObj.PropertyArea(section_name, deselect)


def select_by_property_cable(model, section_name: str, deselect: bool = False) -> int:
    """
    按索属性选择
    
    Args:
        model: SapModel 对象
        section_name: 属性名称
        deselect: False=选择, True=取消选择
        
    Returns:
        0 表示成功
        
    Example:
        select_by_property_cable(model, "Cable1")
    """
    return model.SelectObj.PropertyCable(section_name, deselect)


def select_by_property_tendon(model, section_name: str, deselect: bool = False) -> int:
    """
    按预应力筋属性选择
    
    Args:
        model: SapModel 对象
        section_name: 属性名称
        deselect: False=选择, True=取消选择
        
    Returns:
        0 表示成功
        
    Example:
        select_by_property_tendon(model, "Tendon1")
    """
    return model.SelectObj.PropertyTendon(section_name, deselect)


def select_by_property_link(model, property_name: str, deselect: bool = False) -> int:
    """
    按连接属性选择
    
    Args:
        model: SapModel 对象
        property_name: 属性名称
        deselect: False=选择, True=取消选择
        
    Returns:
        0 表示成功
        
    Example:
        select_by_property_link(model, "GAP1")
    """
    return model.SelectObj.PropertyLink(property_name, deselect)


def select_by_property_link_fd(model, property_name: str, deselect: bool = False) -> int:
    """
    按频率相关连接属性选择
    
    Args:
        model: SapModel 对象
        property_name: 属性名称
        deselect: False=选择, True=取消选择
        
    Returns:
        0 表示成功
        
    Example:
        select_by_property_link_fd(model, "FDLink1")
    """
    return model.SelectObj.PropertyLinkFD(property_name, deselect)


def select_by_property_solid(model, property_name: str, deselect: bool = False) -> int:
    """
    按实体属性选择
    
    Args:
        model: SapModel 对象
        property_name: 属性名称
        deselect: False=选择, True=取消选择
        
    Returns:
        0 表示成功
        
    Example:
        select_by_property_solid(model, "Solid1")
    """
    return model.SelectObj.PropertySolid(property_name, deselect)


def select_by_property_material(model, material_name: str, deselect: bool = False) -> int:
    """
    按材料属性选择
    
    选择使用指定材料的所有对象
    
    Args:
        model: SapModel 对象
        material_name: 材料名称
        deselect: False=选择, True=取消选择
        
    Returns:
        0 表示成功
        
    Example:
        select_by_property_material(model, "A992Fy50")
    """
    return model.SelectObj.PropertyMaterial(material_name, deselect)


# ==================== 按支座选择 ====================

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
    选择有支座的节点
    
    Args:
        model: SapModel 对象
        dof: 6个布尔值的列表，表示自由度
            [0] = U1
            [1] = U2
            [2] = U3
            [3] = R1
            [4] = R2
            [5] = R3
        csys: 坐标系名称 ("Local" 或已定义的坐标系)
        deselect: False=选择, True=取消选择
        select_restraints: 是否选择有约束的节点
        select_joint_springs: 是否选择有节点弹簧的节点
        select_line_springs: 是否选择有线弹簧贡献的节点
        select_area_springs: 是否选择有面弹簧贡献的节点
        select_solid_springs: 是否选择有实体弹簧贡献的节点
        select_one_joint_links: 是否选择有单节点连接的节点
        
    Returns:
        0 表示成功
        
    Example:
        # 选择Z方向有支座的节点
        select_supported_points(model, [False, False, True, False, False, False])
        
        # 选择所有方向有约束的节点
        select_supported_points(model, [True, True, True, True, True, True])
    """
    # 确保列表长度为6
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
    获取当前选中的对象，按类型分类
    
    Args:
        model: SapModel 对象
        
    Returns:
        按类型分类的字典:
        {
            "points": [],   # 节点
            "frames": [],   # 杆件
            "cables": [],   # 索
            "tendons": [],  # 预应力筋
            "areas": [],    # 面单元
            "solids": [],   # 实体
            "links": []     # 连接单元
        }
        
    Example:
        selected = get_selected_objects(model)
        print(f"选中了 {len(selected['frames'])} 个杆件")
        print(f"选中了 {len(selected['areas'])} 个面单元")
        
        # 遍历选中的面单元
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
    
    # 对象类型: 1=Point, 2=Frame, 3=Cable, 4=Tendon, 5=Area, 6=Solid, 7=Link
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
