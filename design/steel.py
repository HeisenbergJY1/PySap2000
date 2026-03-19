# -*- coding: utf-8 -*-
"""
design/steel.py - 钢结构设计函数

SAP2000 DesignSteel API 的 Python 封装。
"""

from typing import List, Optional, Union

from .enums import SteelDesignCode, RatioType, ItemType, STEEL_CODE_NAMES, STEEL_CODE_FROM_NAME
from .data_classes import SteelSummaryResult, VerifyPassedResult
from PySap2000.com_helper import com_ret, com_data


def get_steel_code(model) -> str:
    """获取当前钢结构设计规范
    
    Args:
        model: SapModel 对象
        
    Returns:
        规范名称字符串
    """
    result = model.DesignSteel.GetCode("")
    return com_data(result, 0, "")


def set_steel_code(model, code: Union[SteelDesignCode, str]) -> int:
    """设置钢结构设计规范
    
    Args:
        model: SapModel 对象
        code: 规范枚举或规范名称字符串
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    if isinstance(code, SteelDesignCode):
        code_name = STEEL_CODE_NAMES.get(code, "AISC 360-10")
    else:
        code_name = code
    
    ret = model.DesignSteel.SetCode(code_name)
    return com_ret(ret)


def start_steel_design(model) -> int:
    """开始钢结构设计
    
    注意：需要先运行分析，且模型中存在钢框架对象。
    
    Args:
        model: SapModel 对象
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignSteel.StartDesign()
    return com_ret(ret)


def delete_steel_results(model) -> int:
    """删除所有钢结构设计结果
    
    Args:
        model: SapModel 对象
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignSteel.DeleteResults()
    return com_ret(ret)


def get_steel_results_available(model) -> bool:
    """检查钢结构设计结果是否可用
    
    Args:
        model: SapModel 对象
        
    Returns:
        True 表示结果可用，False 表示不可用
    """
    result = model.DesignSteel.GetResultsAvailable()
    return bool(com_data(result, 0, result))


def get_steel_summary_results(
    model,
    name: str,
    item_type: ItemType = ItemType.OBJECT
) -> List[SteelSummaryResult]:
    """获取钢结构设计汇总结果
    
    Args:
        model: SapModel 对象
        name: 对象名称、组名称或忽略（取决于 item_type）
        item_type: 对象选择类型
        
    Returns:
        设计结果列表
    """
    result = model.DesignSteel.GetSummaryResults(
        name, 0, [], [], [], [], [], [], [], int(item_type)
    )
    
    results = []
    num_items = com_data(result, 0, 0)
    if num_items and num_items > 0:
        frame_names = com_data(result, 1) or []
        ratios = com_data(result, 2) or []
        ratio_types = com_data(result, 3) or []
        locations = com_data(result, 4) or []
        combo_names = com_data(result, 5) or []
        error_summaries = com_data(result, 6) or []
        warning_summaries = com_data(result, 7) or []
        
        for i in range(num_items):
            # 安全处理 ratio_type，未知值默认为 NONE
            try:
                ratio_type_val = ratio_types[i] if i < len(ratio_types) else 0
                ratio_type = RatioType(ratio_type_val)
            except ValueError:
                ratio_type = RatioType.NONE
            
            results.append(SteelSummaryResult(
                frame_name=frame_names[i] if i < len(frame_names) else "",
                ratio=ratios[i] if i < len(ratios) else 0.0,
                ratio_type=ratio_type,
                location=locations[i] if i < len(locations) else 0.0,
                combo_name=combo_names[i] if i < len(combo_names) else "",
                error_summary=error_summaries[i] if i < len(error_summaries) else "",
                warning_summary=warning_summaries[i] if i < len(warning_summaries) else "",
            ))
    
    return results


def get_steel_design_group(model) -> List[str]:
    """获取选中用于钢结构设计的组
    
    Args:
        model: SapModel 对象
        
    Returns:
        组名称列表
    """
    result = model.DesignSteel.GetGroup(0, [])
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


def set_steel_design_group(model, name: str, selected: bool = True) -> int:
    """设置组是否用于钢结构设计
    
    Args:
        model: SapModel 对象
        name: 组名称
        selected: True 选中，False 取消选中
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignSteel.SetGroup(name, selected)
    return com_ret(ret)


def get_steel_design_section(model, name: str) -> str:
    """获取框架对象的设计截面
    
    Args:
        model: SapModel 对象
        name: 框架对象名称
        
    Returns:
        设计截面名称
    """
    result = model.DesignSteel.GetDesignSection(name, "")
    return com_data(result, 0, "")


def set_steel_design_section(
    model,
    name: str,
    prop_name: str = "",
    last_analysis: bool = False,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """设置框架对象的设计截面
    
    Args:
        model: SapModel 对象
        name: 对象名称、组名称或忽略（取决于 item_type）
        prop_name: 截面名称（last_analysis=False 时使用）
        last_analysis: True 使用最后分析截面，False 使用指定截面
        item_type: 对象选择类型
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignSteel.SetDesignSection(name, prop_name, last_analysis, int(item_type))
    return com_ret(ret)


def get_steel_combo_strength(model) -> List[str]:
    """获取用于强度设计的荷载组合
    
    Args:
        model: SapModel 对象
        
    Returns:
        组合名称列表
    """
    result = model.DesignSteel.GetComboStrength(0, [])
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


def set_steel_combo_strength(model, name: str, selected: bool = True) -> int:
    """设置荷载组合是否用于强度设计
    
    Args:
        model: SapModel 对象
        name: 荷载组合名称
        selected: True 选中，False 取消选中
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignSteel.SetComboStrength(name, selected)
    return com_ret(ret)


def get_steel_combo_deflection(model) -> List[str]:
    """获取用于挠度设计的荷载组合
    
    Args:
        model: SapModel 对象
        
    Returns:
        组合名称列表
    """
    result = model.DesignSteel.GetComboDeflection(0, [])
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


def set_steel_combo_deflection(model, name: str, selected: bool = True) -> int:
    """设置荷载组合是否用于挠度设计
    
    Args:
        model: SapModel 对象
        name: 荷载组合名称
        selected: True 选中，False 取消选中
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignSteel.SetComboDeflection(name, selected)
    return com_ret(ret)


def get_steel_combo_auto_generate(model) -> bool:
    """获取是否自动生成设计组合

    Args:
        model: SapModel 对象

    Returns:
        True 表示自动生成
    """
    result = model.DesignSteel.GetComboAutoGenerate(False)
    return bool(com_data(result, 0, False))


def set_steel_combo_auto_generate(model, auto_generate: bool = True) -> int:
    """设置是否自动生成设计组合

    Args:
        model: SapModel 对象
        auto_generate: True 自动生成

    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignSteel.SetComboAutoGenerate(auto_generate)
    return com_ret(ret)


def set_steel_auto_select_null(model, name: str, item_type: ItemType = ItemType.OBJECT) -> int:
    """将自动选择截面设为 None（移除自动选择）

    Args:
        model: SapModel 对象
        name: 对象名称
        item_type: 对象选择类型

    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignSteel.SetAutoSelectNull(name, int(item_type))
    return com_ret(ret)


def reset_steel_overwrites(model) -> int:
    """重置所有钢结构设计覆盖为默认值
    
    Args:
        model: SapModel 对象
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignSteel.ResetOverwrites()
    return com_ret(ret)


def verify_steel_passed(model) -> VerifyPassedResult:
    """验证钢结构设计是否通过
    
    获取未通过设计检查或尚未检查的框架对象。
    
    Args:
        model: SapModel 对象
        
    Returns:
        验证结果
    """
    result = model.DesignSteel.VerifyPassed(0, 0, 0, [])
    
    total_count = com_data(result, 0, 0)
    failed_count = com_data(result, 1, 0)
    unchecked_count = com_data(result, 2, 0)
    names = com_data(result, 3) or []
    
    if total_count is not None:
        return VerifyPassedResult(
            total_count=total_count,
            failed_count=failed_count,
            unchecked_count=unchecked_count,
            frame_names=list(names) if names else [],
        )
    
    return VerifyPassedResult(0, 0, 0, [])


def verify_steel_sections(model) -> List[str]:
    """验证分析截面与设计截面是否一致
    
    获取分析截面与设计截面不同的框架对象。
    
    Args:
        model: SapModel 对象
        
    Returns:
        截面不一致的框架对象名称列表
    """
    result = model.DesignSteel.VerifySections(0, [])
    
    names = com_data(result, 1)
    if names:
        return list(names)
    return []
