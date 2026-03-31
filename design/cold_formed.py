# -*- coding: utf-8 -*-
"""
design/cold_formed.py - Cold-formed steel design helpers

Python wrapper for the SAP2000 `DesignColdFormed` API.
API path: `SapModel.DesignColdFormed`
"""

from typing import List, Union

from .enums import (
    ColdFormedDesignCode, COLD_FORMED_CODE_NAMES, COLD_FORMED_CODE_FROM_NAME,
    ItemType, RatioType,
)
from .data_classes import SteelSummaryResult, VerifyPassedResult
from PySap2000.com_helper import com_ret, com_data

# Reuse `SteelSummaryResult` for cold-formed steel (same API layout)
ColdFormedSummaryResult = SteelSummaryResult


# ============================================================================
# Code selection
# ============================================================================

def get_cold_formed_code(model) -> str:
    """Get the active cold-formed steel design code

    Args:
        model: SAP2000 SapModel object

    Returns:
        Code name string
    """
    result = model.DesignColdFormed.GetCode("")
    return com_data(result, 0, "")


def set_cold_formed_code(model, code: Union[ColdFormedDesignCode, str]) -> int:
    """Set the cold-formed steel design code

    Args:
        model: SAP2000 SapModel object
        code: Code enum or code name string

    Returns:
        `0` on success, non-zero on failure
    """
    if isinstance(code, ColdFormedDesignCode):
        code_name = COLD_FORMED_CODE_NAMES.get(code, "AISI-ASD96")
    else:
        code_name = code
    ret = model.DesignColdFormed.SetCode(code_name)
    return com_ret(ret)


# ============================================================================
# Run design
# ============================================================================

def start_cold_formed_design(model) -> int:
    """Run cold-formed steel design

    Requires analysis to be run and cold-formed frame objects in the model.

    Args:
        model: SAP2000 SapModel object

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignColdFormed.StartDesign()
    return com_ret(ret)


def delete_cold_formed_results(model) -> int:
    """Delete all cold-formed design results"""
    ret = model.DesignColdFormed.DeleteResults()
    return com_ret(ret)


def get_cold_formed_results_available(model) -> bool:
    """Whether cold-formed design results are available"""
    result = model.DesignColdFormed.GetResultsAvailable()
    return bool(com_data(result, 0, result))


# ============================================================================
# Load combinations
# ============================================================================

def get_cold_formed_combo_strength(model) -> List[str]:
    """Load combinations used for strength design"""
    result = model.DesignColdFormed.GetComboStrength(0, [])
    names = com_data(result, 1)
    return list(names) if names else []


def set_cold_formed_combo_strength(model, name: str, selected: bool = True) -> int:
    """Select a load combination for strength design"""
    ret = model.DesignColdFormed.SetComboStrength(name, selected)
    return com_ret(ret)


def get_cold_formed_combo_deflection(model) -> List[str]:
    """Load combinations used for deflection design"""
    result = model.DesignColdFormed.GetComboDeflection(0, [])
    names = com_data(result, 1)
    return list(names) if names else []


def set_cold_formed_combo_deflection(model, name: str, selected: bool = True) -> int:
    """Select a load combination for deflection design"""
    ret = model.DesignColdFormed.SetComboDeflection(name, selected)
    return com_ret(ret)


def get_cold_formed_combo_auto_generate(model) -> bool:
    """Whether design combinations are auto-generated"""
    result = model.DesignColdFormed.GetComboAutoGenerate(False)
    return bool(com_data(result, 0, False))


def set_cold_formed_combo_auto_generate(model, auto_generate: bool = True) -> int:
    """Enable or disable auto-generation of design combinations"""
    ret = model.DesignColdFormed.SetComboAutoGenerate(auto_generate)
    return com_ret(ret)


# ============================================================================
# DesignGroup
# ============================================================================

def get_cold_formed_design_group(model) -> List[str]:
    """Groups selected for cold-formed design"""
    result = model.DesignColdFormed.GetGroup(0, [])
    names = com_data(result, 1)
    return list(names) if names else []


def set_cold_formed_design_group(model, name: str, selected: bool = True) -> int:
    """Select or deselect a group for cold-formed design"""
    ret = model.DesignColdFormed.SetGroup(name, selected)
    return com_ret(ret)


# ============================================================================
# Design section
# ============================================================================

def get_cold_formed_design_section(model, name: str) -> str:
    """Get the design section assigned to a frame"""
    result = model.DesignColdFormed.GetDesignSection(name, "")
    return com_data(result, 0, "")


def set_cold_formed_design_section(
    model,
    name: str,
    prop_name: str = "",
    last_analysis: bool = False,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """Set the design section for frame objects"""
    ret = model.DesignColdFormed.SetDesignSection(name, prop_name, last_analysis, int(item_type))
    return com_ret(ret)


def set_cold_formed_auto_select_null(model, name: str, item_type: ItemType = ItemType.OBJECT) -> int:
    """Clear auto-select section (set to None)"""
    ret = model.DesignColdFormed.SetAutoSelectNull(name, int(item_type))
    return com_ret(ret)


# ============================================================================
# Overwrites and verification
# ============================================================================

def reset_cold_formed_overwrites(model) -> int:
    """Reset all cold-formed design overwrites to defaults"""
    ret = model.DesignColdFormed.ResetOverwrites()
    return com_ret(ret)


def verify_cold_formed_passed(model) -> VerifyPassedResult:
    """Verify cold-formed design acceptance"""
    result = model.DesignColdFormed.VerifyPassed(0, 0, 0, [])
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


def verify_cold_formed_sections(model) -> List[str]:
    """Verify analysis vs. design section assignments"""
    result = model.DesignColdFormed.VerifySections(0, [])
    names = com_data(result, 1)
    return list(names) if names else []


# ============================================================================
# Summary results
# ============================================================================

def get_cold_formed_summary_results(
    model,
    name: str,
    item_type: ItemType = ItemType.OBJECT
) -> List[ColdFormedSummaryResult]:
    """Get cold-formed design summary results

    Note: only `RatioType` values 1 (PMM), 3 (major shear), and 4 (minor shear) apply.

    Args:
        model: SAP2000 SapModel object
        name: Object name, group name, or ignored depending on `item_type`
        item_type: Object selection mode

    Returns:
        List of design results
    """
    result = model.DesignColdFormed.GetSummaryResults(
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

        results.append(ColdFormedSummaryResult(
            frame_name=frame_names[i] if i < len(frame_names) else "",
            ratio=ratios[i] if i < len(ratios) else 0.0,
            ratio_type=ratio_type,
            location=locations[i] if i < len(locations) else 0.0,
            combo_name=combo_names[i] if i < len(combo_names) else "",
            error_summary=error_summaries[i] if i < len(error_summaries) else "",
            warning_summary=warning_summaries[i] if i < len(warning_summaries) else "",
        ))

    return results
