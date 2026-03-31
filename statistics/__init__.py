# -*- coding: utf-8 -*-
"""
statistics - Statistics module.

Provides model-level statistics, including:
- Steel-usage statistics (`SteelUsage`)
- Cable-usage statistics (`CableUsage`)

Usage:
    from statistics import SteelUsage, get_steel_usage
    from statistics import CableUsage, get_cable_usage
    
    # Get total steel usage
    total = get_steel_usage(model)
    
    # Get total cable usage
    total = get_cable_usage(model)
    
    # Group by section
    by_section = get_steel_usage(model, group_by="section")
"""

from .steel_usage import SteelUsage, get_steel_usage
from .cable_usage import CableUsage, get_cable_usage

__all__ = [
    'SteelUsage',
    'get_steel_usage',
    'CableUsage',
    'get_cable_usage',
]
