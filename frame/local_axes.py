# -*- coding: utf-8 -*-
"""
local_axes.py - 杆件局部坐标轴相关函数

用于设置杆件的局部坐标轴方向

SAP2000 API:
- FrameObj.SetLocalAxes(Name, Ang, ItemType)
- FrameObj.GetLocalAxes(Name, Ang, Advanced)
- FrameObj.GetTransformationMatrix(Name, Value[], IsGlobal)
"""

from typing import Tuple, Optional, List
from .enums import ItemType
from .data_classes import FrameLocalAxesData, FrameLocalAxesAdvancedData
from PySap2000.com_helper import com_ret, com_data


def set_frame_local_axes(
    model,
    frame_name: str,
    angle: float,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置杆件局部轴角度
    
    局部2和3轴绕正局部1轴旋转的角度。
    正角度从局部+1轴方向看为逆时针。
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        angle: 旋转角度 [deg]
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        # 旋转局部轴 30 度
        set_frame_local_axes(model, "1", 30)
        
        # 旋转局部轴 90 度 (常用于斜撑)
        set_frame_local_axes(model, "B1", 90)
    """
    return model.FrameObj.SetLocalAxes(str(frame_name), angle, int(item_type))


def get_frame_local_axes(
    model,
    frame_name: str
) -> Optional[FrameLocalAxesData]:
    """
    获取杆件局部轴角度
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        FrameLocalAxesData 对象，失败返回 None
    
    Example:
        axes = get_frame_local_axes(model, "1")
        if axes:
            print(f"局部轴角度: {axes.angle}°")
    """
    try:
        result = model.FrameObj.GetLocalAxes(str(frame_name))
        angle = com_data(result, 0)
        if angle is not None:
            return FrameLocalAxesData(
                frame_name=str(frame_name),
                angle=angle,
                advanced=com_data(result, 1, False)
            )
    except Exception:
        pass
    return None


def set_frame_local_axes_advanced(
    model,
    frame_name: str,
    active: bool,
    plane2: int = 12,
    pl_vect_opt: int = 1,
    pl_csys: str = "Global",
    pl_dir: List[int] = None,
    pl_pt: List[str] = None,
    pl_vect: List[float] = None,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置杆件高级局部轴
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        active: 是否激活高级局部轴
        plane2: 12=1-2平面, 13=1-3平面
        pl_vect_opt: 平面参考向量选项 (1=坐标方向, 2=两节点, 3=用户向量)
        pl_csys: 坐标系名称
        pl_dir: 方向数组 [primary, secondary]
        pl_pt: 参考点数组 [pt1, pt2]
        pl_vect: 用户向量 [x, y, z]
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        # 使用坐标方向定义1-2平面
        set_frame_local_axes_advanced(model, "3", True, 12, 1, "Global", [2, 3])
    """
    if pl_dir is None:
        pl_dir = [0, 0]
    if pl_pt is None:
        pl_pt = ["", ""]
    if pl_vect is None:
        pl_vect = [0.0, 0.0, 0.0]
    
    return model.FrameObj.SetLocalAxesAdvanced(
        str(frame_name), active, plane2, pl_vect_opt, pl_csys,
        pl_dir, pl_pt, pl_vect, int(item_type)
    )


def get_frame_local_axes_advanced(
    model,
    frame_name: str
) -> Optional[FrameLocalAxesAdvancedData]:
    """
    获取杆件高级局部轴设置
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        FrameLocalAxesAdvancedData 对象，失败返回 None
    
    Example:
        data = get_frame_local_axes_advanced(model, "3")
        if data and data.active:
            print(f"平面: {data.plane2}, 选项: {data.pl_vect_opt}")
    """
    try:
        result = model.FrameObj.GetLocalAxesAdvanced(
            str(frame_name), False, 0, 0, "", [], [], []
        )
        ret = com_ret(result)
        if ret == 0:
            active = com_data(result, 0, False)
            plane2 = com_data(result, 1, 12)
            pl_vect_opt = com_data(result, 2, 1)
            pl_csys = com_data(result, 3, "Global")
            pl_dir = com_data(result, 4, [1, 2])
            pl_pt = com_data(result, 5, ["", ""])
            pl_vect = com_data(result, 6, [0.0, 0.0, 0.0])
            return FrameLocalAxesAdvancedData(
                active=active,
                plane2=plane2,
                pl_vect_opt=pl_vect_opt if pl_vect_opt else 1,
                pl_csys=pl_csys or "Global",
                pl_dir=tuple(pl_dir) if pl_dir else (1, 2),
                pl_pt=tuple(pl_pt) if pl_pt else ("", ""),
                pl_vect=tuple(pl_vect) if pl_vect else (0.0, 0.0, 0.0)
            )
    except Exception:
        pass
    return None


def get_frame_transformation_matrix(
    model,
    frame_name: str,
    is_global: bool = True
) -> Optional[List[float]]:
    """
    获取杆件变换矩阵
    
    返回 3x3 变换矩阵（9个值），用于局部坐标和全局坐标转换。
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        is_global: True=全局坐标系, False=当前坐标系
    
    Returns:
        9个浮点数的列表 (3x3矩阵按行排列)，失败返回 None
    
    Example:
        matrix = get_frame_transformation_matrix(model, "1")
        if matrix:
            # matrix[0:3] = 局部1轴在全局坐标系中的方向
            # matrix[3:6] = 局部2轴在全局坐标系中的方向
            # matrix[6:9] = 局部3轴在全局坐标系中的方向
            print(f"局部1轴方向: {matrix[0:3]}")
    """
    try:
        result = model.FrameObj.GetTransformationMatrix(
            str(frame_name), [0.0] * 12, is_global
        )
        values = com_data(result, 0)
        if values and len(values) >= 9:
            return list(values[:9])
    except Exception:
        pass
    return None
