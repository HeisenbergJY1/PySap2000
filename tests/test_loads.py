# -*- coding: utf-8 -*-
"""Tests for applied loads (joint and frame).

Depends on the "MyDead" load pattern created in test_loading.py.
"""

import pytest
from PySap2000.loads import (
    # Joint loads
    set_point_load_force,
    get_point_load_force,
    delete_point_load_force,
    set_point_load_displ,
    get_point_load_displ,
    delete_point_load_displ,
    # Frame loads
    set_frame_load_distributed,
    get_frame_load_distributed,
    delete_frame_load_distributed,
    set_frame_load_point,
    get_frame_load_point,
    delete_frame_load_point,
    # Enums
    FrameLoadType,
    FrameLoadDirection,
)
from PySap2000.loading import LoadPattern, LoadPatternType

pytestmark = pytest.mark.loads

# Load-pattern name ensured by ensure_load_pattern fixture
LP_NAME = "TestLP_Loads"


@pytest.fixture(scope="module", autouse=True)
def ensure_load_pattern(app):
    """Ensure the test load pattern exists."""
    lp = LoadPattern(
        name=LP_NAME,
        load_type=LoadPatternType.DEAD,
        self_weight_multiplier=0.0,
    )
    app.create_object(lp)  # Returns -1 if already exists


class TestPointLoadForce:
    """Joint force loads."""

    def test_set_point_load_force(self, model):
        ret = set_point_load_force(model, "10", LP_NAME, (0, 0, -100, 0, 0, 0))
        assert ret == 0

    def test_get_point_load_force(self, model):
        loads = get_point_load_force(model, "10")
        assert isinstance(loads, list)
        assert len(loads) > 0

    def test_delete_point_load_force(self, model):
        ret = delete_point_load_force(model, "10", LP_NAME)
        assert ret == 0


class TestPointLoadDispl:
    """Joint displacement loads."""

    def test_set_point_load_displ(self, model):
        ret = set_point_load_displ(model, "10", LP_NAME, (0, 0, -0.01, 0, 0, 0))
        assert ret == 0

    def test_get_point_load_displ(self, model):
        loads = get_point_load_displ(model, "10")
        assert isinstance(loads, list)
        assert len(loads) > 0

    def test_delete_point_load_displ(self, model):
        ret = delete_point_load_displ(model, "10", LP_NAME)
        assert ret == 0


class TestFrameLoadDistributed:
    """Frame distributed loads."""

    def test_set_uniform_load(self, model):
        ret = set_frame_load_distributed(model, "1", LP_NAME, 10)
        assert ret == 0

    def test_get_distributed_load(self, model):
        loads = get_frame_load_distributed(model, "1")
        assert isinstance(loads, list)
        assert len(loads) > 0

    def test_delete_distributed_load(self, model):
        ret = delete_frame_load_distributed(model, "1", LP_NAME)
        assert ret == 0


class TestFrameLoadPoint:
    """Frame point loads."""

    def test_set_point_load(self, model):
        ret = set_frame_load_point(model, "1", LP_NAME, 100)
        assert ret == 0

    def test_get_point_load(self, model):
        loads = get_frame_load_point(model, "1")
        assert isinstance(loads, list)
        assert len(loads) > 0

    def test_delete_point_load(self, model):
        ret = delete_frame_load_point(model, "1", LP_NAME)
        assert ret == 0
