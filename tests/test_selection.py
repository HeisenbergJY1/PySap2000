# -*- coding: utf-8 -*-
"""Tests for selection helpers."""

import pytest
from PySap2000.selection import (
    select_all,
    deselect_all,
    clear_selection,
    invert_selection,
    get_selected,
    get_selected_count,
    get_selected_objects,
    select_by_property_frame,
    select_supported_points,
    SelectObjectType,
)

pytestmark = pytest.mark.selection


class TestBasicSelection:
    """Basic selection operations."""

    def test_select_all(self, model):
        ret = select_all(model)
        assert ret == 0

    def test_get_selected_count(self, model):
        select_all(model)
        count = get_selected_count(model)
        assert count > 0

    def test_get_selected(self, model):
        select_all(model)
        selected = get_selected(model)
        assert isinstance(selected, list)
        assert len(selected) > 0

    def test_get_selected_objects(self, model):
        select_all(model)
        objs = get_selected_objects(model)
        assert isinstance(objs, dict)

    def test_deselect_all(self, model):
        ret = deselect_all(model)
        assert ret == 0

    def test_clear_selection(self, model):
        select_all(model)
        ret = clear_selection(model)
        assert ret == 0

    def test_invert_selection(self, model):
        clear_selection(model)
        ret = invert_selection(model)
        assert ret == 0
        count = get_selected_count(model)
        assert count > 0
        # Cleanup
        clear_selection(model)


class TestPropertySelection:
    """Selection by property."""

    def test_select_by_property_frame(self, model):
        clear_selection(model)
        ret = select_by_property_frame(model, "W14X30")
        assert ret == 0

    def test_select_supported_points(self, model):
        clear_selection(model)
        ret = select_supported_points(model, [True, True, True, True, True, True])
        assert ret == 0
        # Cleanup
        clear_selection(model)
