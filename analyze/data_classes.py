# -*- coding: utf-8 -*-
"""
data_classes.py - Analysis-related dataclasses

Dataclasses for analysis-control inputs and outputs.
"""

from dataclasses import dataclass
from typing import List
from .enums import CaseStatus, SolverType, SolverProcessType


@dataclass
class ActiveDOF:
    """
    Active degrees of freedom
    
    Controls global model degree-of-freedom activation.
    
    Attributes:
        ux: Translation in X
        uy: Translation in Y
        uz: Translation in Z
        rx: Rotation about X
        ry: Rotation about Y
        rz: Rotation about Z
    """
    ux: bool = True
    uy: bool = True
    uz: bool = True
    rx: bool = True
    ry: bool = True
    rz: bool = True
    
    def to_list(self) -> List[bool]:
        """Convert to the list format required by the API."""
        return [self.ux, self.uy, self.uz, self.rx, self.ry, self.rz]
    
    @classmethod
    def from_list(cls, values: List[bool]) -> "ActiveDOF":
        """Build from the list returned by the API."""
        if len(values) >= 6:
            return cls(
                ux=values[0], uy=values[1], uz=values[2],
                rx=values[3], ry=values[4], rz=values[5]
            )
        return cls()
    
    @classmethod
    def plane_xz(cls) -> "ActiveDOF":
        """XZ-plane analysis (2D frame)"""
        return cls(ux=True, uy=False, uz=True, rx=False, ry=True, rz=False)
    
    @classmethod
    def plane_xy(cls) -> "ActiveDOF":
        """XY-plane analysis"""
        return cls(ux=True, uy=True, uz=False, rx=False, ry=False, rz=True)
    
    @classmethod
    def space_frame(cls) -> "ActiveDOF":
        """Space-frame analysis (all DOFs active)"""
        return cls(ux=True, uy=True, uz=True, rx=True, ry=True, rz=True)
    
    @classmethod
    def truss_3d(cls) -> "ActiveDOF":
        """3D truss analysis (translations only)"""
        return cls(ux=True, uy=True, uz=True, rx=False, ry=False, rz=False)


@dataclass
class SolverOption:
    """
    Solver options
    
    Attributes:
        solver_type: Solver type
        process_type: Process type
        num_parallel_runs: Parallel run count (`-8..8`; values except `-1` and `0` are explicit)
        response_file_size_max_mb: Max response file size in MB; negative means program-controlled
        num_analysis_threads: Analysis thread count; negative means program-controlled
        stiff_case: Case name for stiffness matrix output; empty string disables output
    """
    solver_type: SolverType = SolverType.ADVANCED
    process_type: SolverProcessType = SolverProcessType.AUTO
    num_parallel_runs: int = 0
    response_file_size_max_mb: int = 0
    num_analysis_threads: int = 0
    stiff_case: str = ""


@dataclass
class CaseStatusInfo:
    """
    Case status info
    
    Attributes:
        name: Case name
        status: Case status
    """
    name: str
    status: CaseStatus
    
    @property
    def is_finished(self) -> bool:
        """Whether the case is finished"""
        return self.status == CaseStatus.FINISHED
    
    @property
    def is_run(self) -> bool:
        """Whether the case has run (including not finished)"""
        return self.status != CaseStatus.NOT_RUN


@dataclass
class RunCaseFlag:
    """
    Case run flag
    
    Attributes:
        name: Case name
        run: Whether to run
    """
    name: str
    run: bool
