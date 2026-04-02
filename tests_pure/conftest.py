# -*- coding: utf-8 -*-
"""Pytest bootstrap for pure Python tests that must not touch SAP2000."""

import os
import sys


_TESTS_PURE_DIR = os.path.dirname(os.path.abspath(__file__))
_PACKAGE_DIR = os.path.dirname(_TESTS_PURE_DIR)
_PARENT_DIR = os.path.dirname(_PACKAGE_DIR)

if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)
