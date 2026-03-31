# -*- coding: utf-8 -*-
"""
design/concrete.py - Concrete frame design helpers

Python wrapper for the SAP2000 `DesignConcrete` API.
API path: `SapModel.DesignConcrete`
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
# Code selection
# ============================================================================

def get_concrete_code(model) -> str:
    """Get the active concrete frame design code

    Args:
        model: SAP2000 SapModel object

    Returns:
        Code name string
    """
    result = model.DesignConcrete.GetCode("")
    return com_data(result, 0, "")


def set_concrete_code(model, code: Union[ConcreteDesignCode, str]) -> int:
    """Set the concrete frame design code

    Args:
        model: SAP2000 SapModel object
        code: Code enum or code name string

    Returns:
        `0` on success, non-zero on failure
    """
    if isinstance(code, ConcreteDesignCode):
        code_name = CONCRETE_CODE_NAMES.get(code, "ACI 318-14")
    else:
        code_name = code
    ret = model.DesignConcrete.SetCode(code_name)
    return com_ret(ret)


# ============================================================================
# Run design
# ============================================================================

def start_concrete_design(model) -> int:
    """Run concrete frame design

    Requires analysis to be run and concrete frame objects in the model.

    Args:
        model: SAP2000 SapModel object

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignConcrete.StartDesign()
    return com_ret(ret)


def delete_concrete_results(model) -> int:
    """Delete all concrete frame design results

    Args:
        model: SAP2000 SapModel object

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignConcrete.DeleteResults()
    return com_ret(ret)


def get_concrete_results_available(model) -> bool:
    """Whether concrete frame design results are available

    Args:
        model: SAP2000 SapModel object

    Returns:
        `True` if results are available
    """
    result = model.DesignConcrete.GetResultsAvailable()
    return bool(com_data(result, 0, result))


# ============================================================================
# Load combinations
# ============================================================================

def get_concrete_combo_strength(model) -> List[str]:
    """Load combinations used for strength design

    Args:
        model: SAP2000 SapModel object

    Returns:
        List of load combination names
    """
    result = model.DesignConcrete.GetComboStrength(0, [])
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


def set_concrete_combo_strength(model, name: str, selected: bool = True) -> int:
    """Select a load combination for strength design

    Args:
        model: SAP2000 SapModel object
        name: Load combination name
        selected: `True` to select, `False` to deselect

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignConcrete.SetComboStrength(name, selected)
    return com_ret(ret)


def get_concrete_combo_auto_generate(model) -> bool:
    """Whether design combinations are auto-generated

    Args:
        model: SAP2000 SapModel object

    Returns:
        `True` if auto-generated
    """
    result = model.DesignConcrete.GetComboAutoGenerate(False)
    return bool(com_data(result, 0, False))


def set_concrete_combo_auto_generate(model, auto_generate: bool = True) -> int:
    """Enable or disable auto-generation of design combinations

    Args:
        model: SAP2000 SapModel object
        auto_generate: `True` to auto-generate

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignConcrete.SetComboAutoGenerate(auto_generate)
    return com_ret(ret)


# ============================================================================
# DesignGroup
# ============================================================================

def get_concrete_design_group(model) -> List[str]:
    """Groups selected for concrete design

    Args:
        model: SAP2000 SapModel object

    Returns:
        List of group names
    """
    result = model.DesignConcrete.GetGroup(0, [])
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


def set_concrete_design_group(model, name: str, selected: bool = True) -> int:
    """Select or deselect a group for concrete design

    Args:
        model: SAP2000 SapModel object
        name: Group name
        selected: `True` to select, `False` to deselect

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignConcrete.SetGroup(name, selected)
    return com_ret(ret)


# ============================================================================
# Design section
# ============================================================================

def get_concrete_design_section(model, name: str) -> str:
    """Get the design section assigned to a frame

    Args:
        model: SAP2000 SapModel object
        name: Frame object name

    Returns:
        Design section name
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
    """Set the design section for frame objects

    Args:
        model: SAP2000 SapModel object
        name: Object name
        prop_name: Section property name
        last_analysis: Use last analysis section if `True`
        item_type: Object selection mode

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignConcrete.SetDesignSection(name, prop_name, last_analysis, int(item_type))
    return com_ret(ret)


# ============================================================================
# Overwrites
# ============================================================================

def reset_concrete_overwrites(model) -> int:
    """Reset all concrete design overwrites to defaults

    Args:
        model: SAP2000 SapModel object

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignConcrete.ResetOverwrites()
    return com_ret(ret)


# ============================================================================
# Verification
# ============================================================================

def verify_concrete_passed(model) -> VerifyPassedResult:
    """Verify concrete design acceptance

    Args:
        model: SAP2000 SapModel object

    Returns:
        Verification result
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
    """Verify analysis vs. design section assignments

    Args:
        model: SAP2000 SapModel object

    Returns:
        Frame names with mismatched sections
    """
    result = model.DesignConcrete.VerifySections(0, [])
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


# ============================================================================
# Summary results
# ============================================================================

def get_concrete_summary_results_beam(
    model,
    name: str,
    item_type: ItemType = ItemType.OBJECT
) -> List[ConcreteBeamResult]:
    """Get concrete beam summary results

    Args:
        model: SAP2000 SapModel object
        name: Object name, group name, or ignored depending on `item_type`
        item_type: Object selection mode

    Returns:
        List of beam design results
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
    """Get concrete column summary results

    Args:
        model: SAP2000 SapModel object
        name: Object name, group name, or ignored depending on `item_type`
        item_type: Object selection mode

    Returns:
        List of column design results
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
    """Get concrete joint summary results

    Joint design is supported only for some codes.

    Args:
        model: SAP2000 SapModel object
        name: Object name, group name, or ignored depending on `item_type`
        item_type: Object selection mode

    Returns:
        List of joint design results
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
