# -*- coding: utf-8 -*-
"""Tests for frame objects."""

import pytest
from PySap2000.structure_core import Frame
from PySap2000.section import FrameSection, FrameSectionType

pytestmark = pytest.mark.frame


class TestFrameSection:
    """Frame sections."""

    def test_create_frame_section(self, app):
        sec = FrameSection(
            name="W14X30",
            material="Q355",
            property_type=FrameSectionType.I_SECTION,
            height=353.1,
            width=171.5,
            flange_thickness=13.8,
            web_thickness=8.5,
        )
        ret = app.create_object(sec)
        assert ret in (0, -1)


class TestFrameCreate:
    """Create frames."""

    def test_create_frame(self, app):
        ret = app.create_object(Frame(no=1, start_point=10, end_point=3, section="W14X30"))
        assert ret in (0, -1)


class TestFrameQuery:
    """Query frames."""

    def test_get_frame(self, app):
        f = app.get_object(Frame(no="1"))
        assert f.start_point is not None
        assert f.end_point is not None
        assert f.section is not None

    def test_get_by_name(self, model):
        f = Frame.get_by_name(model, "1")
        assert f.section != ""

    def test_get_name_list(self, model):
        names = Frame.get_name_list(model)
        assert isinstance(names, list)
        assert len(names) > 0

    def test_get_count(self, model):
        count = Frame.get_count(model)
        assert count > 0

    def test_get_section_name_list(self, model):
        names = Frame.get_section_name_list(model)
        assert isinstance(names, list)
        assert "W14X30" in names

    def test_frame_length(self, model):
        f = Frame.get_by_name(model, "1")
        assert f.length is not None
        assert f.length > 0


class TestFrameUpdate:
    """Update frames."""

    def test_rename_frame(self, app):
        ret = app.rename_object(Frame(no="1"), "F2")
        assert ret == 0

    def test_update_frame_section(self, app):
        frame = Frame(no="F2", section="W14X30")
        ret = app.update_object(frame)
        assert ret == 0

    def test_rename_back(self, app):
        """Restore original name."""
        ret = app.rename_object(Frame(no="F2"), "1")
        assert ret == 0
