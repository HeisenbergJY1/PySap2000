# -*- coding: utf-8 -*-
"""钢结构设计相关测试"""

import pytest
from PySap2000.design.steel import (
    get_steel_code,
    set_steel_code,
    get_steel_results_available,
    delete_steel_results,
    get_steel_design_group,
    get_steel_design_section,
    set_steel_design_section,
    get_steel_combo_strength,
    get_steel_combo_deflection,
    reset_steel_overwrites,
    verify_steel_passed,
    verify_steel_sections,
)
from PySap2000.design.enums import SteelDesignCode, ItemType
from PySap2000.design.data_classes import VerifyPassedResult

pytestmark = pytest.mark.design


class TestSteelDesignCode:
    """设计规范测试"""

    def test_get_steel_code(self, model):
        code = get_steel_code(model)
        assert isinstance(code, str)
        assert len(code) > 0

    def test_set_steel_code(self, model):
        # 先记住当前规范
        original = get_steel_code(model)
        # 设置中国规范
        ret = set_steel_code(model, SteelDesignCode.CHINESE_2010)
        assert ret == 0
        # 验证
        code = get_steel_code(model)
        assert "Chinese" in code or "2010" in code
        # 恢复
        set_steel_code(model, original)


class TestSteelDesignQuery:
    """设计查询测试"""

    def test_results_available(self, model):
        available = get_steel_results_available(model)
        assert isinstance(available, bool)

    def test_get_design_group(self, model):
        groups = get_steel_design_group(model)
        assert isinstance(groups, list)

    def test_get_design_section(self, model):
        # 框架 "1" 在 test_frame 中创建
        section = get_steel_design_section(model, "1")
        assert isinstance(section, str)

    def test_get_combo_strength(self, model):
        combos = get_steel_combo_strength(model)
        assert isinstance(combos, list)

    def test_get_combo_deflection(self, model):
        combos = get_steel_combo_deflection(model)
        assert isinstance(combos, list)

    def test_verify_passed(self, model):
        result = verify_steel_passed(model)
        assert isinstance(result, VerifyPassedResult)
        assert isinstance(result.all_passed, bool)

    def test_verify_sections(self, model):
        names = verify_steel_sections(model)
        assert isinstance(names, list)


class TestSteelDesignUpdate:
    """设计更新测试"""

    def test_set_design_section(self, model):
        ret = set_steel_design_section(model, "1", "W14X30")
        assert ret == 0

    def test_reset_overwrites(self, model):
        ret = reset_steel_overwrites(model)
        assert ret == 0

    def test_delete_results(self, model):
        ret = delete_steel_results(model)
        assert ret == 0
