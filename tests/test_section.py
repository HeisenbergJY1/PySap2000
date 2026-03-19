# -*- coding: utf-8 -*-
"""截面定义相关测试"""

import pytest
from PySap2000.section import (
    FrameSection, FrameSectionType,
    CableSection,
    AreaSection, AreaSectionType, ShellType,
    LinkSection, LinkSectionType,
)

pytestmark = pytest.mark.section


class TestFrameSection:
    """框架截面测试"""

    def test_create_rect_section(self, app):
        sec = FrameSection(
            name="TestRect",
            material="Q355",
            property_type=FrameSectionType.RECTANGULAR,
            height=400,
            width=200,
        )
        ret = app.create_object(sec)
        assert ret in (0, -1)

    def test_get_name_list(self, model):
        names = FrameSection.get_name_list(model)
        assert isinstance(names, list)
        assert len(names) > 0

    def test_get_count(self, model):
        count = FrameSection.get_count(model)
        assert count > 0

    def test_get_by_name(self, model):
        sec = FrameSection.get_by_name(model, "W14X30")
        assert sec is not None
        assert sec.name == "W14X30"


class TestCableSection:
    """索截面测试"""

    def test_create_cable_section(self, app):
        sec = CableSection(name="TestCAB", material="Q355", area=300.0)
        ret = app.create_object(sec)
        assert ret in (0, -1)

    def test_get_name_list(self, model):
        names = CableSection.get_name_list(model)
        assert isinstance(names, list)
        assert "CAB1" in names or "TestCAB" in names


class TestAreaSection:
    """面截面测试"""

    def test_create_shell_section(self, app):
        sec = AreaSection(
            name="TestShell",
            material="Q355",
            shell_type=ShellType.SHELL_THIN,
            membrane_thickness=10.0,
        )
        ret = app.create_object(sec)
        assert ret in (0, -1)

    def test_get_name_list(self, model):
        names = AreaSection.get_name_list(model)
        assert isinstance(names, list)
        assert len(names) > 0


class TestLinkSection:
    """连接截面测试"""

    def test_create_linear_section(self, app):
        sec = LinkSection(
            name="TestLink",
            section_type=LinkSectionType.LINEAR,
            dof=[True, False, False, False, False, False],
            stiffness=[1000.0, 0, 0, 0, 0, 0],
        )
        ret = app.create_object(sec)
        assert ret in (0, -1)

    def test_get_name_list(self, model):
        names = LinkSection.get_name_list(model)
        assert isinstance(names, list)
        assert len(names) > 0
