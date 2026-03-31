# -*- coding: utf-8 -*-
"""
design/steel.py - Steel design helpers

Python wrapper for the SAP2000 `DesignSteel` API.
"""

from typing import List, Optional, Union

from .enums import SteelDesignCode, RatioType, ItemType, STEEL_CODE_NAMES, STEEL_CODE_FROM_NAME
from .data_classes import SteelSummaryResult, VerifyPassedResult
from PySap2000.com_helper import com_ret, com_data


def get_steel_code(model) -> str:
    """Get the active steel design code
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Code name string
    """
    result = model.DesignSteel.GetCode("")
    return com_data(result, 0, "")


def set_steel_code(model, code: Union[SteelDesignCode, str]) -> int:
    """Set the steel design code
    
    Args:
        model: SAP2000 SapModel object
        code: Code enum or code name string
        
    Returns:
        `0` on success, non-zero on failure
    """
    if isinstance(code, SteelDesignCode):
        code_name = STEEL_CODE_NAMES.get(code, "AISC 360-10")
    else:
        code_name = code
    
    ret = model.DesignSteel.SetCode(code_name)
    return com_ret(ret)


def start_steel_design(model) -> int:
    """Run steel design
    
    Requires analysis to be run and steel frame objects in the model.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignSteel.StartDesign()
    return com_ret(ret)


def delete_steel_results(model) -> int:
    """Delete all steel design results
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignSteel.DeleteResults()
    return com_ret(ret)


def get_steel_results_available(model) -> bool:
    """Whether steel design results are available
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `True` if results are available
    """
    result = model.DesignSteel.GetResultsAvailable()
    return bool(com_data(result, 0, result))


def get_steel_summary_results(
    model,
    name: str,
    item_type: ItemType = ItemType.OBJECT
) -> List[SteelSummaryResult]:
    """Get steel design summary results
    
    Args:
        model: SAP2000 SapModel object
        name: Object name, group name, or ignored depending on `item_type`
        item_type: Object selection mode
        
    Returns:
        List of design results
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
            # Coerce `ratio_type`; default to NONE if unknown
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
    """Groups selected for steel design
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        List of group names
    """
    result = model.DesignSteel.GetGroup(0, [])
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


def set_steel_design_group(model, name: str, selected: bool = True) -> int:
    """Select or deselect a group for steel design
    
    Args:
        model: SAP2000 SapModel object
        name: Group name
        selected: `True` to select, `False` to deselect
        
    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignSteel.SetGroup(name, selected)
    return com_ret(ret)


def get_steel_design_section(model, name: str) -> str:
    """Get the design section assigned to a frame
    
    Args:
        model: SAP2000 SapModel object
        name: Frame object name
        
    Returns:
        Design section name
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
    """Set the design section for frame objects
    
    Args:
        model: SAP2000 SapModel object
        name: Object name, group name, or ignored depending on `item_type`
        prop_name: Section name when `last_analysis=False`
        last_analysis: Use last analysis section if `True`, else use `prop_name`
        item_type: Object selection mode
        
    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignSteel.SetDesignSection(name, prop_name, last_analysis, int(item_type))
    return com_ret(ret)


def get_steel_combo_strength(model) -> List[str]:
    """Load combinations used for strength design
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        List of load combination names
    """
    result = model.DesignSteel.GetComboStrength(0, [])
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


def set_steel_combo_strength(model, name: str, selected: bool = True) -> int:
    """Select a load combination for strength design
    
    Args:
        model: SAP2000 SapModel object
        name: Load combination name
        selected: `True` to select, `False` to deselect
        
    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignSteel.SetComboStrength(name, selected)
    return com_ret(ret)


def get_steel_combo_deflection(model) -> List[str]:
    """Load combinations used for deflection design
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        List of load combination names
    """
    result = model.DesignSteel.GetComboDeflection(0, [])
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


def set_steel_combo_deflection(model, name: str, selected: bool = True) -> int:
    """Select a load combination for deflection design
    
    Args:
        model: SAP2000 SapModel object
        name: Load combination name
        selected: `True` to select, `False` to deselect
        
    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignSteel.SetComboDeflection(name, selected)
    return com_ret(ret)


def get_steel_combo_auto_generate(model) -> bool:
    """Whether design combinations are auto-generated

    Args:
        model: SAP2000 SapModel object

    Returns:
        `True` if auto-generated
    """
    result = model.DesignSteel.GetComboAutoGenerate(False)
    return bool(com_data(result, 0, False))


def set_steel_combo_auto_generate(model, auto_generate: bool = True) -> int:
    """Enable or disable auto-generation of design combinations

    Args:
        model: SAP2000 SapModel object
        auto_generate: `True` to auto-generate

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignSteel.SetComboAutoGenerate(auto_generate)
    return com_ret(ret)


def set_steel_auto_select_null(model, name: str, item_type: ItemType = ItemType.OBJECT) -> int:
    """Clear auto-select section (set to None)

    Args:
        model: SAP2000 SapModel object
        name: Object name
        item_type: Object selection mode

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignSteel.SetAutoSelectNull(name, int(item_type))
    return com_ret(ret)


def reset_steel_overwrites(model) -> int:
    """Reset all steel design overwrites to defaults
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignSteel.ResetOverwrites()
    return com_ret(ret)


def verify_steel_passed(model) -> VerifyPassedResult:
    """Verify steel design acceptance
    
    Frames that failed design checks or are not yet checked.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Verification result
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
    """Verify analysis vs. design section assignments
    
    Frames whose analysis section differs from the design section.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Frame names with mismatched sections
    """
    result = model.DesignSteel.VerifySections(0, [])
    
    names = com_data(result, 1)
    if names:
        return list(names)
    return []
