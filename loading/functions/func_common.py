# -*- coding: utf-8 -*-
"""
func_common.py - Common function management helpers.

Wraps common management operations in the SAP2000 `Func` API.

SAP2000 API:
- `Func.ChangeName` - rename a function
- `Func.ConvertToUser` - convert to a user-defined function
- `Func.Count` - count functions
- `Func.Delete` - delete a function
- `Func.GetNameList` - get the function name list
- `Func.GetTypeOAPI` - get the function type
- `Func.GetValues` - get function values
"""

from typing import List, Tuple
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class FuncType(IntEnum):
    """
    Function type.

    SAP2000 API: `eFuncType`
    """
    RESPONSE_SPECTRUM = 0       # Response spectrum
    TIME_HISTORY = 1            # Time history
    POWER_SPECTRAL_DENSITY = 2  # Power spectral density
    STEADY_STATE = 3            # Steady state


# =============================================================================
# Function management
# =============================================================================

def change_func_name(model, old_name: str, new_name: str) -> int:
    """
    Rename a function.
    
    Args:
        model: SAP2000 SapModel object
        old_name: Existing name
        new_name: New name
        
    Returns:
        `0` if successful.
    """
    return model.Func.ChangeName(old_name, new_name)


def convert_func_to_user(model, name: str) -> int:
    """
    Convert a function to a user-defined type.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        `0` if successful.
    """
    return model.Func.ConvertToUser(name)


def get_func_count(model, func_type: FuncType = None) -> int:
    """
    Get the number of functions.
    
    Args:
        model: SAP2000 SapModel object
        func_type: Function type, or `None` for all types
        
    Returns:
        Function count.
    """
    if func_type is None:
        result = model.Func.Count()
    else:
        result = model.Func.Count(int(func_type))
    
    count = com_data(result, 0)
    return count if count is not None else result


def delete_func(model, name: str) -> int:
    """
    Delete a function.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        `0` if successful.
    """
    return model.Func.Delete(name)


def get_func_name_list(model, func_type: FuncType = None) -> List[str]:
    """
    Get the list of function names.
    
    Args:
        model: SAP2000 SapModel object
        func_type: Function type, or `None` for all types
        
    Returns:
        List of function names.
    """
    if func_type is None:
        result = model.Func.GetNameList(0, [])
    else:
        result = model.Func.GetNameList(0, [], int(func_type))
    
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


def get_func_type(model, name: str) -> FuncType:
    """
    Get the type of a function.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        `FuncType`.
    """
    result = model.Func.GetTypeOAPI(name, 0, 0)
    type_val = com_data(result, 0)
    if type_val is not None:
        return FuncType(type_val)
    return FuncType.TIME_HISTORY


def get_func_values(model, name: str) -> Tuple[List[float], List[float]]:
    """
    Get function values.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        Tuple `(x_values, y_values)`.
    """
    result = model.Func.GetValues(name, 0, [], [])
    num = com_data(result, 0, 0)
    x_values = com_data(result, 1)
    y_values = com_data(result, 2)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        return (
            list(x_values) if x_values else [],
            list(y_values) if y_values else []
        )
    return ([], [])
