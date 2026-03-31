# -*- coding: utf-8 -*-
"""
analyze.py - Analysis control functions

Core wrapper functions around the SAP2000 `Analyze` API.

SAP2000 API:
- Analyze.RunAnalysis
- Analyze.CreateAnalysisModel
- Analyze.DeleteResults
- Analyze.GetActiveDOF / SetActiveDOF
- Analyze.GetCaseStatus
- Analyze.GetRunCaseFlag / SetRunCaseFlag
- Analyze.GetSolverOption_3 / SetSolverOption_3
- Analyze.ModifyUnDeformedGeometry
- Analyze.ModifyUndeformedGeometryModeShape
- Analyze.MergeAnalysisResults
"""

from typing import List, Optional
from .enums import CaseStatus, SolverType, SolverProcessType
from .data_classes import ActiveDOF, SolverOption, CaseStatusInfo, RunCaseFlag

from PySap2000.com_helper import com_ret, com_data


# =============================================================================
# Core analysis functions
# =============================================================================

def run_analysis(model) -> int:
    """
    Run analysis
    
    Automatically creates and runs the analysis model. The model file must be saved first.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `0` on success
        
    Note:
        Call `File.Save()` before running analysis.
        
    Example:
        model.File.Save("C:/model.sdb")
        run_analysis(model)
    """
    return model.Analyze.RunAnalysis()


def create_analysis_model(model) -> int:
    """
    Create analysis model
    
    If the analysis model already exists and is up to date, no action is taken.
    Manual calls are usually unnecessary because `RunAnalysis` creates it automatically.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `0` on success
    """
    return model.Analyze.CreateAnalysisModel()


def delete_results(model, case_name: str) -> int:
    """
    Delete analysis results for a specific case
    
    Args:
        model: SAP2000 SapModel object
        case_name: Case name
        
    Returns:
        `0` on success
    """
    return model.Analyze.DeleteResults(case_name, False)


def delete_all_results(model) -> int:
    """
    Delete analysis results for all cases
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `0` on success
    """
    return model.Analyze.DeleteResults("", True)


# =============================================================================
# Active degrees of freedom
# =============================================================================

def get_active_dof(model) -> Optional[ActiveDOF]:
    """
    Get active model degrees of freedom
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `ActiveDOF` instance, or `None` on failure
        
    Example:
        dof = get_active_dof(model)
        if dof:
            print(f"UX: {dof.ux}, UY: {dof.uy}, UZ: {dof.uz}")
    """
    result = model.Analyze.GetActiveDOF([False] * 6)
    values = com_data(result, 0)
    ret = com_data(result, 1, default=-1)
    if ret == 0 and values and len(values) >= 6:
        return ActiveDOF.from_list(list(values))
    return None


def set_active_dof(model, dof: ActiveDOF) -> int:
    """
    Set active model degrees of freedom
    
    Args:
        model: SAP2000 SapModel object
        dof: `ActiveDOF` instance
        
    Returns:
        `0` on success
        
    Example:
        # Set to a 2D plane frame
        set_active_dof(model, ActiveDOF.plane_xz())
        
        # Custom setting
        dof = ActiveDOF(ux=True, uy=True, uz=True, rx=False, ry=False, rz=False)
        set_active_dof(model, dof)
    """
    result = model.Analyze.SetActiveDOF(dof.to_list())
    return com_ret(result)


# =============================================================================
# Case status and run flags
# =============================================================================

def get_case_status(model) -> List[CaseStatusInfo]:
    """
    Get analysis status for all cases
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        List of `CaseStatusInfo`
        
    Example:
        statuses = get_case_status(model)
        for s in statuses:
            print(f"{s.name}: {s.status.name}, Finished: {s.is_finished}")
    """
    result = model.Analyze.GetCaseStatus(0, [], [])
    num = com_data(result, 0, default=0)
    names = com_data(result, 1)
    statuses = com_data(result, 2)
    ret = com_data(result, 3, default=-1)
    
    if ret == 0 and names and statuses:
        return [
            CaseStatusInfo(name=names[i], status=CaseStatus(statuses[i]))
            for i in range(num)
        ]
    return []


def get_run_case_flag(model) -> List[RunCaseFlag]:
    """
    Get run flags for all cases
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        List of `RunCaseFlag`
        
    Example:
        flags = get_run_case_flag(model)
        for f in flags:
            print(f"{f.name}: {'Run' if f.run else 'Do not run'}")
    """
    result = model.Analyze.GetRunCaseFlag(0, [], [])
    num = com_data(result, 0, default=0)
    names = com_data(result, 1)
    runs = com_data(result, 2)
    ret = com_data(result, 3, default=-1)
    
    if ret == 0 and names and runs:
        return [
            RunCaseFlag(name=names[i], run=bool(runs[i]))
            for i in range(num)
        ]
    return []


def set_run_case_flag(model, case_name: str, run: bool) -> int:
    """
    Set run flag for a specific case
    
    Args:
        model: SAP2000 SapModel object
        case_name: Case name
        run: Whether to run
        
    Returns:
        `0` on success
        
    Example:
        # Disable the MODAL case
        set_run_case_flag(model, "MODAL", False)
    """
    return model.Analyze.SetRunCaseFlag(case_name, run, False)


def set_run_case_flag_all(model, run: bool) -> int:
    """
    Set run flag for all cases
    
    Args:
        model: SAP2000 SapModel object
        run: Whether to run
        
    Returns:
        `0` on success
        
    Example:
        # Disable all cases
        set_run_case_flag_all(model, False)
        # Then enable only required cases
        set_run_case_flag(model, "DEAD", True)
    """
    return model.Analyze.SetRunCaseFlag("", run, True)


# =============================================================================
# Solver options
# =============================================================================

def get_solver_option(model) -> Optional[SolverOption]:
    """
    Get solver options
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        `SolverOption` instance, or `None` on failure
    """
    result = model.Analyze.GetSolverOption_3(0, 0, 0, 0, 0, "")
    solver_type = com_data(result, 0)
    if solver_type is not None:
        process_type = com_data(result, 1, default=0)
        num_parallel = com_data(result, 2, default=0)
        response_size = com_data(result, 3, default=0)
        num_threads = com_data(result, 4, default=0)
        stiff_case = com_data(result, 5, default="")
        ret = com_ret(result)
        
        if ret == 0:
            return SolverOption(
                solver_type=SolverType(solver_type),
                process_type=SolverProcessType(process_type),
                num_parallel_runs=num_parallel,
                response_file_size_max_mb=response_size,
                num_analysis_threads=num_threads,
                stiff_case=stiff_case if stiff_case else ""
            )
    return None


def set_solver_option(model, option: SolverOption) -> int:
    """
    Set solver options
    
    Args:
        model: SAP2000 SapModel object
        option: `SolverOption` instance
        
    Returns:
        `0` on success
        
    Example:
        opt = SolverOption(
            solver_type=SolverType.MULTI_THREADED,
            num_parallel_runs=4
        )
        set_solver_option(model, opt)
    """
    return model.Analyze.SetSolverOption_3(
        int(option.solver_type),
        int(option.process_type),
        option.num_parallel_runs,
        option.response_file_size_max_mb,
        option.num_analysis_threads,
        option.stiff_case
    )


# =============================================================================
# Geometry modification
# =============================================================================

def modify_undeformed_geometry(
    model,
    case_name: str,
    scale_factor: float,
    stage: int = 0,
    original: bool = False
) -> int:
    """
    Modify undeformed geometry based on case results
    
    Args:
        model: SAP2000 SapModel object
        case_name: Case name
        scale_factor: Scale factor
        stage: Stage number (for staged construction)
        original: Whether to use original geometry
        
    Returns:
        `0` on success
    """
    return model.Analyze.ModifyUnDeformedGeometry(
        case_name, scale_factor, stage, original
    )


def modify_undeformed_geometry_mode_shape(
    model,
    case_name: str,
    mode: int,
    max_disp: float,
    direction: int,
    original: bool = False
) -> int:
    """
    Modify undeformed geometry based on mode shape
    
    Args:
        model: SAP2000 SapModel object
        case_name: Modal case name
        mode: Mode number
        max_disp: Maximum displacement
        direction: Direction (`1=UX`, `2=UY`, `3=UZ`, `4=RX`, `5=RY`, `6=RZ`)
        original: Whether to use original geometry
        
    Returns:
        `0` on success
    """
    return model.Analyze.ModifyUndeformedGeometryModeShape(
        case_name, mode, max_disp, direction, original
    )


def merge_analysis_results(model, file_name: str) -> int:
    """
    Merge analysis result files
    
    Args:
        model: SAP2000 SapModel object
        file_name: Result file path
        
    Returns:
        `0` on success
    """
    return model.Analyze.MergeAnalysisResults(file_name)
