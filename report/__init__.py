# -*- coding: utf-8 -*-
"""
report - Calculation report generation helpers.

Extracts data from a SAP2000 model and builds structural report tables.

Usage:
    from report import ReportGenerator

    with Application() as app:
        rg = ReportGenerator(app.model)
        rg.generate("output.docx", frame_names=["56", "57", "59"])
"""

from .generator import ReportGenerator
from .data_collector import discover_tables, discover_table_fields

__all__ = ["ReportGenerator", "discover_tables", "discover_table_fields"]
