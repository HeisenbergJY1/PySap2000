# -*- coding: utf-8 -*-
"""统计模块测试 (Statistics)

注意: 统计依赖模型中已有的杆件和截面数据。
测试只验证返回类型和基本逻辑，不验证具体数值。
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
    """用钢量统计测试"""

    def test_get_total(self, model):
        total = get_steel_usage(model)
        assert isinstance(total, float)
        assert total >= 0

    def test_get_by_section(self, model):
        result = get_steel_usage(model, group_by="section")
        assert isinstance(result, dict)
        # 如果模型有杆件，应该有截面分组
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
    """用索量统计测试"""

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
