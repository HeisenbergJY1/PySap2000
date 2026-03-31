# -*- coding: utf-8 -*-
"""
conftest.py - pytest shared fixtures

Usage:
    pytest tests/                          # run all
    pytest tests/test_point.py             # run point only
    pytest tests/ -m point                 # by marker
    pytest tests/ -k "test_create"         # by name
    pytest tests/ -v                       # verbose
"""

import sys
import os
import pytest

# Project layout:
#   mysite_spancore/
#     PySap2000/          <-- _pkg_dir  (bare imports like 'from frame.enums')
#       tests/
#         conftest.py     <-- this file
#       __init__.py
#       structure_core/
#       frame/
#       ...

_pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_parent_dir = os.path.dirname(_pkg_dir)

# Add parent so 'from PySap2000 import ...' works
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# Add pkg dir so bare 'from frame.enums import ...' works
if _pkg_dir not in sys.path:
    sys.path.insert(0, _pkg_dir)

from PySap2000 import Application
from PySap2000.global_parameters import Units, UnitSystem
from PySap2000.structure_core import Point


@pytest.fixture(scope="session")
def app():
    """
    Session-scoped SAP2000 connection.
    Connects once, shared by all tests.
    """
    with Application() as _app:
        Units.set_present_units(_app.model, UnitSystem.N_MM_C)
        yield _app


@pytest.fixture(scope="session")
def model(app):
    """Quick access to SapModel"""
    return app.model


@pytest.fixture(scope="session", autouse=True)
def ensure_base_points(app):
    """
    Ensure base joints exist before any tests run.

    Several test modules (area, cable, frame) depend on these points, but
    test_point.py runs later alphabetically. Create them here; `_create`
    skips existing points (returns -1).
    """
    base_points = [
        Point(no=10, x=0, y=0, z=0),
        Point(no=2, x=10, y=0, z=0),
        Point(no=3, x=10, y=0, z=10),
        Point(no=4, x=0, y=0, z=10),
        Point(no=5, x=5, y=5, z=0),
    ]
    for p in base_points:
        app.create_object(p)
