# -*- coding: utf-8 -*-
"""Tests for the statistics module.

Statistics depend on existing frames/sections in the model. These tests only
check return types and basic logic, not numeric accuracy.
"""

import pytest
from PySap2000.statistics import (
    get_steel_usage,
    get_cable_usage,
    SteelUsage,
    CableUsage,
)

pytestmark = pytest.mark.statistics


class TestSteelUsage:
    """Steel usage statistics."""

    def test_get_total(self, model):
        total = get_steel_usage(model)
        assert isinstance(total, float)
        assert total >= 0

    def test_get_by_section(self, model):
        result = get_steel_usage(model, group_by="section")
        assert isinstance(result, dict)
        # If the model has frames, expect section-grouped totals
        for key, val in result.items():
            assert isinstance(key, str)
            assert isinstance(val, float)
            assert val >= 0

    def test_get_by_material(self, model):
        result = get_steel_usage(model, group_by="material")
        assert isinstance(result, dict)

    def test_calculate_class(self, model):
        usage = SteelUsage.calculate(model)
        assert isinstance(usage, SteelUsage)
        assert usage.total >= 0

    def test_calculate_with_section(self, model):
        usage = SteelUsage.calculate(model, group_by="section")
        assert isinstance(usage.by_section, dict)


class TestCableUsage:
    """Cable usage statistics."""

    def test_get_total(self, model):
        total = get_cable_usage(model)
        assert isinstance(total, float)
        assert total >= 0

    def test_get_by_section(self, model):
        result = get_cable_usage(model, group_by="section")
        assert isinstance(result, dict)

    def test_calculate_class(self, model):
        usage = CableUsage.calculate(model)
        assert isinstance(usage, CableUsage)
        assert usage.total >= 0
