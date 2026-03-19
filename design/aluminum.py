# -*- coding: utf-8 -*-
"""
design/aluminum.py - 铝结构设计函数

SAP2000 DesignAluminum API 的 Python 封装。
API 路径: SapModel.DesignAluminum
"""

from typing import List, Union

from .enums import (
    AluminumDesignCode, ALUMINUM_CODE_NAMES, ALUMINUM_CODE_FROM_NAME,
    ItemType, RatioType,
)
from .data_classes import SteelSummaryResult, VerifyPassedResult
from PySap2000.com_helper import com_ret, com_data

# 铝结构汇总结果复用 SteelSummaryResult（API 签名完全相同）
AluminumSummaryResult = SteelSummaryResult


# ============================================================================
# 规范设置
# ============================================================================

def get_aluminum_code(model) -> str:
    """获取当前铝结构设计规范

    Args:
        model: SapModel 对象

    Returns:
        规范名称字符串
    """
    result = model.DesignAluminum.GetCode("")
    return com_data(result, 0, "")


def set_aluminum_code(model, code: Union[AluminumDesignCode, str]) -> int:
    """设置铝结构设计规范

    Args:
        model: SapModel 对象
        code: 规范枚举或规范名称字符串

    Returns:
        0 表示成功，非 0 表示失败
    """
    if isinstance(code, AluminumDesignCode):
        code_name = ALUMINUM_CODE_NAMES.get(code, "AA-ASD 2000")
    else:
        code_name = code
    ret = model.DesignAluminum.SetCode(code_name)
    return com_ret(ret)


# ============================================================================
# 设计执行
# ============================================================================

def start_aluminum_design(model) -> int:
    """开始铝结构设计

    注意：需要先运行分析，且模型中存在铝框架对象。

    Args:
        model: SapModel 对象

    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignAluminum.StartDesign()
    return com_ret(ret)


def delete_aluminum_results(model) -> int:
    """删除所有铝结构设计结果

    Args:
        model: SapModel 对象

    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignAluminum.DeleteResults()
    return com_ret(ret)


def get_aluminum_results_available(model) -> bool:
    """检查铝结构设计结果是否可用

    Args:
        model: SapModel 对象

    Returns:
        True 表示结果可用
    """
    result = model.DesignAluminum.GetResultsAvailable()
    return bool(com_data(result, 0, result))


# ============================================================================
# 设计组合
# ============================================================================

def get_aluminum_combo_strength(model) -> List[str]:
    """获取用于强度设计的荷载组合"""
    result = model.DesignAluminum.GetComboStrength(0, [])
    names = com_data(result, 1)
    return list(names) if names else []


def set_aluminum_combo_strength(model, name: str, selected: bool = True) -> int:
    """设置荷载组合是否用于强度设计"""
    ret = model.DesignAluminum.SetComboStrength(name, selected)
    return com_ret(ret)


def get_aluminum_combo_deflection(model) -> List[str]:
    """获取用于挠度设计的荷载组合"""
    result = model.DesignAluminum.GetComboDeflection(0, [])
    names = com_data(result, 1)
    return list(names) if names else []


def set_aluminum_combo_deflection(model, name: str, selected: bool = True) -> int:
    """设置荷载组合是否用于挠度设计"""
    ret = model.DesignAluminum.SetComboDeflection(name, selected)
    return com_ret(ret)


def get_aluminum_combo_auto_generate(model) -> bool:
    """获取是否自动生成设计组合"""
    result = model.DesignAluminum.GetComboAutoGenerate(False)
    return bool(com_data(result, 0, False))


def set_aluminum_combo_auto_generate(model, auto_generate: bool = True) -> int:
    """设置是否自动生成设计组合"""
    ret = model.DesignAluminum.SetComboAutoGenerate(auto_generate)
    return com_ret(ret)


# ============================================================================
# 设计组
# ============================================================================

def get_aluminum_design_group(model) -> List[str]:
    """获取选中用于铝结构设计的组"""
    result = model.DesignAluminum.GetGroup(0, [])
    names = com_data(result, 1)
    return list(names) if names else []


def set_aluminum_design_group(model, name: str, selected: bool = True) -> int:
    """设置组是否用于铝结构设计"""
    ret = model.DesignAluminum.SetGroup(name, selected)
    return com_ret(ret)


# ============================================================================
# 设计截面
# ============================================================================

def get_aluminum_design_section(model, name: str) -> str:
    """获取框架对象的设计截面"""
    result = model.DesignAluminum.GetDesignSection(name, "")
    return com_data(result, 0, "")


def set_aluminum_design_section(
    model,
    name: str,
    prop_name: str = "",
    last_analysis: bool = False,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """设置框架对象的设计截面"""
    ret = model.DesignAluminum.SetDesignSection(name, prop_name, last_analysis, int(item_type))
    return com_ret(ret)


def set_aluminum_auto_select_null(model, name: str, item_type: ItemType = ItemType.OBJECT) -> int:
    """将自动选择截面设为 None（移除自动选择）

    Args:
        model: SapModel 对象
        name: 对象名称
        item_type: 对象选择类型

    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignAluminum.SetAutoSelectNull(name, int(item_type))
    return com_ret(ret)


# ============================================================================
# 覆盖重置与验证
# ============================================================================

def reset_aluminum_overwrites(model) -> int:
    """重置所有铝结构设计覆盖为默认值"""
    ret = model.DesignAluminum.ResetOverwrites()
    return com_ret(ret)


def verify_aluminum_passed(model) -> VerifyPassedResult:
    """验证铝结构设计是否通过"""
    result = model.DesignAluminum.VerifyPassed(0, 0, 0, [])
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


def verify_aluminum_sections(model) -> List[str]:
    """验证分析截面与设计截面是否一致"""
    result = model.DesignAluminum.VerifySections(0, [])
    names = com_data(result, 1)
    return list(names) if names else []


# ============================================================================
# 汇总结果
# ============================================================================

def get_aluminum_summary_results(
    model,
    name: str,
    item_type: ItemType = ItemType.OBJECT
) -> List[AluminumSummaryResult]:
    """获取铝结构设计汇总结果

    注意：RatioType 仅有 1(PMM), 3(Major shear), 4(Minor shear)。

    Args:
        model: SapModel 对象
        name: 对象名称、组名称或忽略（取决于 item_type）
        item_type: 对象选择类型

    Returns:
        设计结果列表
    """
    result = model.DesignAluminum.GetSummaryResults(
        name, 0, [], [], [], [], [], [], [], int(item_type)
    )

    results = []
    num_items = com_data(result, 0, 0)
    if not num_items or num_items <= 0:
        return results

    frame_names = com_data(result, 1) or []
    ratios = com_data(result, 2) or []
    ratio_types = com_data(result, 3) or []
    locations = com_data(result, 4) or []
    combo_names = com_data(result, 5) or []
    error_summaries = com_data(result, 6) or []
    warning_summaries = com_data(result, 7) or []

    for i in range(num_items):
        try:
            ratio_type_val = ratio_types[i] if i < len(ratio_types) else 0
            ratio_type = RatioType(ratio_type_val)
        except ValueError:
            ratio_type = RatioType.NONE

        results.append(AluminumSummaryResult(
            frame_name=frame_names[i] if i < len(frame_names) else "",
            ratio=ratios[i] if i < len(ratios) else 0.0,
            ratio_type=ratio_type,
            location=locations[i] if i < len(locations) else 0.0,
            combo_name=combo_names[i] if i < len(combo_names) else "",
            error_summary=error_summaries[i] if i < len(error_summaries) else "",
            warning_summary=warning_summaries[i] if i < len(warning_summaries) else "",
        ))

    return results
