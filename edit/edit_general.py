# -*- coding: utf-8 -*-
"""
edit_general.py - 通用编辑

SAP2000 EditGeneral API 封装

SAP2000 API:
- EditGeneral.ExtrudeAreaToSolidLinearNormal - 面拉伸为实体（法向）
- EditGeneral.ExtrudeAreaToSolidLinearUser - 面拉伸为实体（用户定义）
- EditGeneral.ExtrudeAreaToSolidRadial - 面拉伸为实体（径向）
- EditGeneral.ExtrudeFrameToAreaLinear - 框架拉伸为面
- EditGeneral.ExtrudeFrameToAreaRadial - 框架拉伸为面（径向）
- EditGeneral.ExtrudePointToFrameLinear - 点拉伸为框架
- EditGeneral.ExtrudePointToFrameRadial - 点拉伸为框架（径向）
- EditGeneral.Move - 移动
- EditGeneral.ReplicateLinear - 线性复制
- EditGeneral.ReplicateMirror - 镜像复制
- EditGeneral.ReplicateRadial - 径向复制
"""

from typing import List
from PySap2000.com_helper import com_ret, com_data


def extrude_area_to_solid_linear_normal(
    model,
    num_solid: int,
    thickness: float,
    delete_original: bool = False
) -> List[str]:
    """
    沿法向将选中面单元拉伸为实体
    
    Args:
        model: SapModel 对象
        num_solid: 实体数量
        thickness: 总厚度
        delete_original: 是否删除原面单元
        
    Returns:
        新创建的实体名称列表
    """
    result = model.EditGeneral.ExtrudeAreaToSolidLinearNormal(
        num_solid, thickness, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def extrude_area_to_solid_linear_user(
    model,
    num_solid: int,
    dx: float,
    dy: float,
    dz: float,
    delete_original: bool = False
) -> List[str]:
    """
    沿用户定义方向将选中面单元拉伸为实体
    
    Args:
        model: SapModel 对象
        num_solid: 实体数量
        dx: X方向增量
        dy: Y方向增量
        dz: Z方向增量
        delete_original: 是否删除原面单元
        
    Returns:
        新创建的实体名称列表
    """
    result = model.EditGeneral.ExtrudeAreaToSolidLinearUser(
        num_solid, dx, dy, dz, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def extrude_area_to_solid_radial(
    model,
    num_solid: int,
    total_angle: float,
    x: float,
    y: float,
    z: float,
    rx: float,
    ry: float,
    rz: float,
    delete_original: bool = False
) -> List[str]:
    """
    径向将选中面单元拉伸为实体
    
    Args:
        model: SapModel 对象
        num_solid: 实体数量
        total_angle: 总角度 [deg]
        x, y, z: 旋转轴上的点坐标
        rx, ry, rz: 旋转轴方向向量
        delete_original: 是否删除原面单元
        
    Returns:
        新创建的实体名称列表
    """
    result = model.EditGeneral.ExtrudeAreaToSolidRadial(
        num_solid, total_angle, x, y, z, rx, ry, rz, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def extrude_frame_to_area_linear(
    model,
    num_area: int,
    dx: float,
    dy: float,
    dz: float,
    delete_original: bool = False
) -> List[str]:
    """
    线性将选中框架拉伸为面单元
    
    Args:
        model: SapModel 对象
        num_area: 面单元数量
        dx: X方向增量
        dy: Y方向增量
        dz: Z方向增量
        delete_original: 是否删除原框架
        
    Returns:
        新创建的面单元名称列表
    """
    result = model.EditGeneral.ExtrudeFrameToAreaLinear(
        num_area, dx, dy, dz, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def extrude_frame_to_area_radial(
    model,
    num_area: int,
    total_angle: float,
    x: float,
    y: float,
    z: float,
    rx: float,
    ry: float,
    rz: float,
    delete_original: bool = False
) -> List[str]:
    """
    径向将选中框架拉伸为面单元
    
    Args:
        model: SapModel 对象
        num_area: 面单元数量
        total_angle: 总角度 [deg]
        x, y, z: 旋转轴上的点坐标
        rx, ry, rz: 旋转轴方向向量
        delete_original: 是否删除原框架
        
    Returns:
        新创建的面单元名称列表
    """
    result = model.EditGeneral.ExtrudeFrameToAreaRadial(
        num_area, total_angle, x, y, z, rx, ry, rz, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def extrude_point_to_frame_linear(
    model,
    num_frame: int,
    dx: float,
    dy: float,
    dz: float,
    delete_original: bool = False
) -> List[str]:
    """
    线性将选中点拉伸为框架
    
    Args:
        model: SapModel 对象
        num_frame: 框架数量
        dx: X方向增量
        dy: Y方向增量
        dz: Z方向增量
        delete_original: 是否删除原点
        
    Returns:
        新创建的框架名称列表
    """
    result = model.EditGeneral.ExtrudePointToFrameLinear(
        num_frame, dx, dy, dz, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def extrude_point_to_frame_radial(
    model,
    num_frame: int,
    total_angle: float,
    x: float,
    y: float,
    z: float,
    rx: float,
    ry: float,
    rz: float,
    delete_original: bool = False
) -> List[str]:
    """
    径向将选中点拉伸为框架
    
    Args:
        model: SapModel 对象
        num_frame: 框架数量
        total_angle: 总角度 [deg]
        x, y, z: 旋转轴上的点坐标
        rx, ry, rz: 旋转轴方向向量
        delete_original: 是否删除原点
        
    Returns:
        新创建的框架名称列表
    """
    result = model.EditGeneral.ExtrudePointToFrameRadial(
        num_frame, total_angle, x, y, z, rx, ry, rz, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def move_selected(
    model,
    dx: float,
    dy: float,
    dz: float
) -> int:
    """
    移动选中对象
    
    Args:
        model: SapModel 对象
        dx: X方向移动量
        dy: Y方向移动量
        dz: Z方向移动量
        
    Returns:
        0 表示成功
    """
    return model.EditGeneral.Move(dx, dy, dz)


def replicate_linear(
    model,
    num: int,
    dx: float,
    dy: float,
    dz: float
) -> int:
    """
    线性复制选中对象
    
    Args:
        model: SapModel 对象
        num: 复制数量
        dx: X方向增量
        dy: Y方向增量
        dz: Z方向增量
        
    Returns:
        0 表示成功
    """
    return model.EditGeneral.ReplicateLinear(num, dx, dy, dz)


def replicate_mirror(
    model,
    plane: int,
    x: float = 0.0,
    y: float = 0.0,
    z: float = 0.0
) -> int:
    """
    镜像复制选中对象
    
    Args:
        model: SapModel 对象
        plane: 镜像平面
            1 = 平行于YZ平面
            2 = 平行于XZ平面
            3 = 平行于XY平面
        x, y, z: 镜像平面上的点坐标
        
    Returns:
        0 表示成功
    """
    return model.EditGeneral.ReplicateMirror(plane, x, y, z)


def replicate_radial(
    model,
    num: int,
    total_angle: float,
    x: float,
    y: float,
    z: float,
    rx: float,
    ry: float,
    rz: float
) -> int:
    """
    径向复制选中对象
    
    Args:
        model: SapModel 对象
        num: 复制数量
        total_angle: 总角度 [deg]
        x, y, z: 旋转轴上的点坐标
        rx, ry, rz: 旋转轴方向向量
        
    Returns:
        0 表示成功
    """
    return model.EditGeneral.ReplicateRadial(num, total_angle, x, y, z, rx, ry, rz)
