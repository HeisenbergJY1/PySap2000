# -*- coding: utf-8 -*-
"""全局参数测试 (Units, ModelSettings, ProjectInfo)"""

import pytest
from PySap2000.global_parameters import (
    Units,
    UnitSystem,
    ModelSettings,
    ActiveDOF,
    ProjectInfo,
)
from PySap2000.global_parameters.model_settings import DOFState, DOF_PRESETS
from PySap2000.global_parameters.units import UNIT_DESCRIPTIONS

pytestmark = pytest.mark.global_parameters


class TestUnits:
    """单位系统测试"""

    def test_get_present_units(self, model):
        units = Units.get_present_units(model)
        assert isinstance(units, UnitSystem)

    def test_set_and_restore_units(self, model):
        original = Units.get_present_units(model)
        # 切换到 kN-m
        ret = Units.set_present_units(model, UnitSystem.KN_M_C)
        assert ret == 0
        current = Units.get_present_units(model)
        assert current == UnitSystem.KN_M_C
        # 恢复
        Units.set_present_units(model, original)

    def test_get_database_units(self, model):
        units = Units.get_database_units(model)
        assert isinstance(units, UnitSystem)

    def test_get_unit_description(self):
        desc = Units.get_unit_description(UnitSystem.KN_M_C)
        assert desc == "kN-m-C"

    def test_get_force_unit(self):
        assert Units.get_force_unit(UnitSystem.KN_M_C) == "kN"
        assert Units.get_force_unit(UnitSystem.N_MM_C) == "N"

    def test_get_length_unit(self):
        assert Units.get_length_unit(UnitSystem.KN_M_C) == "m"
        assert Units.get_length_unit(UnitSystem.N_MM_C) == "mm"

    def test_get_temp_unit(self):
        assert Units.get_temp_unit(UnitSystem.KN_M_C) == "°C"
        assert Units.get_temp_unit(UnitSystem.KIP_FT_F) == "°F"


class TestModelSettings:
    """模型设置测试"""

    def test_get_active_dof(self, model):
        dof = ModelSettings.get_active_dof(model)
        assert isinstance(dof, DOFState)

    def test_set_active_dof_preset(self, model):
        # 保存原始
        original = ModelSettings.get_active_dof(model)
        # 设置 XZ 平面
        ret = ModelSettings.set_active_dof(model, ActiveDOF.XZ_PLANE)
        assert ret == 0
        dof = ModelSettings.get_active_dof(model)
        assert dof.ux is True
        assert dof.uy is False
        assert dof.uz is True
        # 恢复
        ModelSettings.set_active_dof(model, custom_dof=original.to_tuple())

    def test_set_3d_full(self, model):
        original = ModelSettings.get_active_dof(model)
        ret = ModelSettings.set_3d_full(model)
        assert ret == 0
        dof = ModelSettings.get_active_dof(model)
        assert all([dof.ux, dof.uy, dof.uz, dof.rx, dof.ry, dof.rz])
        # 恢复
        ModelSettings.set_active_dof(model, custom_dof=original.to_tuple())

    def test_get_merge_tolerance(self, model):
        tol = ModelSettings.get_merge_tolerance(model)
        assert isinstance(tol, float)
        assert tol >= 0

    def test_get_present_coord_system(self, model):
        csys = ModelSettings.get_present_coord_system(model)
        assert isinstance(csys, str)
        assert len(csys) > 0

    def test_model_lock_unlock(self, model):
        # 确保解锁
        ModelSettings.unlock_model(model)
        assert ModelSettings.is_model_locked(model) is False

    def test_get_model_filename(self, model):
        filename = ModelSettings.get_model_filename(model)
        assert isinstance(filename, str)


class TestProjectInfo:
    """项目信息测试"""

    def test_get_all(self, model):
        info = ProjectInfo.get_all(model)
        assert isinstance(info, ProjectInfo)

    def test_set_and_get_item(self, model):
        ret = ProjectInfo.set_item(model, "Engineer", "TestEngineer")
        assert ret == 0
        val = ProjectInfo.get_item(model, "Engineer")
        assert val == "TestEngineer"

    def test_user_comment(self, model):
        ret = ProjectInfo.set_user_comment(model, "PySap2000 test")
        assert ret == 0
        comment = ProjectInfo.get_user_comment(model)
        assert "PySap2000 test" in comment


class TestDOFState:
    """DOFState 纯数据类测试（不需要 SAP2000）"""

    def test_to_tuple(self):
        dof = DOFState(ux=True, uy=False, uz=True, rx=False, ry=True, rz=False)
        assert dof.to_tuple() == (True, False, True, False, True, False)

    def test_from_tuple(self):
        dof = DOFState.from_tuple((True, False, True, False, True, False))
        assert dof.ux is True
        assert dof.uy is False

    def test_from_preset(self):
        dof = DOFState.from_preset(ActiveDOF.XZ_PLANE)
        assert dof.ux is True
        assert dof.uy is False
        assert dof.uz is True
        assert dof.ry is True
