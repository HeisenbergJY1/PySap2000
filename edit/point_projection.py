# -*- coding: utf-8 -*-
"""
point_projection.py - Point projection utilities

Project points onto lines or frame objects.

Functions:
- `project_point_to_line`: project one point onto a line defined by two points
- `project_points_to_line`: project multiple points onto a line
- `project_point_to_frame`: project one point onto a frame centerline
- `project_points_to_frame`: project multiple points onto a frame centerline
- `move_point_on_line`: move a point to a ratio-based location on a line
- `move_point_to_intersection`: move a point to the intersection of two lines

Usage:
    from PySap2000.edit.point_projection import project_point_to_line, move_point_on_line
    
    # Project point 922 onto the line through points 1160 and 738
    project_point_to_line(model, "922", "1160", "738")
    
    # Move the point to `t=0.5` on the line (midpoint)
    move_point_on_line(model, "922", "1160", "738", t=0.5)
    
    # Move the point to the intersection of two lines
    move_point_to_intersection(model, "711", "559", "1064", "770", "678")
"""

from typing import List, Tuple, Union, Optional
import numpy as np


def _get_point_coord(model, point_name: str) -> Tuple[float, float, float]:
    """
    Get point coordinates (using current model units)
    
    Args:
        model: SAP2000 SapModel object
        point_name: Point name
        
    Returns:
        Coordinate tuple `(x, y, z)`
    """
    ret = model.PointObj.GetCoordCartesian(str(point_name), 0.0, 0.0, 0.0)
    if isinstance(ret, (list, tuple)) and len(ret) >= 3:
        return (ret[0], ret[1], ret[2])
    raise ValueError(f"Failed to get point {point_name} coordinates")


def _change_point_coord(model, name: str, x: float, y: float, z: float) -> int:
    """Change point coordinates (using current model units)"""
    return model.EditPoint.ChangeCoordinates_1(name, x, y, z, "Global")


def _calc_point_on_line(
    point_a: Tuple[float, float, float],
    point_b: Tuple[float, float, float],
    t: float
) -> Tuple[float, float, float]:
    """
    Compute point coordinates on line AB using ratio `t`
    
    Args:
        point_a: Start point A `(x, y, z)`
        point_b: End point B `(x, y, z)`
        t: Ratio (`0` at A, `1` at B)
        
    Returns:
        Point coordinates `(x, y, z)`
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
    Compute nearest points between two 3D lines (approximate intersection).
    
    Line 1: `P1 + t * (P2 - P1)`
    Line 2: `P3 + s * (P4 - P3)`
    
    In 3D, lines are usually skew; this computes the midpoint of nearest points as an approximate intersection.
    
    Args:
        p1, p2: Two points on line 1
        p3, p4: Two points on line 2
        
    Returns:
        Intersection coordinates `(x, y, z)`, or `None` if lines are parallel
    """
    # Direction vectors
    d1 = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    d2 = np.array([p4[0] - p3[0], p4[1] - p3[1], p4[2] - p3[2]])
    
    # Start-point difference vector
    r = np.array([p1[0] - p3[0], p1[1] - p3[1], p1[2] - p3[2]])
    
    a = np.dot(d1, d1)  # |d1|^2
    b = np.dot(d1, d2)  # d1 · d2
    c = np.dot(d2, d2)  # |d2|^2
    d = np.dot(d1, r)   # d1 · r
    e = np.dot(d2, r)   # d2 · r
    
    denom = a * c - b * b
    
    if abs(denom) < 1e-10:
        # Lines are parallel
        return None
    
    # Compute parameters `t` and `s`
    t = (b * e - c * d) / denom
    s = (a * e - b * d) / denom
    
    # Nearest points on the two lines
    point_on_line1 = np.array(p1) + t * d1
    point_on_line2 = np.array(p3) + s * d2
    
    # Return midpoint of the two nearest points as intersection
    intersection = (point_on_line1 + point_on_line2) / 2
    
    return (float(intersection[0]), float(intersection[1]), float(intersection[2]))


def _calc_projection(
    point_a: Tuple[float, float, float],
    point_b: Tuple[float, float, float],
    point_p: Tuple[float, float, float]
) -> Tuple[Tuple[float, float, float], float]:
    """
    Compute the projection of point P onto line AB
    
    Args:
        point_a: Point A on the line `(x, y, z)`
        point_b: Point B on the line `(x, y, z)`
        point_p: Point P to project `(x, y, z)`
        
    Returns:
        (projection coordinates, ratio `t`)
        - Projection coordinates: `(x, y, z)`
        - Ratio `t`: position on AB (`0`=A, `1`=B)
    """
    x1, y1, z1 = point_a
    x2, y2, z2 = point_b
    x, y, z = point_p
    
    # Vector AB
    ab = (x2 - x1, y2 - y1, z2 - z1)
    # Vector AP
    ap = (x - x1, y - y1, z - z1)
    
    # AB · AB
    ab_dot_ab = ab[0]**2 + ab[1]**2 + ab[2]**2
    if ab_dot_ab == 0:
        return point_a, 0.0  # A and B coincide; return A
    
    # AP · AB
    ap_dot_ab = ap[0]*ab[0] + ap[1]*ab[1] + ap[2]*ab[2]
    
    # Parameter `t` (ratio)
    t = ap_dot_ab / ab_dot_ab
    
    # Projection coordinates
    proj = (
        x1 + t * ab[0],
        y1 + t * ab[1],
        z1 + t * ab[2]
    )
    return proj, t


def _save_and_set_units(model):
    """Save current units and switch to `N-mm-C`"""
    from PySap2000.global_parameters.units import Units, UnitSystem
    original = Units.get_present_units(model)
    Units.set_present_units(model, UnitSystem.N_MM_C)
    return original


def _restore_units(model, original):
    """Restore original units"""
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
    Move a point to a ratio-based location on a line
    
    Args:
        model: SAP2000 SapModel object
        point_name: Point name to move
        line_start: Line start point (A), point name or coordinate tuple `(x, y, z)`
        line_end: Line end point (B), point name or coordinate tuple `(x, y, z)`
        t: Ratio value
            - `t=0`: move to start point A
            - `t=1`: move to end point B
            - `t=0.5`: move to midpoint
            - `0<t<1`: inside segment
        apply: Whether to apply updates (`True` changes coordinates, `False` only computes)
        
    Returns:
        New coordinates `(x, y, z)` in mm
        
    Example:
        # Move the point to the line midpoint
        coord = move_point_on_line(model, "520", "778", "453", t=0.5)
        
        # Move the point to 30% from the start point
        coord = move_point_on_line(model, "520", "778", "453", t=0.3)
    """
    # Save and switch units
    original_units = _save_and_set_units(model)
    
    try:
        # Get line-point coordinates
        if isinstance(line_start, str):
            point_a = _get_point_coord(model, line_start)
        else:
            point_a = line_start
        
        if isinstance(line_end, str):
            point_b = _get_point_coord(model, line_end)
        else:
            point_b = line_end
        
        # Compute new coordinates from ratio
        new_coord = _calc_point_on_line(point_a, point_b, t)
        
        # Apply updates
        if apply:
            _change_point_coord(model, point_name, new_coord[0], new_coord[1], new_coord[2])
        
        return new_coord
    finally:
        # Restore original units
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
    Move a point to the intersection of two lines
    
    In 3D, two lines are usually not exactly intersecting; this function uses the midpoint of nearest points as an approximate intersection.
    
    Args:
        model: SAP2000 SapModel object
        point_name: Point name to move
        line1_start: Start of line 1, point name or coordinate tuple `(x, y, z)`
        line1_end: End of line 1
        line2_start: Start of line 2
        line2_end: End of line 2
        apply: Whether to apply updates (`True` changes coordinates, `False` only computes)
        
    Returns:
        Intersection coordinates `(x, y, z)` in mm, or `None` if lines are parallel
        
    Example:
        # Move point 711 to the intersection of lines 559-1064 and 770-678
        coord = move_point_to_intersection(model, "711", "559", "1064", "770", "678")
    """
    # Save and switch units
    original_units = _save_and_set_units(model)
    
    try:
        # Get coordinates for line 1
        if isinstance(line1_start, str):
            p1 = _get_point_coord(model, line1_start)
        else:
            p1 = line1_start
        
        if isinstance(line1_end, str):
            p2 = _get_point_coord(model, line1_end)
        else:
            p2 = line1_end
        
        # Get coordinates for line 2
        if isinstance(line2_start, str):
            p3 = _get_point_coord(model, line2_start)
        else:
            p3 = line2_start
        
        if isinstance(line2_end, str):
            p4 = _get_point_coord(model, line2_end)
        else:
            p4 = line2_end
        
        # Compute intersection
        intersection = _calc_lines_intersection(p1, p2, p3, p4)
        
        if intersection is None:
            print("Warning: lines are parallel; cannot compute intersection")
            return None
        
        # Apply updates
        if apply:
            _change_point_coord(model, point_name, intersection[0], intersection[1], intersection[2])
        
        return intersection
    finally:
        # Restore original units
        _restore_units(model, original_units)


def project_point_to_line(
    model,
    point_name: str,
    line_start: Union[str, Tuple[float, float, float]],
    line_end: Union[str, Tuple[float, float, float]],
    apply: bool = True
) -> Tuple[Tuple[float, float, float], float]:
    """
    Project a point onto a line
    
    Computes the orthogonal projection of a point onto a line defined by two points, optionally updating coordinates.
    Uses `N-mm-C` units internally and restores original units after completion.
    
    Args:
        model: SAP2000 SapModel object
        point_name: Point name to project
        line_start: Point 1 on line (A), point name or coordinate tuple `(x, y, z)`
        line_end: Point 2 on line (B), point name or coordinate tuple `(x, y, z)`
        apply: Whether to apply updates (`True` changes coordinates, `False` only computes)
        
    Returns:
        (projection coordinates, ratio `t`)
        - Projection coordinates `(x, y, z)` in mm
        - Ratio `t`: position on AB (`0`=A, `1`=B, values between `0` and `1` are inside the segment)
        
    Example:
        # Define line with point names
        coord, t = project_point_to_line(model, "922", "1160", "738")
        print(f"Projection: {coord}, Ratio: {t:.4f}")
        
        # Compute only, do not update
        coord, t = project_point_to_line(model, "922", "1160", "738", apply=False)
    """
    # Save and switch units
    original_units = _save_and_set_units(model)
    
    try:
        # Get line-point coordinates
        if isinstance(line_start, str):
            point_a = _get_point_coord(model, line_start)
        else:
            point_a = line_start
        
        if isinstance(line_end, str):
            point_b = _get_point_coord(model, line_end)
        else:
            point_b = line_end
        
        # Get point coordinates for projection
        point_p = _get_point_coord(model, point_name)
        
        # Compute projection
        proj, t = _calc_projection(point_a, point_b, point_p)
        
        # Apply updates
        if apply:
            _change_point_coord(model, point_name, proj[0], proj[1], proj[2])
        
        return proj, t
    finally:
        # Restore original units
        _restore_units(model, original_units)


def project_points_to_line(
    model,
    point_names: List[str],
    line_start: Union[str, Tuple[float, float, float]],
    line_end: Union[str, Tuple[float, float, float]],
    apply: bool = True
) -> List[Tuple[str, Tuple[float, float, float], float]]:
    """
    Project multiple points onto a line
    
    Uses `N-mm-C` units internally and restores original units after completion.
    
    Args:
        model: SAP2000 SapModel object
        point_names: List of point names to project
        line_start: Point 1 on line (A), point name or coordinate tuple `(x, y, z)`
        line_end: Point 2 on line (B), point name or coordinate tuple `(x, y, z)`
        apply: Whether to apply updates (`True` changes coordinates, `False` only computes)
        
    Returns:
        List of `[(point_name, projection, ratio_t), ...]`
        - Projection coordinates `(x, y, z)` in mm
        - Ratio `t`: position on AB (`0`=A, `1`=B)
        
    Example:
        results = project_points_to_line(model, ["922", "923"], "1160", "738")
        for name, coord, t in results:
            print(f"{name}: {coord}, Ratio: {t:.4f}")
    """
    # Save and switch units
    original_units = _save_and_set_units(model)
    
    try:
        # Get line-point coordinates
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
        # Restore original units
        _restore_units(model, original_units)


def project_point_to_frame(
    model,
    point_name: str,
    frame_name: str,
    apply: bool = True
) -> Tuple[Tuple[float, float, float], float]:
    """
    Project a point onto a frame centerline
    
    Args:
        model: SAP2000 SapModel object
        point_name: Point name to project
        frame_name: Frame name (defines the projection line)
        apply: Whether to apply updates (`True` changes coordinates, `False` only computes)
        
    Returns:
        (projection coordinates, ratio `t`)
        - Projection: (x, y, z)
        - ratio_t: Projection position on the frame (`0`=I end, `1`=J end)
        
    Example:
        coord, t = project_point_to_frame(model, "922", "F100")
    """
    # Get frame endpoints
    ret = model.FrameObj.GetPoints(str(frame_name), "", "")
    if not isinstance(ret, (list, tuple)) or len(ret) < 2:
        raise ValueError(f"Failed to get frame {frame_name} endpoints")
    
    point_i, point_j = ret[0], ret[1]
    
    return project_point_to_line(model, point_name, point_i, point_j, apply)


def project_points_to_frame(
    model,
    point_names: List[str],
    frame_name: str,
    apply: bool = True
) -> List[Tuple[str, Tuple[float, float, float], float]]:
    """
    Project multiple points onto a frame centerline
    
    Args:
        model: SAP2000 SapModel object
        point_names: List of point names to project
        frame_name: Frame name (defines the projection line)
        apply: Whether to apply updates (`True` changes coordinates, `False` only computes)
        
    Returns:
        List of `[(point_name, projection, ratio_t), ...]`
        - ratio_t: Projection position on the frame (`0`=I end, `1`=J end)
        
    Example:
        results = project_points_to_frame(model, ["922", "923"], "F100")
        for name, coord, t in results:
            print(f"{name}: {coord}, Ratio: {t:.4f}")
    """
    # Get frame endpoints
    ret = model.FrameObj.GetPoints(str(frame_name), "", "")
    if not isinstance(ret, (list, tuple)) or len(ret) < 2:
        raise ValueError(f"Failed to get frame {frame_name} endpoints")
    
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
    # Move a point to the intersection of two lines
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
        print(f"Point {point_to_move} moved to intersection: ({coord[0]:.3f}, {coord[1]:.3f}, {coord[2]:.3f}) mm")
    
    # =========================================================================
    # Example 1: Project one point onto a line
    # =========================================================================
    # coord, t = project_point_to_line(model, "922", "1160", "738")
    # print(f"Projection: {coord}, Ratio: {t:.4f}")
    
    # =========================================================================
    # Example 2: Move a point to a ratio-based location on a line
    # =========================================================================
    # coord = move_point_on_line(model, "520", "778", "453", t=0.5)  # move to midpoint
    
    # =========================================================================
    # Example 3: Move a point to the intersection of two lines
    # =========================================================================
    # coord = move_point_to_intersection(model, "711", "559", "1064", "770", "678")
    
    print("Done")
