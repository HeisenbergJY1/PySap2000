# -*- coding: utf-8 -*-
"""
local_axes.py - 节点局部坐标轴相关函数

用于设置节点的局部坐标系

SAP2000 API:
- PointObj.SetLocalAxes / GetLocalAxes
- PointObj.SetLocalAxesAdvanced / GetLocalAxesAdvanced
"""

from typing import Tuple, Optional
from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


def set_point_local_axes(
    model,
    point_name: str,
    a: float,
    b: float,
    c: float,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置节点局部坐标轴角度
    
    局部坐标轴的定义方式 (按顺序旋转):
    1. 首先将局部 1, 2, 3 轴设置为与全局 X, Y, Z 轴相同
    2. 绕局部 3 轴旋转角度 a
    3. 绕旋转后的局部 2 轴旋转角度 b
    4. 绕旋转后的局部 1 轴旋转角度 c
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        a: 绕 3 轴旋转角度 [deg]
        b: 绕 2 轴旋转角度 [deg]
        c: 绕 1 轴旋转角度 [deg]
        item_type: 项目类型
    
    Returns:
        0 表示成功
    
    Example:
        # 绕 Z 轴旋转 90°
        set_point_local_axes(model, "1", 90, 0, 0)
        
        # 绕 Y 轴旋转 45°
        set_point_local_axes(model, "2", 0, 45, 0)
    """
    return model.PointObj.SetLocalAxes(str(point_name), a, b, c, item_type)


def get_point_local_axes(
    model,
    point_name: str
) -> Optional[Tuple[float, float, float]]:
    """
    获取节点局部坐标轴角度
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
    
    Returns:
        角度元组 (a, b, c) [deg]，失败返回 None
    
    Example:
        angles = get_point_local_axes(model, "1")
        if angles:
            a, b, c = angles
            print(f"旋转角度: a={a}°, b={b}°, c={c}°")
    """
    try:
        result = model.PointObj.GetLocalAxes(str(point_name), 0.0, 0.0, 0.0, False)
        a = com_data(result, 0)
        b = com_data(result, 1)
        c = com_data(result, 2)
        if a is not None:
            return (a, b, c)
    except Exception:
        pass
    return None


def set_point_local_axes_advanced(
    model,
    point_name: str,
    active: bool,
    axvec_opt: int,
    axcsys: str,
    axdir: Tuple[int, int],
    axpt: Tuple[str, str],
    axvec: Tuple[float, float, float],
    plane2: int,
    plvec_opt: int,
    plcsys: str,
    pldir: Tuple[int, int],
    plpt: Tuple[str, str],
    plvec: Tuple[float, float, float],
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置节点高级局部坐标轴
    
    这是高级方法，允许通过多种方式定义局部坐标轴。
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        active: True=使用高级定义, False=使用简单角度定义
        axvec_opt: 轴向量选项 (1=坐标方向, 2=两点, 3=用户向量)
        axcsys: 轴坐标系名称
        axdir: 轴方向 (正向, 负向)
        axpt: 轴定义点 (点1, 点2)
        axvec: 轴向量 (x, y, z)
        plane2: 平面定义选项
        plvec_opt: 平面向量选项
        plcsys: 平面坐标系名称
        pldir: 平面方向
        plpt: 平面定义点
        plvec: 平面向量
        item_type: 项目类型
    
    Returns:
        0 表示成功
    
    Note:
        对于大多数情况，建议使用简单的 set_point_local_axes() 函数。
    """
    return model.PointObj.SetLocalAxesAdvanced(
        str(point_name),
        active,
        axvec_opt,
        axcsys,
        axdir[0], axdir[1],
        axpt[0], axpt[1],
        axvec[0], axvec[1], axvec[2],
        plane2,
        plvec_opt,
        plcsys,
        pldir[0], pldir[1],
        plpt[0], plpt[1],
        plvec[0], plvec[1], plvec[2],
        item_type
    )


def get_point_local_axes_advanced(
    model,
    point_name: str
) -> Optional[dict]:
    """
    获取节点高级局部坐标轴设置
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
    
    Returns:
        包含高级设置的字典，失败返回 None
    """
    try:
        result = model.PointObj.GetLocalAxesAdvanced(str(point_name))
        active = com_data(result, 0)
        if active is not None and com_data(result, 19) is not None:
            return {
                'active': active,
                'axvec_opt': com_data(result, 1),
                'axcsys': com_data(result, 2),
                'axdir': (com_data(result, 3), com_data(result, 4)),
                'axpt': (com_data(result, 5), com_data(result, 6)),
                'axvec': (com_data(result, 7), com_data(result, 8), com_data(result, 9)),
                'plane2': com_data(result, 10),
                'plvec_opt': com_data(result, 11),
                'plcsys': com_data(result, 12),
                'pldir': (com_data(result, 13), com_data(result, 14)),
                'plpt': (com_data(result, 15), com_data(result, 16)),
                'plvec': (com_data(result, 17), com_data(result, 18), com_data(result, 19))
            }
    except Exception:
        pass
    return None


def get_point_transformation_matrix(
    model,
    point_name: str,
    is_global: bool = True
) -> Optional[Tuple[float, ...]]:
    """
    获取节点坐标变换矩阵
    
    Args:
        model: SapModel 对象
        point_name: 节点名称
        is_global: True=全局到局部, False=局部到全局
    
    Returns:
        12个元素的变换矩阵，失败返回 None
    """
    try:
        result = model.PointObj.GetTransformationMatrix(
            str(point_name), [0.0] * 12, is_global
        )
        matrix = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and matrix:
            return tuple(matrix)
    except Exception:
        pass
    return None
