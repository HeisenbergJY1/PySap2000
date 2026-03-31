# -*- coding: utf-8 -*-
"""
spring.py - Point spring helpers.

Helpers for assigning and querying point spring stiffness.

SAP2000 API:
- PointObj.SetSpring(Name, k, ItemType, IsLocalCSys, Replace)
- PointObj.GetSpring(Name)
- PointObj.DeleteSpring(Name, ItemType)
- PointObj.SetSpringCoupled(Name, k, ItemType, IsLocalCSys, Replace)
- PointObj.GetSpringCoupled(Name)
"""

from typing import Tuple, Optional, List
from .enums import ItemType
from .data_classes import PointSpringData
from PySap2000.com_helper import com_ret, com_data


def set_point_spring(
    model,
    point_name: str,
    k: Tuple[float, float, float, float, float, float],
    item_type: ItemType = ItemType.OBJECT,
    is_local_csys: bool = False,
    replace: bool = True
) -> int:
    """
    Assign uncoupled spring stiffness to a point.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        k: Spring stiffness tuple `(U1, U2, U3, R1, R2, R3)`
            - `U1, U2, U3`: translational stiffness [F/L]
            - `R1, R2, R3`: rotational stiffness [FL/rad]
        item_type: Item scope
        is_local_csys: `True` for local coordinates, `False` for global
        replace: `True` to replace existing springs, `False` to add to them
    
    Returns:
        `0` on success
    
    Example:
        # Set vertical spring stiffness to 1000 kN/m
        set_point_spring(model, "1", (0, 0, 1000, 0, 0, 0))
        
        # Set springs for all six degrees of freedom
        set_point_spring(model, "2", (100, 100, 1000, 50, 50, 50))
    """
    k_list = list(k)
    while len(k_list) < 6:
        k_list.append(0.0)
    
    result = model.PointObj.SetSpring(
        str(point_name), k_list[:6], item_type, is_local_csys, replace
    )
    return com_ret(result)


def get_point_spring(
    model,
    point_name: str
) -> Optional[PointSpringData]:
    """
    Return uncoupled point spring stiffness.
    
    Args:
        model: `SapModel` object
        point_name: Point name
    
    Returns:
        `PointSpringData`, or `None` on failure
    
    Example:
        spring = get_point_spring(model, "1")
        if spring:
            print(f"Vertical stiffness: {spring.u3}")
    """
    try:
        result = model.PointObj.GetSpring(str(point_name))
        k_values = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and k_values and len(k_values) >= 6:
            return PointSpringData(
                point_name=str(point_name),
                u1=k_values[0],
                u2=k_values[1],
                u3=k_values[2],
                r1=k_values[3],
                r2=k_values[4],
                r3=k_values[5]
            )
    except Exception:
        pass
    return None


def delete_point_spring(
    model,
    point_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Delete point spring assignments.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        item_type: Item scope
    
    Returns:
        `0` on success
    
    Example:
        delete_point_spring(model, "1")
    """
    return model.PointObj.DeleteSpring(str(point_name), item_type)


def set_point_spring_coupled(
    model,
    point_name: str,
    k: Tuple[float, ...],
    item_type: ItemType = ItemType.OBJECT,
    is_local_csys: bool = False,
    replace: bool = True
) -> int:
    """
    Assign coupled spring stiffness to a point.

    Coupled springs include interaction terms between different DOFs.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        k: 21 spring coefficients for the upper triangle of the symmetric matrix
            k[0] = U1-U1
            k[1] = U1-U2, k[2] = U2-U2
            k[3] = U1-U3, k[4] = U2-U3, k[5] = U3-U3
            ... (21 terms in total)
        item_type: Item scope
        is_local_csys: Whether local coordinates are used
        replace: Whether to replace existing springs
    
    Returns:
        `0` on success
    """
    k_list = list(k)
    while len(k_list) < 21:
        k_list.append(0.0)
    
    return model.PointObj.SetSpringCoupled(
        str(point_name), k_list[:21], item_type, is_local_csys, replace
    )


def get_point_spring_coupled(
    model,
    point_name: str
) -> Optional[Tuple[float, ...]]:
    """
    Return coupled point spring stiffness.
    
    Args:
        model: `SapModel` object
        point_name: Point name
    
    Returns:
        Tuple of 21 stiffness coefficients, or `None` on failure
    """
    try:
        result = model.PointObj.GetSpringCoupled(str(point_name))
        k_values = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and k_values:
            return tuple(k_values)
    except Exception:
        pass
    return None


def is_point_spring_coupled(
    model,
    point_name: str
) -> bool:
    """
    Check whether a point has coupled springs assigned.
    
    Args:
        model: `SapModel` object
        point_name: Point name
    
    Returns:
        `True` if coupled springs exist, otherwise `False`
    """
    try:
        result = model.PointObj.IsSpringCoupled(str(point_name), False)
        value = com_data(result, 0)
        if value is not None:
            return value
    except Exception:
        pass
    return False
