# -*- coding: utf-8 -*-
"""
data_classes.py - 分析相关数据类

用于封装分析控制的参数和返回值
"""

from dataclasses import dataclass
from typing import List
from .enums import CaseStatus, SolverType, SolverProcessType


@dataclass
class ActiveDOF:
    """
    活动自由度
    
    控制模型的全局自由度激活状态
    
    Attributes:
        ux: X方向平动
        uy: Y方向平动
        uz: Z方向平动
        rx: 绕X轴转动
        ry: 绕Y轴转动
        rz: 绕Z轴转动
    """
    ux: bool = True
    uy: bool = True
    uz: bool = True
    rx: bool = True
    ry: bool = True
    rz: bool = True
    
    def to_list(self) -> List[bool]:
        """转换为 API 需要的列表格式"""
        return [self.ux, self.uy, self.uz, self.rx, self.ry, self.rz]
    
    @classmethod
    def from_list(cls, values: List[bool]) -> "ActiveDOF":
        """从 API 返回的列表创建"""
        if len(values) >= 6:
            return cls(
                ux=values[0], uy=values[1], uz=values[2],
                rx=values[3], ry=values[4], rz=values[5]
            )
        return cls()
    
    @classmethod
    def plane_xz(cls) -> "ActiveDOF":
        """XZ平面分析 (2D框架)"""
        return cls(ux=True, uy=False, uz=True, rx=False, ry=True, rz=False)
    
    @classmethod
    def plane_xy(cls) -> "ActiveDOF":
        """XY平面分析"""
        return cls(ux=True, uy=True, uz=False, rx=False, ry=False, rz=True)
    
    @classmethod
    def space_frame(cls) -> "ActiveDOF":
        """空间框架分析 (全部激活)"""
        return cls(ux=True, uy=True, uz=True, rx=True, ry=True, rz=True)
    
    @classmethod
    def truss_3d(cls) -> "ActiveDOF":
        """3D桁架分析 (仅平动)"""
        return cls(ux=True, uy=True, uz=True, rx=False, ry=False, rz=False)


@dataclass
class SolverOption:
    """
    求解器选项
    
    Attributes:
        solver_type: 求解器类型
        process_type: 进程类型
        num_parallel_runs: 并行运行数 (-8到8，不含-1和0表示自动)
        response_file_size_max_mb: 响应文件最大尺寸(MB)，负值表示程序决定
        num_analysis_threads: 分析线程数，负值表示程序决定
        stiff_case: 输出刚度矩阵的工况名，空字符串表示不输出
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
    工况状态信息
    
    Attributes:
        name: 工况名称
        status: 工况状态
    """
    name: str
    status: CaseStatus
    
    @property
    def is_finished(self) -> bool:
        """是否已完成"""
        return self.status == CaseStatus.FINISHED
    
    @property
    def is_run(self) -> bool:
        """是否已运行（包括未完成）"""
        return self.status != CaseStatus.NOT_RUN


@dataclass
class RunCaseFlag:
    """
    工况运行标志
    
    Attributes:
        name: 工况名称
        run: 是否运行
    """
    name: str
    run: bool
