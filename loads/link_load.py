# -*- coding: utf-8 -*-
"""
link_load.py - Link-object loads

Includes:
- Enums: LinkLoadItemType
- Dataclasses: LinkLoadDeformationData, LinkLoadGravityData, LinkLoadTargetForceData
- Functions: set_link_load_xxx, get_link_load_xxx, delete_link_load_xxx

SAP2000 API:
- LinkObj.SetLoadDeformation / GetLoadDeformation / DeleteLoadDeformation
- LinkObj.SetLoadGravity / GetLoadGravity / DeleteLoadGravity
- LinkObj.SetLoadTargetForce / GetLoadTargetForce / DeleteLoadTargetForce
"""

from dataclasses import dataclass, field
from typing import List, Tuple
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


# ==================== Enums ====================

class LinkLoadItemType(IntEnum):
    """Load assignment target type."""
    OBJECT = 0              # Single object
    GROUP = 1               # Group
    SELECTED_OBJECTS = 2    # Selected objects


# ==================== Dataclasses ====================

@dataclass
class LinkLoadDeformationData:
    """Link deformation load data."""
    link_name: str = ""
    load_pattern: str = ""
    dof: Tuple[bool, ...] = field(default_factory=lambda: (False,) * 6)  # U1,U2,U3,R1,R2,R3
    deformation: Tuple[float, ...] = field(default_factory=lambda: (0.0,) * 6)  # [L] or [rad]


@dataclass
class LinkLoadGravityData:
    """Link gravity load data."""
    link_name: str = ""
    load_pattern: str = ""
    x: float = 0.0
    y: float = 0.0
    z: float = -1.0
    csys: str = "Global"


@dataclass
class LinkLoadTargetForceData:
    """Link target-force load data."""
    link_name: str = ""
    load_pattern: str = ""
    dof: Tuple[bool, ...] = field(default_factory=lambda: (False,) * 6)  # P,V2,V3,T,M2,M3
    force: Tuple[float, ...] = field(default_factory=lambda: (0.0,) * 6)  # [F] or [FL]
    relative_dist: Tuple[float, ...] = field(default_factory=lambda: (0.5,) * 6)


# ==================== deformation load functions ====================

def set_link_load_deformation(
    model,
    link_name: str,
    load_pattern: str,
    dof: Tuple[bool, ...],
    deformation: Tuple[float, ...],
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> int:
    """
    Set link object deformation load.

    Args:
        model: SapModel object
        link_name: Link object name
        load_pattern: Load pattern name
        dof: Whether each DOF has deformation load (U1, U2, U3, R1, R2, R3)
        deformation: Deformation values (U1, U2, U3 [L], R1, R2, R3 [rad])
        item_type: Operation scope
    
    Returns:
        `0` on success
    
    Example:
        set_link_load_deformation(model, "1", "DEAD", 
            (True, False, False, False, False, False), (0.01, 0, 0, 0, 0, 0))
    """
    dof_list = list(dof) if len(dof) >= 6 else list(dof) + [False] * (6 - len(dof))
    d_list = list(deformation) if len(deformation) >= 6 else list(deformation) + [0.0] * (6 - len(deformation))
    
    return model.LinkObj.SetLoadDeformation(
        str(link_name), load_pattern, dof_list, d_list, int(item_type)
    )


def get_link_load_deformation(
    model,
    link_name: str,
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> List[LinkLoadDeformationData]:
    """
    Get link object deformation load.

    Args:
        model: SapModel object
        link_name: Link object name
        item_type: Operation scope
    
    Returns:
        List of LinkLoadDeformationData
    """
    loads = []
    try:
        result = model.LinkObj.GetLoadDeformation(str(link_name), int(item_type))
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            link_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            dof1 = com_data(result, 3)
            dof2 = com_data(result, 4)
            dof3 = com_data(result, 5)
            dof4 = com_data(result, 6)
            dof5 = com_data(result, 7)
            dof6 = com_data(result, 8)
            u1 = com_data(result, 9)
            u2 = com_data(result, 10)
            u3 = com_data(result, 11)
            r1 = com_data(result, 12)
            r2 = com_data(result, 13)
            r3 = com_data(result, 14)

            for i in range(num_items):
                loads.append(LinkLoadDeformationData(
                    link_name=link_names[i] if link_names else str(link_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    dof=(dof1[i], dof2[i], dof3[i], dof4[i], dof5[i], dof6[i]),
                    deformation=(u1[i], u2[i], u3[i], r1[i], r2[i], r3[i])
                ))
    except Exception:
        pass
    return loads


def delete_link_load_deformation(
    model,
    link_name: str,
    load_pattern: str,
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> int:
    """
    Delete link object deformation load.

    Args:
        model: SapModel object
        link_name: Link object name
        load_pattern: Load pattern name
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.LinkObj.DeleteLoadDeformation(str(link_name), load_pattern, int(item_type))


# ==================== gravity load functions ====================

def set_link_load_gravity(
    model,
    link_name: str,
    load_pattern: str,
    x: float = 0.0,
    y: float = 0.0,
    z: float = -1.0,
    replace: bool = True,
    csys: str = "Global",
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> int:
    """
    Set link object gravity load.

    Args:
        model: SapModel object
        link_name: Link object name
        load_pattern: Load pattern name
        x: X-direction gravity factor
        y: Y-direction gravity factor
        z: Z-direction gravity factor (default -1)
        replace: `True` replaces existing loads, `False` adds to existing loads
        csys: Coordinate system name
        item_type: Operation scope

    Returns:
        `0` on success
    """
    return model.LinkObj.SetLoadGravity(
        str(link_name), load_pattern, x, y, z, replace, csys, int(item_type)
    )


def get_link_load_gravity(
    model,
    link_name: str,
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> List[LinkLoadGravityData]:
    """
    Get link object gravity load.

    Args:
        model: SapModel object
        link_name: Link object name
        item_type: Operation scope
    
    Returns:
        List of LinkLoadGravityData
    """
    loads = []
    try:
        result = model.LinkObj.GetLoadGravity(str(link_name), int(item_type))
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            link_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            csys_list = com_data(result, 3)
            x_list = com_data(result, 4)
            y_list = com_data(result, 5)
            z_list = com_data(result, 6)

            for i in range(num_items):
                loads.append(LinkLoadGravityData(
                    link_name=link_names[i] if link_names else str(link_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    x=x_list[i] if x_list else 0.0,
                    y=y_list[i] if y_list else 0.0,
                    z=z_list[i] if z_list else 0.0,
                    csys=csys_list[i] if csys_list else "Global"
                ))
    except Exception:
        pass
    return loads


def delete_link_load_gravity(
    model,
    link_name: str,
    load_pattern: str,
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> int:
    """
    Delete link object gravity load.

    Args:
        model: SapModel object
        link_name: Link object name
        load_pattern: Load pattern name
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.LinkObj.DeleteLoadGravity(str(link_name), load_pattern, int(item_type))


# ==================== target-force load functions ====================

def set_link_load_target_force(
    model,
    link_name: str,
    load_pattern: str,
    dof: Tuple[bool, ...],
    force: Tuple[float, ...],
    relative_dist: Tuple[float, ...],
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> int:
    """
    Set link object target-force load.

    Args:
        model: SapModel object
        link_name: Link object name
        load_pattern: Load pattern name
        dof: Whether each DOF has target force (P, V2, V3, T, M2, M3)
        force: Target force values (P [F], V2 [F], V3 [F], T [FL], M2 [FL], M3 [FL])
        relative_dist: Relative distance along element (0-1) per DOF
        item_type: Operation scope

    Returns:
        `0` on success
    """
    dof_list = list(dof) if len(dof) >= 6 else list(dof) + [False] * (6 - len(dof))
    f_list = list(force) if len(force) >= 6 else list(force) + [0.0] * (6 - len(force))
    rd_list = list(relative_dist) if len(relative_dist) >= 6 else list(relative_dist) + [0.5] * (6 - len(relative_dist))
    
    return model.LinkObj.SetLoadTargetForce(
        str(link_name), load_pattern, dof_list, f_list, rd_list, int(item_type)
    )


def get_link_load_target_force(
    model,
    link_name: str,
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> List[LinkLoadTargetForceData]:
    """
    Get link object target-force load.

    Args:
        model: SapModel object
        link_name: Link object name
        item_type: Operation scope
    
    Returns:
        List of LinkLoadTargetForceData
    """
    loads = []
    try:
        result = model.LinkObj.GetLoadTargetForce(str(link_name), int(item_type))
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            link_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            dof1 = com_data(result, 3)
            dof2 = com_data(result, 4)
            dof3 = com_data(result, 5)
            dof4 = com_data(result, 6)
            dof5 = com_data(result, 7)
            dof6 = com_data(result, 8)
            p_vals = com_data(result, 9)
            v2_vals = com_data(result, 10)
            v3_vals = com_data(result, 11)
            t_vals = com_data(result, 12)
            m2_vals = com_data(result, 13)
            m3_vals = com_data(result, 14)
            t1_vals = com_data(result, 15)
            t2_vals = com_data(result, 16)
            t3_vals = com_data(result, 17)
            t4_vals = com_data(result, 18)
            t5_vals = com_data(result, 19)
            t6_vals = com_data(result, 20)

            for i in range(num_items):
                loads.append(LinkLoadTargetForceData(
                    link_name=link_names[i] if link_names else str(link_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    dof=(dof1[i], dof2[i], dof3[i], dof4[i], dof5[i], dof6[i]),
                    force=(p_vals[i], v2_vals[i], v3_vals[i], t_vals[i], m2_vals[i], m3_vals[i]),
                    relative_dist=(t1_vals[i], t2_vals[i], t3_vals[i], t4_vals[i], t5_vals[i], t6_vals[i])
                ))
    except Exception:
        pass
    return loads


def delete_link_load_target_force(
    model,
    link_name: str,
    load_pattern: str,
    item_type: LinkLoadItemType = LinkLoadItemType.OBJECT
) -> int:
    """
    Delete link object target-force load.

    Args:
        model: SapModel object
        link_name: Link object name
        load_pattern: Load pattern name
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.LinkObj.DeleteLoadTargetForce(str(link_name), load_pattern, int(item_type))
