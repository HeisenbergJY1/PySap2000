# -*- coding: utf-8 -*-
"""数据库表格相关测试"""

import pytest
from PySap2000.database_tables import DatabaseTables, TableData

pytestmark = pytest.mark.database_tables


class TestTableQuery:
    """表格查询测试"""

    def test_get_available_tables(self, model):
        tables = DatabaseTables.get_available_tables(model)
        assert isinstance(tables, list)
        assert len(tables) > 0

    def test_get_all_tables(self, model):
        tables = DatabaseTables.get_all_tables(model)
        assert isinstance(tables, list)
        assert len(tables) > 0

    def test_find_tables(self, model):
        tables = DatabaseTables.find_tables(model, "Joint")
        assert isinstance(tables, list)
        assert len(tables) > 0

    def test_get_fields_in_table(self, model):
        fields = DatabaseTables.get_fields_in_table(model, "Joint Coordinates")
        assert isinstance(fields, list)
        assert len(fields) > 0


class TestTableRead:
    """表格读取测试"""

    def test_get_table_for_display(self, model):
        data = DatabaseTables.get_table_for_display(model, "Joint Coordinates")
        assert data is not None
        assert isinstance(data, TableData)

    def test_read_table(self, model):
        data = DatabaseTables.read_table(model, "Joint Coordinates")
        assert data is not None

    def test_get_table_for_editing(self, model):
        data = DatabaseTables.get_table_for_editing(model, "Joint Coordinates")
        assert data is not None
        assert isinstance(data, TableData)
