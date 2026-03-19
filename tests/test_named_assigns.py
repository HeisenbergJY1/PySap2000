# -*- coding: utf-8 -*-
"""命名赋值定义测试 (NamedAssign)"""

import pytest
from PySap2000.named_assigns import (
    NamedFrameModifier,
    NamedFrameRelease,
    NamedAreaModifier,
    NamedCableModifier,
)

pytestmark = pytest.mark.named_assigns


class TestNamedFrameModifier:
    """杆件修改器测试"""

    def test_create(self, model):
        mod = NamedFrameModifier(name="TestFMod", area=0.8, inertia_33=0.5)
        ret = mod._create(model)
        assert ret == 0

    def test_get_count(self, model):
        count = NamedFrameModifier.get_count(model)
        assert count >= 1

    def test_get_name_list(self, model):
        names = NamedFrameModifier.get_name_list(model)
        assert "TestFMod" in names

    def test_get_by_name(self, model):
        mod = NamedFrameModifier.get_by_name(model, "TestFMod")
        assert mod is not None
        assert mod.name == "TestFMod"
        assert abs(mod.area - 0.8) < 0.01
        assert abs(mod.inertia_33 - 0.5) < 0.01

    def test_change_name(self, model):
        mod = NamedFrameModifier(name="TestFMod")
        ret = mod.change_name(model, "TestFMod_R")
        assert ret == 0
        assert mod.name == "TestFMod_R"
        # 改回来
        mod.change_name(model, "TestFMod")

    def test_to_list_from_list(self):
        mod = NamedFrameModifier(name="X", area=0.5, shear_2=0.6, shear_3=0.7,
                                  torsion=0.8, inertia_22=0.9, inertia_33=1.0,
                                  mass=1.1, weight=1.2)
        lst = mod.to_list()
        assert len(lst) == 8
        mod2 = NamedFrameModifier.from_list("X", lst)
        assert abs(mod2.area - 0.5) < 0.001

    def test_delete(self, model):
        tmp = NamedFrameModifier(name="TmpFMod")
        tmp._create(model)
        ret = tmp._delete(model)
        assert ret == 0


class TestNamedFrameRelease:
    """杆件端部释放测试"""

    def test_create_pinned_both(self, model):
        rel = NamedFrameRelease.create_pinned_both("TestRelease")
        assert rel.ii[4] is True  # R2
        assert rel.ii[5] is True  # R3
        assert rel.jj[4] is True
        assert rel.jj[5] is True
        ret = rel._create(model)
        assert ret == 0

    def test_get_count(self, model):
        count = NamedFrameRelease.get_count(model)
        assert count >= 1

    def test_get_name_list(self, model):
        names = NamedFrameRelease.get_name_list(model)
        assert "TestRelease" in names

    def test_get_by_name(self, model):
        rel = NamedFrameRelease.get_by_name(model, "TestRelease")
        assert rel is not None
        assert rel.name == "TestRelease"
        # 验证铰接设置
        assert rel.ii[4] is True or rel.ii[4] == True
        assert rel.jj[4] is True or rel.jj[4] == True

    def test_convenience_properties(self):
        rel = NamedFrameRelease(name="X")
        rel.i_r3 = True
        assert rel.ii[5] is True
        rel.j_u1 = True
        assert rel.jj[0] is True

    def test_delete(self, model):
        tmp = NamedFrameRelease(name="TmpRelease")
        tmp._create(model)
        ret = tmp._delete(model)
        assert ret == 0
