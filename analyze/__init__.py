# -*- coding: utf-8 -*-
"""
analyze - 分析控制模块

SAP2000 的 Analyze API，用于控制分析执行。

SAP2000 API 结构:
- Analyze.RunAnalysis - 运行分析
- Analyze.CreateAnalysisModel - 创建分析模型
- Analyze.DeleteResults - 删除结果
- Analyze.GetActiveDOF / SetActiveDOF - 活动自由度
- Analyze.GetCaseStatus - 工况状态
- Analyze.GetRunCaseFlag / SetRunCaseFlag - 运行标志
- Analyze.GetSolverOption_3 / SetSolverOption_3 - 求解器选项
- Analyze.ModifyUnDeformedGeometry - 修改未变形几何
- Analyze.MergeAnalysisResults - 合并分析结果

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
    
    # 运行分析
    run_analysis(model)
    
    # 设置活动自由度
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
    # 枚举
    "CaseStatus",
    "SolverType",
    "SolverProcessType",
    # 数据类
    "ActiveDOF",
    "SolverOption",
    "CaseStatusInfo",
    "RunCaseFlag",
    # 核心分析函数
    "run_analysis",
    "create_analysis_model",
    "delete_results",
    "delete_all_results",
    # 自由度
    "get_active_dof",
    "set_active_dof",
    # 工况状态
    "get_case_status",
    "get_run_case_flag",
    "set_run_case_flag",
    "set_run_case_flag_all",
    # 求解器
    "get_solver_option",
    "set_solver_option",
    # 几何修改
    "modify_undeformed_geometry",
    "modify_undeformed_geometry_mode_shape",
    "merge_analysis_results",
]

# AI Agent 友好的 API 分类
ANALYZE_API_CATEGORIES = {
    "core": {
        "description": "核心分析控制",
        "functions": ["run_analysis", "create_analysis_model", "delete_results", "delete_all_results"],
        "api_path": "Analyze",
    },
    "dof": {
        "description": "活动自由度控制",
        "functions": ["get_active_dof", "set_active_dof"],
        "classes": ["ActiveDOF"],
        "api_path": "Analyze.GetActiveDOF/SetActiveDOF",
    },
    "case_control": {
        "description": "工况运行控制",
        "functions": ["get_case_status", "get_run_case_flag", "set_run_case_flag", "set_run_case_flag_all"],
        "classes": ["CaseStatusInfo", "RunCaseFlag"],
        "enums": ["CaseStatus"],
        "api_path": "Analyze.GetCaseStatus/GetRunCaseFlag/SetRunCaseFlag",
    },
    "solver": {
        "description": "求解器选项",
        "functions": ["get_solver_option", "set_solver_option"],
        "classes": ["SolverOption"],
        "enums": ["SolverType", "SolverProcessType"],
        "api_path": "Analyze.GetSolverOption_3/SetSolverOption_3",
    },
    "geometry": {
        "description": "几何修改",
        "functions": ["modify_undeformed_geometry", "modify_undeformed_geometry_mode_shape", "merge_analysis_results"],
        "api_path": "Analyze.ModifyUnDeformedGeometry/MergeAnalysisResults",
    },
}
