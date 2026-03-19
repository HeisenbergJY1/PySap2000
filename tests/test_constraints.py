# -*- coding: utf-8 -*-
"""约束相关测试"""

import pytest
from PySap2000.constraints import (
    get_constraint_count,
    get_constraint_name_list,
    get_constraint_type,
    change_constraint_name,
    delete_constraint,
    set_diaphragm,
    get_diaphragm,
    set_body,
    get_body,
    set_equal,
    get_equal,
)
from PySap2000.constraints.enums import ConstraintType, ConstraintAxis

pytestmark = pytest.mark.constraints


class TestConstraintCreate:
    """约束创建测试"""

    def test_create_diaphragm(self, model):
        ret = set_diaphragm(model, "TestDiaph", ConstraintAxis.Z)
        assert ret is True

    def test_create_body(self, model):
        ret = set_body(model, "TestBody")
        assert ret is True

    def test_create_equal(self, model):
        ret = set_equal(model, "TestEqual")
        assert ret is True
        # 验证约束确实存在
        names = get_constraint_name_list(model)
        assert "TestEqual" in names


class TestConstraintQuery:
    """约束查询测试"""

    def test_get_count(self, model):
        count = get_constraint_count(model)
        assert count >= 3

    def test_get_name_list(self, model):
        names = get_constraint_name_list(model)
        assert isinstance(names, list)
        assert "TestDiaph" in names

    def test_get_type_diaphragm(self, model):
        ct = get_constraint_type(model, "TestDiaph")
        assert ct == ConstraintType.DIAPHRAGM

    def test_get_type_body(self, model):
        ct = get_constraint_type(model, "TestBody")
        assert ct == ConstraintType.BODY

    def test_get_diaphragm(self, model):
        info = get_diaphragm(model, "TestDiaph")
        assert info is not None

    def test_get_body(self, model):
        info = get_body(model, "TestBody")
        assert info is not None

    def test_get_equal(self, model):
        # 先确认约束存在
        names = get_constraint_name_list(model)
        assert "TestEqual" in names
        ct = get_constraint_type(model, "TestEqual")
        assert ct == ConstraintType.EQUAL
        # 获取详情
        info = get_equal(model, "TestEqual")
        assert info is not None


class TestConstraintUpdate:
    """约束更新测试"""

    def test_rename_constraint(self, model):
        ret = change_constraint_name(model, "TestEqual", "TestEqual2")
        assert ret is True
        # 改回来
        change_constraint_name(model, "TestEqual2", "TestEqual")

    def test_delete_constraint(self, model):
        # 创建一个临时约束再删除
        set_diaphragm(model, "TempDiaph")
        ret = delete_constraint(model, "TempDiaph")
        assert ret is True
