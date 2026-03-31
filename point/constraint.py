# -*- coding: utf-8 -*-
"""
constraint.py - Point constraint helpers.

Helpers for assigning rigid point constraints such as diaphragms.

SAP2000 API:
- PointObj.SetConstraint / GetConstraint / DeleteConstraint

Note:
    `Constraint` here means a SAP2000 joint constraint such as `Diaphragm`
    or `Body`, not a support restraint.
"""

from typing import List
from .enums import ItemType
from .data_classes import PointConstraintAssignment
from PySap2000.com_helper import com_ret, com_data


def set_point_constraint(
    model,
    point_name: str,
    constraint_name: str,
    item_type: ItemType = ItemType.OBJECT,
    replace: bool = True
) -> int:
    """
    Assign a joint constraint to a point.

    The target constraint must already be defined in SAP2000.

    Common constraint types:
    - `Diaphragm`: restrains in-plane translation and rotation
    - `Body`: rigid-body constraint across all DOFs
    - `Equal`: equal-displacement constraint
    
    Args:
        model: `SapModel` object
        point_name: Point name
        constraint_name: Constraint name, which must already exist
        item_type: Item scope
        replace: `True` to replace all existing constraints, `False` to append
    
    Returns:
        `0` on success
    
    Example:
        # Assign a point to diaphragm "Diaph1"
        set_point_constraint(model, "1", "Diaph1")
        
        # Assign multiple points to the same diaphragm
        for name in ["1", "2", "3", "4"]:
            set_point_constraint(model, name, "Diaph1")
    """
    return model.PointObj.SetConstraint(
        str(point_name), constraint_name, item_type, replace
    )


def get_point_constraint(
    model,
    point_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> List[PointConstraintAssignment]:
    """
    Return all constraint assignments for a point.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        item_type: Item scope
    
    Returns:
        List of `PointConstraintAssignment` objects
    
    Example:
        constraints = get_point_constraint(model, "1")
        for c in constraints:
            print(f"Point {c.point_name} belongs to constraint {c.constraint_name}")
    """
    assignments = []
    try:
        result = model.PointObj.GetConstraint(
            str(point_name), 0, [], [], item_type
        )
        num_items = com_data(result, 0, 0)
        point_names = com_data(result, 1, [])
        constraint_names = com_data(result, 2, [])
        
        for i in range(num_items):
            assignments.append(PointConstraintAssignment(
                point_name=point_names[i] if point_names else str(point_name),
                constraint_name=constraint_names[i] if constraint_names else ""
            ))
    except Exception:
        pass
    return assignments


def delete_point_constraint(
    model,
    point_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Delete all constraint assignments from a point.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        item_type: Item scope
    
    Returns:
        `0` on success
    
    Example:
        delete_point_constraint(model, "1")
    """
    return model.PointObj.DeleteConstraint(str(point_name), item_type)


def get_points_in_constraint(
    model,
    constraint_name: str
) -> List[str]:
    """
    Return all points assigned to a specific constraint.
    
    Args:
        model: `SapModel` object
        constraint_name: Constraint name
    
    Returns:
        List of point names
    
    Example:
        points = get_points_in_constraint(model, "Diaph1")
        print(f"Diaphragm Diaph1 contains {len(points)} points")
    """
    points_in_constraint = []
    
    # Get all point names.
    result = model.PointObj.GetNameList(0, [])
    names = com_data(result, 1)
    if not names:
        return points_in_constraint
    
    # Check each point for the requested constraint.
    for name in names:
        constraints = get_point_constraint(model, name)
        for c in constraints:
            if c.constraint_name == constraint_name:
                points_in_constraint.append(name)
                break
    
    return points_in_constraint
