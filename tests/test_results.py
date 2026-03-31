# -*- coding: utf-8 -*-
"""Tests for analysis results.

These tests assume analysis has been run; some helpers may return empty lists
if the model has not been analyzed.
"""

import pytest
from PySap2000.results import (
    # Output selection
    deselect_all_cases_and_combos,
    set_case_selected_for_output,
    get_case_selected_for_output,
    select_cases_for_output,
    get_option_base_react_loc,
    set_option_base_react_loc,
    # Enums
    ItemTypeElm,
)

pytestmark = pytest.mark.results


class TestResultsSetup:
    """Output setup."""

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
