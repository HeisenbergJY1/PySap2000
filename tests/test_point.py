# -*- coding: utf-8 -*-
"""节点相关测试"""

import pytest
from PySap2000.structure_core import Point
from PySap2000.point import (
    set_point_support, get_point_restraint, get_point_support_type,
    delete_point_restraint, PointSupportType,
    set_point_restraint,
)

pytestmark = pytest.mark.point


class TestPointCreate:
    """节点创建测试"""

    def test_create_single_point(self, app):
        ret = app.create_object(Point(no=10, x=0, y=0, z=0))
        assert ret in (0, -1)

    def test_create_multiple_points(self, app):
        points = [
            Point(no=2, x=10, y=0, z=0),
            Point(no=3, x=10, y=0, z=10),
            Point(no=4, x=0, y=0, z=10),
            Point(no=5, x=5, y=5, z=0),
        ]
        for p in points:
            ret = app.create_object(p)
            assert ret in (0, -1)


class TestPointQuery:
    """节点查询测试"""

    def test_get_point(self, app):
        p = app.get_object(Point(no="10"))
        assert p.x == 0.0
        assert p.y == 0.0
        assert p.z == 0.0

    def test_get_by_name(self, model):
        p = Point.get_by_name(model, "2")
        assert p.x == 10.0
        assert p.y == 0.0
        assert p.z == 0.0

    def test_get_all(self, model):
        points = Point.get_all(model)
        assert isinstance(points, list)
        assert len(points) > 0
        assert all(isinstance(p, Point) for p in points)

    def test_get_name_list(self, model):
        names = Point.get_name_list(model)
        assert isinstance(names, list)
        assert len(names) > 0
        assert "10" in names

    def test_get_count(self, model):
        count = Point.get_count(model)
        assert count >= 4

    def test_get_connectivity(self, model):
        """测试节点连接信息（需要先创建了连接到该节点的单元）"""
        p = Point(no="10")
        conn = p.get_connectivity(model)
        assert isinstance(conn, dict)
        assert "num_items" in conn


class TestPointSupport:
    """节点支座测试"""

    def test_set_fixed_support(self, model):
        ret = set_point_support(model, "10", PointSupportType.FIXED)
        assert ret == 0

    def test_get_restraint(self, model):
        restraints = get_point_restraint(model, "10")
        assert restraints is not None
        # 固定支座: 全部约束
        assert all(r is True for r in restraints)

    def test_get_support_type(self, model):
        support_type = get_point_support_type(model, "10")
        assert support_type == PointSupportType.FIXED

    def test_set_hinged_support(self, model):
        ret = set_point_support(model, "2", PointSupportType.HINGED)
        assert ret == 0

    def test_set_custom_restraint(self, model):
        ret = set_point_restraint(model, "3", (True, True, True, False, False, False))
        assert ret == 0

    def test_delete_restraint(self, model):
        ret = delete_point_restraint(model, "3")
        assert ret == 0


class TestPointRename:
    """节点重命名测试"""

    def test_rename_point(self, app):
        ret = app.rename_object(Point(no="5"), "P5")
        assert ret == 0

    def test_get_renamed_point(self, model):
        p = Point.get_by_name(model, "P5")
        assert p.x == 5.0
        assert p.y == 5.0

    def test_rename_back(self, app):
        """恢复原名，避免影响后续测试"""
        ret = app.rename_object(Point(no="P5"), "5")
        assert ret == 0
