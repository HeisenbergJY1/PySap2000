# -*- coding: utf-8 -*-
"""
design/concrete.py - 混凝土框架设计函数

SAP2000 DesignConcrete API 的 Python 封装。
API 路径: SapModel.DesignConcrete
"""

from typing import List, Union

from .enums import (
    ConcreteDesignCode, CONCRETE_CODE_NAMES, CONCRETE_CODE_FROM_NAME,
    ItemType, ColumnDesignOption,
)
from .data_classes import (
    ConcreteBeamResult, ConcreteColumnResult, ConcreteJointResult,
    VerifyPassedResult,
)
from PySap2000.com_helper import com_ret, com_data


# ============================================================================
# 规范设置
# ============================================================================

def get_concrete_code(model) -> str:
    """获取当前混凝土框架设计规范

    Args:
        model: SapModel 对象

    Returns:
        规范名称字符串
    """
    result = model.DesignConcrete.GetCode("")
    return com_data(result, 0, "")


def set_concrete_code(model, code: Union[ConcreteDesignCode, str]) -> int:
    """设置混凝土框架设计规范

    Args:
        model: SapModel 对象
        code: 规范枚举或规范名称字符串

    Returns:
        0 表示成功，非 0 表示失败
    """
    if isinstance(code, ConcreteDesignCode):
        code_name = CONCRETE_CODE_NAMES.get(code, "ACI 318-14")
    else:
        code_name = code
    ret = model.DesignConcrete.SetCode(code_name)
    return com_ret(ret)


# ============================================================================
# 设计执行
# ============================================================================

def start_concrete_design(model) -> int:
    """开始混凝土框架设计

    注意：需要先运行分析，且模型中存在混凝土框架对象。

    Args:
        model: SapModel 对象

    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignConcrete.StartDesign()
    return com_ret(ret)


def delete_concrete_results(model) -> int:
    """删除所有混凝土框架设计结果

    Args:
        model: SapModel 对象

    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignConcrete.DeleteResults()
    return com_ret(ret)


def get_concrete_results_available(model) -> bool:
    """检查混凝土框架设计结果是否可用

    Args:
        model: SapModel 对象

    Returns:
        True 表示结果可用
    """
    result = model.DesignConcrete.GetResultsAvailable()
    return bool(com_data(result, 0, result))


# ============================================================================
# 设计组合
# ============================================================================

def get_concrete_combo_strength(model) -> List[str]:
    """获取用于强度设计的荷载组合

    Args:
        model: SapModel 对象

    Returns:
        组合名称列表
    """
    result = model.DesignConcrete.GetComboStrength(0, [])
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


def set_concrete_combo_strength(model, name: str, selected: bool = True) -> int:
    """设置荷载组合是否用于强度设计

    Args:
        model: SapModel 对象
        name: 荷载组合名称
        selected: True 选中，False 取消选中

    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignConcrete.SetComboStrength(name, selected)
    return com_ret(ret)


def get_concrete_combo_auto_generate(model) -> bool:
    """获取是否自动生成设计组合

    Args:
        model: SapModel 对象

    Returns:
        True 表示自动生成
    """
    result = model.DesignConcrete.GetComboAutoGenerate(False)
    return bool(com_data(result, 0, False))


def set_concrete_combo_auto_generate(model, auto_generate: bool = True) -> int:
    """设置是否自动生成设计组合

    Args:
        model: SapModel 对象
        auto_generate: True 自动生成

    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignConcrete.SetComboAutoGenerate(auto_generate)
    return com_ret(ret)


# ============================================================================
# 设计组
# ============================================================================

def get_concrete_design_group(model) -> List[str]:
    """获取选中用于混凝土设计的组

    Args:
        model: SapModel 对象

    Returns:
        组名称列表
    """
    result = model.DesignConcrete.GetGroup(0, [])
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


def set_concrete_design_group(model, name: str, selected: bool = True) -> int:
    """设置组是否用于混凝土设计

    Args:
        model: SapModel 对象
        name: 组名称
        selected: True 选中，False 取消选中

    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignConcrete.SetGroup(name, selected)
    return com_ret(ret)


# ============================================================================
# 设计截面
# ============================================================================

def get_concrete_design_section(model, name: str) -> str:
    """获取框架对象的设计截面

    Args:
        model: SapModel 对象
        name: 框架对象名称

    Returns:
        设计截面名称
    """
    result = model.DesignConcrete.GetDesignSection(name, "")
    return com_data(result, 0, "")


def set_concrete_design_section(
    model,
    name: str,
    prop_name: str = "",
    last_analysis: bool = False,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """设置框架对象的设计截面

    Args:
        model: SapModel 对象
        name: 对象名称
        prop_name: 截面名称
        last_analysis: True 使用最后分析截面
        item_type: 对象选择类型

    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignConcrete.SetDesignSection(name, prop_name, last_analysis, int(item_type))
    return com_ret(ret)


# ============================================================================
# 覆盖重置
# ============================================================================

def reset_concrete_overwrites(model) -> int:
    """重置所有混凝土设计覆盖为默认值

    Args:
        model: SapModel 对象

    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignConcrete.ResetOverwrites()
    return com_ret(ret)


# ============================================================================
# 验证
# ============================================================================

def verify_concrete_passed(model) -> VerifyPassedResult:
    """验证混凝土设计是否通过

    Args:
        model: SapModel 对象

    Returns:
        验证结果
    """
    result = model.DesignConcrete.VerifyPassed(0, 0, 0, [])
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


def verify_concrete_sections(model) -> List[str]:
    """验证分析截面与设计截面是否一致

    Args:
        model: SapModel 对象

    Returns:
        截面不一致的框架对象名称列表
    """
    result = model.DesignConcrete.VerifySections(0, [])
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


# ============================================================================
# 汇总结果
# ============================================================================

def get_concrete_summary_results_beam(
    model,
    name: str,
    item_type: ItemType = ItemType.OBJECT
) -> List[ConcreteBeamResult]:
    """获取混凝土梁设计汇总结果

    Args:
        model: SapModel 对象
        name: 对象名称、组名称或忽略（取决于 item_type）
        item_type: 对象选择类型

    Returns:
        梁设计结果列表
    """
    result = model.DesignConcrete.GetSummaryResultsBeam(
        name, 0, [], [], [], [], [], [], [], [], [], [], [], [], [], int(item_type)
    )

    results = []
    num_items = com_data(result, 0, 0)
    if not num_items or num_items <= 0:
        return results

    frame_names = com_data(result, 1) or []
    locations = com_data(result, 2) or []
    top_combos = com_data(result, 3) or []
    top_areas = com_data(result, 4) or []
    bot_combos = com_data(result, 5) or []
    bot_areas = com_data(result, 6) or []
    vmajor_combos = com_data(result, 7) or []
    vmajor_areas = com_data(result, 8) or []
    tl_combos = com_data(result, 9) or []
    tl_areas = com_data(result, 10) or []
    tt_combos = com_data(result, 11) or []
    tt_areas = com_data(result, 12) or []
    error_summaries = com_data(result, 13) or []
    warning_summaries = com_data(result, 14) or []

    for i in range(num_items):
        results.append(ConcreteBeamResult(
            frame_name=frame_names[i] if i < len(frame_names) else "",
            location=locations[i] if i < len(locations) else 0.0,
            top_combo=top_combos[i] if i < len(top_combos) else "",
            top_area=top_areas[i] if i < len(top_areas) else 0.0,
            bot_combo=bot_combos[i] if i < len(bot_combos) else "",
            bot_area=bot_areas[i] if i < len(bot_areas) else 0.0,
            vmajor_combo=vmajor_combos[i] if i < len(vmajor_combos) else "",
            vmajor_area=vmajor_areas[i] if i < len(vmajor_areas) else 0.0,
            tl_combo=tl_combos[i] if i < len(tl_combos) else "",
            tl_area=tl_areas[i] if i < len(tl_areas) else 0.0,
            tt_combo=tt_combos[i] if i < len(tt_combos) else "",
            tt_area=tt_areas[i] if i < len(tt_areas) else 0.0,
            error_summary=error_summaries[i] if i < len(error_summaries) else "",
            warning_summary=warning_summaries[i] if i < len(warning_summaries) else "",
        ))

    return results


def get_concrete_summary_results_column(
    model,
    name: str,
    item_type: ItemType = ItemType.OBJECT
) -> List[ConcreteColumnResult]:
    """获取混凝土柱设计汇总结果

    Args:
        model: SapModel 对象
        name: 对象名称、组名称或忽略（取决于 item_type）
        item_type: 对象选择类型

    Returns:
        柱设计结果列表
    """
    result = model.DesignConcrete.GetSummaryResultsColumn(
        name, 0, [], [], [], [], [], [], [], [], [], [], [], [], int(item_type)
    )

    results = []
    num_items = com_data(result, 0, 0)
    if not num_items or num_items <= 0:
        return results

    frame_names = com_data(result, 1) or []
    my_options = com_data(result, 2) or []
    locations = com_data(result, 3) or []
    pmm_combos = com_data(result, 4) or []
    pmm_areas = com_data(result, 5) or []
    pmm_ratios = com_data(result, 6) or []
    vmajor_combos = com_data(result, 7) or []
    av_majors = com_data(result, 8) or []
    vminor_combos = com_data(result, 9) or []
    av_minors = com_data(result, 10) or []
    error_summaries = com_data(result, 11) or []
    warning_summaries = com_data(result, 12) or []

    for i in range(num_items):
        try:
            opt_val = my_options[i] if i < len(my_options) else 1
            design_opt = ColumnDesignOption(opt_val)
        except ValueError:
            design_opt = ColumnDesignOption.CHECK

        results.append(ConcreteColumnResult(
            frame_name=frame_names[i] if i < len(frame_names) else "",
            design_option=design_opt,
            location=locations[i] if i < len(locations) else 0.0,
            pmm_combo=pmm_combos[i] if i < len(pmm_combos) else "",
            pmm_area=pmm_areas[i] if i < len(pmm_areas) else 0.0,
            pmm_ratio=pmm_ratios[i] if i < len(pmm_ratios) else 0.0,
            vmajor_combo=vmajor_combos[i] if i < len(vmajor_combos) else "",
            av_major=av_majors[i] if i < len(av_majors) else 0.0,
            vminor_combo=vminor_combos[i] if i < len(vminor_combos) else "",
            av_minor=av_minors[i] if i < len(av_minors) else 0.0,
            error_summary=error_summaries[i] if i < len(error_summaries) else "",
            warning_summary=warning_summaries[i] if i < len(warning_summaries) else "",
        ))

    return results


def get_concrete_summary_results_joint(
    model,
    name: str,
    item_type: ItemType = ItemType.OBJECT
) -> List[ConcreteJointResult]:
    """获取混凝土节点设计汇总结果

    注意：节点设计仅部分规范支持。

    Args:
        model: SapModel 对象
        name: 对象名称、组名称或忽略（取决于 item_type）
        item_type: 对象选择类型

    Returns:
        节点设计结果列表
    """
    result = model.DesignConcrete.GetSummaryResultsJoint(
        name, 0, [], [], [], [], [], [], [], [], [], [], [], int(item_type)
    )

    results = []
    num_items = com_data(result, 0, 0)
    if not num_items or num_items <= 0:
        return results

    frame_names = com_data(result, 1) or []
    lc_js_major = com_data(result, 2) or []
    js_major = com_data(result, 3) or []
    lc_js_minor = com_data(result, 4) or []
    js_minor = com_data(result, 5) or []
    lc_bcc_major = com_data(result, 6) or []
    bcc_major = com_data(result, 7) or []
    lc_bcc_minor = com_data(result, 8) or []
    bcc_minor = com_data(result, 9) or []
    error_summaries = com_data(result, 10) or []
    warning_summaries = com_data(result, 11) or []

    for i in range(num_items):
        results.append(ConcreteJointResult(
            frame_name=frame_names[i] if i < len(frame_names) else "",
            js_ratio_major_combo=lc_js_major[i] if i < len(lc_js_major) else "",
            js_ratio_major=js_major[i] if i < len(js_major) else 0.0,
            js_ratio_minor_combo=lc_js_minor[i] if i < len(lc_js_minor) else "",
            js_ratio_minor=js_minor[i] if i < len(js_minor) else 0.0,
            bcc_ratio_major_combo=lc_bcc_major[i] if i < len(lc_bcc_major) else "",
            bcc_ratio_major=bcc_major[i] if i < len(bcc_major) else 0.0,
            bcc_ratio_minor_combo=lc_bcc_minor[i] if i < len(lc_bcc_minor) else "",
            bcc_ratio_minor=bcc_minor[i] if i < len(bcc_minor) else 0.0,
            error_summary=error_summaries[i] if i < len(error_summaries) else "",
            warning_summary=warning_summaries[i] if i < len(warning_summaries) else "",
        ))

    return results
