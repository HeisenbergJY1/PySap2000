# -*- coding: utf-8 -*-
"""
cable_load.py - Cable-object loads

Includes:
- Enums: CableLoadDirection, CableLoadItemType
- Dataclasses: CableLoadDistributedData, CableLoadTemperatureData, CableLoadStrainData,
          CableLoadDeformationData, CableLoadGravityData, CableLoadTargetForceData
- Functions: set_cable_load_xxx, get_cable_load_xxx, delete_cable_load_xxx

SAP2000 API:
- CableObj.SetLoadDistributed / GetLoadDistributed / DeleteLoadDistributed
- CableObj.SetLoadTemperature / GetLoadTemperature / DeleteLoadTemperature
- CableObj.SetLoadStrain / GetLoadStrain / DeleteLoadStrain
- CableObj.SetLoadDeformation / GetLoadDeformation / DeleteLoadDeformation
- CableObj.SetLoadGravity / GetLoadGravity / DeleteLoadGravity
- CableObj.SetLoadTargetForce / GetLoadTargetForce / DeleteLoadTargetForce
"""

from dataclasses import dataclass
from typing import List
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


# ==================== Enums ====================

class CableLoadDirection(IntEnum):
    """Cable object load direction."""
    LOCAL_1 = 1                 # Local-1 axis (only CSys=Local)
    LOCAL_2 = 2                 # Local-2 axis (only CSys=Local)
    LOCAL_3 = 3                 # Local-3 axis (only CSys=Local)
    GLOBAL_X = 4                # Global-X direction
    GLOBAL_Y = 5                # Global-Y direction
    GLOBAL_Z = 6                # Global-Z direction
    PROJECTED_GLOBAL_X = 7      # Projected global-X direction
    PROJECTED_GLOBAL_Y = 8      # Projected global-Y direction
    PROJECTED_GLOBAL_Z = 9      # Projected global-Z direction
    GRAVITY = 10                # Gravity direction (negative global Z)
    PROJECTED_GRAVITY = 11      # Projected gravity direction


class CableLoadItemType(IntEnum):
    """Load assignment target type."""
    OBJECT = 0              # Single object
    GROUP = 1               # Group
    SELECTED_OBJECTS = 2    # Selected objects


# ==================== Dataclasses ====================

@dataclass
class CableLoadDistributedData:
    """Cable distributed load data."""
    cable_name: str = ""
    load_pattern: str = ""
    load_type: int = 1      # 1=Force, 2=Moment
    direction: int = 10     # Default gravity direction
    value: float = 0.0
    csys: str = "Global"


@dataclass
class CableLoadTemperatureData:
    """Cable temperature load data."""
    cable_name: str = ""
    load_pattern: str = ""
    load_type: int = 1      # 1=Temperature, 2=Temperature Gradient
    value: float = 0.0
    pattern_name: str = ""


@dataclass
class CableLoadStrainData:
    """Cable strain load data."""
    cable_name: str = ""
    load_pattern: str = ""
    strain_type: int = 1    # 1=Axial
    value: float = 0.0
    pattern_name: str = ""


@dataclass
class CableLoadDeformationData:
    """Cable deformation load data."""
    cable_name: str = ""
    load_pattern: str = ""
    value: float = 0.0      # axial deformation [L]


@dataclass
class CableLoadGravityData:
    """Cable gravity-load data."""
    cable_name: str = ""
    load_pattern: str = ""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    csys: str = "Global"


@dataclass
class CableLoadTargetForceData:
    """Cable target-force load data."""
    cable_name: str = ""
    load_pattern: str = ""
    p: float = 0.0          # Target axial force [F]
    rd: float = 0.5         # relative distance (0-1)


# ==================== Distributed load functions ====================

def set_cable_load_distributed(
    model,
    cable_name: str,
    load_pattern: str,
    value: float,
    load_type: int = 1,
    direction: CableLoadDirection = CableLoadDirection.GRAVITY,
    csys: str = "Global",
    replace: bool = True,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    Set cable object distributed loads.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        load_pattern: Load pattern name
        value: Load value [F/L]
        load_type: Load type (1=Force, 2=Moment)
        direction: Load direction
        csys: Coordinate system name
        replace: `True` replaces existing loads, `False` adds to existing loads
        item_type: Operation scope
    
    Returns:
        `0` on success
    
    Example:
        set_cable_load_distributed(model, "1", "DEAD", 10)
    """
    return model.CableObj.SetLoadDistributed(
        str(cable_name), load_pattern, load_type, int(direction),
        value, csys, replace, int(item_type)
    )


def get_cable_load_distributed(
    model,
    cable_name: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> List[CableLoadDistributedData]:
    """
    Get cable object distributed loads.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        item_type: Operation scope
    
    Returns:
        List of CableLoadDistributedData
    """
    loads = []
    try:
        result = model.CableObj.GetLoadDistributed(
            str(cable_name), 0, [], [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            cable_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            my_types = com_data(result, 3)
            csys_list = com_data(result, 4)
            dirs = com_data(result, 5)
            vals = com_data(result, 6)
            for i in range(num_items):
                loads.append(CableLoadDistributedData(
                    cable_name=cable_names[i] if cable_names else str(cable_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    load_type=my_types[i] if my_types else 1,
                    direction=dirs[i] if dirs else 10,
                    value=vals[i] if vals else 0.0,
                    csys=csys_list[i] if csys_list else "Global"
                ))
    except Exception:
        pass
    return loads


def delete_cable_load_distributed(
    model,
    cable_name: str,
    load_pattern: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    Delete cable object distributed loads.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        load_pattern: Load pattern name
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.CableObj.DeleteLoadDistributed(str(cable_name), load_pattern, int(item_type))


# ==================== temperature load functions ====================

def set_cable_load_temperature(
    model,
    cable_name: str,
    load_pattern: str,
    value: float,
    pattern_name: str = "",
    replace: bool = True,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    Set cable object temperature load.

    SAP2000 API: CableObj.SetLoadTemperature(Name, LoadPat, Val, PatternName, Replace, ItemType)
    Note: Cable temperature load has no `load_type` parameter (unlike frame loads).

    Args:
        model: SapModel object
        cable_name: Cable object name
        load_pattern: Load pattern name
        value: Temperature change value [T]
        pattern_name: Pattern name (blank means uniform distribution)
        replace: `True` replaces existing loads, `False` adds to existing loads
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.CableObj.SetLoadTemperature(
        str(cable_name), load_pattern, value, pattern_name, replace, int(item_type)
    )


def get_cable_load_temperature(
    model,
    cable_name: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> List[CableLoadTemperatureData]:
    """
    Get cable object temperature load.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        item_type: Operation scope
    
    Returns:
        List of CableLoadTemperatureData
    """
    loads = []
    try:
        result = model.CableObj.GetLoadTemperature(
            str(cable_name), 0, [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            cable_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            load_types = com_data(result, 3)
            values = com_data(result, 4)
            patterns = com_data(result, 5)
            for i in range(num_items):
                loads.append(CableLoadTemperatureData(
                    cable_name=cable_names[i] if cable_names else str(cable_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    load_type=load_types[i] if load_types else 1,
                    value=values[i] if values else 0.0,
                    pattern_name=patterns[i] if patterns else ""
                ))
    except Exception:
        pass
    return loads


def delete_cable_load_temperature(
    model,
    cable_name: str,
    load_pattern: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    Delete cable object temperature load.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        load_pattern: Load pattern name
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.CableObj.DeleteLoadTemperature(str(cable_name), load_pattern, int(item_type))


# ==================== strain load functions ====================

def set_cable_load_strain(
    model,
    cable_name: str,
    load_pattern: str,
    value: float,
    strain_type: int = 1,
    pattern_name: str = "",
    replace: bool = True,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    Set cable object strain load.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        load_pattern: Load pattern name
        value: Strain value
        strain_type: Strain type (1=Axial)
        pattern_name: Pattern name
        replace: `True` replaces existing loads, `False` adds to existing loads
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.CableObj.SetLoadStrain(
        str(cable_name), load_pattern, strain_type, value, pattern_name, replace, int(item_type)
    )


def get_cable_load_strain(
    model,
    cable_name: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> List[CableLoadStrainData]:
    """
    Get cable object strain load.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        item_type: Operation scope
    
    Returns:
        List of CableLoadStrainData
    """
    loads = []
    try:
        result = model.CableObj.GetLoadStrain(
            str(cable_name), 0, [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            cable_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            strain_types = com_data(result, 3)
            values = com_data(result, 4)
            patterns = com_data(result, 5)
            for i in range(num_items):
                loads.append(CableLoadStrainData(
                    cable_name=cable_names[i] if cable_names else str(cable_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    strain_type=strain_types[i] if strain_types else 1,
                    value=values[i] if values else 0.0,
                    pattern_name=patterns[i] if patterns else ""
                ))
    except Exception:
        pass
    return loads


def delete_cable_load_strain(
    model,
    cable_name: str,
    load_pattern: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    Delete cable object strain load.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        load_pattern: Load pattern name
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.CableObj.DeleteLoadStrain(str(cable_name), load_pattern, int(item_type))



# ==================== deformation load functions ====================

def set_cable_load_deformation(
    model,
    cable_name: str,
    load_pattern: str,
    value: float,
    replace: bool = True,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    Set cable object deformation load.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        load_pattern: Load pattern name
        value: Axial deformation value [L]
        replace: `True` replaces existing loads, `False` adds to existing loads
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.CableObj.SetLoadDeformation(
        str(cable_name), load_pattern, value, replace, int(item_type)
    )


def get_cable_load_deformation(
    model,
    cable_name: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> List[CableLoadDeformationData]:
    """
    Get cable object deformation load.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        item_type: Operation scope
    
    Returns:
        List of CableLoadDeformationData
    """
    loads = []
    try:
        result = model.CableObj.GetLoadDeformation(
            str(cable_name), 0, [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            cable_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            values = com_data(result, 3)
            for i in range(num_items):
                loads.append(CableLoadDeformationData(
                    cable_name=cable_names[i] if cable_names else str(cable_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    value=values[i] if values else 0.0
                ))
    except Exception:
        pass
    return loads


def delete_cable_load_deformation(
    model,
    cable_name: str,
    load_pattern: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    Delete cable object deformation load.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        load_pattern: Load pattern name
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.CableObj.DeleteLoadDeformation(str(cable_name), load_pattern, int(item_type))


# ==================== gravity load functions ====================

def set_cable_load_gravity(
    model,
    cable_name: str,
    load_pattern: str,
    x: float = 0.0,
    y: float = 0.0,
    z: float = -1.0,
    replace: bool = True,
    csys: str = "Global",
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    Set cable object gravity load.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
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
    return model.CableObj.SetLoadGravity(
        str(cable_name), load_pattern, x, y, z, replace, csys, int(item_type)
    )


def get_cable_load_gravity(
    model,
    cable_name: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> List[CableLoadGravityData]:
    """
    Get cable object gravity load.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        item_type: Operation scope
    
    Returns:
        List of CableLoadGravityData
    """
    loads = []
    try:
        result = model.CableObj.GetLoadGravity(
            str(cable_name), 0, [], [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            cable_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            csys_list = com_data(result, 3)
            x_list = com_data(result, 4)
            y_list = com_data(result, 5)
            z_list = com_data(result, 6)
            for i in range(num_items):
                loads.append(CableLoadGravityData(
                    cable_name=cable_names[i] if cable_names else str(cable_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    x=x_list[i] if x_list else 0.0,
                    y=y_list[i] if y_list else 0.0,
                    z=z_list[i] if z_list else 0.0,
                    csys=csys_list[i] if csys_list else "Global"
                ))
    except Exception:
        pass
    return loads


def delete_cable_load_gravity(
    model,
    cable_name: str,
    load_pattern: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    Delete cable object gravity load.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        load_pattern: Load pattern name
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.CableObj.DeleteLoadGravity(str(cable_name), load_pattern, int(item_type))


# ==================== target-force load functions ====================

def set_cable_load_target_force(
    model,
    cable_name: str,
    load_pattern: str,
    p: float,
    rd: float = 0.5,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    Set cable object target-force load.
    
    SAP2000 API: CableObj.SetLoadTargetForce(Name, LoadPat, P, RD, ItemType)
    Note: Cable target force has no `replace` parameter.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        load_pattern: Load pattern name
        p: Target axial force [F]
        rd: relative distance (0-1)
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.CableObj.SetLoadTargetForce(
        str(cable_name), load_pattern, p, rd, int(item_type)
    )


def get_cable_load_target_force(
    model,
    cable_name: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> List[CableLoadTargetForceData]:
    """
    Get cable object target-force load.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        item_type: Operation scope
    
    Returns:
        List of CableLoadTargetForceData
    """
    loads = []
    try:
        result = model.CableObj.GetLoadTargetForce(
            str(cable_name), 0, [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            cable_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            p_list = com_data(result, 3)
            rd_list = com_data(result, 4)
            for i in range(num_items):
                loads.append(CableLoadTargetForceData(
                    cable_name=cable_names[i] if cable_names else str(cable_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    p=p_list[i] if p_list else 0.0,
                    rd=rd_list[i] if rd_list else 0.5
                ))
    except Exception:
        pass
    return loads


def delete_cable_load_target_force(
    model,
    cable_name: str,
    load_pattern: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    Delete cable object target-force load.
    
    Args:
        model: SapModel object
        cable_name: Cable object name
        load_pattern: Load pattern name
        item_type: Operation scope
    
    Returns:
        `0` on success
    """
    return model.CableObj.DeleteLoadTargetForce(str(cable_name), load_pattern, int(item_type))