# -*- coding: utf-8 -*-
"""分析结果相关测试

注意：结果测试依赖分析已运行。如果模型未分析，部分测试可能返回空列表。
"""

import pytest
from PySap2000.results import (
    # 输出设置
    deselect_all_cases_and_combos,
    set_case_selected_for_output,
    get_case_selected_for_output,
    select_cases_for_output,
    get_option_base_react_loc,
    set_option_base_react_loc,
    # 枚举
    ItemTypeElm,
)

pytestmark = pytest.mark.results


class TestResultsSetup:
    """输出设置测试"""

    def test_deselect_all(self, model):
        ret = deselect_all_cases_and_combos(model)
        assert ret == 0

    def test_set_case_selected(self, model):
        ret = set_case_selected_for_output(model, "Dead", True)
        assert ret == 0

    def test_get_case_selected(self, model):
        set_case_selected_for_output(model, "Dead", True)
        selected = get_case_selected_for_output(model, "Dead")
        assert isinstance(selected, bool)

    def test_select_cases_for_output(self, model):
        ret = select_cases_for_output(model, ["Dead"])
        assert ret == 0

    def test_get_base_react_loc(self, model):
        loc = get_option_base_react_loc(model)
        assert isinstance(loc, tuple)
        assert len(loc) == 3

    def test_set_base_react_loc(self, model):
        ret = set_option_base_react_loc(model, 0.0, 0.0, 0.0)
        assert ret == 0
