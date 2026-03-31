# -*- coding: utf-8 -*-
"""
response_spectrum.py - Response-spectrum function helpers.

Wraps the SAP2000 `Func.FuncRS` API, including GB 50011-2010 helpers.

SAP2000 API:
- `Func.FuncRS.GetChinese2010` / `SetChinese2010` - GB 50011-2010
- `Func.FuncRS.GetUser` / `SetUser` - user-defined response spectrum
- `Func.FuncRS.GetFromFile_1` / `SetFromFile_1` - file-based definition
"""

from typing import List, Tuple
from dataclasses import dataclass
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class Chinese2010SiteClass(IntEnum):
    """
    Site class in the Chinese code.

    GB 50011-2010.
    """
    I_0 = 0     # Class I0
    I_1 = 1     # Class I1
    II = 2      # Class II
    III = 3     # Class III
    IV = 4      # Class IV


class Chinese2010DesignGroup(IntEnum):
    """
    Design earthquake group in the Chinese code.

    GB 50011-2010.
    """
    GROUP_1 = 0     # Group 1
    GROUP_2 = 1     # Group 2
    GROUP_3 = 2     # Group 3


@dataclass
class Chinese2010Params:
    """
    Parameters for a GB 50011-2010 response spectrum.
    
    Attributes:
        alpha_max: Maximum seismic influence coefficient
        site_class: Site class
        design_group: Design earthquake group
        period_time_discount: Period reduction factor
        damping_ratio: Damping ratio
    """
    alpha_max: float = 0.0
    site_class: Chinese2010SiteClass = Chinese2010SiteClass.II
    design_group: Chinese2010DesignGroup = Chinese2010DesignGroup.GROUP_1
    period_time_discount: float = 1.0
    damping_ratio: float = 0.05


# =============================================================================
# Chinese code GB 50011-2010
# =============================================================================

def get_func_rs_chinese_2010(model, name: str) -> Chinese2010Params:
    """
    Get parameters for a GB 50011-2010 response-spectrum function.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        `Chinese2010Params` instance.
    """
    result = model.Func.FuncRS.GetChinese2010(name, 0.0, 0, 0, 0.0, 0.0)
    alpha_max = com_data(result, 0)
    if alpha_max is not None:
        return Chinese2010Params(
            alpha_max=alpha_max,
            site_class=Chinese2010SiteClass(com_data(result, 1, 2)),
            design_group=Chinese2010DesignGroup(com_data(result, 2, 0)),
            period_time_discount=com_data(result, 3, 1.0),
            damping_ratio=com_data(result, 4, 0.05),
        )
    return Chinese2010Params()


def set_func_rs_chinese_2010(
    model,
    name: str,
    alpha_max: float,
    site_class: Chinese2010SiteClass,
    design_group: Chinese2010DesignGroup,
    period_time_discount: float = 1.0,
    damping_ratio: float = 0.05
) -> int:
    """
    Set a GB 50011-2010 response-spectrum function.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        alpha_max: Maximum seismic influence coefficient
        site_class: Site class
        design_group: Design earthquake group
        period_time_discount: Period reduction factor
        damping_ratio: Damping ratio
        
    Returns:
        `0` if successful.
        
    Example:
        set_func_rs_chinese_2010(
            model, "RS-X",
            alpha_max=0.08,
            site_class=Chinese2010SiteClass.II,
            design_group=Chinese2010DesignGroup.GROUP_1,
            damping_ratio=0.05
        )
    """
    return model.Func.FuncRS.SetChinese2010(
        name,
        alpha_max,
        int(site_class),
        int(design_group),
        period_time_discount,
        damping_ratio
    )


# =============================================================================
# User-defined response spectrum
# =============================================================================

def get_func_rs_user(model, name: str) -> Tuple[List[float], List[float], float]:
    """
    Get user-defined response-spectrum data.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        Tuple `(periods, values, damping_ratio)`.
        - `periods`: list of periods [s]
        - `values`: list of spectrum values
        - `damping_ratio`: damping ratio
    """
    result = model.Func.FuncRS.GetUser(name, 0, [], [], 0.0)
    num = com_data(result, 0, 0)
    periods = com_data(result, 1)
    values = com_data(result, 2)
    damping = com_data(result, 3, 0.05)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        return (
            list(periods) if periods else [],
            list(values) if values else [],
            damping
        )
    return ([], [], 0.05)


def set_func_rs_user(
    model,
    name: str,
    periods: List[float],
    values: List[float],
    damping_ratio: float = 0.05
) -> int:
    """
    Set a user-defined response-spectrum function.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        periods: List of periods [s]
        values: List of spectrum values
        damping_ratio: Damping ratio
        
    Returns:
        `0` if successful.
    """
    num = len(periods)
    return model.Func.FuncRS.SetUser(name, num, periods, values, damping_ratio)


# =============================================================================
# File-based definitions
# =============================================================================

def get_func_rs_from_file(model, name: str) -> Tuple[str, int, int, float]:
    """
    Get parameters for a file-based response-spectrum function.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        Tuple `(file_name, header_lines, prefix_chars, damping_ratio)`.
    """
    result = model.Func.FuncRS.GetFromFile_1(name, "", 0, 0, 0.0)
    file_name = com_data(result, 0)
    if file_name is not None:
        return (
            file_name if file_name else "",
            com_data(result, 1, 0),
            com_data(result, 2, 0),
            com_data(result, 3, 0.05),
        )
    return ("", 0, 0, 0.05)


def set_func_rs_from_file(
    model,
    name: str,
    file_name: str,
    header_lines: int = 0,
    prefix_chars: int = 0,
    damping_ratio: float = 0.05
) -> int:
    """
    Set a response-spectrum function from file data.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        file_name: File path
        header_lines: Number of header lines to skip
        prefix_chars: Number of prefix characters to skip per line
        damping_ratio: Damping ratio
        
    Returns:
        `0` if successful.
    """
    return model.Func.FuncRS.SetFromFile_1(
        name, file_name, header_lines, prefix_chars, damping_ratio
    )
