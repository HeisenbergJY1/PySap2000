# -*- coding: utf-8 -*-
"""
global_parameters - Global model parameters.

Includes unit systems, project information, degrees of freedom, and related settings.
"""

from .units import Units, UnitSystem
from .project_info import ProjectInfo
from .model_settings import ModelSettings, ActiveDOF

__all__ = [
    'Units',
    'UnitSystem',
    'ProjectInfo',
    'ModelSettings',
    'ActiveDOF',
]
