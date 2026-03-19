# -*- coding: utf-8 -*-
"""
file.py - 文件操作

SAP2000 File API 封装

SAP2000 API:
- File.New2DFrame - 新建2D框架
- File.New3DFrame - 新建3D框架
- File.NewBeam - 新建梁
- File.NewBlank - 新建空白模型
- File.NewSolidBlock - 新建实体块
- File.NewWall - 新建墙
- File.OpenFile - 打开文件
- File.Save - 保存文件
"""

from enum import IntEnum


class Units(IntEnum):
    """
    单位制
    
    SAP2000 API: eUnits
    """
    LB_IN_F = 1         # lb, in, F
    LB_FT_F = 2         # lb, ft, F
    KIP_IN_F = 3        # kip, in, F
    KIP_FT_F = 4        # kip, ft, F
    KN_MM_C = 5         # kN, mm, C
    KN_M_C = 6          # kN, m, C
    KGF_MM_C = 7        # kgf, mm, C
    KGF_M_C = 8         # kgf, m, C
    N_MM_C = 9          # N, mm, C
    N_M_C = 10          # N, m, C
    TON_MM_C = 11       # Ton, mm, C
    TON_M_C = 12        # Ton, m, C
    KN_CM_C = 13        # kN, cm, C
    KGF_CM_C = 14       # kgf, cm, C
    N_CM_C = 15         # N, cm, C
    TON_CM_C = 16       # Ton, cm, C


# =============================================================================
# 新建模型
# =============================================================================

def new_blank(model, units: Units = Units.KN_M_C) -> int:
    """
    新建空白模型
    
    Args:
        model: SapModel 对象
        units: 单位制
        
    Returns:
        0 表示成功
        
    Example:
        new_blank(model, Units.KN_M_C)
    """
    return model.File.NewBlank(int(units))


def new_2d_frame(
    model,
    template_type: int,
    num_stories: int,
    story_height: float,
    num_bays: int,
    bay_width: float,
    restraint: bool = True,
    beam_section: str = "",
    column_section: str = "",
    brace_section: str = "",
    units: Units = Units.KN_M_C
) -> int:
    """
    新建2D框架模型
    
    Args:
        model: SapModel 对象
        template_type: 模板类型
            0 = 门式框架
            1 = 连续梁
            2 = 简支梁
            3 = 悬臂梁
            4 = 桁架
        num_stories: 层数
        story_height: 层高
        num_bays: 跨数
        bay_width: 跨度
        restraint: 是否添加约束
        beam_section: 梁截面名称
        column_section: 柱截面名称
        brace_section: 支撑截面名称
        units: 单位制
        
    Returns:
        0 表示成功
    """
    return model.File.New2DFrame(
        template_type, num_stories, story_height, num_bays, bay_width,
        restraint, beam_section, column_section, brace_section, int(units)
    )


def new_3d_frame(
    model,
    template_type: int,
    num_stories: int,
    story_height: float,
    num_bays_x: int,
    bay_width_x: float,
    num_bays_y: int,
    bay_width_y: float,
    restraint: bool = True,
    beam_section: str = "",
    column_section: str = "",
    brace_section: str = "",
    units: Units = Units.KN_M_C
) -> int:
    """
    新建3D框架模型
    
    Args:
        model: SapModel 对象
        template_type: 模板类型
            0 = 开放框架
            1 = 周边框架
            2 = 带支撑框架
        num_stories: 层数
        story_height: 层高
        num_bays_x: X方向跨数
        bay_width_x: X方向跨度
        num_bays_y: Y方向跨数
        bay_width_y: Y方向跨度
        restraint: 是否添加约束
        beam_section: 梁截面名称
        column_section: 柱截面名称
        brace_section: 支撑截面名称
        units: 单位制
        
    Returns:
        0 表示成功
    """
    return model.File.New3DFrame(
        template_type, num_stories, story_height,
        num_bays_x, bay_width_x, num_bays_y, bay_width_y,
        restraint, beam_section, column_section, brace_section, int(units)
    )


def new_beam(
    model,
    num_spans: int,
    span_length: float,
    restraint: bool = True,
    section: str = "",
    units: Units = Units.KN_M_C
) -> int:
    """
    新建梁模型
    
    Args:
        model: SapModel 对象
        num_spans: 跨数
        span_length: 跨度
        restraint: 是否添加约束
        section: 截面名称
        units: 单位制
        
    Returns:
        0 表示成功
    """
    return model.File.NewBeam(num_spans, span_length, restraint, section, int(units))


def new_solid_block(
    model,
    width_x: float,
    width_y: float,
    height: float,
    restraint: bool = True,
    units: Units = Units.KN_M_C
) -> int:
    """
    新建实体块模型
    
    Args:
        model: SapModel 对象
        width_x: X方向宽度
        width_y: Y方向宽度
        height: 高度
        restraint: 是否添加约束
        units: 单位制
        
    Returns:
        0 表示成功
    """
    return model.File.NewSolidBlock(width_x, width_y, height, restraint, int(units))


def new_wall(
    model,
    num_x: int,
    num_z: int,
    width: float,
    height: float,
    restraint: bool = True,
    section: str = "",
    units: Units = Units.KN_M_C
) -> int:
    """
    新建墙模型
    
    Args:
        model: SapModel 对象
        num_x: X方向分割数
        num_z: Z方向分割数
        width: 宽度
        height: 高度
        restraint: 是否添加约束
        section: 截面名称
        units: 单位制
        
    Returns:
        0 表示成功
    """
    return model.File.NewWall(num_x, num_z, width, height, restraint, section, int(units))


# =============================================================================
# 文件操作
# =============================================================================

def open_file(model, file_path: str) -> int:
    """
    打开文件
    
    Args:
        model: SapModel 对象
        file_path: 文件路径
        
    Returns:
        0 表示成功
        
    Example:
        open_file(model, r"C:\\Models\\example.sdb")
    """
    return model.File.OpenFile(file_path)


def save(model, file_path: str = "") -> int:
    """
    保存文件
    
    Args:
        model: SapModel 对象
        file_path: 文件路径（空字符串表示保存到当前路径）
        
    Returns:
        0 表示成功
        
    Example:
        save(model)  # 保存到当前路径
        save(model, r"C:\\Models\\example.sdb")  # 另存为
    """
    if file_path:
        return model.File.Save(file_path)
    else:
        return model.File.Save()
