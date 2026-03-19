# -*- coding: utf-8 -*-
"""
analyze.py - 分析控制函数

SAP2000 Analyze API 的核心函数封装

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
# 核心分析函数
# =============================================================================

def run_analysis(model) -> int:
    """
    运行分析
    
    自动创建分析模型并运行。运行前必须保存模型文件。
    
    Args:
        model: SapModel 对象
        
    Returns:
        0 表示成功
        
    Note:
        运行前必须调用 File.Save() 保存模型
        
    Example:
        model.File.Save("C:/model.sdb")
        run_analysis(model)
    """
    return model.Analyze.RunAnalysis()


def create_analysis_model(model) -> int:
    """
    创建分析模型
    
    如果分析模型已存在且是最新的，则不执行任何操作。
    通常不需要手动调用，RunAnalysis 会自动创建。
    
    Args:
        model: SapModel 对象
        
    Returns:
        0 表示成功
    """
    return model.Analyze.CreateAnalysisModel()


def delete_results(model, case_name: str) -> int:
    """
    删除指定工况的分析结果
    
    Args:
        model: SapModel 对象
        case_name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.Analyze.DeleteResults(case_name, False)


def delete_all_results(model) -> int:
    """
    删除所有工况的分析结果
    
    Args:
        model: SapModel 对象
        
    Returns:
        0 表示成功
    """
    return model.Analyze.DeleteResults("", True)


# =============================================================================
# 活动自由度
# =============================================================================

def get_active_dof(model) -> Optional[ActiveDOF]:
    """
    获取模型活动自由度
    
    Args:
        model: SapModel 对象
        
    Returns:
        ActiveDOF 对象，失败返回 None
        
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
    设置模型活动自由度
    
    Args:
        model: SapModel 对象
        dof: ActiveDOF 对象
        
    Returns:
        0 表示成功
        
    Example:
        # 设置为2D平面框架
        set_active_dof(model, ActiveDOF.plane_xz())
        
        # 自定义设置
        dof = ActiveDOF(ux=True, uy=True, uz=True, rx=False, ry=False, rz=False)
        set_active_dof(model, dof)
    """
    result = model.Analyze.SetActiveDOF(dof.to_list())
    return com_ret(result)


# =============================================================================
# 工况状态和运行标志
# =============================================================================

def get_case_status(model) -> List[CaseStatusInfo]:
    """
    获取所有工况的分析状态
    
    Args:
        model: SapModel 对象
        
    Returns:
        CaseStatusInfo 列表
        
    Example:
        statuses = get_case_status(model)
        for s in statuses:
            print(f"{s.name}: {s.status.name}, 完成: {s.is_finished}")
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
    获取所有工况的运行标志
    
    Args:
        model: SapModel 对象
        
    Returns:
        RunCaseFlag 列表
        
    Example:
        flags = get_run_case_flag(model)
        for f in flags:
            print(f"{f.name}: {'运行' if f.run else '不运行'}")
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
    设置指定工况的运行标志
    
    Args:
        model: SapModel 对象
        case_name: 工况名称
        run: 是否运行
        
    Returns:
        0 表示成功
        
    Example:
        # 禁用 MODAL 工况
        set_run_case_flag(model, "MODAL", False)
    """
    return model.Analyze.SetRunCaseFlag(case_name, run, False)


def set_run_case_flag_all(model, run: bool) -> int:
    """
    设置所有工况的运行标志
    
    Args:
        model: SapModel 对象
        run: 是否运行
        
    Returns:
        0 表示成功
        
    Example:
        # 禁用所有工况
        set_run_case_flag_all(model, False)
        # 然后只启用需要的
        set_run_case_flag(model, "DEAD", True)
    """
    return model.Analyze.SetRunCaseFlag("", run, True)


# =============================================================================
# 求解器选项
# =============================================================================

def get_solver_option(model) -> Optional[SolverOption]:
    """
    获取求解器选项
    
    Args:
        model: SapModel 对象
        
    Returns:
        SolverOption 对象，失败返回 None
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
    设置求解器选项
    
    Args:
        model: SapModel 对象
        option: SolverOption 对象
        
    Returns:
        0 表示成功
        
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
# 几何修改
# =============================================================================

def modify_undeformed_geometry(
    model,
    case_name: str,
    scale_factor: float,
    stage: int = 0,
    original: bool = False
) -> int:
    """
    根据工况结果修改未变形几何
    
    Args:
        model: SapModel 对象
        case_name: 工况名称
        scale_factor: 缩放系数
        stage: 阶段号 (用于分阶段施工)
        original: 是否基于原始几何
        
    Returns:
        0 表示成功
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
    根据振型修改未变形几何
    
    Args:
        model: SapModel 对象
        case_name: 模态工况名称
        mode: 振型号
        max_disp: 最大位移
        direction: 方向 (1=UX, 2=UY, 3=UZ, 4=RX, 5=RY, 6=RZ)
        original: 是否基于原始几何
        
    Returns:
        0 表示成功
    """
    return model.Analyze.ModifyUndeformedGeometryModeShape(
        case_name, mode, max_disp, direction, original
    )


def merge_analysis_results(model, file_name: str) -> int:
    """
    合并分析结果文件
    
    Args:
        model: SapModel 对象
        file_name: 结果文件路径
        
    Returns:
        0 表示成功
    """
    return model.Analyze.MergeAnalysisResults(file_name)
