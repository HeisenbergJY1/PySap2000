# -*- coding: utf-8 -*-
"""
edit_point.py - 点编辑

SAP2000 EditPoint API 封装

SAP2000 API:
- EditPoint.Align - 对齐
- EditPoint.Connect - 连接
- EditPoint.Disconnect - 断开
- EditPoint.Merge - 合并
- EditPoint.ChangeCoordinates_1 - 修改坐标
"""

from typing import List


def align_point(
    model,
    axis: int,
    ordinate: float = 0.0,
    csys: str = "Global"
) -> int:
    """
    对齐选中的点
    
    Args:
        model: SapModel 对象
        axis: 对齐轴
            1 = X轴
            2 = Y轴
            3 = Z轴
        ordinate: 对齐坐标值
        csys: 坐标系名称
        
    Returns:
        0 表示成功
    """
    return model.EditPoint.Align(axis, ordinate, csys)


def connect_point(model) -> int:
    """
    连接选中的点（创建框架）
    
    Args:
        model: SapModel 对象
        
    Returns:
        0 表示成功
    """
    return model.EditPoint.Connect()


def disconnect_point(model, name: str) -> int:
    """
    断开点连接
    
    Args:
        model: SapModel 对象
        name: 点名称
        
    Returns:
        0 表示成功
    """
    return model.EditPoint.Disconnect(name)


def merge_point(model, tolerance: float = 0.001) -> int:
    """
    合并选中的点
    
    Args:
        model: SapModel 对象
        tolerance: 合并容差
        
    Returns:
        0 表示成功
    """
    return model.EditPoint.Merge(tolerance)


def change_point_coordinates(
    model,
    name: str,
    x: float,
    y: float,
    z: float,
    csys: str = "Global"
) -> int:
    """
    修改点坐标
    
    Args:
        model: SapModel 对象
        name: 点名称
        x: X坐标
        y: Y坐标
        z: Z坐标
        csys: 坐标系名称
        
    Returns:
        0 表示成功
    """
    return model.EditPoint.ChangeCoordinates_1(name, x, y, z, csys)
