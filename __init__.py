# -*- coding: utf-8 -*-
"""
PySap2000 - SAP2000 Python API 封装库
参考 dlubal.api 设计模式

Usage:
    from PySap2000 import Application
    from PySap2000.structure_core import Point, Frame, Material
    from PySap2000.point import set_point_support, PointSupportType
    from PySap2000.loads import set_point_load_force
    from PySap2000.loading import LoadPattern, LoadCombination
    from PySap2000.results import get_joint_displ, deselect_all_cases_and_combos
    from PySap2000.global_parameters import Units, UnitSystem, ModelSettings
    from PySap2000.design import set_steel_code, start_steel_design, SteelDesignCode
    
    # 连接 SAP2000
    with Application() as app:
        # 设置单位
        Units.set_present_units(app.model, UnitSystem.KN_M_C)
        
        # 创建节点
        app.create_object(Point(no=1, x=0, y=0, z=0))
        app.create_object(Point(no=2, x=10, y=0, z=0))
        
        # 创建框架
        app.create_object(Frame(no=1, start_point=1, end_point=2, section="W14X30"))
        
        # 添加支座
        set_point_support(app.model, "1", PointSupportType.FIXED)
        
        # 添加荷载
        set_point_load_force(app.model, "2", "DEAD", fz=-10)
        
        # 运行分析
        app.calculate()
        
        # 钢结构设计
        set_steel_code(app.model, SteelDesignCode.AISC_360_16)
        start_steel_design(app.model)
        
        # 获取结果
        deselect_all_cases_and_combos(app.model)
        displ = get_joint_displ(app.model, "2")

Author: JIANGYAO-AISA
Version: 2.0.0
"""

__version__ = "2.0.16"
__author__ = "JIANGYAO-AISA"

# 核心类
from .application import Application

# 异常
from .exceptions import (
    PySap2000Error,
    ConnectionError,
    ObjectError,
    PointError,
    FrameError,
    AreaError,
    CableError,
    LinkError,
    SurfaceError,
    MaterialError,
    SectionError,
    LoadError,
    AnalysisError,
    ResultError,
    # 弃用的异常（保留向后兼容）
    NodeError,
    MemberError,
)

# 配置和日志
from .config import config
from .logger import logger, setup_logger, get_logger

# 工具类
from .utils.deprecation import deprecated

__all__ = [
    # 版本信息
    '__version__',
    '__author__',
    
    # 核心类
    'Application',
    
    # 配置和日志
    'config',
    'logger',
    'setup_logger',
    'get_logger',
    
    # 工具类
    'deprecated',
    
    # 异常（推荐使用）
    'PySap2000Error',
    'ConnectionError',
    'ObjectError',
    'PointError',
    'FrameError',
    'AreaError',
    'CableError',
    'LinkError',
    'SurfaceError',
    'MaterialError',
    'SectionError',
    'LoadError',
    'AnalysisError',
    'ResultError',
    
    # 异常（弃用，保留向后兼容）
    'NodeError',
    'MemberError',
]
