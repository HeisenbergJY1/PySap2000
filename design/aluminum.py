# -*- coding: utf-8 -*-
"""
design/aluminum.py - Aluminum design helpers

Python wrapper for the SAP2000 `DesignAluminum` API.
API path: `SapModel.DesignAluminum`
"""

from typing import List, Union

from .enums import (
    AluminumDesignCode, ALUMINUM_CODE_NAMES, ALUMINUM_CODE_FROM_NAME,
    ItemType, RatioType,
)
from .data_classes import SteelSummaryResult, VerifyPassedResult
from PySap2000.com_helper import com_ret, com_data

# Reuse `SteelSummaryResult` for aluminum (same API layout)
AluminumSummaryResult = SteelSummaryResult


# ============================================================================
# Code selection
# ============================================================================

def get_aluminum_code(model) -> str:
    """Get the active aluminum design code

    Args:
        model: SAP2000 SapModel object

    Returns:
        Code name string
    """
    result = model.DesignAluminum.GetCode("")
    return com_data(result, 0, "")


def set_aluminum_code(model, code: Union[AluminumDesignCode, str]) -> int:
    """Set the aluminum design code

    Args:
        model: SAP2000 SapModel object
        code: Code enum or code name string

    Returns:
        `0` on success, non-zero on failure
    """
    if isinstance(code, AluminumDesignCode):
        code_name = ALUMINUM_CODE_NAMES.get(code, "AA-ASD 2000")
    else:
        code_name = code
    ret = model.DesignAluminum.SetCode(code_name)
    return com_ret(ret)


# ============================================================================
# Run design
# ============================================================================

def start_aluminum_design(model) -> int:
    """Run aluminum design

    Requires analysis to be run and aluminum frame objects in the model.

    Args:
        model: SAP2000 SapModel object

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignAluminum.StartDesign()
    return com_ret(ret)


def delete_aluminum_results(model) -> int:
    """Delete all aluminum design results

    Args:
        model: SAP2000 SapModel object

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignAluminum.DeleteResults()
    return com_ret(ret)


def get_aluminum_results_available(model) -> bool:
    """Whether aluminum design results are available

    Args:
        model: SAP2000 SapModel object

    Returns:
        `True` if results are available
    """
    result = model.DesignAluminum.GetResultsAvailable()
    return bool(com_data(result, 0, result))


# ============================================================================
# Load combinations
# ============================================================================

def get_aluminum_combo_strength(model) -> List[str]:
    """Load combinations used for strength design"""
    result = model.DesignAluminum.GetComboStrength(0, [])
    names = com_data(result, 1)
    return list(names) if names else []


def set_aluminum_combo_strength(model, name: str, selected: bool = True) -> int:
    """Select a load combination for strength design"""
    ret = model.DesignAluminum.SetComboStrength(name, selected)
    return com_ret(ret)


def get_aluminum_combo_deflection(model) -> List[str]:
    """Load combinations used for deflection design"""
    result = model.DesignAluminum.GetComboDeflection(0, [])
    names = com_data(result, 1)
    return list(names) if names else []


def set_aluminum_combo_deflection(model, name: str, selected: bool = True) -> int:
    """Select a load combination for deflection design"""
    ret = model.DesignAluminum.SetComboDeflection(name, selected)
    return com_ret(ret)


def get_aluminum_combo_auto_generate(model) -> bool:
    """Whether design combinations are auto-generated"""
    result = model.DesignAluminum.GetComboAutoGenerate(False)
    return bool(com_data(result, 0, False))


def set_aluminum_combo_auto_generate(model, auto_generate: bool = True) -> int:
    """Enable or disable auto-generation of design combinations"""
    ret = model.DesignAluminum.SetComboAutoGenerate(auto_generate)
    return com_ret(ret)


# ============================================================================
# DesignGroup
# ============================================================================

def get_aluminum_design_group(model) -> List[str]:
    """Groups selected for aluminum design"""
    result = model.DesignAluminum.GetGroup(0, [])
    names = com_data(result, 1)
    return list(names) if names else []


def set_aluminum_design_group(model, name: str, selected: bool = True) -> int:
    """Select or deselect a group for aluminum design"""
    ret = model.DesignAluminum.SetGroup(name, selected)
    return com_ret(ret)


# ============================================================================
# Design section
# ============================================================================

def get_aluminum_design_section(model, name: str) -> str:
    """Get the design section assigned to a frame"""
    result = model.DesignAluminum.GetDesignSection(name, "")
    return com_data(result, 0, "")


def set_aluminum_design_section(
    model,
    name: str,
    prop_name: str = "",
    last_analysis: bool = False,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """Set the design section for frame objects"""
    ret = model.DesignAluminum.SetDesignSection(name, prop_name, last_analysis, int(item_type))
    return com_ret(ret)


def set_aluminum_auto_select_null(model, name: str, item_type: ItemType = ItemType.OBJECT) -> int:
    """Clear auto-select section (set to None)

    Args:
        model: SAP2000 SapModel object
        name: Object name
        item_type: Object selection mode

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignAluminum.SetAutoSelectNull(name, int(item_type))
    return com_ret(ret)


# ============================================================================
# Overwrites and verification
# ============================================================================

def reset_aluminum_overwrites(model) -> int:
    """Reset all aluminum design overwrites to defaults"""
    ret = model.DesignAluminum.ResetOverwrites()
    return com_ret(ret)


def verify_aluminum_passed(model) -> VerifyPassedResult:
    """Verify aluminum design acceptance"""
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
    """Verify analysis vs. design section assignments"""
    result = model.DesignAluminum.VerifySections(0, [])
    names = com_data(result, 1)
    return list(names) if names else []


# ============================================================================
# Summary results
# ============================================================================

def get_aluminum_summary_results(
    model,
    name: str,
    item_type: ItemType = ItemType.OBJECT
) -> List[AluminumSummaryResult]:
    """Get aluminum design summary results

    Note: only `RatioType` values 1 (PMM), 3 (major shear), and 4 (minor shear) apply.

    Args:
        model: SAP2000 SapModel object
        name: Object name, group name, or ignored depending on `item_type`
        item_type: Object selection mode

    Returns:
        List of design results
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
