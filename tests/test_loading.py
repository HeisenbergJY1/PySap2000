# -*- coding: utf-8 -*-
"""Tests for load patterns and load cases."""

import pytest
from PySap2000.loading import (
    LoadPattern, LoadPatternType,
    LoadCase, LoadCaseType,
)

pytestmark = pytest.mark.loading


class TestLoadPatternCreate:
    """Create load patterns."""

    def test_create_dead_pattern(self, app):
        lp = LoadPattern(
            name="MyDead",
            load_type=LoadPatternType.DEAD,
            self_weight_multiplier=1.0,
        )
        ret = app.create_object(lp)
        assert ret in (0, -1)

    def test_create_live_pattern(self, app):
        lp = LoadPattern(
            name="MyLive",
            load_type=LoadPatternType.LIVE,
            self_weight_multiplier=0.0,
        )
        ret = app.create_object(lp)
        assert ret in (0, -1)


class TestLoadPatternQuery:
    """Query load patterns."""

    def test_get_name_list(self, model):
        names = LoadPattern.get_name_list(model)
        assert isinstance(names, list)
        assert len(names) > 0

    def test_get_count(self, model):
        count = LoadPattern.get_count(model)
        assert count > 0

    def test_get_by_name(self, model):
        lp = LoadPattern.get_by_name(model, "Dead")
        if lp is None:
            # Default template may use a different pattern name
            names = LoadPattern.get_name_list(model)
            assert len(names) > 0
            lp = LoadPattern.get_by_name(model, names[0])
        assert lp is not None
        assert lp.load_type is not None

    def test_get_all(self, model):
        patterns = LoadPattern.get_all(model)
        assert isinstance(patterns, list)
        assert len(patterns) > 0


class TestLoadPatternUpdate:
    """Update load patterns."""

    def test_set_self_weight_multiplier(self, model):
        lp = LoadPattern(name="MyDead")
        lp._get(model)
        ret = lp.set_self_weight_multiplier(model, 1.5)
        assert ret == 0

    def test_set_load_type(self, model):
        lp = LoadPattern(name="MyLive")
        lp._get(model)
        ret = lp.set_load_type(model, LoadPatternType.REDUCELIVE)
        assert ret == 0

    def test_rename_pattern(self, model):
        lp = LoadPattern(name="MyLive")
        ret = lp.change_name(model, "MyLive2")
        assert ret == 0
        # Rename back
        lp.change_name(model, "MyLive")


class TestLoadCaseQuery:
    """Query load cases."""

    def test_get_name_list(self, model):
        names = LoadCase.get_name_list(model)
        assert isinstance(names, list)
        assert len(names) > 0

    def test_get_count(self, model):
        count = LoadCase.get_count(model)
        assert count > 0

    def test_get_by_name(self, model):
        names = LoadCase.get_name_list(model)
        assert len(names) > 0
        case = LoadCase.get_by_name(model, names[0])
        assert case is not None
        assert case.case_type is not None

    def test_get_all(self, model):
        cases = LoadCase.get_all(model)
        assert isinstance(cases, list)
        assert len(cases) > 0
