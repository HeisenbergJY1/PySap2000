# -*- coding: utf-8 -*-
"""
mass.py - Point mass helpers.

Helpers for assigning and querying additional point mass.

SAP2000 API:
- PointObj.SetMass / GetMass / DeleteMass
- PointObj.SetMassByVolume
- PointObj.SetMassByWeight
"""

from typing import Tuple, Optional
from .enums import ItemType
from .data_classes import PointMassData
from PySap2000.com_helper import com_ret, com_data


def set_point_mass(
    model,
    point_name: str,
    mass: Tuple[float, float, float, float, float, float],
    item_type: ItemType = ItemType.OBJECT,
    is_local_csys: bool = True,
    replace: bool = True
) -> int:
    """
    Assign mass to a point.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        mass: Mass tuple `(M1, M2, M3, MR1, MR2, MR3)`
            - `M1, M2, M3`: translational mass [M]
            - `MR1, MR2, MR3`: rotational inertia [ML^2]
        item_type: Item scope
        is_local_csys: `True` for local coordinates, `False` for global
        replace: `True` to replace, `False` to add
    
    Returns:
        `0` on success
    
    Example:
        # Set a 1000 kg lumped mass
        set_point_mass(model, "1", (1000, 1000, 1000, 0, 0, 0))
        
        # Set different mass values by direction
        set_point_mass(model, "2", (500, 500, 1000, 100, 100, 50))
    """
    m_list = list(mass)
    while len(m_list) < 6:
        m_list.append(0.0)
    
    result = model.PointObj.SetMass(
        str(point_name), m_list[:6], item_type, is_local_csys, replace
    )
    return com_ret(result)


def get_point_mass(
    model,
    point_name: str
) -> Optional[PointMassData]:
    """
    Return point mass data.
    
    Args:
        model: `SapModel` object
        point_name: Point name
    
    Returns:
        `PointMassData`, or `None` on failure
    
    Example:
        mass = get_point_mass(model, "1")
        if mass:
            print(f"Mass: {mass.m1}, {mass.m2}, {mass.m3}")
    """
    try:
        result = model.PointObj.GetMass(str(point_name))
        m_values = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and m_values and len(m_values) >= 6:
            return PointMassData(
                point_name=str(point_name),
                m1=m_values[0],
                m2=m_values[1],
                m3=m_values[2],
                mr1=m_values[3],
                mr2=m_values[4],
                mr3=m_values[5]
            )
    except Exception:
        pass
    return None


def delete_point_mass(
    model,
    point_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Delete point mass assignments.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        item_type: Item scope
    
    Returns:
        `0` on success
    """
    return model.PointObj.DeleteMass(str(point_name), item_type)


def set_point_mass_by_weight(
    model,
    point_name: str,
    weight: float,
    item_type: ItemType = ItemType.OBJECT,
    is_local_csys: bool = True,
    replace: bool = True
) -> int:
    """
    Assign point mass from weight.

    SAP2000 converts weight to mass internally using gravitational acceleration.
    Translational masses are identical in all three directions and rotational
    inertias are set to zero.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        weight: Weight [F]
        item_type: Item scope
        is_local_csys: Whether local coordinates are used
        replace: Whether to replace existing values
    
    Returns:
        `0` on success
    
    Example:
        # Assign a 10 kN weight
        set_point_mass_by_weight(model, "1", 10.0)
    """
    return model.PointObj.SetMassByWeight(
        str(point_name), weight, item_type, is_local_csys, replace
    )


def set_point_mass_by_volume(
    model,
    point_name: str,
    volume: float,
    material_name: str,
    item_type: ItemType = ItemType.OBJECT,
    is_local_csys: bool = True,
    replace: bool = True
) -> int:
    """
    Assign point mass from volume and material.

    SAP2000 computes the mass from the given volume and material density.
    
    Args:
        model: `SapModel` object
        point_name: Point name
        volume: Volume [L^3]
        material_name: Material name, which must already exist
        item_type: Item scope
        is_local_csys: Whether local coordinates are used
        replace: Whether to replace existing values
    
    Returns:
        `0` on success
    
    Example:
        # Assign mass from 1 m^3 of concrete
        set_point_mass_by_volume(model, "1", 1.0, "C30")
    """
    return model.PointObj.SetMassByVolume(
        str(point_name), volume, material_name, item_type, is_local_csys, replace
    )
