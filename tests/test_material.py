# -*- coding: utf-8 -*-
"""Tests for material properties."""

import pytest
from PySap2000.structure_core import Material, MaterialType, MaterialSymmetryType

pytestmark = pytest.mark.material


class TestMaterialCreate:
    """Create materials."""

    def test_create_steel(self, app):
        steel = Material(
            name="TestSteel",
            type=MaterialType.STEEL,
            symmetry_type=MaterialSymmetryType.ISOTROPIC,
            e=2.06e5,   # N/mm²
            u=0.3,
            a=1.2e-5,
            w=7.698e-5, # N/mm³
        )
        ret = app.create_object(steel)
        assert ret in (0, -1)

    def test_create_concrete(self, app):
        concrete = Material(
            name="TestC30",
            type=MaterialType.CONCRETE,
            symmetry_type=MaterialSymmetryType.ISOTROPIC,
            e=3.0e4,
            u=0.2,
            a=1.0e-5,
            w=2.5e-5,
        )
        ret = app.create_object(concrete)
        assert ret in (0, -1)


class TestMaterialQuery:
    """Query materials."""

    def test_get_by_name(self, model):
        mat = Material.get_by_name(model, "Q355")
        assert mat.name == "Q355"
        assert mat.e > 0

    def test_get_all(self, model):
        materials = Material.get_all(model)
        assert isinstance(materials, list)
        assert len(materials) > 0

    def test_get_name_list(self, model):
        names = Material.get_name_list(model)
        assert isinstance(names, list)
        assert len(names) > 0
        assert "Q355" in names

    def test_get_count(self, model):
        count = Material.get_count(model)
        assert count > 0

    def test_get_count_by_type(self, model):
        count = Material.get_count(model, MaterialType.STEEL)
        assert count >= 1

    def test_material_properties(self, model):
        mat = Material.get_by_name(model, "Q355")
        assert mat.elastic_modulus > 0
        assert 0 < mat.poisson_ratio < 0.5


class TestMaterialUpdate:
    """Update materials."""

    def test_set_isotropic(self, model):
        mat = Material.get_by_name(model, "TestSteel")
        ret = mat.set_isotropic(model, e=2.1e5, u=0.3, a=1.2e-5)
        assert ret == 0

    def test_rename_material(self, app):
        ret = app.rename_object(Material(name="TestSteel"), "TestSteel2")
        assert ret == 0

    def test_rename_back(self, app):
        ret = app.rename_object(Material(name="TestSteel2"), "TestSteel")
        assert ret == 0
