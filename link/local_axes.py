# -*- coding: utf-8 -*-
"""
local_axes.py - 连接单元局部坐标轴相关函数

用于设置连接单元的局部坐标轴方向

SAP2000 API:
- LinkObj.SetLocalAxes(Name, Ang, ItemType)
- LinkObj.GetLocalAxes(Name, Ang, Advanced)
- LinkObj.SetLocalAxesAdvanced(Name, Active, AxVectOpt, AxCSys, AxDir[], AxPt[], AxVect[], 
                                Plane2, PlVectOpt, PlCSys, PlDir[], PlPt[], PlVect[], ItemType)
- LinkObj.GetLocalAxesAdvanced(Name, Active, AxVectOpt, AxCSys, AxDir[], AxPt[], AxVect[],
                                Plane2, PlVectOpt, PlCSys, PlDir[], PlPt[], PlVect[])
- LinkObj.GetTransformationMatrix(Name, Value[], IsGlobal)
"""

from typing import Optional, List
from .enums import LinkItemType
from .data_classes import LinkLocalAxesData, LinkLocalAxesAdvancedData
from PySap2000.com_helper import com_data


def set_link_local_axes(
    model,
    link_name: str,
    angle: float,
    item_type: LinkItemType = LinkItemType.OBJECT
) -> int:
    """
    设置连接单元局部轴角度
    
    局部2和3轴绕正局部1轴旋转的角度。
    正角度从局部+1轴方向看为逆时针。
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        angle: 旋转角度 [deg]
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        set_link_local_axes(model, "1", 30)
    """
    return model.LinkObj.SetLocalAxes(str(link_name), angle, int(item_type))


def get_link_local_axes(
    model,
    link_name: str
) -> Optional[LinkLocalAxesData]:
    """
    获取连接单元局部轴角度
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
    
    Returns:
        LinkLocalAxesData 对象，失败返回 None
    
    Example:
        axes = get_link_local_axes(model, "1")
        if axes:
            print(f"局部轴角度: {axes.angle}°")
    """
    try:
        result = model.LinkObj.GetLocalAxes(str(link_name), 0.0, False)
        angle = com_data(result, 0)
        if angle is not None:
            return LinkLocalAxesData(
                link_name=str(link_name),
                angle=angle,
                advanced=com_data(result, 1, False)
            )
    except Exception:
        pass
    return None



def set_link_local_axes_advanced(
    model,
    link_name: str,
    active: bool,
    ax_vect_opt: int = 1,
    ax_csys: str = "Global",
    ax_dir: List[int] = None,
    ax_pt: List[str] = None,
    ax_vect: List[float] = None,
    plane2: int = 12,
    pl_vect_opt: int = 1,
    pl_csys: str = "Global",
    pl_dir: List[int] = None,
    pl_pt: List[str] = None,
    pl_vect: List[float] = None,
    item_type: LinkItemType = LinkItemType.OBJECT
) -> int:
    """
    设置连接单元高级局部轴
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        active: 是否激活高级局部轴
        ax_vect_opt: 轴向量选项 (1=坐标方向, 2=两节点, 3=用户向量)
        ax_csys: 轴坐标系
        ax_dir: 轴方向数组 [primary, secondary]
        ax_pt: 轴参考点数组 [pt1, pt2]
        ax_vect: 轴向量 [x, y, z]
        plane2: 平面2定义 (12 或 13)
        pl_vect_opt: 平面向量选项
        pl_csys: 平面坐标系
        pl_dir: 平面方向数组 [primary, secondary]
        pl_pt: 平面参考点数组 [pt1, pt2]
        pl_vect: 平面向量 [x, y, z]
        item_type: 操作范围
        
    Returns:
        0 表示成功
    
    Example:
        set_link_local_axes_advanced(model, "1", True, ax_vect_opt=3, ax_vect=[1, 0, 0])
    """
    if ax_dir is None:
        ax_dir = [0, 0]
    if ax_pt is None:
        ax_pt = ["", ""]
    if ax_vect is None:
        ax_vect = [0.0, 0.0, 0.0]
    if pl_dir is None:
        pl_dir = [0, 0]
    if pl_pt is None:
        pl_pt = ["", ""]
    if pl_vect is None:
        pl_vect = [0.0, 0.0, 0.0]
    
    return model.LinkObj.SetLocalAxesAdvanced(
        str(link_name), active, ax_vect_opt, ax_csys, ax_dir, ax_pt, ax_vect,
        plane2, pl_vect_opt, pl_csys, pl_dir, pl_pt, pl_vect, int(item_type)
    )


def get_link_local_axes_advanced(
    model,
    link_name: str
) -> Optional[LinkLocalAxesAdvancedData]:
    """
    获取连接单元高级局部轴设置
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
    
    Returns:
        LinkLocalAxesAdvancedData 对象，失败返回 None
    
    Example:
        axes = get_link_local_axes_advanced(model, "1")
        if axes and axes.active:
            print(f"使用高级局部轴，轴向量选项: {axes.ax_vect_opt}")
    """
    try:
        result = model.LinkObj.GetLocalAxesAdvanced(
            str(link_name), False, 0, "", [], [], [], 0, 0, "", [], [], []
        )
        
        active = com_data(result, 0)
        if active is not None:
            return LinkLocalAxesAdvancedData(
                link_name=str(link_name),
                active=com_data(result, 0, False),
                ax_vect_opt=com_data(result, 1, 0),
                ax_csys=com_data(result, 2) or "Global",
                ax_dir=list(com_data(result, 3)) if com_data(result, 3) else [0, 0],
                ax_pt=list(com_data(result, 4)) if com_data(result, 4) else ["", ""],
                ax_vect=list(com_data(result, 5)) if com_data(result, 5) else [0.0, 0.0, 0.0],
                plane2=com_data(result, 6, 0),
                pl_vect_opt=com_data(result, 7, 0),
                pl_csys=com_data(result, 8) or "Global",
                pl_dir=list(com_data(result, 9)) if com_data(result, 9) else [0, 0],
                pl_pt=list(com_data(result, 10)) if com_data(result, 10) else ["", ""],
                pl_vect=list(com_data(result, 11)) if com_data(result, 11) else [0.0, 0.0, 0.0]
            )
    except Exception:
        pass
    return None


def get_link_transformation_matrix(
    model,
    link_name: str,
    is_global: bool = True
) -> Optional[List[float]]:
    """
    获取连接单元变换矩阵
    
    返回 3x3 变换矩阵（9个值），用于局部坐标和全局坐标转换。
    
    Args:
        model: SapModel 对象
        link_name: 连接单元名称
        is_global: True=全局坐标系, False=当前坐标系
    
    Returns:
        9个浮点数的列表 (3x3矩阵按行排列)，失败返回 None
    
    Example:
        matrix = get_link_transformation_matrix(model, "1")
        if matrix:
            print(f"局部1轴方向: {matrix[0:3]}")
    """
    try:
        result = model.LinkObj.GetTransformationMatrix(str(link_name), [], is_global)
        values = com_data(result, 0)
        if values:
            return list(values)[:9]
    except Exception:
        pass
    return None
