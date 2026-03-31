# -*- coding: utf-8 -*-
"""Tests for analysis control."""

import pytest
from PySap2000.analyze import (
    create_analysis_model,
    get_active_dof,
    set_active_dof,
    get_case_status,
    get_run_case_flag,
    set_run_case_flag,
    set_run_case_flag_all,
    get_solver_option,
    set_solver_option,
    delete_all_results,
    ActiveDOF,
    SolverOption,
    CaseStatus,
)

pytestmark = pytest.mark.analyze


class TestActiveDOF:
    """Active degrees of freedom."""

    def test_get_active_dof(self, model):
        dof = get_active_dof(model)
        assert dof is not None
        assert isinstance(dof.ux, bool)
        assert isinstance(dof.uz, bool)

    def test_set_active_dof(self, model):
        # Save current DOF
        original = get_active_dof(model)
        # Enable all DOFs
        dof = ActiveDOF(ux=True, uy=True, uz=True, rx=True, ry=True, rz=True)
        ret = set_active_dof(model, dof)
        assert ret == 0
        # Verify
        current = get_active_dof(model)
        assert current.ux is True
        assert current.rz is True
        # Restore
        if original:
            set_active_dof(model, original)


class TestCaseControl:
    """Load case run flags."""

    def test_get_case_status(self, model):
        statuses = get_case_status(model)
        assert isinstance(statuses, list)
        assert len(statuses) > 0
        assert statuses[0].name != ""

    def test_get_run_case_flag(self, model):
        flags = get_run_case_flag(model)
        assert isinstance(flags, list)
        assert len(flags) > 0

    def test_set_run_case_flag(self, model):
        flags = get_run_case_flag(model)
        if flags:
            name = flags[0].name
            original_run = flags[0].run
            ret = set_run_case_flag(model, name, not original_run)
            assert ret == 0
            # Restore
            set_run_case_flag(model, name, original_run)

    def test_set_run_case_flag_all(self, model):
        ret = set_run_case_flag_all(model, True)
        assert ret == 0


class TestSolverOption:
    """Solver options."""

    def test_get_solver_option(self, model):
        opt = get_solver_option(model)
        assert opt is not None
        assert isinstance(opt, SolverOption)

    def test_set_solver_option(self, model):
        opt = get_solver_option(model)
        if opt:
            ret = set_solver_option(model, opt)
            assert ret == 0


class TestAnalysisModel:
    """Analysis model and results cleanup."""

    def test_create_analysis_model(self, model):
        ret = create_analysis_model(model)
        assert ret == 0

    def test_delete_all_results(self, model):
        ret = delete_all_results(model)
        assert ret == 0
