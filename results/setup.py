# -*- coding: utf-8 -*-
"""
setup.py - Analysis result output settings.

Function wrappers for the SAP2000 `Results.Setup` API.

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
    Deselect all cases and combinations for output.

    This is commonly called before querying results so the caller can select
    only the required cases or combinations.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `0` if successful.
        
    Example:
        deselect_all_cases_and_combos(model)
        set_case_selected_for_output(model, "DEAD", True)
        results = get_joint_displ(model, "ALL", ItemTypeElm.GROUP_ELM)
    """
    return model.Results.Setup.DeselectAllCasesAndCombosForOutput()


def set_case_selected_for_output(model, case_name: str, selected: bool = True) -> int:
    """
    Set whether a case is selected for output.
    
    Args:
        model: SAP2000 SapModel object
        case_name: Case name
        selected: `True` to select, `False` to deselect
        
    Returns:
        `0` if successful.
        
    Example:
        set_case_selected_for_output(model, "DEAD", True)
        set_case_selected_for_output(model, "MODAL", True)
    """
    return model.Results.Setup.SetCaseSelectedForOutput(case_name, selected)


def get_case_selected_for_output(model, case_name: str) -> bool:
    """
    Get whether a case is selected for output.
    
    Args:
        model: SAP2000 SapModel object
        case_name: Case name
        
    Returns:
        `True` if selected, otherwise `False`.
    """
    result = model.Results.Setup.GetCaseSelectedForOutput(case_name, False)
    return bool(com_data(result, 0, False))


def set_combo_selected_for_output(model, combo_name: str, selected: bool = True) -> int:
    """
    Set whether a combination is selected for output.
    
    Args:
        model: SAP2000 SapModel object
        combo_name: Combination name
        selected: `True` to select, `False` to deselect
        
    Returns:
        `0` if successful.
        
    Example:
        set_combo_selected_for_output(model, "COMB1", True)
    """
    return model.Results.Setup.SetComboSelectedForOutput(combo_name, selected)


def get_combo_selected_for_output(model, combo_name: str) -> bool:
    """
    Get whether a combination is selected for output.
    
    Args:
        model: SAP2000 SapModel object
        combo_name: Combination name
        
    Returns:
        `True` if selected, otherwise `False`.
    """
    result = model.Results.Setup.GetComboSelectedForOutput(combo_name, False)
    return bool(com_data(result, 0, False))


def select_cases_for_output(model, case_names: List[str]) -> int:
    """
    Convenience helper that clears all selections and selects the given cases.
    
    Args:
        model: SAP2000 SapModel object
        case_names: List of case names
        
    Returns:
        `0` if successful.
        
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
    Convenience helper that clears all selections and selects the given combinations.
    
    Args:
        model: SAP2000 SapModel object
        combo_names: List of combination names
        
    Returns:
        `0` if successful.
        
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
# Base reaction location options
# =============================================================================

def get_option_base_react_loc(model) -> Tuple[float, float, float]:
    """
    Get the reporting location for base reactions.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Tuple `(gx, gy, gz)` in global coordinates.
    """
    result = model.Results.Setup.GetOptionBaseReactLoc(0.0, 0.0, 0.0)
    return (
        com_data(result, 0, 0.0),
        com_data(result, 1, 0.0),
        com_data(result, 2, 0.0),
    )


def set_option_base_react_loc(model, gx: float, gy: float, gz: float) -> int:
    """
    Set the reporting location for base reactions.
    
    Args:
        model: SAP2000 SapModel object
        gx: Global X coordinate
        gy: Global Y coordinate
        gz: Global Z coordinate
        
    Returns:
        `0` if successful.
    """
    return model.Results.Setup.SetOptionBaseReactLoc(gx, gy, gz)


# =============================================================================
# Buckling mode options
# =============================================================================

def get_option_buckling_mode(model) -> int:
    """
    Get the buckling mode result option.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Buckling mode number (1-based).
    """
    result = model.Results.Setup.GetOptionBucklingMode(0)
    return com_data(result, 0, 1)


def set_option_buckling_mode(model, buckling_mode_num: int) -> int:
    """
    Set the buckling mode result option.
    
    Args:
        model: SAP2000 SapModel object
        buckling_mode_num: Buckling mode number (1-based)
        
    Returns:
        `0` if successful.
    """
    return model.Results.Setup.SetOptionBucklingMode(buckling_mode_num)


# =============================================================================
# Direct-history options
# =============================================================================

def get_option_direct_hist(model) -> int:
    """
    Get the direct-integration time-history result option.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Option value:
        `1` = Envelopes
        `2` = Step-by-Step
        `3` = Last Step
    """
    result = model.Results.Setup.GetOptionDirectHist(0)
    return com_data(result, 0, 1)


def set_option_direct_hist(model, value: int) -> int:
    """
    Set the direct-integration time-history result option.
    
    Args:
        model: SAP2000 SapModel object
        value: Option value
            `1` = Envelopes
            `2` = Step-by-Step
            `3` = Last Step
        
    Returns:
        `0` if successful.
    """
    return model.Results.Setup.SetOptionDirectHist(value)


# =============================================================================
# Modal-history options
# =============================================================================

def get_option_modal_hist(model) -> int:
    """
    Get the modal time-history result option.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Option value:
        `1` = Envelopes
        `2` = Step-by-Step
        `3` = Last Step
    """
    result = model.Results.Setup.GetOptionModalHist(0)
    return com_data(result, 0, 1)


def set_option_modal_hist(model, value: int) -> int:
    """
    Set the modal time-history result option.
    
    Args:
        model: SAP2000 SapModel object
        value: Option value
            `1` = Envelopes
            `2` = Step-by-Step
            `3` = Last Step
        
    Returns:
        `0` if successful.
    """
    return model.Results.Setup.SetOptionModalHist(value)


# =============================================================================
# Mode-shape options
# =============================================================================

def get_option_mode_shape(model) -> Tuple[int, int]:
    """
    Get the mode-shape result option.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Tuple `(mode_num, run_case_num)`.
    """
    result = model.Results.Setup.GetOptionModeShape(0, 0)
    return (com_data(result, 0, 1), com_data(result, 1, 1))


def set_option_mode_shape(model, mode_num: int, run_case_num: int = 1) -> int:
    """
    Set the mode-shape result option.
    
    Args:
        model: SAP2000 SapModel object
        mode_num: Mode number (1-based)
        run_case_num: Run-case number (1-based)
        
    Returns:
        `0` if successful.
    """
    return model.Results.Setup.SetOptionModeShape(mode_num, run_case_num)


# =============================================================================
# Multi-step static options
# =============================================================================

def get_option_multi_step_static(model) -> int:
    """
    Get the multi-step static result option.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Option value:
        `1` = Envelopes
        `2` = Step-by-Step
        `3` = Last Step
    """
    result = model.Results.Setup.GetOptionMultiStepStatic(0)
    return com_data(result, 0, 1)


def set_option_multi_step_static(model, value: int) -> int:
    """
    Set the multi-step static result option.
    
    Args:
        model: SAP2000 SapModel object
        value: Option value
            `1` = Envelopes
            `2` = Step-by-Step
            `3` = Last Step
        
    Returns:
        `0` if successful.
    """
    return model.Results.Setup.SetOptionMultiStepStatic(value)


# =============================================================================
# Multi-valued combo options
# =============================================================================

def get_option_multi_valued_combo(model) -> int:
    """
    Get the multi-valued combination result option.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Option value:
        `1` = Envelopes
        `2` = Multiple Values if Possible
        `3` = Correspondence
    """
    result = model.Results.Setup.GetOptionMultiValuedCombo(0)
    return com_data(result, 0, 1)


def set_option_multi_valued_combo(model, value: int) -> int:
    """
    Set the multi-valued combination result option.
    
    Args:
        model: SAP2000 SapModel object
        value: Option value
            `1` = Envelopes
            `2` = Multiple Values if Possible
            `3` = Correspondence
        
    Returns:
        `0` if successful.
    """
    return model.Results.Setup.SetOptionMultiValuedCombo(value)


# =============================================================================
# Nonlinear static options
# =============================================================================

def get_option_nl_static(model) -> int:
    """
    Get the nonlinear static result option.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Option value:
        `1` = Envelopes
        `2` = Step-by-Step
        `3` = Last Step
    """
    result = model.Results.Setup.GetOptionNLStatic(0)
    return com_data(result, 0, 1)


def set_option_nl_static(model, value: int) -> int:
    """
    Set the nonlinear static result option.
    
    Args:
        model: SAP2000 SapModel object
        value: Option value
            `1` = Envelopes
            `2` = Step-by-Step
            `3` = Last Step
        
    Returns:
        `0` if successful.
    """
    return model.Results.Setup.SetOptionNLStatic(value)


# =============================================================================
# PSD options
# =============================================================================

def get_option_psd(model) -> int:
    """
    Get the power spectral density result option.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Option value:
        `1` = RMS
        `2` = sqrt(PSD)
    """
    result = model.Results.Setup.GetOptionPSD(0)
    return com_data(result, 0, 1)


def set_option_psd(model, value: int) -> int:
    """
    Set the power spectral density result option.
    
    Args:
        model: SAP2000 SapModel object
        value: Option value
            `1` = RMS
            `2` = sqrt(PSD)
        
    Returns:
        `0` if successful.
    """
    return model.Results.Setup.SetOptionPSD(value)


# =============================================================================
# Steady-state options
# =============================================================================

def get_option_steady_state(model) -> int:
    """
    Get the steady-state result option.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Option value:
        `1` = Envelopes
        `2` = At Frequencies
    """
    result = model.Results.Setup.GetOptionSteadyState(0)
    return com_data(result, 0, 1)


def set_option_steady_state(model, value: int) -> int:
    """
    Set the steady-state result option.
    
    Args:
        model: SAP2000 SapModel object
        value: Option value
            `1` = Envelopes
            `2` = At Frequencies
        
    Returns:
        `0` if successful.
    """
    return model.Results.Setup.SetOptionSteadyState(value)


# =============================================================================
# Section-cut options
# =============================================================================

def get_section_cut_selected_for_output(model, name: str) -> bool:
    """
    Get whether a section cut is selected for output.
    
    Args:
        model: SAP2000 SapModel object
        name: Section-cut name
        
    Returns:
        `True` if selected, otherwise `False`.
    """
    result = model.Results.Setup.GetSectionCutSelectedForOutput(name, False)
    return bool(com_data(result, 0, False))


def set_section_cut_selected_for_output(model, name: str, selected: bool = True) -> int:
    """
    Set whether a section cut is selected for output.
    
    Args:
        model: SAP2000 SapModel object
        name: Section-cut name
        selected: `True` to select, `False` to deselect
        
    Returns:
        `0` if successful.
    """
    return model.Results.Setup.SetSectionCutSelectedForOutput(name, selected)


def select_all_section_cuts_for_output(model, selected: bool = True) -> int:
    """
    Select or deselect all section cuts for output.
    
    Args:
        model: SAP2000 SapModel object
        selected: `True` to select all, `False` to deselect all
        
    Returns:
        `0` if successful.
    """
    return model.Results.Setup.SelectAllSectionCutsForOutput(selected)
