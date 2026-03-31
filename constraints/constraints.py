# -*- coding: utf-8 -*-
"""
constraints.py - Constraint definition helpers.

API path: `SapModel.ConstraintDef`
"""

from typing import List, Optional, Tuple
from .enums import ConstraintType, ConstraintAxis
from PySap2000.com_helper import com_ret, com_data


# =============================================================================
# Common helpers
# =============================================================================

def get_constraint_count(model) -> int:
    """
    Get the number of constraints.
    
    Returns:
        Constraint count.
    """
    result = model.ConstraintDef.Count()
    return com_data(result, 0, result)


def get_constraint_name_list(model) -> List[str]:
    """
    Get the list of all constraint names.
    
    Returns:
        List of constraint names.
    """
    result = model.ConstraintDef.GetNameList(0, [])
    ret = com_ret(result)
    if ret == 0:
        names = com_data(result, 1)
        if names:
            return list(names)
    return []


def get_constraint_type(model, name: str) -> Optional[ConstraintType]:
    """
    Get the constraint type.
    
    Args:
        name: Constraint name
        
    Returns:
        `ConstraintType`, or `None` if the query fails.
    """
    result = model.ConstraintDef.GetConstraintType(name, 0)
    ret = com_ret(result)
    if ret == 0:
        return ConstraintType(com_data(result, 0))
    return None


def change_constraint_name(model, old_name: str, new_name: str) -> bool:
    """
    Rename a constraint.
    
    Returns:
        `True` if successful.
    """
    result = model.ConstraintDef.ChangeName(old_name, new_name)
    return com_ret(result) == 0


def delete_constraint(model, name: str) -> bool:
    """
    Delete a constraint.
    
    Returns:
        `True` if successful.
    """
    result = model.ConstraintDef.Delete(name)
    return com_ret(result) == 0


# =============================================================================
# Diaphragm constraints
# =============================================================================

def get_diaphragm(
    model,
    name: str
) -> Optional[Tuple[ConstraintAxis, str]]:
    """
    Get a diaphragm constraint definition.
    
    Args:
        name: Constraint name
        
    Returns:
        Tuple `(axis, csys)`, or `None` if the query fails.
        - `axis`: axis normal to the diaphragm plane
        - `csys`: coordinate system name
    """
    result = model.ConstraintDef.GetDiaphragm(name, 0, "")
    ret = com_ret(result)
    if ret == 0:
        return (ConstraintAxis(com_data(result, 0)), com_data(result, 1))
    return None


def set_diaphragm(
    model,
    name: str,
    axis: ConstraintAxis = ConstraintAxis.AUTO,
    csys: str = "Global"
) -> bool:
    """
    Set a diaphragm constraint.
    
    Args:
        name: Constraint name
        axis: Axis normal to the diaphragm plane, default is automatic
        csys: Coordinate system name
        
    Returns:
        `True` if successful.
    """
    result = model.ConstraintDef.SetDiaphragm(name, int(axis), csys)
    return com_ret(result) == 0


# =============================================================================
# Body constraints
# =============================================================================

def get_body(
    model,
    name: str
) -> Optional[Tuple[List[bool], str]]:
    """
    Get a body constraint definition.
    
    Args:
        name: Constraint name
        
    Returns:
        Tuple `(dof_values, csys)`, or `None` if the query fails.
        - `dof_values`: boolean list `[UX, UY, UZ, RX, RY, RZ]`
        - `csys`: coordinate system name
    """
    result = model.ConstraintDef.GetBody(name, [], "")
    ret = com_ret(result)
    if ret == 0:
        values = list(com_data(result, 0)) if com_data(result, 0) else [False] * 6
        return (values, com_data(result, 1))
    return None


def set_body(
    model,
    name: str,
    dof: List[bool] = None,
    csys: str = "Global"
) -> bool:
    """
    Set a body constraint.
    
    Args:
        name: Constraint name
        dof: Boolean list `[UX, UY, UZ, RX, RY, RZ]`, defaults to all `True`
        csys: Coordinate system name
        
    Returns:
        `True` if successful.
    """
    if dof is None:
        dof = [True] * 6
    result = model.ConstraintDef.SetBody(name, dof, csys)
    return com_ret(result) == 0


# =============================================================================
# Equal constraints
# =============================================================================

def get_equal(
    model,
    name: str
) -> Optional[Tuple[List[bool], str]]:
    """
    Get an equal-displacement constraint definition.
    
    Args:
        name: Constraint name
        
    Returns:
        Tuple `(dof_values, csys)`, or `None` if the query fails.
        - `dof_values`: boolean list `[UX, UY, UZ, RX, RY, RZ]`
        - `csys`: coordinate system name
    """
    result = model.ConstraintDef.GetEqual(name, (False,)*6, "")
    values = com_data(result, 0)
    csys = com_data(result, 1)
    # Some SAP2000 versions return `ret=1` even when the data is valid.
    if values and len(values) >= 6:
        return (list(values), csys if csys else "Global")
    return None


def set_equal(
    model,
    name: str,
    dof: List[bool] = None,
    csys: str = "Global"
) -> bool:
    """
    Set an equal-displacement constraint.
    
    Args:
        name: Constraint name
        dof: Boolean list `[UX, UY, UZ, RX, RY, RZ]`, defaults to all `True`
        csys: Coordinate system name
        
    Returns:
        `True` if successful.
    """
    if dof is None:
        dof = [True] * 6
    result = model.ConstraintDef.SetEqual(name, dof, csys)
    return com_ret(result) == 0


# =============================================================================
# Local constraints
# =============================================================================

def get_local(
    model,
    name: str
) -> Optional[List[bool]]:
    """
    Get a local constraint definition.
    
    Args:
        name: Constraint name
        
    Returns:
        Boolean list `[U1, U2, U3, R1, R2, R3]`, or `None` if the query fails.
        
    Note:
        Local constraints use the joint local coordinate system and do not
        require an explicit coordinate system.
    """
    result = model.ConstraintDef.GetLocal(name, [])
    ret = com_ret(result)
    if ret == 0:
        values = com_data(result, 0)
        return list(values) if values else [False] * 6
    return None


def set_local(
    model,
    name: str,
    dof: List[bool] = None
) -> bool:
    """
    Set a local constraint.
    
    Args:
        name: Constraint name
        dof: Boolean list `[U1, U2, U3, R1, R2, R3]`, defaults to all `True`
        
    Returns:
        `True` if successful.
        
    Note:
        Local constraints use the joint local coordinate system.
    """
    if dof is None:
        dof = [True] * 6
    result = model.ConstraintDef.SetLocal(name, dof)
    return com_ret(result) == 0


# =============================================================================
# Beam constraints
# =============================================================================

def get_beam(
    model,
    name: str
) -> Optional[Tuple[ConstraintAxis, str]]:
    """
    Get a beam constraint definition.
    
    Args:
        name: Constraint name
        
    Returns:
        Tuple `(axis, csys)`, or `None` if the query fails.
        - `axis`: direction parallel to the beam axis
        - `csys`: coordinate system name
    """
    result = model.ConstraintDef.GetBeam(name, 0, "")
    ret = com_ret(result)
    if ret == 0:
        return (ConstraintAxis(com_data(result, 0)), com_data(result, 1))
    return None


def set_beam(
    model,
    name: str,
    axis: ConstraintAxis = ConstraintAxis.AUTO,
    csys: str = "Global"
) -> bool:
    """
    Set a beam constraint.
    
    Args:
        name: Constraint name
        axis: Direction parallel to the beam axis, default is automatic
        csys: Coordinate system name
        
    Returns:
        `True` if successful.
    """
    result = model.ConstraintDef.SetBeam(name, int(axis), csys)
    return com_ret(result) == 0


# =============================================================================
# Plate constraints
# =============================================================================

def get_plate(
    model,
    name: str
) -> Optional[Tuple[ConstraintAxis, str]]:
    """
    Get a plate constraint definition.
    
    Args:
        name: Constraint name
        
    Returns:
        Tuple `(axis, csys)`, or `None` if the query fails.
        - `axis`: axis normal to the plate plane
        - `csys`: coordinate system name
    """
    result = model.ConstraintDef.GetPlate(name, 0, "")
    ret = com_ret(result)
    if ret == 0:
        return (ConstraintAxis(com_data(result, 0)), com_data(result, 1))
    return None


def set_plate(
    model,
    name: str,
    axis: ConstraintAxis = ConstraintAxis.AUTO,
    csys: str = "Global"
) -> bool:
    """
    Set a plate constraint.
    
    Args:
        name: Constraint name
        axis: Axis normal to the plate plane, default is automatic
        csys: Coordinate system name
        
    Returns:
        `True` if successful.
    """
    result = model.ConstraintDef.SetPlate(name, int(axis), csys)
    return com_ret(result) == 0


# =============================================================================
# Rod constraints
# =============================================================================

def get_rod(
    model,
    name: str
) -> Optional[Tuple[ConstraintAxis, str]]:
    """
    Get a rod constraint definition.
    
    Args:
        name: Constraint name
        
    Returns:
        Tuple `(axis, csys)`, or `None` if the query fails.
        - `axis`: direction parallel to the rod axis
        - `csys`: coordinate system name
    """
    result = model.ConstraintDef.GetRod(name, 0, "")
    ret = com_ret(result)
    if ret == 0:
        return (ConstraintAxis(com_data(result, 0)), com_data(result, 1))
    return None


def set_rod(
    model,
    name: str,
    axis: ConstraintAxis = ConstraintAxis.AUTO,
    csys: str = "Global"
) -> bool:
    """
    Set a rod constraint.
    
    Args:
        name: Constraint name
        axis: Direction parallel to the rod axis, default is automatic
        csys: Coordinate system name
        
    Returns:
        `True` if successful.
    """
    result = model.ConstraintDef.SetRod(name, int(axis), csys)
    return com_ret(result) == 0


# =============================================================================
# Weld constraints
# =============================================================================

def get_weld(
    model,
    name: str
) -> Optional[Tuple[List[bool], float, str]]:
    """
    Get a weld constraint definition.
    
    Args:
        name: Constraint name
        
    Returns:
        Tuple `(dof_values, tolerance, csys)`, or `None` if the query fails.
        - `dof_values`: boolean list `[UX, UY, UZ, RX, RY, RZ]`
        - `tolerance`: weld tolerance
        - `csys`: coordinate system name
    """
    result = model.ConstraintDef.GetWeld(name, [], 0.0, "")
    ret = com_ret(result)
    if ret == 0:
        values = list(com_data(result, 0)) if com_data(result, 0) else [False] * 6
        return (values, com_data(result, 1), com_data(result, 2))
    return None


def set_weld(
    model,
    name: str,
    dof: List[bool] = None,
    tolerance: float = 0.0,
    csys: str = "Global"
) -> bool:
    """
    Set a weld constraint.
    
    Args:
        name: Constraint name
        dof: Boolean list `[UX, UY, UZ, RX, RY, RZ]`, defaults to all `True`
        tolerance: Weld tolerance
        csys: Coordinate system name
        
    Returns:
        `True` if successful.
    """
    if dof is None:
        dof = [True] * 6
    result = model.ConstraintDef.SetWeld(name, dof, tolerance, csys)
    return com_ret(result) == 0


# =============================================================================
# Line constraints
# =============================================================================

def get_line(
    model,
    name: str
) -> Optional[Tuple[List[bool], str]]:
    """
    Get a line constraint definition.
    
    Args:
        name: Constraint name
        
    Returns:
        Tuple `(dof_values, csys)`, or `None` if the query fails.
        - `dof_values`: boolean list `[UX, UY, UZ, RX, RY, RZ]`
        - `csys`: coordinate system name
    """
    result = model.ConstraintDef.GetLine(name, [], "")
    ret = com_ret(result)
    if ret == 0:
        values = list(com_data(result, 0)) if com_data(result, 0) else [False] * 6
        return (values, com_data(result, 1))
    return None


def set_line(
    model,
    name: str,
    dof: List[bool] = None,
    csys: str = "Global"
) -> bool:
    """
    Set a line constraint.
    
    Args:
        name: Constraint name
        dof: Boolean list `[UX, UY, UZ, RX, RY, RZ]`, defaults to all `True`
        csys: Coordinate system name
        
    Returns:
        `True` if successful.
    """
    if dof is None:
        dof = [True] * 6
    result = model.ConstraintDef.SetLine(name, dof, csys)
    return com_ret(result) == 0


# =============================================================================
# Special helpers
# =============================================================================

def get_special_rigid_diaphragm_list(model) -> List[str]:
    """
    Get the list of special rigid diaphragms.
    
    Returns:
        List of rigid diaphragm constraint names.
    """
    result = model.ConstraintDef.GetSpecialRigidDiaphragmList(0, [])
    ret = com_ret(result)
    if ret == 0:
        names = com_data(result, 1)
        if names:
            return list(names)
    return []
