# -*- coding: utf-8 -*-
"""
local_axes.py - 面单元局部坐标轴函数
对应 SAP2000 的 AreaObj 局部坐标轴相关 API
"""

from typing import Optional, List

from .enums import PlaneRefVectorOption, ItemType
from .data_classes import AreaLocalAxesData, AreaLocalAxesAdvancedData
from PySap2000.com_helper import com_ret, com_data


def set_area_local_axes(
    model,
    area_name: str,
    angle: float,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置面单元局部坐标轴角度
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        angle: 局部坐标轴角度 [deg]
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
        
    Example:
        # 设置面单元 "1" 的局部轴角度为 45 度
        set_area_local_axes(model, "1", 45.0)
    """
    return model.AreaObj.SetLocalAxes(str(area_name), angle, int(item_type))


def get_area_local_axes(
    model,
    area_name: str
) -> Optional[AreaLocalAxesData]:
    """
    获取面单元局部坐标轴角度
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        AreaLocalAxesData 对象，失败返回 None
        
    Example:
        result = get_area_local_axes(model, "1")
        if result:
            print(f"角度: {result.angle}°, 高级设置: {result.advanced}")
    """
    try:
        result = model.AreaObj.GetLocalAxes(str(area_name), 0.0, False)
        angle = com_data(result, 0)
        if angle is not None:
            return AreaLocalAxesData(
                area_name=str(area_name),
                angle=angle,
                advanced=com_data(result, 1, False)
            )
    except Exception:
        pass
    return None


def set_area_local_axes_advanced(
    model,
    area_name: str,
    active: bool,
    plane2: int = 31,
    pl_vect_opt: PlaneRefVectorOption = PlaneRefVectorOption.COORDINATE_DIRECTION,
    pl_csys: str = "Global",
    pl_dir: Tuple[int, int] = (1, 2),
    pl_pt: Tuple[str, str] = ("", ""),
    pl_vect: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置面单元高级局部坐标轴
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        active: 是否启用高级局部坐标轴
        plane2: 31=3-1平面, 32=3-2平面
        pl_vect_opt: 平面参考向量选项
            - COORDINATE_DIRECTION (1): 坐标方向
            - TWO_JOINTS (2): 两节点
            - USER_VECTOR (3): 用户向量
        pl_csys: 坐标系名称
        pl_dir: 主方向和次方向 (用于 pl_vect_opt=1)
        pl_pt: 两个节点名称 (用于 pl_vect_opt=2)
        pl_vect: 用户向量 (用于 pl_vect_opt=3)
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
        
    Example:
        # 使用坐标方向定义
        set_area_local_axes_advanced(model, "1", True, 31, 
            PlaneRefVectorOption.COORDINATE_DIRECTION, "Global", (2, 3))
    """
    return model.AreaObj.SetLocalAxesAdvanced(
        str(area_name), active, plane2, int(pl_vect_opt), pl_csys,
        list(pl_dir), list(pl_pt), list(pl_vect), int(item_type)
    )


def get_area_local_axes_advanced(
    model,
    area_name: str
) -> Optional[AreaLocalAxesAdvancedData]:
    """
    获取面单元高级局部坐标轴设置
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        AreaLocalAxesAdvancedData 对象，失败返回 None
        
    Example:
        data = get_area_local_axes_advanced(model, "1")
        if data and data.active:
            print(f"平面: {data.plane2}, 选项: {data.pl_vect_opt}")
    """
    try:
        result = model.AreaObj.GetLocalAxesAdvanced(
            str(area_name), False, 0, 0, "", [], [], []
        )
        ret = com_ret(result)
        if ret == 0:
            active = com_data(result, 0, False)
            plane2 = com_data(result, 1, 31)
            pl_vect_opt = com_data(result, 2, 1)
            pl_csys = com_data(result, 3, "Global")
            pl_dir = com_data(result, 4, [1, 2])
            pl_pt = com_data(result, 5, ["", ""])
            pl_vect = com_data(result, 6, [0.0, 0.0, 0.0])
            return AreaLocalAxesAdvancedData(
                active=active,
                plane2=plane2,
                pl_vect_opt=PlaneRefVectorOption(pl_vect_opt) if pl_vect_opt else PlaneRefVectorOption.COORDINATE_DIRECTION,
                pl_csys=pl_csys or "Global",
                pl_dir=tuple(pl_dir) if pl_dir else (1, 2),
                pl_pt=tuple(pl_pt) if pl_pt else ("", ""),
                pl_vect=tuple(pl_vect) if pl_vect else (0.0, 0.0, 0.0)
            )
    except Exception:
        pass
    return None


def get_area_transformation_matrix(
    model,
    area_name: str,
    is_global: bool = True
) -> Optional[List[float]]:
    """
    获取面单元变换矩阵
    
    变换矩阵用于将局部坐标系转换为全局坐标系（或当前坐标系）。
    矩阵包含9个方向余弦值。
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        is_global: True=全局坐标系, False=当前坐标系
        
    Returns:
        9个方向余弦值的列表 [c0, c1, c2, c3, c4, c5, c6, c7, c8]，失败返回 None
        
    Example:
        matrix = get_area_transformation_matrix(model, "1")
        if matrix:
            # 矩阵方程: [GlobalX, GlobalY, GlobalZ] = [c0-c8] * [Local1, Local2, Local3]
            print(f"变换矩阵: {matrix}")
    """
    try:
        result = model.AreaObj.GetTransformationMatrix(str(area_name), [], is_global)
        matrix = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and matrix:
            return list(matrix)
    except Exception:
        pass
    return None
