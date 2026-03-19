# -*- coding: utf-8 -*-
"""索单元相关测试"""

import pytest
from PySap2000.structure_core import Cable, Point
from PySap2000.section import CableSection

pytestmark = pytest.mark.cable


@pytest.fixture(scope="module")
def cable_points(app):
    """创建 cable 专用的节点（距离足够大，满足索的几何要求）"""
    app.create_object(Point(no=101, x=0, y=0, z=5000))
    app.create_object(Point(no=102, x=10000, y=0, z=5000))


class TestCableSection:
    """索截面测试"""

    def test_create_cable_section(self, app):
        ret = app.create_object(CableSection(name="CAB1", material="Q355", area=500.0))
        assert ret in (0, -1)


class TestCableCreate:
    """索单元创建测试"""

    def test_create_cable(self, app, cable_points):
        ret = app.create_object(Cable(no="C1", start_point="101", end_point="102", section="CAB1"))
        assert ret in (0, -1)


class TestCableQuery:
    """索单元查询测试"""

    def test_get_cable(self, app):
        c = app.get_object(Cable(no="C1"))
        assert c.start_point is not None
        assert c.end_point is not None
        assert c.section is not None

    def test_get_name_list(self, model):
        names = Cable.get_name_list(model)
        assert isinstance(names, list)
        assert len(names) > 0

    def test_get_count(self, model):
        count = Cable.get_count(model)
        assert count > 0

    def test_get_section_name_list(self, model):
        names = Cable.get_section_name_list(model)
        assert isinstance(names, list)
        assert "CAB1" in names

    def test_cable_length(self, app):
        c = app.get_object(Cable(no="C1"))
        assert c.length is not None
        assert c.length > 0


class TestCableUpdate:
    """索单元更新测试"""

    def test_update_cable_section(self, app):
        ret = app.update_object(Cable(no="C1", section="CAB1"))
        assert ret == 0
