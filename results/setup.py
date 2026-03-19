# -*- coding: utf-8 -*-
"""
setup.py - 分析结果输出设置

SAP2000 Results.Setup API 的函数封装

SAP2000 API:
- Results.Setup.DeselectAllCasesAndCombosForOutput
- Results.Setup.SetCaseSelectedForOutput / GetCaseSelectedForOutput
- Results.Setup.SetComboSelectedForOutput / GetComboSelectedForOutput
- Results.Setup.SetOptionBaseReactLoc / GetOptionBaseReactLoc
- Results.Setup.SetOptionBucklingMode / GetOptionBucklingMode
- Results.Setup.SetOptionDirectHist / GetOptionDirectHist
- Results.Setup.SetOptionModalHist / GetOptionModalHist
- Results.Setup.SetOptionModeShape / GetOptionModeShape
- Results.Setup.SetOptionMultiStepStatic / GetOptionMultiStepStatic
- Results.Setup.SetOptionMultiValuedCombo / GetOptionMultiValuedCombo
- Results.Setup.SetOptionNLStatic / GetOptionNLStatic
- Results.Setup.SetOptionPSD / GetOptionPSD
- Results.Setup.SetOptionSteadyState / GetOptionSteadyState
- Results.Setup.SetSectionCutSelectedForOutput / GetSectionCutSelectedForOutput
- Results.Setup.SelectAllSectionCutsForOutput
"""

from typing import List, Tuple, Optional
from PySap2000.com_helper import com_ret, com_data


def deselect_all_cases_and_combos(model) -> int:
    """
    取消选择所有工况和组合用于输出
    
    在获取结果前，通常先调用此函数清除所有选择，
    然后再选择需要的工况或组合。
    
    Args:
        model: SapModel 对象
        
    Returns:
        0 表示成功
        
    Example:
        deselect_all_cases_and_combos(model)
        set_case_selected_for_output(model, "DEAD", True)
        results = get_joint_displ(model, "ALL", ItemTypeElm.GROUP_ELM)
    """
    return model.Results.Setup.DeselectAllCasesAndCombosForOutput()


def set_case_selected_for_output(model, case_name: str, selected: bool = True) -> int:
    """
    设置工况是否选择用于输出
    
    Args:
        model: SapModel 对象
        case_name: 工况名称
        selected: True 选择，False 取消选择
        
    Returns:
        0 表示成功
        
    Example:
        set_case_selected_for_output(model, "DEAD", True)
        set_case_selected_for_output(model, "MODAL", True)
    """
    return model.Results.Setup.SetCaseSelectedForOutput(case_name, selected)


def get_case_selected_for_output(model, case_name: str) -> bool:
    """
    获取工况是否被选择用于输出
    
    Args:
        model: SapModel 对象
        case_name: 工况名称
        
    Returns:
        True 表示已选择，False 表示未选择
    """
    result = model.Results.Setup.GetCaseSelectedForOutput(case_name, False)
    return bool(com_data(result, 0, False))


def set_combo_selected_for_output(model, combo_name: str, selected: bool = True) -> int:
    """
    设置组合是否选择用于输出
    
    Args:
        model: SapModel 对象
        combo_name: 组合名称
        selected: True 选择，False 取消选择
        
    Returns:
        0 表示成功
        
    Example:
        set_combo_selected_for_output(model, "COMB1", True)
    """
    return model.Results.Setup.SetComboSelectedForOutput(combo_name, selected)


def get_combo_selected_for_output(model, combo_name: str) -> bool:
    """
    获取组合是否被选择用于输出
    
    Args:
        model: SapModel 对象
        combo_name: 组合名称
        
    Returns:
        True 表示已选择，False 表示未选择
    """
    result = model.Results.Setup.GetComboSelectedForOutput(combo_name, False)
    return bool(com_data(result, 0, False))


def select_cases_for_output(model, case_names: List[str]) -> int:
    """
    便捷函数：清除所有选择并选择指定工况
    
    Args:
        model: SapModel 对象
        case_names: 工况名称列表
        
    Returns:
        0 表示成功
        
    Example:
        select_cases_for_output(model, ["DEAD", "LIVE"])
    """
    ret = deselect_all_cases_and_combos(model)
    if ret != 0:
        return ret
    for name in case_names:
        ret = set_case_selected_for_output(model, name, True)
        if ret != 0:
            return ret
    return 0


def select_combos_for_output(model, combo_names: List[str]) -> int:
    """
    便捷函数：清除所有选择并选择指定组合
    
    Args:
        model: SapModel 对象
        combo_names: 组合名称列表
        
    Returns:
        0 表示成功
        
    Example:
        select_combos_for_output(model, ["COMB1", "COMB2"])
    """
    ret = deselect_all_cases_and_combos(model)
    if ret != 0:
        return ret
    for name in combo_names:
        ret = set_combo_selected_for_output(model, name, True)
        if ret != 0:
            return ret
    return 0


# =============================================================================
# 基底反力位置选项
# =============================================================================

def get_option_base_react_loc(model) -> Tuple[float, float, float]:
    """
    获取基底反力报告位置
    
    Args:
        model: SapModel 对象
        
    Returns:
        (gx, gy, gz) 全局坐标
    """
    result = model.Results.Setup.GetOptionBaseReactLoc(0.0, 0.0, 0.0)
    return (
        com_data(result, 0, 0.0),
        com_data(result, 1, 0.0),
        com_data(result, 2, 0.0),
    )


def set_option_base_react_loc(model, gx: float, gy: float, gz: float) -> int:
    """
    设置基底反力报告位置
    
    Args:
        model: SapModel 对象
        gx: 全局X坐标
        gy: 全局Y坐标
        gz: 全局Z坐标
        
    Returns:
        0 表示成功
    """
    return model.Results.Setup.SetOptionBaseReactLoc(gx, gy, gz)


# =============================================================================
# 屈曲模态选项
# =============================================================================

def get_option_buckling_mode(model) -> int:
    """
    获取屈曲模态结果选项
    
    Args:
        model: SapModel 对象
        
    Returns:
        屈曲模态号 (1-based)
    """
    result = model.Results.Setup.GetOptionBucklingMode(0)
    return com_data(result, 0, 1)


def set_option_buckling_mode(model, buckling_mode_num: int) -> int:
    """
    设置屈曲模态结果选项
    
    Args:
        model: SapModel 对象
        buckling_mode_num: 屈曲模态号 (1-based)
        
    Returns:
        0 表示成功
    """
    return model.Results.Setup.SetOptionBucklingMode(buckling_mode_num)


# =============================================================================
# 直接积分时程选项
# =============================================================================

def get_option_direct_hist(model) -> int:
    """
    获取直接积分时程分析结果选项
    
    Args:
        model: SapModel 对象
        
    Returns:
        选项值:
        1 = Envelopes (包络)
        2 = Step-by-Step (逐步)
        3 = Last Step (最后一步)
    """
    result = model.Results.Setup.GetOptionDirectHist(0)
    return com_data(result, 0, 1)


def set_option_direct_hist(model, value: int) -> int:
    """
    设置直接积分时程分析结果选项
    
    Args:
        model: SapModel 对象
        value: 选项值
            1 = Envelopes (包络)
            2 = Step-by-Step (逐步)
            3 = Last Step (最后一步)
        
    Returns:
        0 表示成功
    """
    return model.Results.Setup.SetOptionDirectHist(value)


# =============================================================================
# 模态时程选项
# =============================================================================

def get_option_modal_hist(model) -> int:
    """
    获取模态时程分析结果选项
    
    Args:
        model: SapModel 对象
        
    Returns:
        选项值:
        1 = Envelopes (包络)
        2 = Step-by-Step (逐步)
        3 = Last Step (最后一步)
    """
    result = model.Results.Setup.GetOptionModalHist(0)
    return com_data(result, 0, 1)


def set_option_modal_hist(model, value: int) -> int:
    """
    设置模态时程分析结果选项
    
    Args:
        model: SapModel 对象
        value: 选项值
            1 = Envelopes (包络)
            2 = Step-by-Step (逐步)
            3 = Last Step (最后一步)
        
    Returns:
        0 表示成功
    """
    return model.Results.Setup.SetOptionModalHist(value)


# =============================================================================
# 振型选项
# =============================================================================

def get_option_mode_shape(model) -> Tuple[int, int]:
    """
    获取振型结果选项
    
    Args:
        model: SapModel 对象
        
    Returns:
        (mode_num, run_case_num) 振型号和运行工况号
    """
    result = model.Results.Setup.GetOptionModeShape(0, 0)
    return (com_data(result, 0, 1), com_data(result, 1, 1))


def set_option_mode_shape(model, mode_num: int, run_case_num: int = 1) -> int:
    """
    设置振型结果选项
    
    Args:
        model: SapModel 对象
        mode_num: 振型号 (1-based)
        run_case_num: 运行工况号 (1-based)
        
    Returns:
        0 表示成功
    """
    return model.Results.Setup.SetOptionModeShape(mode_num, run_case_num)


# =============================================================================
# 多步静力选项
# =============================================================================

def get_option_multi_step_static(model) -> int:
    """
    获取多步静力分析结果选项
    
    Args:
        model: SapModel 对象
        
    Returns:
        选项值:
        1 = Envelopes (包络)
        2 = Step-by-Step (逐步)
        3 = Last Step (最后一步)
    """
    result = model.Results.Setup.GetOptionMultiStepStatic(0)
    return com_data(result, 0, 1)


def set_option_multi_step_static(model, value: int) -> int:
    """
    设置多步静力分析结果选项
    
    Args:
        model: SapModel 对象
        value: 选项值
            1 = Envelopes (包络)
            2 = Step-by-Step (逐步)
            3 = Last Step (最后一步)
        
    Returns:
        0 表示成功
    """
    return model.Results.Setup.SetOptionMultiStepStatic(value)


# =============================================================================
# 多值组合选项
# =============================================================================

def get_option_multi_valued_combo(model) -> int:
    """
    获取多值组合结果选项
    
    Args:
        model: SapModel 对象
        
    Returns:
        选项值:
        1 = Envelopes (包络)
        2 = Multiple Values if Possible (尽可能多值)
        3 = Correspondence (对应)
    """
    result = model.Results.Setup.GetOptionMultiValuedCombo(0)
    return com_data(result, 0, 1)


def set_option_multi_valued_combo(model, value: int) -> int:
    """
    设置多值组合结果选项
    
    Args:
        model: SapModel 对象
        value: 选项值
            1 = Envelopes (包络)
            2 = Multiple Values if Possible (尽可能多值)
            3 = Correspondence (对应)
        
    Returns:
        0 表示成功
    """
    return model.Results.Setup.SetOptionMultiValuedCombo(value)


# =============================================================================
# 非线性静力选项
# =============================================================================

def get_option_nl_static(model) -> int:
    """
    获取非线性静力分析结果选项
    
    Args:
        model: SapModel 对象
        
    Returns:
        选项值:
        1 = Envelopes (包络)
        2 = Step-by-Step (逐步)
        3 = Last Step (最后一步)
    """
    result = model.Results.Setup.GetOptionNLStatic(0)
    return com_data(result, 0, 1)


def set_option_nl_static(model, value: int) -> int:
    """
    设置非线性静力分析结果选项
    
    Args:
        model: SapModel 对象
        value: 选项值
            1 = Envelopes (包络)
            2 = Step-by-Step (逐步)
            3 = Last Step (最后一步)
        
    Returns:
        0 表示成功
    """
    return model.Results.Setup.SetOptionNLStatic(value)


# =============================================================================
# 功率谱密度选项
# =============================================================================

def get_option_psd(model) -> int:
    """
    获取功率谱密度分析结果选项
    
    Args:
        model: SapModel 对象
        
    Returns:
        选项值:
        1 = RMS (均方根)
        2 = sqrt(PSD) (功率谱密度平方根)
    """
    result = model.Results.Setup.GetOptionPSD(0)
    return com_data(result, 0, 1)


def set_option_psd(model, value: int) -> int:
    """
    设置功率谱密度分析结果选项
    
    Args:
        model: SapModel 对象
        value: 选项值
            1 = RMS (均方根)
            2 = sqrt(PSD) (功率谱密度平方根)
        
    Returns:
        0 表示成功
    """
    return model.Results.Setup.SetOptionPSD(value)


# =============================================================================
# 稳态选项
# =============================================================================

def get_option_steady_state(model) -> int:
    """
    获取稳态分析结果选项
    
    Args:
        model: SapModel 对象
        
    Returns:
        选项值:
        1 = Envelopes (包络)
        2 = At Frequencies (在频率处)
    """
    result = model.Results.Setup.GetOptionSteadyState(0)
    return com_data(result, 0, 1)


def set_option_steady_state(model, value: int) -> int:
    """
    设置稳态分析结果选项
    
    Args:
        model: SapModel 对象
        value: 选项值
            1 = Envelopes (包络)
            2 = At Frequencies (在频率处)
        
    Returns:
        0 表示成功
    """
    return model.Results.Setup.SetOptionSteadyState(value)


# =============================================================================
# 截面切割选项
# =============================================================================

def get_section_cut_selected_for_output(model, name: str) -> bool:
    """
    获取截面切割是否被选择用于输出
    
    Args:
        model: SapModel 对象
        name: 截面切割名称
        
    Returns:
        True 表示已选择，False 表示未选择
    """
    result = model.Results.Setup.GetSectionCutSelectedForOutput(name, False)
    return bool(com_data(result, 0, False))


def set_section_cut_selected_for_output(model, name: str, selected: bool = True) -> int:
    """
    设置截面切割是否选择用于输出
    
    Args:
        model: SapModel 对象
        name: 截面切割名称
        selected: True 选择，False 取消选择
        
    Returns:
        0 表示成功
    """
    return model.Results.Setup.SetSectionCutSelectedForOutput(name, selected)


def select_all_section_cuts_for_output(model, selected: bool = True) -> int:
    """
    选择或取消选择所有截面切割用于输出
    
    Args:
        model: SapModel 对象
        selected: True 选择所有，False 取消选择所有
        
    Returns:
        0 表示成功
    """
    return model.Results.Setup.SelectAllSectionCutsForOutput(selected)
