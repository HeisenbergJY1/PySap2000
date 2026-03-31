# -*- coding: utf-8 -*-
"""
load_combination.py - Load combinations.

Wraps the SAP2000 `RespCombo` API.

SAP2000 API:
- `RespCombo.Add` - add a combination
- `RespCombo.AddDesignDefaultCombos` - add default design combinations
- `RespCombo.ChangeName` - rename a combination
- `RespCombo.Count` - get the number of combinations
- `RespCombo.CountCase` - get the number of cases in a combination
- `RespCombo.Delete` - delete a combination
- `RespCombo.DeleteCase` - delete a case from a combination
- `RespCombo.GetCaseList_1` - get the case list
- `RespCombo.GetNameList` - get the name list
- `RespCombo.GetNote` - get the note
- `RespCombo.GetTypeOAPI` - get the combination type
- `RespCombo.SetCaseList_1` - set the case list
- `RespCombo.SetNote` - set the note
- `RespCombo.SetTypeOAPI` - set the combination type
"""

from typing import List, Tuple
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class ComboCaseType(IntEnum):
    """
    Case type used within a combination.

    SAP2000 API: `eCNameType`
    """
    LOAD_CASE = 0       # Load case
    LOAD_COMBO = 1      # Load combination


class ComboType(IntEnum):
    """
    Combination type.

    SAP2000 API: `eComboType`
    """
    LINEAR_ADD = 0      # Linear add
    ENVELOPE = 1        # Envelope
    ABS_ADD = 2         # Absolute add
    SRSS = 3            # Square root of sum of squares
    RANGE = 4           # Range


# =============================================================================
# Combination management
# =============================================================================

def add_combo(model, name: str, combo_type: ComboType = ComboType.LINEAR_ADD) -> int:
    """
    Add a load combination.
    
    Args:
        model: SAP2000 SapModel object
        name: Combination name
        combo_type: Combination type
        
    Returns:
        `0` if successful.
    """
    return model.RespCombo.Add(name, int(combo_type))


def add_design_default_combos(
    model,
    design_steel: bool = True,
    design_concrete: bool = True,
    design_aluminum: bool = True,
    design_cold_formed: bool = True
) -> int:
    """
    Add default design combinations.
    
    Args:
        model: SAP2000 SapModel object
        design_steel: Whether to add steel design combinations
        design_concrete: Whether to add concrete design combinations
        design_aluminum: Whether to add aluminum design combinations
        design_cold_formed: Whether to add cold-formed steel design combinations
        
    Returns:
        `0` if successful.
    """
    return model.RespCombo.AddDesignDefaultCombos(
        design_steel, design_concrete, design_aluminum, design_cold_formed
    )


def change_combo_name(model, old_name: str, new_name: str) -> int:
    """
    Rename a combination.
    
    Args:
        model: SAP2000 SapModel object
        old_name: Existing name
        new_name: New name
        
    Returns:
        `0` if successful.
    """
    return model.RespCombo.ChangeName(old_name, new_name)


def get_combo_count(model) -> int:
    """
    Get the number of combinations.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        Combination count.
    """
    result = model.RespCombo.Count()
    count = com_data(result, 0)
    return count if count is not None else result


def get_combo_case_count(model, name: str) -> int:
    """
    Get the number of cases in a combination.
    
    Args:
        model: SAP2000 SapModel object
        name: Combination name
        
    Returns:
        Case count.
    """
    result = model.RespCombo.CountCase(name)
    count = com_data(result, 0)
    return count if count is not None else result


def delete_combo(model, name: str) -> int:
    """
    Delete a combination.
    
    Args:
        model: SAP2000 SapModel object
        name: Combination name
        
    Returns:
        `0` if successful.
    """
    return model.RespCombo.Delete(name)


def delete_combo_case(model, name: str, case_type: ComboCaseType, case_name: str) -> int:
    """
    Remove a case from a combination.
    
    Args:
        model: SAP2000 SapModel object
        name: Combination name
        case_type: Case type (`LOAD_CASE` or `LOAD_COMBO`)
        case_name: Case or combination name to remove
        
    Returns:
        `0` if successful.
    """
    return model.RespCombo.DeleteCase(name, int(case_type), case_name)


def get_combo_name_list(model) -> List[str]:
    """
    Get the list of all combination names.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        List of combination names.
    """
    result = model.RespCombo.GetNameList(0, [])
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


# =============================================================================
# Case-list helpers
# =============================================================================

def get_combo_case_list(model, name: str) -> Tuple[List[ComboCaseType], List[str], List[float]]:
    """
    Get the case list in a combination.
    
    Args:
        model: SAP2000 SapModel object
        name: Combination name
        
    Returns:
        Tuple `(case_types, case_names, scale_factors)`.
        - `case_types`: list of case types
        - `case_names`: list of case names
        - `scale_factors`: list of scale factors
    """
    result = model.RespCombo.GetCaseList_1(name, 0, [], [], [])
    num = com_data(result, 0, 0)
    case_types = com_data(result, 1)
    case_names = com_data(result, 2)
    scale_factors = com_data(result, 3)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        types = [ComboCaseType(t) for t in case_types] if case_types else []
        names = list(case_names) if case_names else []
        factors = list(scale_factors) if scale_factors else []
        return (types, names, factors)
    return ([], [], [])


def set_combo_case_list(
    model,
    name: str,
    case_type: ComboCaseType,
    case_name: str,
    scale_factor: float
) -> int:
    """
    Add a case to a combination.
    
    Args:
        model: SAP2000 SapModel object
        name: Combination name
        case_type: Case type (`LOAD_CASE` or `LOAD_COMBO`)
        case_name: Case or combination name
        scale_factor: Scale factor
        
    Returns:
        `0` if successful.
    """
    return model.RespCombo.SetCaseList_1(name, int(case_type), case_name, 0, scale_factor)


# =============================================================================
# Note helpers
# =============================================================================

def get_combo_note(model, name: str) -> str:
    """
    Get the note attached to a combination.
    
    Args:
        model: SAP2000 SapModel object
        name: Combination name
        
    Returns:
        Note text.
    """
    result = model.RespCombo.GetNote(name, "")
    note = com_data(result, 0)
    return note if note else ""


def set_combo_note(model, name: str, note: str) -> int:
    """
    Set the note of a combination.
    
    Args:
        model: SAP2000 SapModel object
        name: Combination name
        note: Note text
        
    Returns:
        `0` if successful.
    """
    return model.RespCombo.SetNote(name, note)


# =============================================================================
# Type helpers
# =============================================================================

def get_combo_type(model, name: str) -> ComboType:
    """
    Get the type of a combination.
    
    Args:
        model: SAP2000 SapModel object
        name: Combination name
        
    Returns:
        `ComboType`.
    """
    result = model.RespCombo.GetTypeOAPI(name, 0)
    type_val = com_data(result, 0)
    if type_val is not None:
        return ComboType(type_val)
    return ComboType.LINEAR_ADD


def set_combo_type(model, name: str, combo_type: ComboType) -> int:
    """
    Set the type of a combination.
    
    Args:
        model: SAP2000 SapModel object
        name: Combination name
        combo_type: Combination type
        
    Returns:
        `0` if successful.
    """
    return model.RespCombo.SetTypeOAPI(name, int(combo_type))
