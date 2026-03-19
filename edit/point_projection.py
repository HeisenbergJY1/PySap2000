# -*- coding: utf-8 -*-
"""
point_projection.py - 点投影功能

将节点投影到直线或杆件上

功能:
- project_point_to_line: 将点投影到由两点定义的直线上
- project_points_to_line: 批量投影多个点到直线上
- project_point_to_frame: 将点投影到杆件所在直线上
- project_points_to_frame: 批量投影多个点到杆件所在直线上
- move_point_on_line: 根据比例将点移动到直线上指定位置
- move_point_to_intersection: 将点移动到两条直线的交点

Usage:
    from PySap2000.edit.point_projection import project_point_to_line, move_point_on_line
    
    # 将节点 922 投影到节点 1160 和 738 连成的直线上
    project_point_to_line(model, "922", "1160", "738")
    
    # 将节点移动到直线上 t=0.5 的位置 (中点)
    move_point_on_line(model, "922", "1160", "738", t=0.5)
    
    # 将节点移动到两条直线的交点
    move_point_to_intersection(model, "711", "559", "1064", "770", "678")
"""

from typing import List, Tuple, Union, Optional
import numpy as np


def _get_point_coord(model, point_name: str) -> Tuple[float, float, float]:
    """
    获取节点坐标 (使用当前模型单位)
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        
    Returns:
        (x, y, z) 坐标元组
    """
    ret = model.PointObj.GetCoordCartesian(str(point_name), 0.0, 0.0, 0.0)
    if isinstance(ret, (list, tuple)) and len(ret) >= 3:
        return (ret[0], ret[1], ret[2])
    raise ValueError(f"无法获取节点 {point_name} 的坐标")


def _change_point_coord(model, name: str, x: float, y: float, z: float) -> int:
    """修改节点坐标 (使用当前模型单位)"""
    return model.EditPoint.ChangeCoordinates_1(name, x, y, z, "Global")


def _calc_point_on_line(
    point_a: Tuple[float, float, float],
    point_b: Tuple[float, float, float],
    t: float
) -> Tuple[float, float, float]:
    """
    根据比例 t 计算直线 AB 上的点坐标
    
    Args:
        point_a: 起点 A (x, y, z)
        point_b: 终点 B (x, y, z)
        t: 比例，0=A点，1=B点
        
    Returns:
        点坐标 (x, y, z)
    """
    x1, y1, z1 = point_a
    x2, y2, z2 = point_b
    
    return (
        x1 + t * (x2 - x1),
        y1 + t * (y2 - y1),
        z1 + t * (z2 - z1)
    )


def _calc_lines_intersection(
    p1: Tuple[float, float, float],
    p2: Tuple[float, float, float],
    p3: Tuple[float, float, float],
    p4: Tuple[float, float, float]
) -> Optional[Tuple[float, float, float]]:
    """
    计算两条3D直线的最近点（近似交点）
    
    直线1: P1 + t * (P2 - P1)
    直线2: P3 + s * (P4 - P3)
    
    在3D空间中两条直线通常不相交，这里计算两直线最近点的中点作为"交点"
    
    Args:
        p1, p2: 直线1上的两点
        p3, p4: 直线2上的两点
        
    Returns:
        交点坐标 (x, y, z)，如果直线平行返回 None
    """
    # 方向向量
    d1 = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    d2 = np.array([p4[0] - p3[0], p4[1] - p3[1], p4[2] - p3[2]])
    
    # 起点差向量
    r = np.array([p1[0] - p3[0], p1[1] - p3[1], p1[2] - p3[2]])
    
    a = np.dot(d1, d1)  # |d1|^2
    b = np.dot(d1, d2)  # d1 · d2
    c = np.dot(d2, d2)  # |d2|^2
    d = np.dot(d1, r)   # d1 · r
    e = np.dot(d2, r)   # d2 · r
    
    denom = a * c - b * b
    
    if abs(denom) < 1e-10:
        # 直线平行
        return None
    
    # 计算参数 t 和 s
    t = (b * e - c * d) / denom
    s = (a * e - b * d) / denom
    
    # 两直线上的最近点
    point_on_line1 = np.array(p1) + t * d1
    point_on_line2 = np.array(p3) + s * d2
    
    # 返回两点的中点作为交点
    intersection = (point_on_line1 + point_on_line2) / 2
    
    return (float(intersection[0]), float(intersection[1]), float(intersection[2]))


def _calc_projection(
    point_a: Tuple[float, float, float],
    point_b: Tuple[float, float, float],
    point_p: Tuple[float, float, float]
) -> Tuple[Tuple[float, float, float], float]:
    """
    计算点 P 在直线 AB 上的投影点坐标
    
    Args:
        point_a: 直线上的点 A (x, y, z)
        point_b: 直线上的点 B (x, y, z)
        point_p: 待投影点 P (x, y, z)
        
    Returns:
        (投影点坐标, 比例t)
        - 投影点坐标: (x, y, z)
        - 比例t: 投影点在AB上的位置，0=A点，1=B点
    """
    x1, y1, z1 = point_a
    x2, y2, z2 = point_b
    x, y, z = point_p
    
    # 向量 AB
    ab = (x2 - x1, y2 - y1, z2 - z1)
    # 向量 AP
    ap = (x - x1, y - y1, z - z1)
    
    # AB · AB
    ab_dot_ab = ab[0]**2 + ab[1]**2 + ab[2]**2
    if ab_dot_ab == 0:
        return point_a, 0.0  # A、B 重合，返回 A
    
    # AP · AB
    ap_dot_ab = ap[0]*ab[0] + ap[1]*ab[1] + ap[2]*ab[2]
    
    # 参数 t (比例)
    t = ap_dot_ab / ab_dot_ab
    
    # 投影点坐标
    proj = (
        x1 + t * ab[0],
        y1 + t * ab[1],
        z1 + t * ab[2]
    )
    return proj, t


def _save_and_set_units(model):
    """保存当前单位并切换到 N-mm-C"""
    from PySap2000.global_parameters.units import Units, UnitSystem
    original = Units.get_present_units(model)
    Units.set_present_units(model, UnitSystem.N_MM_C)
    return original


def _restore_units(model, original):
    """恢复原单位"""
    from PySap2000.global_parameters.units import Units
    Units.set_present_units(model, original)


def move_point_on_line(
    model,
    point_name: str,
    line_start: Union[str, Tuple[float, float, float]],
    line_end: Union[str, Tuple[float, float, float]],
    t: float,
    apply: bool = True
) -> Tuple[float, float, float]:
    """
    根据比例 t 将点移动到直线上指定位置
    
    Args:
        model: SapModel 对象
        point_name: 要移动的节点名称
        line_start: 直线起点 (A点)，可以是节点名称或坐标元组 (x, y, z)
        line_end: 直线终点 (B点)，可以是节点名称或坐标元组 (x, y, z)
        t: 比例值
            - t=0: 移动到起点 A
            - t=1: 移动到终点 B
            - t=0.5: 移动到中点
            - 0<t<1: 在线段内部
        apply: 是否应用修改 (True=修改节点坐标, False=仅计算)
        
    Returns:
        新坐标 (x, y, z)，单位为 mm
        
    Example:
        # 将节点移动到直线中点
        coord = move_point_on_line(model, "520", "778", "453", t=0.5)
        
        # 将节点移动到距起点 30% 的位置
        coord = move_point_on_line(model, "520", "778", "453", t=0.3)
    """
    # 保存并切换单位
    original_units = _save_and_set_units(model)
    
    try:
        # 获取直线上的点坐标
        if isinstance(line_start, str):
            point_a = _get_point_coord(model, line_start)
        else:
            point_a = line_start
        
        if isinstance(line_end, str):
            point_b = _get_point_coord(model, line_end)
        else:
            point_b = line_end
        
        # 根据比例计算新坐标
        new_coord = _calc_point_on_line(point_a, point_b, t)
        
        # 应用修改
        if apply:
            _change_point_coord(model, point_name, new_coord[0], new_coord[1], new_coord[2])
        
        return new_coord
    finally:
        # 恢复原单位
        _restore_units(model, original_units)


def move_point_to_intersection(
    model,
    point_name: str,
    line1_start: Union[str, Tuple[float, float, float]],
    line1_end: Union[str, Tuple[float, float, float]],
    line2_start: Union[str, Tuple[float, float, float]],
    line2_end: Union[str, Tuple[float, float, float]],
    apply: bool = True
) -> Optional[Tuple[float, float, float]]:
    """
    将点移动到两条直线的交点
    
    在3D空间中，两条直线通常不会精确相交，此函数计算两直线最近点的中点作为"交点"。
    
    Args:
        model: SapModel 对象
        point_name: 要移动的节点名称
        line1_start: 直线1的起点，可以是节点名称或坐标元组 (x, y, z)
        line1_end: 直线1的终点
        line2_start: 直线2的起点
        line2_end: 直线2的终点
        apply: 是否应用修改 (True=修改节点坐标, False=仅计算)
        
    Returns:
        交点坐标 (x, y, z)，单位为 mm。如果直线平行返回 None
        
    Example:
        # 将节点 711 移动到直线 559-1064 和直线 770-678 的交点
        coord = move_point_to_intersection(model, "711", "559", "1064", "770", "678")
    """
    # 保存并切换单位
    original_units = _save_and_set_units(model)
    
    try:
        # 获取直线1的点坐标
        if isinstance(line1_start, str):
            p1 = _get_point_coord(model, line1_start)
        else:
            p1 = line1_start
        
        if isinstance(line1_end, str):
            p2 = _get_point_coord(model, line1_end)
        else:
            p2 = line1_end
        
        # 获取直线2的点坐标
        if isinstance(line2_start, str):
            p3 = _get_point_coord(model, line2_start)
        else:
            p3 = line2_start
        
        if isinstance(line2_end, str):
            p4 = _get_point_coord(model, line2_end)
        else:
            p4 = line2_end
        
        # 计算交点
        intersection = _calc_lines_intersection(p1, p2, p3, p4)
        
        if intersection is None:
            print("警告: 两条直线平行，无法计算交点")
            return None
        
        # 应用修改
        if apply:
            _change_point_coord(model, point_name, intersection[0], intersection[1], intersection[2])
        
        return intersection
    finally:
        # 恢复原单位
        _restore_units(model, original_units)


def project_point_to_line(
    model,
    point_name: str,
    line_start: Union[str, Tuple[float, float, float]],
    line_end: Union[str, Tuple[float, float, float]],
    apply: bool = True
) -> Tuple[Tuple[float, float, float], float]:
    """
    将点投影到直线上
    
    计算点在由两点定义的直线上的垂直投影，并可选择更新节点坐标。
    内部使用 N-mm-C 单位进行计算，完成后恢复原单位。
    
    Args:
        model: SapModel 对象
        point_name: 待投影的节点名称
        line_start: 直线上的点1 (A点)，可以是节点名称或坐标元组 (x, y, z)
        line_end: 直线上的点2 (B点)，可以是节点名称或坐标元组 (x, y, z)
        apply: 是否应用修改 (True=修改节点坐标, False=仅计算)
        
    Returns:
        (投影坐标, 比例t)
        - 投影坐标: (x, y, z)，单位为 mm
        - 比例t: 投影点在AB上的位置，0=A点，1=B点，0-1之间表示在线段内
        
    Example:
        # 使用节点名称定义直线
        coord, t = project_point_to_line(model, "922", "1160", "738")
        print(f"投影坐标: {coord}, 比例: {t:.4f}")
        
        # 仅计算不修改
        coord, t = project_point_to_line(model, "922", "1160", "738", apply=False)
    """
    # 保存并切换单位
    original_units = _save_and_set_units(model)
    
    try:
        # 获取直线上的点坐标
        if isinstance(line_start, str):
            point_a = _get_point_coord(model, line_start)
        else:
            point_a = line_start
        
        if isinstance(line_end, str):
            point_b = _get_point_coord(model, line_end)
        else:
            point_b = line_end
        
        # 获取待投影点坐标
        point_p = _get_point_coord(model, point_name)
        
        # 计算投影
        proj, t = _calc_projection(point_a, point_b, point_p)
        
        # 应用修改
        if apply:
            _change_point_coord(model, point_name, proj[0], proj[1], proj[2])
        
        return proj, t
    finally:
        # 恢复原单位
        _restore_units(model, original_units)


def project_points_to_line(
    model,
    point_names: List[str],
    line_start: Union[str, Tuple[float, float, float]],
    line_end: Union[str, Tuple[float, float, float]],
    apply: bool = True
) -> List[Tuple[str, Tuple[float, float, float], float]]:
    """
    批量将多个点投影到直线上
    
    内部使用 N-mm-C 单位进行计算，完成后恢复原单位。
    
    Args:
        model: SapModel 对象
        point_names: 待投影的节点名称列表
        line_start: 直线上的点1 (A点)，可以是节点名称或坐标元组 (x, y, z)
        line_end: 直线上的点2 (B点)，可以是节点名称或坐标元组 (x, y, z)
        apply: 是否应用修改 (True=修改节点坐标, False=仅计算)
        
    Returns:
        [(节点名称, 投影坐标, 比例t), ...] 列表
        - 投影坐标: (x, y, z)，单位为 mm
        - 比例t: 投影点在AB上的位置，0=A点，1=B点
        
    Example:
        results = project_points_to_line(model, ["922", "923"], "1160", "738")
        for name, coord, t in results:
            print(f"{name}: {coord}, 比例: {t:.4f}")
    """
    # 保存并切换单位
    original_units = _save_and_set_units(model)
    
    try:
        # 获取直线上的点坐标
        if isinstance(line_start, str):
            point_a = _get_point_coord(model, line_start)
        else:
            point_a = line_start
        
        if isinstance(line_end, str):
            point_b = _get_point_coord(model, line_end)
        else:
            point_b = line_end
        
        results = []
        for name in point_names:
            point_p = _get_point_coord(model, name)
            proj, t = _calc_projection(point_a, point_b, point_p)
            
            if apply:
                _change_point_coord(model, name, proj[0], proj[1], proj[2])
            
            results.append((name, proj, t))
        
        return results
    finally:
        # 恢复原单位
        _restore_units(model, original_units)


def project_point_to_frame(
    model,
    point_name: str,
    frame_name: str,
    apply: bool = True
) -> Tuple[Tuple[float, float, float], float]:
    """
    将点投影到杆件所在直线上
    
    Args:
        model: SapModel 对象
        point_name: 待投影的节点名称
        frame_name: 杆件名称 (用于定义投影直线)
        apply: 是否应用修改 (True=修改节点坐标, False=仅计算)
        
    Returns:
        (投影坐标, 比例t)
        - 投影坐标: (x, y, z)
        - 比例t: 投影点在杆件上的位置，0=I端，1=J端
        
    Example:
        coord, t = project_point_to_frame(model, "922", "F100")
    """
    # 获取杆件端点
    ret = model.FrameObj.GetPoints(str(frame_name), "", "")
    if not isinstance(ret, (list, tuple)) or len(ret) < 2:
        raise ValueError(f"无法获取杆件 {frame_name} 的端点")
    
    point_i, point_j = ret[0], ret[1]
    
    return project_point_to_line(model, point_name, point_i, point_j, apply)


def project_points_to_frame(
    model,
    point_names: List[str],
    frame_name: str,
    apply: bool = True
) -> List[Tuple[str, Tuple[float, float, float], float]]:
    """
    批量将多个点投影到杆件所在直线上
    
    Args:
        model: SapModel 对象
        point_names: 待投影的节点名称列表
        frame_name: 杆件名称 (用于定义投影直线)
        apply: 是否应用修改 (True=修改节点坐标, False=仅计算)
        
    Returns:
        [(节点名称, 投影坐标, 比例t), ...] 列表
        - 比例t: 投影点在杆件上的位置，0=I端，1=J端
        
    Example:
        results = project_points_to_frame(model, ["922", "923"], "F100")
        for name, coord, t in results:
            print(f"{name}: {coord}, 比例: {t:.4f}")
    """
    # 获取杆件端点
    ret = model.FrameObj.GetPoints(str(frame_name), "", "")
    if not isinstance(ret, (list, tuple)) or len(ret) < 2:
        raise ValueError(f"无法获取杆件 {frame_name} 的端点")
    
    point_i, point_j = ret[0], ret[1]
    
    return project_points_to_line(model, point_names, point_i, point_j, apply)


if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from PySap2000.application import Application
    from PySap2000.global_parameters.units import Units, UnitSystem
    
    app = Application()
    model = app.model
    
    # =========================================================================
    # 将点移动到两条直线的交点
    # =========================================================================
    point_to_move = "1139"
    line1_start = "1223"
    line1_end = "821"
    line2_start = "1161"
    line2_end = "1113"
    
    coord = move_point_to_intersection(
        model, point_to_move, 
        line1_start, line1_end, 
        line2_start, line2_end, 
        apply=True
    )
    if coord:
        print(f"节点 {point_to_move} 已移动到交点: ({coord[0]:.3f}, {coord[1]:.3f}, {coord[2]:.3f}) mm")
    
    # =========================================================================
    # 示例1: 单个点投影到直线
    # =========================================================================
    # coord, t = project_point_to_line(model, "922", "1160", "738")
    # print(f"投影坐标: {coord}, 比例: {t:.4f}")
    
    # =========================================================================
    # 示例2: 根据比例移动点到直线上指定位置
    # =========================================================================
    # coord = move_point_on_line(model, "520", "778", "453", t=0.5)  # 移动到中点
    
    # =========================================================================
    # 示例3: 将点移动到两条直线的交点
    # =========================================================================
    # coord = move_point_to_intersection(model, "711", "559", "1064", "770", "678")
    
    print("完成")
