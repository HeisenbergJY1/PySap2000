# -*- coding: utf-8 -*-
"""Tests for file helpers."""

import pytest
from PySap2000.file import save, Units

pytestmark = pytest.mark.file


class TestFileOperations:
    """Save and related helpers."""

    def test_save(self, model):
        # Save to current path
        ret = save(model)
        assert ret == 0

    def test_units_enum(self):
        assert Units.N_MM_C == 9
        assert Units.KN_M_C == 6
        assert Units.KN_MM_C == 5
