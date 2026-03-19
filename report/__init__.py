# -*- coding: utf-8 -*-
"""
report - 计算书生成模块

从 SAP2000 模型中提取数据，生成结构计算书表格。

Usage:
    from report import ReportGenerator

    with Application() as app:
        rg = ReportGenerator(app.model)
        rg.generate("output.docx", frame_names=["56", "57", "59"])
"""

from .generator import ReportGenerator
from .data_collector import discover_tables, discover_table_fields

__all__ = ["ReportGenerator", "discover_tables", "discover_table_fields"]
