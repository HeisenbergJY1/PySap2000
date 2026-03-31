# -*- coding: utf-8 -*-
"""
edit_frame.py - Frame editing

Wrappers for the SAP2000 `EditFrame` API.

SAP2000 API:
- `EditFrame.DivideAtDistance` - Divide by distance
- `EditFrame.DivideAtIntersections` - Divide at intersections
- `EditFrame.DivideByRatio` - Divide by ratio
- `EditFrame.Extend` - Extend
- `EditFrame.Join` - Join
- `EditFrame.Trim` - Trim
- `EditFrame.ChangeConnectivity` - Change connectivity
"""

from typing import List, Tuple
from PySap2000.com_helper import com_ret, com_data


def divide_frame_at_distance(
    model,
    name: str,
    dist: float,
    i_end: bool = True
) -> Tuple[str, str]:
    """
    Divide a frame by distance
    
    Args:
        model: SAP2000 SapModel object
        name: Frame name
        dist: Divide distance
        i_end: `True` measure from I end, `False` from J end
        
    Returns:
        `(name1, name2)` names of the two resulting frame objects
    """
    result = model.EditFrame.DivideAtDistance(name, dist, i_end, "", "")
    name1 = com_data(result, 0, "")
    name2 = com_data(result, 1, "")
    return (name1 if name1 else "", name2 if name2 else "")


def divide_frame_at_intersections(model, name: str) -> List[str]:
    """
    Divide a frame at intersections
    
    Args:
        model: SAP2000 SapModel object
        name: Frame name
        
    Returns:
        List of resulting frame object names
    """
    result = model.EditFrame.DivideAtIntersections(name, 0, [])
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def divide_frame_by_ratio(
    model,
    name: str,
    num_segments: int = 2,
    ratio: float = 1.0
) -> List[str]:
    """
    Divide a frame by ratio
    
    Args:
        model: SAP2000 SapModel object
        name: Frame name
        num_segments: Number of segments
        ratio: Last/First length ratio (`1.0` = equal segments)
        
    Returns:
        List of resulting frame object names
    """
    result = model.EditFrame.DivideByRatio(name, num_segments, ratio, [])
    names = com_data(result, 0, None)
    if names and len(names) > 0:
        return list(names)
    return []


def extend_frame(
    model,
    name: str,
    i_end: bool,
    extend_to_name: str
) -> int:
    """
    Extend a frame
    
    Args:
        model: SAP2000 SapModel object
        name: Frame name
        i_end: `True` extend I end, `False` extend J end
        extend_to_name: Target object name for extension
        
    Returns:
        `0` on success
    """
    return model.EditFrame.Extend(name, i_end, extend_to_name)


def join_frame(model, name1: str, name2: str) -> str:
    """
    Join two frames
    
    Args:
        model: SAP2000 SapModel object
        name1: First frame name
        name2: Second frame name
        
    Returns:
        Resulting frame name after join
    """
    result = model.EditFrame.Join(name1, name2)
    name = com_data(result, 0, "")
    return name if name else ""


def trim_frame(
    model,
    name: str,
    i_end: bool,
    trim_to_name: str
) -> int:
    """
    Trim a frame
    
    Args:
        model: SAP2000 SapModel object
        name: Frame name
        i_end: `True` trim I end, `False` trim J end
        trim_to_name: Target object name for trim
        
    Returns:
        `0` on success
    """
    return model.EditFrame.Trim(name, i_end, trim_to_name)


def change_frame_connectivity(
    model,
    name: str,
    point_i: str,
    point_j: str
) -> int:
    """
    Change frame connectivity
    
    Args:
        model: SAP2000 SapModel object
        name: Frame name
        point_i: I-end point name
        point_j: J-end point name
        
    Returns:
        `0` on success
    """
    return model.EditFrame.ChangeConnectivity(name, point_i, point_j)
