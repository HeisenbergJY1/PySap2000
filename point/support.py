# -*- coding: utf-8 -*-
"""
support.py - Point support helpers.

Helpers for assigning and querying point boundary conditions.

SAP2000 API:
- PointObj.SetRestraint(Name, Value, ItemType)
- PointObj.GetRestraint(Name)
- PointObj.DeleteRestraint(Name, ItemType)
"""

from typing import Tuple, Optional, List
from .enums import PointSupportType, ItemType, SUPPORT_RESTRAINTS
from PySap2000.com_helper import com_ret, com_data


def set_point_support(
    model,
    point_name: str,
    support_type: PointSupportType,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Assign a predefined support type to a point.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        support_type: Support preset
            - `FIXED`: fully restrained
            - `HINGED`: translations restrained, rotations released
            - `ROLLER`: only Z translation restrained
            - `FREE`: no restraint
        item_type: Item scope
    
    Returns:
        `0` on success, non-zero on failure
    
    Example:
        # Set point "1" as fixed
        set_point_support(model, "1", PointSupportType.FIXED)
        
        # Set point "2" as hinged
        set_point_support(model, "2", PointSupportType.HINGED)
    """
    restraints = list(SUPPORT_RESTRAINTS.get(support_type, (False,) * 6))
    result = model.PointObj.SetRestraint(str(point_name), restraints, item_type)
    return com_ret(result)


def set_point_restraint(
    model,
    point_name: str,
    restraints: Tuple[bool, bool, bool, bool, bool, bool],
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Assign custom restraints to a point.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        restraints: Restraint state `(U1, U2, U3, R1, R2, R3)`
            - `True`: restrain this degree of freedom
            - `False`: release this degree of freedom
        item_type: Item scope
    
    Returns:
        `0` on success
    
    Example:
        # Restrain X and Y translations only
        set_point_restraint(model, "1", (True, True, False, False, False, False))
        
        # Restrain all translations and release all rotations
        set_point_restraint(model, "2", (True, True, True, False, False, False))
    """
    result = model.PointObj.SetRestraint(str(point_name), list(restraints), item_type)
    return com_ret(result)


def get_point_restraint(
    model,
    point_name: str
) -> Optional[Tuple[bool, bool, bool, bool, bool, bool]]:
    """
    Return the point restraint state.
    
    Args:
        model: `SapModel` object
        point_name: Point name
    
    Returns:
        Restraint tuple `(U1, U2, U3, R1, R2, R3)`, or `None` on failure
    
    Example:
        restraints = get_point_restraint(model, "1")
        if restraints:
            print(f"U1 restrained: {restraints[0]}, U2 restrained: {restraints[1]}")
    """
    try:
        result = model.PointObj.GetRestraint(str(point_name))
        restraints = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and restraints:
            return tuple(restraints)
    except Exception:
        pass
    return None


def get_point_support_type(
    model,
    point_name: str
) -> Optional[PointSupportType]:
    """
    Infer the support preset from the current restraint state.
    
    Args:
        model: `SapModel` object
        point_name: Point name
    
    Returns:
        Matching support type, or `None` if no preset matches
    
    Example:
        support_type = get_point_support_type(model, "1")
        if support_type == PointSupportType.FIXED:
            print("This is a fixed support")
    """
    restraints = get_point_restraint(model, point_name)
    if restraints:
        for support_type, expected in SUPPORT_RESTRAINTS.items():
            if restraints == expected:
                return support_type
    return None


def delete_point_restraint(
    model,
    point_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Delete point restraints and release all degrees of freedom.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        item_type: Item scope
    
    Returns:
        `0` on success
    
    Example:
        delete_point_restraint(model, "1")
    """
    return model.PointObj.DeleteRestraint(str(point_name), item_type)


def get_points_with_support(model) -> List[str]:
    """
    Return all point names that currently have support restraints.

    This uses the Database Tables API instead of per-point COM calls.
    
    Args:
        model: `SapModel` object
    
    Returns:
        List of supported point names
    
    Example:
        supported_points = get_points_with_support(model)
        print(f"Total supported points: {len(supported_points)}")
    """
    from PySap2000.database_tables import DatabaseTables
    
    # Fetch all restraint assignments in one call.
    table_data = DatabaseTables.get_table_for_display(
        model, "Joint Restraint Assignments"
    )
    
    if table_data is None or table_data.num_records == 0:
        return []
    
    supported = []
    restraint_fields = ["U1", "U2", "U3", "R1", "R2", "R3"]
    
    for row in table_data.to_dict_list():
        joint_name = row.get("Joint", "")
        # Any restrained DOF means the point has support conditions.
        has_restraint = any(
            row.get(f, "").strip().lower() == "yes"
            for f in restraint_fields
        )
        if has_restraint:
            supported.append(joint_name)
    
    return supported
