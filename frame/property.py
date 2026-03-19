# -*- coding: utf-8 -*-
"""
property.py - 杆件属性分配函数
对应 SAP2000 的 FrameObj.SetSection / GetSection

本模块用于分配属性到杆件（怎么用），而非定义属性（是什么）。
属性定义请使用 properties 模块。

Usage:
    from frame import set_frame_section, get_frame_section
    
    # 分配截面到杆件
    set_frame_section(model, "1", "W14X22")
    
    # 获取杆件的截面
    section_name = get_frame_section(model, "1")
"""

from typing import Optional, Tuple
from .enums import ItemType
from .data_classes import FrameSectionNonPrismaticData
from PySap2000.com_helper import com_ret, com_data


def set_frame_section(
    model,
    frame_name: str,
    section_name: str,
    item_type: ItemType = ItemType.OBJECT,
    var_total_length: float = 0.0,
    var_rel_start_loc: float = 0.0,
) -> int:
    """
    设置杆件的截面属性
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        section_name: 截面名称 (必须已在 PropFrame 中定义)
        item_type: 项目类型
            - OBJECT (0): 单个对象
            - GROUP (1): 组内所有对象
            - SELECTED (2): 所有选中对象
        var_total_length: 变截面假定总长度，0 表示与杆件等长（仅变截面有效）
        var_rel_start_loc: 变截面起点到杆件 I 端的相对距离（仅 var_total_length > 0 时有效）
    
    Returns:
        0 表示成功，非 0 表示失败
    
    Example:
        # 设置杆件 "1" 的截面为 "W14X22"
        set_frame_section(model, "1", "W14X22")
        
        # 设置组 "Beams" 内所有杆件的截面
        set_frame_section(model, "Beams", "W14X22", ItemType.GROUP)
        
        # 分配变截面，指定总长度和起始位置
        set_frame_section(model, "8", "NP1", var_total_length=360, var_rel_start_loc=0.1)
    """
    return model.FrameObj.SetSection(
        str(frame_name),
        section_name,
        item_type.value,
        var_rel_start_loc,
        var_total_length,
    )


def get_frame_section(model, frame_name: str) -> str:
    """
    获取杆件的截面属性名称
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        截面名称
    
    Example:
        section = get_frame_section(model, "1")
        print(f"杆件 1 的截面: {section}")
    """
    result = model.FrameObj.GetSection(str(frame_name))
    return com_data(result, 0, "") or ""


def get_frame_section_info(model, frame_name: str) -> Tuple[str, str]:
    """
    获取杆件的截面信息（包括自动选择截面）
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        (section_name, auto_select_list) 元组
        - section_name: 当前截面名称
        - auto_select_list: 自动选择列表名称（如果有）
    
    Example:
        section, auto_list = get_frame_section_info(model, "1")
        if auto_list:
            print(f"使用自动选择: {auto_list}")
    """
    result = model.FrameObj.GetSection(str(frame_name))
    return (com_data(result, 0, "") or "", com_data(result, 1, "") or "")


def set_frame_material_overwrite(
    model,
    frame_name: str,
    material_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置杆件的材料覆盖
    
    覆盖截面属性中定义的材料。
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        material_name: 材料名称，空字符串表示使用截面属性中的材料
        item_type: 项目类型
    
    Returns:
        0 表示成功，非 0 表示失败
    
    Example:
        # 覆盖杆件 "1" 的材料为 "A992Fy50"
        set_frame_material_overwrite(model, "1", "A992Fy50")
        
        # 清除材料覆盖，使用截面属性中的材料
        set_frame_material_overwrite(model, "1", "")
    """
    return model.FrameObj.SetMaterialOverwrite(
        str(frame_name),
        material_name,
        item_type.value
    )


def get_frame_material_overwrite(model, frame_name: str) -> str:
    """
    获取杆件的材料覆盖
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        材料名称，空字符串表示未覆盖
    
    Example:
        mat = get_frame_material_overwrite(model, "1")
        if mat:
            print(f"材料覆盖: {mat}")
        else:
            print("使用截面属性中的材料")
    """
    result = model.FrameObj.GetMaterialOverwrite(str(frame_name))
    material = com_data(result, 0, "") or ""
    # 'None' 字符串表示无覆盖，返回空字符串
    if material == "None":
        return ""
    return material


def set_frame_material_temperature(
    model,
    frame_name: str,
    temperature: float,
    pattern_name: str = "",
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置杆件的材料温度
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        temperature: 温度值 [T]
        pattern_name: 荷载模式名称，空字符串表示无模式
        item_type: 项目类型
    
    Returns:
        0 表示成功，非 0 表示失败
    
    Example:
        # 设置杆件 "1" 的材料温度为 20°C
        set_frame_material_temperature(model, "1", 20.0)
    """
    return model.FrameObj.SetMatTemp(
        str(frame_name),
        temperature,
        pattern_name,
        item_type.value
    )


def get_frame_material_temperature(model, frame_name: str) -> Tuple[float, str]:
    """
    获取杆件的材料温度
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        (temperature, pattern_name) 元组
    
    Example:
        temp, pattern = get_frame_material_temperature(model, "1")
        print(f"温度: {temp}, 模式: {pattern}")
    """
    result = model.FrameObj.GetMatTemp(str(frame_name))
    return (com_data(result, 0, 0.0), com_data(result, 1, "") or "")


def get_frame_section_nonprismatic(
    model,
    frame_name: str,
) -> FrameSectionNonPrismaticData:
    """
    获取杆件的变截面属性数据
    
    对应 FrameObj.GetSectionNonPrismatic API。
    仅当杆件分配了变截面属性时有效，否则返回错误。
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        FrameSectionNonPrismaticData 数据类
    
    Raises:
        ValueError: 杆件未分配变截面属性
    
    Example:
        data = get_frame_section_nonprismatic(model, "876")
        print(f"变截面: {data.prop_name}, 总长: {data.total_length}")
    """
    result = model.FrameObj.GetSectionNonPrismatic(
        str(frame_name), "", 0.0, 0.0
    )
    ret = com_ret(result)
    if ret != 0:
        raise ValueError(f"杆件 {frame_name} 未分配变截面属性或获取失败")
    return FrameSectionNonPrismaticData(
        frame_name=frame_name,
        prop_name=com_data(result, 0, "") or "",
        total_length=com_data(result, 1, 0.0),
        rel_start_loc=com_data(result, 2, 0.0),
    )
