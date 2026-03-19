# -*- coding: utf-8 -*-
"""连接单元相关测试"""

import pytest
from PySap2000.structure_core import Link
from PySap2000.section import LinkSection, LinkSectionType

pytestmark = pytest.mark.link


class TestLinkSection:
    """连接属性测试"""

    def test_create_linear_section(self, app):
        ret = app.create_object(LinkSection(
            name="Linear1",
            section_type=LinkSectionType.LINEAR,
            dof=[True, False, False, False, False, False],
            stiffness=[1000.0, 0, 0, 0, 0, 0],
        ))
        assert ret in (0, -1)

    def test_get_section_by_name(self, model):
        sec = LinkSection.get_by_name(model, "Linear1")
        assert sec.name == "Linear1"
        assert sec.section_type == LinkSectionType.LINEAR

    def test_get_section_name_list(self, model):
        names = LinkSection.get_name_list(model)
        assert isinstance(names, list)
        assert "Linear1" in names

    def test_get_section_count(self, model):
        count = LinkSection.get_count(model)
        assert count > 0


class TestLinkCreate:
    """连接单元创建测试"""

    def test_create_two_joint_link(self, app):
        ret = app.create_object(Link(no=1, start_point="3", end_point="4", property_name="Linear1"))
        assert ret in (0, -1)

    def test_create_single_joint_link(self, app):
        ret = app.create_object(Link(no=2, start_point="3", is_single_joint=True))
        assert ret in (0, -1)


class TestLinkQuery:
    """连接单元查询测试"""

    def test_get_link(self, app):
        lk = app.get_object(Link(no="1"))
        assert lk.start_point is not None
        assert lk.property_name is not None

    def test_get_single_joint_link(self, app):
        lk = app.get_object(Link(no="2"))
        assert lk.is_single_joint is True

    def test_get_by_name(self, model):
        lk = Link.get_by_name(model, "1")
        assert lk.property_name != ""

    def test_get_all(self, model):
        links = Link.get_all(model)
        assert isinstance(links, list)
        assert len(links) > 0

    def test_get_name_list(self, model):
        names = Link.get_name_list(model)
        assert isinstance(names, list)
        assert len(names) > 0

    def test_get_count(self, model):
        count = Link.get_count(model)
        assert count > 0

    def test_get_property_name_list(self, model):
        names = Link.get_property_name_list(model)
        assert isinstance(names, list)
        assert "Linear1" in names

    def test_get_local_axes(self, model):
        lk = Link(no="1")
        angle, advanced = lk.get_local_axes(model)
        assert isinstance(angle, float)

    def test_get_transformation_matrix(self, model):
        lk = Link(no="1")
        matrix = lk.get_transformation_matrix(model)
        assert isinstance(matrix, list)
        assert len(matrix) == 9


class TestLinkUpdate:
    """连接单元更新测试"""

    def test_update_link_property(self, app):
        ret = app.update_object(Link(no="1", property_name="Linear1"))
        assert ret == 0

    def test_set_local_axes(self, model):
        lk = Link(no="1")
        ret = lk.set_local_axes(model, 45.0)
        assert ret == 0

    def test_reset_local_axes(self, model):
        lk = Link(no="1")
        ret = lk.set_local_axes(model, 0.0)
        assert ret == 0
