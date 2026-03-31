# -*- coding: utf-8 -*-
"""
cable_modifier.py - Named cable modifiers

Wraps SAP2000 `NamedAssign.ModifierCable`.

Creates reusable cable modifier definitions that can be referenced by multiple cable objects.

SAP2000 API:
- NamedAssign.ModifierCable.ChangeName
- NamedAssign.ModifierCable.Count
- NamedAssign.ModifierCable.Delete
- NamedAssign.ModifierCable.GetModifiers
- NamedAssign.ModifierCable.GetNameList
- NamedAssign.ModifierCable.SetModifiers

Modifier array (3 values):
- [0] area: Section area
- [1] mass: Mass
- [2] weight: Weight
"""

from dataclasses import dataclass
from typing import List, Optional, ClassVar
from PySap2000.com_helper import com_ret, com_data


@dataclass
class NamedCableModifier:
    """
    Named cable modifier
    
    Attributes:
        name: Modifier name
        area: Section area modifier
        mass: Mass modifier
        weight: Weight modifier
    """
    name: str = ""
    area: float = 1.0
    mass: float = 1.0
    weight: float = 1.0
    
    _object_type: ClassVar[str] = "NamedAssign.ModifierCable"
    
    def to_list(self) -> List[float]:
        """Convert to the list format required by the API"""
        return [self.area, self.mass, self.weight]
    
    @classmethod
    def from_list(cls, name: str, values: List[float]) -> "NamedCableModifier":
        """Build from the list returned by the API"""
        if len(values) >= 3:
            return cls(
                name=name,
                area=values[0], mass=values[1], weight=values[2]
            )
        return cls(name=name)
    
    def _create(self, model) -> int:
        """
        Create or update the named modifier
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` on success
        """
        from PySap2000.com_helper import com_ret
        return com_ret(model.NamedAssign.ModifierCable.SetModifiers(
            self.name, self.to_list()
        ))
    
    def _get(self, model) -> int:
        """
        Load modifier data from the model
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` on success
        """
        result = model.NamedAssign.ModifierCable.GetModifiers(
            self.name, [0.0] * 3
        )
        
        values = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and values and len(values) >= 3:
            self.area = values[0]
            self.mass = values[1]
            self.weight = values[2]
        return ret if isinstance(ret, int) else -1
    
    def _delete(self, model) -> int:
        """
        Delete the named modifier
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` on success
        """
        from PySap2000.com_helper import com_ret
        return com_ret(model.NamedAssign.ModifierCable.Delete(self.name))
    
    def change_name(self, model, new_name: str) -> int:
        """
        Rename the modifier
        
        Args:
            model: SAP2000 SapModel object
            new_name: New name
            
        Returns:
            `0` on success
        """
        from PySap2000.com_helper import com_ret
        ret = com_ret(model.NamedAssign.ModifierCable.ChangeName(self.name, new_name))
        if ret == 0:
            self.name = new_name
        return ret
    
    @staticmethod
    def get_count(model) -> int:
        """Get the number of modifiers"""
        return model.NamedAssign.ModifierCable.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """Get all modifier names"""
        result = model.NamedAssign.ModifierCable.GetNameList(0, [])
        names = com_data(result, 1)
        if names:
            return list(names)
        return []
    
    @classmethod
    def get_by_name(cls, model, name: str) -> Optional["NamedCableModifier"]:
        """Get a modifier by name"""
        mod = cls(name=name)
        ret = mod._get(model)
        if ret == 0:
            return mod
        return None
    
    @classmethod
    def get_all(cls, model) -> List["NamedCableModifier"]:
        """Get all modifiers"""
        names = cls.get_name_list(model)
        result = []
        for name in names:
            mod = cls.get_by_name(model, name)
            if mod:
                result.append(mod)
        return result
