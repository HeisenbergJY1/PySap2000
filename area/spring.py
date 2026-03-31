# -*- coding: utf-8 -*-
"""
spring.py - Area spring helpers.

Wraps SAP2000 `AreaObj` spring APIs.
"""

from typing import Optional, List, Tuple

from .enums import (
    AreaSpringType, AreaSimpleSpringType, AreaSpringLocalOneType, ItemType
)
from .data_classes import AreaSpringData
from PySap2000.com_helper import com_ret, com_data


def set_area_spring(
    model,
    area_name: str,
    spring_type: AreaSpringType,
    stiffness: float,
    simple_spring_type: AreaSimpleSpringType = AreaSimpleSpringType.TENSION_COMPRESSION,
    link_prop: str = "",
    face: int = -1,
    local_one_type: AreaSpringLocalOneType = AreaSpringLocalOneType.PARALLEL_TO_LOCAL_AXIS,
    direction: int = 3,
    outward: bool = True,
    vector: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    angle: float = 0.0,
    replace: bool = True,
    csys: str = "Local",
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Assign springs to an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        spring_type: Spring type
            - `SIMPLE_SPRING (1)`: simple spring
            - `LINK_PROPERTY (2)`: link property
        stiffness: Spring stiffness
        simple_spring_type: Simple spring behavior type
            - `TENSION_COMPRESSION (1)`: tension and compression
            - `COMPRESSION_ONLY (2)`: compression only
            - `TENSION_ONLY (3)`: tension only
        link_prop: Link property name for `LINK_PROPERTY`
        face: Face identifier (`-1`=bottom, `-2`=top)
        local_one_type: Local-1 axis direction type
        direction: Direction index
        outward: Whether the spring acts outward
        vector: User vector
        angle: Angle
        replace: Whether to replace existing springs
        csys: Coordinate system
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
        
    Example:
        # Set a simple spring on the bottom face of area "1"
        set_area_spring(model, "1", AreaSpringType.SIMPLE_SPRING, 1000.0, face=-1)
    """
    result = model.AreaObj.SetSpring(
        str(area_name), int(spring_type), stiffness, int(simple_spring_type),
        link_prop, face, int(local_one_type), direction, outward,
        list(vector), angle, replace, csys, int(item_type)
    )
    return com_ret(result)


def set_area_spring_data(
    model,
    area_name: str,
    data: AreaSpringData,
    replace: bool = True,
    csys: str = "Local",
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Assign area springs from a data object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        data: `AreaSpringData` instance
        replace: Whether to replace existing springs
        csys: Coordinate system
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
    """
    return model.AreaObj.SetSpring(
        str(area_name), int(data.spring_type), data.stiffness, int(data.simple_spring_type),
        data.link_prop, data.face, int(data.local_one_type), data.direction, data.outward,
        list(data.vector), data.angle, replace, csys, int(item_type)
    )


def get_area_spring(
    model,
    area_name: str
) -> Optional[List[AreaSpringData]]:
    """
    Get springs assigned to an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        List of `AreaSpringData`, or `None` if the query fails.
        
    Example:
        springs = get_area_spring(model, "1")
        if springs:
            for spring in springs:
                print(f"Stiffness: {spring.stiffness}, face: {spring.face}")
    """
    try:
        result = model.AreaObj.GetSpring(
            str(area_name), 0, [], [], [], [], [], [], [], [], [], []
        )
        num_springs = com_data(result, 0, 0)
        if num_springs > 0:
            springs = []
            types = com_data(result, 1)
            stiffnesses = com_data(result, 2)
            simple_types = com_data(result, 3)
            link_props = com_data(result, 4)
            faces = com_data(result, 5)
            local_one_types = com_data(result, 6)
            directions = com_data(result, 7)
            outwards = com_data(result, 8)
            vectors = com_data(result, 9)
            angles = com_data(result, 10)
            if True:
                
                for i in range(num_springs):
                    springs.append(AreaSpringData(
                        spring_type=AreaSpringType(types[i]) if types else AreaSpringType.SIMPLE_SPRING,
                        stiffness=stiffnesses[i] if stiffnesses else 0.0,
                        simple_spring_type=AreaSimpleSpringType(simple_types[i]) if simple_types else AreaSimpleSpringType.TENSION_COMPRESSION,
                        link_prop=link_props[i] if link_props else "",
                        face=faces[i] if faces else -1,
                        local_one_type=AreaSpringLocalOneType(local_one_types[i]) if local_one_types else AreaSpringLocalOneType.PARALLEL_TO_LOCAL_AXIS,
                        direction=directions[i] if directions else 3,
                        outward=outwards[i] if outwards else True,
                        vector=tuple(vectors[i]) if vectors and vectors[i] else (0.0, 0.0, 0.0),
                        angle=angles[i] if angles else 0.0
                    ))
                return springs
    except Exception:
        pass
    return None


def delete_area_spring(
    model,
    area_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Delete springs assigned to an area object.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        item_type: Target scope
        
    Returns:
        `0` on success. Nonzero indicates failure.
    """
    return model.AreaObj.DeleteSpring(str(area_name), int(item_type))


def has_area_spring(
    model,
    area_name: str
) -> bool:
    """
    Check whether an area object has springs assigned.
    
    Args:
        model: SAP2000 SapModel object
        area_name: Area object name
        
    Returns:
        `True` if springs are assigned, otherwise `False`.
    """
    springs = get_area_spring(model, area_name)
    return springs is not None and len(springs) > 0
