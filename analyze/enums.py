# -*- coding: utf-8 -*-
"""
enums.py - Analysis-related enums

Enum types used by the SAP2000 `Analyze` API.
"""

from enum import IntEnum


class CaseStatus(IntEnum):
    """
    Analysis case status
    
    Matches the `Status` values returned by `Analyze.GetCaseStatus`.
    """
    NOT_RUN = 1           # Not run
    COULD_NOT_START = 2   # Could not start
    NOT_FINISHED = 3      # Not finished
    FINISHED = 4          # Finished


class SolverType(IntEnum):
    """
    Solver type
    
    Used for the `SolverType` parameter in `GetSolverOption_3` / `SetSolverOption_3`.
    """
    STANDARD = 0          # Standard solver
    ADVANCED = 1          # Advanced solver
    MULTI_THREADED = 2    # Multithreaded solver


class SolverProcessType(IntEnum):
    """
    Solver process type
    
    Used for the `SolverProcessType` parameter in `GetSolverOption_3` / `SetSolverOption_3`.
    """
    AUTO = 0              # Auto (program decides)
    GUI_PROCESS = 1       # GUI process
    SEPARATE_PROCESS = 2  # Separate process
