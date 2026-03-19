# -*- coding: utf-8 -*-
"""
statistics - 统计分析模块

提供模型级别的统计功能，包括:
- 用钢量统计 (SteelUsage)
- 用索量统计 (CableUsage)

Usage:
    from statistics import SteelUsage, get_steel_usage
    from statistics import CableUsage, get_cable_usage
    
    # 获取总用钢量
    total = get_steel_usage(model)
    
    # 获取总用索量
    total = get_cable_usage(model)
    
    # 按截面分组
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
