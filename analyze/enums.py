# -*- coding: utf-8 -*-
"""
enums.py - 分析相关枚举

SAP2000 Analyze API 使用的枚举类型
"""

from enum import IntEnum


class CaseStatus(IntEnum):
    """
    工况分析状态
    
    对应 Analyze.GetCaseStatus 返回的 Status 值
    """
    NOT_RUN = 1           # 未运行
    COULD_NOT_START = 2   # 无法启动
    NOT_FINISHED = 3      # 未完成
    FINISHED = 4          # 已完成


class SolverType(IntEnum):
    """
    求解器类型
    
    对应 Analyze.GetSolverOption_3 / SetSolverOption_3 的 SolverType 参数
    """
    STANDARD = 0          # 标准求解器
    ADVANCED = 1          # 高级求解器
    MULTI_THREADED = 2    # 多线程求解器


class SolverProcessType(IntEnum):
    """
    求解器进程类型
    
    对应 Analyze.GetSolverOption_3 / SetSolverOption_3 的 SolverProcessType 参数
    """
    AUTO = 0              # 自动 (程序决定)
    GUI_PROCESS = 1       # GUI 进程
    SEPARATE_PROCESS = 2  # 独立进程
