# -*- coding: utf-8 -*-
"""Tests for the Application connection manager."""

import pytest
from PySap2000 import Application
from PySap2000.exceptions import ObjectError

pytestmark = pytest.mark.application


class TestApplicationConnection:
    """Connection and basic info."""

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
    """Model metadata."""

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
    """Modification mode."""

    def test_begin_finish_modification(self, app):
        app.begin_modification()
        assert app._in_modification is True
        app.finish_modification()
        assert app._in_modification is False

    def test_refresh_view(self, app):
        # Should not raise
        app.refresh_view()


class TestApplicationUserComment:
    """User comment."""

    def test_set_user_comment(self, app):
        ret = app.set_user_comment("PySap2000 test run", replace=True)
        assert ret == 0

    def test_get_user_comment(self, app):
        comment = app.get_user_comment()
        assert isinstance(comment, str)


class TestApplicationBulkGet:
    """Bulk retrieval dispatch."""

    @staticmethod
    def _make_app():
        app = Application.__new__(Application)
        app._model = object()
        return app

    def test_get_object_list_uses_name_filtered_get_all(self):
        class NameFiltered:
            calls = []

            @classmethod
            def get_all(cls, model, names=None):
                cls.calls.append((model, names))
                return ["ok"]

        app = self._make_app()
        result = app.get_object_list(NameFiltered, ["1", "2"])

        assert result == ["ok"]
        assert NameFiltered.calls == [(app._model, ["1", "2"])]

    def test_get_object_list_uses_name_filtered__get_all(self):
        class LegacyNameFiltered:
            calls = []

            @classmethod
            def _get_all(cls, model, nos=None):
                cls.calls.append((model, nos))
                return ["legacy"]

        app = self._make_app()
        result = app.get_object_list(LegacyNameFiltered, ["3"])

        assert result == ["legacy"]
        assert LegacyNameFiltered.calls == [(app._model, ["3"])]

    def test_get_object_list_rejects_non_name_filtered_get_all(self):
        class EnumFiltered:
            calls = []

            @classmethod
            def get_all(cls, model, prop_type=None):
                cls.calls.append((model, prop_type))
                return ["unexpected"]

        app = self._make_app()

        with pytest.raises(ObjectError, match="does not support filtered bulk retrieval"):
            app.get_object_list(EnumFiltered, ["DECK"])

        assert EnumFiltered.calls == []

    def test_get_object_list_still_supports_unfiltered_get_all(self):
        class EnumFiltered:
            calls = []

            @classmethod
            def get_all(cls, model, prop_type=None):
                cls.calls.append((model, prop_type))
                return ["all"]

        app = self._make_app()
        result = app.get_object_list(EnumFiltered)

        assert result == ["all"]
        assert EnumFiltered.calls == [(app._model, None)]
