# -*- coding: utf-8 -*-
"""
edit_frame.py - 框架编辑

SAP2000 EditFrame API 封装

SAP2000 API:
- EditFrame.DivideAtDistance - 按距离分割
- EditFrame.DivideAtIntersections - 在交点分割
- EditFrame.DivideByRatio - 按比例分割
- EditFrame.Extend - 延伸
- EditFrame.Join - 连接
- EditFrame.Trim - 修剪
- EditFrame.ChangeConnectivity - 修改连接
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
    按距离分割框架
    
    Args:
        model: SapModel 对象
        name: 框架名称
        dist: 分割距离
        i_end: True 从 I 端测量，False 从 J 端测量
        
    Returns:
        (name1, name2) 分割后的两个框架名称
    """
    result = model.EditFrame.DivideAtDistance(name, dist, i_end, "", "")
    name1 = com_data(result, 0, "")
    name2 = com_data(result, 1, "")
    return (name1 if name1 else "", name2 if name2 else "")


def divide_frame_at_intersections(model, name: str) -> List[str]:
    """
    在交点处分割框架
    
    Args:
        model: SapModel 对象
        name: 框架名称
        
    Returns:
        分割后的框架名称列表
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
    按比例分割框架
    
    Args:
        model: SapModel 对象
        name: 框架名称
        num_segments: 分割段数
        ratio: Last/First 长度比 (1.0 = 等分)
        
    Returns:
        分割后的框架名称列表
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
    延伸框架
    
    Args:
        model: SapModel 对象
        name: 框架名称
        i_end: True 延伸 I 端，False 延伸 J 端
        extend_to_name: 延伸到的对象名称
        
    Returns:
        0 表示成功
    """
    return model.EditFrame.Extend(name, i_end, extend_to_name)


def join_frame(model, name1: str, name2: str) -> str:
    """
    连接两个框架
    
    Args:
        model: SapModel 对象
        name1: 第一个框架名称
        name2: 第二个框架名称
        
    Returns:
        连接后的框架名称
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
    修剪框架
    
    Args:
        model: SapModel 对象
        name: 框架名称
        i_end: True 修剪 I 端，False 修剪 J 端
        trim_to_name: 修剪到的对象名称
        
    Returns:
        0 表示成功
    """
    return model.EditFrame.Trim(name, i_end, trim_to_name)


def change_frame_connectivity(
    model,
    name: str,
    point_i: str,
    point_j: str
) -> int:
    """
    修改框架连接
    
    Args:
        model: SapModel 对象
        name: 框架名称
        point_i: I 端点名称
        point_j: J 端点名称
        
    Returns:
        0 表示成功
    """
    return model.EditFrame.ChangeConnectivity(name, point_i, point_j)
