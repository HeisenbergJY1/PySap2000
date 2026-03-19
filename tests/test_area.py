# -*- coding: utf-8 -*-
"""面单元相关测试"""

import pytest
from PySap2000.structure_core import Area
from PySap2000.section import AreaSection, AreaSectionType, ShellType, AreaModifiers

pytestmark = pytest.mark.area


class TestAreaSection:
    """面截面测试"""

    def test_create_shell_section(self, app):
        ret = app.create_object(AreaSection(
            name="SLAB200",
            material="Q355",
            prop_type=AreaSectionType.SHELL,
            shell_type=ShellType.SHELL_THIN,
            membrane_thickness=200.0,
        ))
        assert ret in (0, -1)

    def test_get_section_by_name(self, model):
        sec = AreaSection.get_by_name(model, "SLAB200")
        assert sec.name == "SLAB200"
        assert sec.membrane_thickness == 200.0

    def test_get_section_name_list(self, model):
        names = AreaSection.get_name_list(model)
        assert isinstance(names, list)
        assert "SLAB200" in names

    def test_get_section_count(self, model):
        count = AreaSection.get_count(model)
        assert count > 0


class TestAreaCreate:
    """面单元创建测试"""

    def test_create_area_by_points(self, app):
        ret = app.create_object(Area(no=1, points=["10", "2", "3"], section="SLAB200"))
        assert ret in (0, -1)

    def test_create_area_4_points(self, app):
        ret = app.create_object(Area(no=2, points=["10", "2", "3", "4"], section="SLAB200"))
        assert ret in (0, -1)


class TestAreaQuery:
    """面单元查询测试"""

    def test_get_area(self, app):
        a = app.get_object(Area(no="1"))
        assert a.points is not None
        assert len(a.points) >= 3

    def test_get_area_property(self, app):
        a = app.get_object(Area(no="1"))
        assert a.section is not None

    def test_get_by_name(self, model):
        a = Area.get_by_name(model, "1")
        assert a.points is not None
        assert a.section != ""

    def test_get_all(self, model):
        areas = Area.get_all(model)
        assert isinstance(areas, list)
        assert len(areas) > 0

    def test_get_name_list(self, model):
        names = Area.get_name_list(model)
        assert isinstance(names, list)
        assert len(names) > 0

    def test_get_count(self, model):
        count = Area.get_count(model)
        assert count > 0

    def test_get_section_name_list(self, model):
        names = Area.get_section_name_list(model)
        assert isinstance(names, list)
        assert "SLAB200" in names

    def test_get_local_axes(self, model):
        a = Area(no="1")
        result = a.get_local_axes(model)
        assert result is not None

    def test_get_transformation_matrix(self, model):
        a = Area(no="1")
        matrix = a.get_transformation_matrix(model)
        assert matrix is not None
        assert len(matrix) == 9


class TestAreaUpdate:
    """面单元更新测试"""

    def test_update_area_section(self, app):
        ret = app.update_object(Area(no="1", section="SLAB200"))
        assert ret == 0

    def test_set_local_axes(self, model):
        a = Area(no="1")
        ret = a.set_local_axes(model, 30.0)
        assert ret == 0

    def test_reset_local_axes(self, model):
        a = Area(no="1")
        ret = a.set_local_axes(model, 0.0)
        assert ret == 0
