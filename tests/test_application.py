# -*- coding: utf-8 -*-
"""Application 连接管理器测试"""

import pytest

pytestmark = pytest.mark.application


class TestApplicationConnection:
    """连接和基本信息测试"""

    def test_model_not_none(self, app):
        assert app.model is not None

    def test_get_version(self, app):
        version = app.get_version()
        assert isinstance(version, tuple)
        assert len(version) == 2
        assert version[0] != ""

    def test_get_units(self, app):
        units = app.get_units()
        assert isinstance(units, int)
        assert units > 0

    def test_get_units_name(self, app):
        name = app.get_units_name()
        assert name != "Unknown"
        assert name == "N_mm_C"

    def test_get_model_filename(self, app):
        filename = app.get_model_filename()
        assert isinstance(filename, str)

    def test_get_database_units(self, app):
        db_units = app.get_database_units()
        assert isinstance(db_units, int)
        assert db_units > 0


class TestApplicationModelInfo:
    """模型信息测试"""

    def test_get_project_info(self, app):
        info = app.get_project_info()
        assert isinstance(info, dict)

    def test_set_project_info(self, app):
        ret = app.set_project_info("Project Name", "PySap2000 Test")
        assert ret == 0

    def test_get_present_coord_system(self, app):
        csys = app.get_present_coord_system()
        assert csys == "Global"

    def test_get_merge_tol(self, app):
        tol = app.get_merge_tol()
        assert isinstance(tol, float)
        assert tol > 0

    def test_model_lock_status(self, app):
        locked = app.get_model_is_locked()
        assert isinstance(locked, bool)


class TestApplicationModification:
    """修改模式测试"""

    def test_begin_finish_modification(self, app):
        app.begin_modification()
        assert app._in_modification is True
        app.finish_modification()
        assert app._in_modification is False

    def test_refresh_view(self, app):
        # 不应抛异常
        app.refresh_view()


class TestApplicationUserComment:
    """用户注释测试"""

    def test_set_user_comment(self, app):
        ret = app.set_user_comment("PySap2000 test run", replace=True)
        assert ret == 0

    def test_get_user_comment(self, app):
        comment = app.get_user_comment()
        assert isinstance(comment, str)
