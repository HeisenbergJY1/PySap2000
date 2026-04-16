# -*- coding: utf-8 -*-
"""
PySap2000 - Python wrapper for the SAP2000 API.

The package follows a design inspired by `dlubal.api`.

Usage:
    from PySap2000 import Application
    from PySap2000.structure_core import Point, Frame, Material
    from PySap2000.point import set_point_support, PointSupportType
    from PySap2000.loads import set_point_load_force
    from PySap2000.loading import LoadPattern, LoadCombination
    from PySap2000.results import get_joint_displ, deselect_all_cases_and_combos
    from PySap2000.global_parameters import Units, UnitSystem, ModelSettings
    from PySap2000.design import set_steel_code, start_steel_design, SteelDesignCode
    
    # Connect to SAP2000
    with Application() as app:
        # Set units
        Units.set_present_units(app.model, UnitSystem.KN_M_C)
        
        # Create points
        app.create_object(Point(no=1, x=0, y=0, z=0))
        app.create_object(Point(no=2, x=10, y=0, z=0))
        
        # Create a frame
        app.create_object(Frame(no=1, start_point=1, end_point=2, section="W14X30"))
        
        # Add supports
        set_point_support(app.model, "1", PointSupportType.FIXED)
        
        # Add loads
        set_point_load_force(app.model, "2", "DEAD", fz=-10)
        
        # Run analysis
        app.calculate()
        
        # Steel design
        set_steel_code(app.model, SteelDesignCode.AISC_360_16)
        start_steel_design(app.model)
        
        # Get results
        deselect_all_cases_and_combos(app.model)
        displ = get_joint_displ(app.model, "2")

Author: JIANGYAO-AISA
Version: 2.0.0
"""

__version__ = "2.0.17"
__author__ = "JIANGYAO-AISA"

# Core class
from .application import Application

# Exceptions
from .exceptions import (
    PySap2000Error,
    SAPConnectionError,
    ConnectionError,  # Backward-compatible alias; prefer SAPConnectionError
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
    # Deprecated exceptions kept for backward compatibility
    NodeError,
    MemberError,
)

# Configuration and logging
from .config import config
from .logger import logger, setup_logger, get_logger

# Utilities
from .utils.deprecation import deprecated

__all__ = [
    # Version info
    '__version__',
    '__author__',
    
    # Core class
    'Application',
    
    # Configuration and logging
    'config',
    'logger',
    'setup_logger',
    'get_logger',
    
    # Utilities
    'deprecated',
    
    # Exceptions (recommended)
    'PySap2000Error',
    'SAPConnectionError',
    'ConnectionError',  # Backward-compatible alias
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
    
    # Deprecated exceptions kept for backward compatibility
    'NodeError',
    'MemberError',
]
