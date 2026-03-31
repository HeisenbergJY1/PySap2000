# -*- coding: utf-8 -*-
"""
analyze - Analysis control helpers

Wraps the SAP2000 `Analyze` API for controlling analysis execution.

SAP2000 API structure:
- Analyze.RunAnalysis - Run analysis
- Analyze.CreateAnalysisModel - Create analysis model
- Analyze.DeleteResults - Delete results
- Analyze.GetActiveDOF / SetActiveDOF - Active degrees of freedom
- Analyze.GetCaseStatus - Case status
- Analyze.GetRunCaseFlag / SetRunCaseFlag - Run flags
- Analyze.GetSolverOption_3 / SetSolverOption_3 - Solver options
- Analyze.ModifyUnDeformedGeometry - Modify undeformed geometry
- Analyze.MergeAnalysisResults - Merge analysis results

Usage:
    from PySap2000.analyze import (
        run_analysis,
        create_analysis_model,
        delete_results,
        ActiveDOF,
        get_active_dof,
        set_active_dof,
        SolverOption,
        get_solver_option,
        set_solver_option,
    )
    
    # Run analysis
    run_analysis(model)
    
    # Set active degrees of freedom
    dof = ActiveDOF(ux=True, uy=True, uz=True, rx=False, ry=False, rz=False)
    set_active_dof(model, dof)
"""

from .enums import CaseStatus, SolverType, SolverProcessType
from .data_classes import ActiveDOF, SolverOption, CaseStatusInfo, RunCaseFlag
from .analyze import (
    run_analysis,
    create_analysis_model,
    delete_results,
    delete_all_results,
    get_active_dof,
    set_active_dof,
    get_case_status,
    get_run_case_flag,
    set_run_case_flag,
    set_run_case_flag_all,
    get_solver_option,
    set_solver_option,
    modify_undeformed_geometry,
    modify_undeformed_geometry_mode_shape,
    merge_analysis_results,
)

__all__ = [
    # Enums
    "CaseStatus",
    "SolverType",
    "SolverProcessType",
    # Dataclasses
    "ActiveDOF",
    "SolverOption",
    "CaseStatusInfo",
    "RunCaseFlag",
    # Core analysis functions
    "run_analysis",
    "create_analysis_model",
    "delete_results",
    "delete_all_results",
    # Degrees of freedom
    "get_active_dof",
    "set_active_dof",
    # Case status
    "get_case_status",
    "get_run_case_flag",
    "set_run_case_flag",
    "set_run_case_flag_all",
    # Solver
    "get_solver_option",
    "set_solver_option",
    # Geometry modification
    "modify_undeformed_geometry",
    "modify_undeformed_geometry_mode_shape",
    "merge_analysis_results",
]

# API categories for discoverability
ANALYZE_API_CATEGORIES = {
    "core": {
        "description": "Core analysis control",
        "functions": ["run_analysis", "create_analysis_model", "delete_results", "delete_all_results"],
        "api_path": "Analyze",
    },
    "dof": {
        "description": "Active degree-of-freedom control",
        "functions": ["get_active_dof", "set_active_dof"],
        "classes": ["ActiveDOF"],
        "api_path": "Analyze.GetActiveDOF/SetActiveDOF",
    },
    "case_control": {
        "description": "Case run control",
        "functions": ["get_case_status", "get_run_case_flag", "set_run_case_flag", "set_run_case_flag_all"],
        "classes": ["CaseStatusInfo", "RunCaseFlag"],
        "enums": ["CaseStatus"],
        "api_path": "Analyze.GetCaseStatus/GetRunCaseFlag/SetRunCaseFlag",
    },
    "solver": {
        "description": "Solver options",
        "functions": ["get_solver_option", "set_solver_option"],
        "classes": ["SolverOption"],
        "enums": ["SolverType", "SolverProcessType"],
        "api_path": "Analyze.GetSolverOption_3/SetSolverOption_3",
    },
    "geometry": {
        "description": "Geometry modification",
        "functions": ["modify_undeformed_geometry", "modify_undeformed_geometry_mode_shape", "merge_analysis_results"],
        "api_path": "Analyze.ModifyUnDeformedGeometry/MergeAnalysisResults",
    },
}
