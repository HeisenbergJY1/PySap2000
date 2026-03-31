# -*- coding: utf-8 -*-
"""
time_history.py - Time-history function helpers.

Wraps the SAP2000 `Func.FuncTH` API.

SAP2000 API:
- `Func.FuncTH.GetCosine` / `SetCosine` - cosine functions
- `Func.FuncTH.GetFromFile_1` / `SetFromFile_1` - file-based definition
- `Func.FuncTH.GetRamp` / `SetRamp` - ramp functions
- `Func.FuncTH.GetSawtooth` / `SetSawtooth` - sawtooth functions
- `Func.FuncTH.GetSine` / `SetSine` - sine functions
- `Func.FuncTH.GetTriangular` / `SetTriangular` - triangular functions
- `Func.FuncTH.GetUser` / `SetUser` - user-defined functions
- `Func.FuncTH.GetUserPeriodic` / `SetUserPeriodic` - user-defined periodic functions
"""

from typing import List, Tuple
from dataclasses import dataclass

from PySap2000.com_helper import com_ret, com_data


# =============================================================================
# Data classes
# =============================================================================

@dataclass
class CosineParams:
    """Cosine function parameters."""
    period: float = 0.0         # Period [s]
    steps: int = 0              # Steps per period
    cycles: int = 0             # Number of cycles
    amplitude: float = 0.0      # Amplitude


@dataclass
class RampParams:
    """Ramp function parameters."""
    time: float = 0.0           # Ramp time [s]
    amplitude: float = 0.0      # Amplitude
    max_time: float = 0.0       # Maximum time [s]


@dataclass
class SawtoothParams:
    """Sawtooth function parameters."""
    period: float = 0.0         # Period [s]
    time: float = 0.0           # Rise time [s]
    cycles: int = 0             # Number of cycles
    amplitude: float = 0.0      # Amplitude


@dataclass
class SineParams:
    """Sine function parameters."""
    period: float = 0.0         # Period [s]
    steps: int = 0              # Steps per period
    cycles: int = 0             # Number of cycles
    amplitude: float = 0.0      # Amplitude


@dataclass
class TriangularParams:
    """Triangular function parameters."""
    period: float = 0.0         # Period [s]
    cycles: int = 0             # Number of cycles
    amplitude: float = 0.0      # Amplitude


@dataclass
class FromFileParams:
    """File-based function parameters."""
    file_name: str = ""         # File name
    header_lines: int = 0       # Number of header lines
    prefix_chars: int = 0       # Number of prefix characters


# =============================================================================
# Cosine functions
# =============================================================================

def get_func_th_cosine(model, name: str) -> CosineParams:
    """
    Get cosine time-history function parameters.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        `CosineParams` instance.
    """
    result = model.Func.FuncTH.GetCosine(name, 0.0, 0, 0, 0.0)
    period = com_data(result, 0)
    if period is not None:
        return CosineParams(
            period=period,
            steps=com_data(result, 1, 0),
            cycles=com_data(result, 2, 0),
            amplitude=com_data(result, 3, 0.0),
        )
    return CosineParams()


def set_func_th_cosine(
    model,
    name: str,
    period: float,
    steps: int,
    cycles: int,
    amplitude: float
) -> int:
    """
    Set a cosine time-history function.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        period: Period [s]
        steps: Steps per period
        cycles: Number of cycles
        amplitude: Amplitude
        
    Returns:
        `0` if successful.
    """
    return model.Func.FuncTH.SetCosine(name, period, steps, cycles, amplitude)


# =============================================================================
# File-based definitions
# =============================================================================

def get_func_th_from_file(model, name: str) -> FromFileParams:
    """
    Get parameters for a file-based time-history function.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        `FromFileParams` instance.
    """
    result = model.Func.FuncTH.GetFromFile_1(name, "", 0, 0)
    file_name = com_data(result, 0)
    if file_name is not None:
        return FromFileParams(
            file_name=file_name if file_name else "",
            header_lines=com_data(result, 1, 0),
            prefix_chars=com_data(result, 2, 0),
        )
    return FromFileParams()


def set_func_th_from_file(
    model,
    name: str,
    file_name: str,
    header_lines: int = 0,
    prefix_chars: int = 0
) -> int:
    """
    Set a time-history function from file data.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        file_name: File path
        header_lines: Number of header lines to skip
        prefix_chars: Number of prefix characters to skip per line
        
    Returns:
        `0` if successful.
    """
    return model.Func.FuncTH.SetFromFile_1(name, file_name, header_lines, prefix_chars)


# =============================================================================
# Ramp functions
# =============================================================================

def get_func_th_ramp(model, name: str) -> RampParams:
    """
    Get ramp time-history function parameters.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        `RampParams` instance.
    """
    result = model.Func.FuncTH.GetRamp(name, 0.0, 0.0, 0.0)
    time = com_data(result, 0)
    if time is not None:
        return RampParams(
            time=time,
            amplitude=com_data(result, 1, 0.0),
            max_time=com_data(result, 2, 0.0),
        )
    return RampParams()


def set_func_th_ramp(
    model,
    name: str,
    time: float,
    amplitude: float,
    max_time: float
) -> int:
    """
    Set a ramp time-history function.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        time: Ramp time [s]
        amplitude: Amplitude
        max_time: Maximum time [s]
        
    Returns:
        `0` if successful.
    """
    return model.Func.FuncTH.SetRamp(name, time, amplitude, max_time)


# =============================================================================
# Sawtooth functions
# =============================================================================

def get_func_th_sawtooth(model, name: str) -> SawtoothParams:
    """
    Get sawtooth time-history function parameters.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        `SawtoothParams` instance.
    """
    result = model.Func.FuncTH.GetSawtooth(name, 0.0, 0.0, 0, 0.0)
    period = com_data(result, 0)
    if period is not None:
        return SawtoothParams(
            period=period,
            time=com_data(result, 1, 0.0),
            cycles=com_data(result, 2, 0),
            amplitude=com_data(result, 3, 0.0),
        )
    return SawtoothParams()


def set_func_th_sawtooth(
    model,
    name: str,
    period: float,
    time: float,
    cycles: int,
    amplitude: float
) -> int:
    """
    Set a sawtooth time-history function.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        period: Period [s]
        time: Rise time [s]
        cycles: Number of cycles
        amplitude: Amplitude
        
    Returns:
        `0` if successful.
    """
    return model.Func.FuncTH.SetSawtooth(name, period, time, cycles, amplitude)


# =============================================================================
# Sine functions
# =============================================================================

def get_func_th_sine(model, name: str) -> SineParams:
    """
    Get sine time-history function parameters.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        `SineParams` instance.
    """
    result = model.Func.FuncTH.GetSine(name, 0.0, 0, 0, 0.0)
    period = com_data(result, 0)
    if period is not None:
        return SineParams(
            period=period,
            steps=com_data(result, 1, 0),
            cycles=com_data(result, 2, 0),
            amplitude=com_data(result, 3, 0.0),
        )
    return SineParams()


def set_func_th_sine(
    model,
    name: str,
    period: float,
    steps: int,
    cycles: int,
    amplitude: float
) -> int:
    """
    Set a sine time-history function.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        period: Period [s]
        steps: Steps per period
        cycles: Number of cycles
        amplitude: Amplitude
        
    Returns:
        `0` if successful.
    """
    return model.Func.FuncTH.SetSine(name, period, steps, cycles, amplitude)


# =============================================================================
# Triangular functions
# =============================================================================

def get_func_th_triangular(model, name: str) -> TriangularParams:
    """
    Get triangular time-history function parameters.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        `TriangularParams` instance.
    """
    result = model.Func.FuncTH.GetTriangular(name, 0.0, 0, 0.0)
    period = com_data(result, 0)
    if period is not None:
        return TriangularParams(
            period=period,
            cycles=com_data(result, 1, 0),
            amplitude=com_data(result, 2, 0.0),
        )
    return TriangularParams()


def set_func_th_triangular(
    model,
    name: str,
    period: float,
    cycles: int,
    amplitude: float
) -> int:
    """
    Set a triangular time-history function.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        period: Period [s]
        cycles: Number of cycles
        amplitude: Amplitude
        
    Returns:
        `0` if successful.
    """
    return model.Func.FuncTH.SetTriangular(name, period, cycles, amplitude)


# =============================================================================
# User-defined functions
# =============================================================================

def get_func_th_user(model, name: str) -> Tuple[List[float], List[float]]:
    """
    Get user-defined time-history function data.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        Tuple `(times, values)`.
        - `times`: list of times [s]
        - `values`: list of values
    """
    result = model.Func.FuncTH.GetUser(name, 0, [], [])
    num = com_data(result, 0, 0)
    times = com_data(result, 1)
    values = com_data(result, 2)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        return (list(times) if times else [], list(values) if values else [])
    return ([], [])


def set_func_th_user(
    model,
    name: str,
    times: List[float],
    values: List[float]
) -> int:
    """
    Set a user-defined time-history function.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        times: List of times [s]
        values: List of values
        
    Returns:
        `0` if successful.
    """
    num = len(times)
    return model.Func.FuncTH.SetUser(name, num, times, values)


# =============================================================================
# User-defined periodic functions
# =============================================================================

def get_func_th_user_periodic(model, name: str) -> Tuple[List[float], List[float], int]:
    """
    Get user-defined periodic time-history function data.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        
    Returns:
        Tuple `(times, values, cycles)`.
        - `times`: list of times [s]
        - `values`: list of values
        - `cycles`: number of cycles
    """
    result = model.Func.FuncTH.GetUserPeriodic(name, 0, [], [], 0)
    num = com_data(result, 0, 0)
    times = com_data(result, 1)
    values = com_data(result, 2)
    cycles = com_data(result, 3, 0)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        return (
            list(times) if times else [],
            list(values) if values else [],
            cycles
        )
    return ([], [], 0)


def set_func_th_user_periodic(
    model,
    name: str,
    times: List[float],
    values: List[float],
    cycles: int
) -> int:
    """
    Set a user-defined periodic time-history function.
    
    Args:
        model: SAP2000 SapModel object
        name: Function name
        times: List of times [s]
        values: List of values
        cycles: Number of cycles
        
    Returns:
        `0` if successful.
    """
    num = len(times)
    return model.Func.FuncTH.SetUserPeriodic(name, num, times, values, cycles)
