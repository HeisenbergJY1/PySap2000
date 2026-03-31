# -*- coding: utf-8 -*-
"""
modifier.py - Cable modifier helpers.

SAP2000 API:
- CableObj.SetModifiers(Name, Value, ItemType)
- CableObj.GetModifiers(Name, Value)
- CableObj.DeleteModifiers(Name, ItemType)

Modifier array `Value[3]`:
- `Value[0]`: area modifier
- `Value[1]`: mass modifier
- `Value[2]`: weight modifier
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Union
from enum import IntEnum
from PySap2000.com_helper import com_ret, com_data


class CableItemType(IntEnum):
    """Target scope for cable operations."""
    OBJECT = 0              # Single object
    GROUP = 1               # Group
    SELECTED_OBJECTS = 2    # Selected objects


@dataclass
class CableModifiers:
    """
    Cable modifier data.
    
    Attributes:
        area: Area modifier, default `1.0`
        mass: Mass modifier, default `1.0`
        weight: Weight modifier, default `1.0`
    """
    area: float = 1.0
    mass: float = 1.0
    weight: float = 1.0
    
    def to_list(self) -> List[float]:
        """Return modifiers as the list format expected by the API."""
        return [self.area, self.mass, self.weight]
    
    @classmethod
    def from_list(cls, values: List[float]) -> 'CableModifiers':
        """Create an instance from an API-returned list."""
        if len(values) >= 3:
            return cls(area=values[0], mass=values[1], weight=values[2])
        return cls()


def set_cable_modifiers(
    model,
    cable_name: str,
    modifiers: Union[CableModifiers, Tuple[float, float, float]],
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    Set modifiers for a cable object.
    
    Args:
        model: SAP2000 SapModel object
        cable_name: Cable object name
        modifiers: Modifier values as `CableModifiers` or `(area, mass, weight)`
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    
    Example:
        # Use a CableModifiers instance
        set_cable_modifiers(model, "1", CableModifiers(area=1.5, mass=1.2))
        
        # Use a tuple
        set_cable_modifiers(model, "1", (1.5, 1.2, 1.0))
    """
    if isinstance(modifiers, CableModifiers):
        values = modifiers.to_list()
    else:
        values = list(modifiers)
    
    return model.CableObj.SetModifiers(str(cable_name), values, int(item_type))


def get_cable_modifiers(model, cable_name: str) -> Optional[CableModifiers]:
    """
    Get modifiers assigned to a cable object.
    
    Args:
        model: SAP2000 SapModel object
        cable_name: Cable object name
    
    Returns:
        `CableModifiers`, or `None` if the query fails.
    
    Example:
        modifiers = get_cable_modifiers(model, "1")
        if modifiers:
            print(f"Area modifier: {modifiers.area}")
    """
    try:
        result = model.CableObj.GetModifiers(str(cable_name), [0.0, 0.0, 0.0])
        values = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and values:
            return CableModifiers.from_list(list(values))
    except Exception:
        pass
    return None


def delete_cable_modifiers(
    model,
    cable_name: str,
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    Delete cable modifiers and restore defaults of `1.0`.
    
    Args:
        model: SAP2000 SapModel object
        cable_name: Cable object name
        item_type: Target scope for the operation
    
    Returns:
        `0` if successful.
    """
    return model.CableObj.DeleteModifiers(str(cable_name), int(item_type))
