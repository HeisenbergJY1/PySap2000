# -*- coding: utf-8 -*-
"""
constraints - Constraint definition helpers.

SAP2000 constraint types:
    Body - rigid-body constraint (all joints move as a rigid body)
    Diaphragm - rigid diaphragm (in-plane rigidity)
    Plate - plate constraint (out-of-plane rigidity)
    Rod - rod constraint (axial rigidity)
    Beam - beam constraint (beam section remains plane)
    Equal - equal displacement constraint on selected degrees of freedom
    Local - constraint defined in the local coordinate system
    Weld - welded constraint (fully rigid connection)
    Line - line constraint (rigid along a line)
"""

from .enums import ConstraintType, ConstraintAxis
from .constraints import (
    # Common helpers
    get_constraint_count,
    get_constraint_name_list,
    get_constraint_type,
    change_constraint_name,
    delete_constraint,
    # Diaphragm
    get_diaphragm,
    set_diaphragm,
    # Body
    get_body,
    set_body,
    # Equal
    get_equal,
    set_equal,
    # Local
    get_local,
    set_local,
    # Beam
    get_beam,
    set_beam,
    # Plate
    get_plate,
    set_plate,
    # Rod
    get_rod,
    set_rod,
    # Weld
    get_weld,
    set_weld,
    # Line
    get_line,
    set_line,
    # Special helpers
    get_special_rigid_diaphragm_list,
)

__all__ = [
    # Enums
    "ConstraintType",
    "ConstraintAxis",
    # Common helpers
    "get_constraint_count",
    "get_constraint_name_list",
    "get_constraint_type",
    "change_constraint_name",
    "delete_constraint",
    # Diaphragm
    "get_diaphragm",
    "set_diaphragm",
    # Body
    "get_body",
    "set_body",
    # Equal
    "get_equal",
    "set_equal",
    # Local
    "get_local",
    "set_local",
    # Beam
    "get_beam",
    "set_beam",
    # Plate
    "get_plate",
    "set_plate",
    # Rod
    "get_rod",
    "set_rod",
    # Weld
    "get_weld",
    "set_weld",
    # Line
    "get_line",
    "set_line",
    # Special helpers
    "get_special_rigid_diaphragm_list",
]
