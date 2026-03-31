# -*- coding: utf-8 -*-
"""Tests for group definitions."""

import pytest
from PySap2000.group import Group, GroupObjectType

pytestmark = pytest.mark.group


class TestGroupCreate:
    """Create groups."""

    def test_create_group(self, model):
        g = Group(name="TestGroup")
        ret = g._create(model)
        assert ret in (0, -1)

    def test_create_another_group(self, model):
        g = Group(name="TestGroup2")
        ret = g._create(model)
        assert ret in (0, -1)


class TestGroupQuery:
    """Query groups."""

    def test_get_count(self, model):
        count = Group.get_count(model)
        assert count >= 2

    def test_get_name_list(self, model):
        names = Group.get_name_list(model)
        assert isinstance(names, list)
        assert "TestGroup" in names

    def test_get_by_name(self, model):
        g = Group.get_by_name(model, "TestGroup")
        assert g is not None
        assert g.name == "TestGroup"

    def test_get_all(self, model):
        groups = Group.get_all(model)
        assert isinstance(groups, list)
        assert len(groups) > 0

    def test_get_assignments(self, model):
        g = Group(name="TestGroup")
        assignments = g.get_assignments(model)
        assert isinstance(assignments, list)

    def test_get_member_count(self, model):
        g = Group(name="TestGroup")
        count = g.get_member_count(model)
        assert isinstance(count, int)


class TestGroupUpdate:
    """Update groups."""

    def test_rename_group(self, model):
        g = Group(name="TestGroup2")
        ret = g.change_name(model, "TestGroup2R")
        assert ret == 0
        # Revert name
        g.change_name(model, "TestGroup2")

    def test_clear_group(self, model):
        g = Group(name="TestGroup")
        ret = g.clear(model)
        assert ret == 0

    def test_delete_group(self, model):
        g = Group(name="TestGroup2")
        ret = g._delete(model)
        assert ret == 0
