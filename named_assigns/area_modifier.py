# -*- coding: utf-8 -*-
"""
area_modifier.py - Named area stiffness modifiers

Wraps SAP2000 `NamedAssign.ModifierArea`.

Creates reusable area stiffness modifier definitions that can be referenced by multiple area objects.

SAP2000 API:
- NamedAssign.ModifierArea.ChangeName
- NamedAssign.ModifierArea.Count
- NamedAssign.ModifierArea.Delete
- NamedAssign.ModifierArea.GetModifiers
- NamedAssign.ModifierArea.GetNameList
- NamedAssign.ModifierArea.SetModifiers

Modifier array (10 values):
- [0] f11: Membrane stiffness 11
- [1] f22: Membrane stiffness 22
- [2] f12: Membrane stiffness 12
- [3] m11: Bending stiffness 11
- [4] m22: Bending stiffness 22
- [5] m12: Bending stiffness 12
- [6] v13: Shear stiffness 13
- [7] v23: Shear stiffness 23
- [8] mass: Mass
- [9] weight: Weight
"""

from dataclasses import dataclass
from typing import List, Optional, ClassVar
from PySap2000.com_helper import com_ret, com_data


@dataclass
class NamedAreaModifier:
    """
    Named area stiffness modifier
    
    Attributes:
        name: Modifier name
        f11: Membrane stiffness 11 modifier
        f22: Membrane stiffness 22 modifier
        f12: Membrane stiffness 12 modifier
        m11: Bending stiffness 11 modifier
        m22: Bending stiffness 22 modifier
        m12: Bending stiffness 12 modifier
        v13: Shear stiffness 13 modifier
        v23: Shear stiffness 23 modifier
        mass: Mass modifier
        weight: Weight modifier
    """
    name: str = ""
    f11: float = 1.0
    f22: float = 1.0
    f12: float = 1.0
    m11: float = 1.0
    m22: float = 1.0
    m12: float = 1.0
    v13: float = 1.0
    v23: float = 1.0
    mass: float = 1.0
    weight: float = 1.0
    
    _object_type: ClassVar[str] = "NamedAssign.ModifierArea"
    
    def to_list(self) -> List[float]:
        """Convert to the list format required by the API"""
        return [
            self.f11, self.f22, self.f12,
            self.m11, self.m22, self.m12,
            self.v13, self.v23,
            self.mass, self.weight
        ]
    
    @classmethod
    def from_list(cls, name: str, values: List[float]) -> "NamedAreaModifier":
        """Build from the list returned by the API"""
        if len(values) >= 10:
            return cls(
                name=name,
                f11=values[0], f22=values[1], f12=values[2],
                m11=values[3], m22=values[4], m12=values[5],
                v13=values[6], v23=values[7],
                mass=values[8], weight=values[9]
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
        return com_ret(model.NamedAssign.ModifierArea.SetModifiers(
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
        result = model.NamedAssign.ModifierArea.GetModifiers(
            self.name, [0.0] * 10
        )
        
        values = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and values and len(values) >= 10:
            self.f11, self.f22, self.f12 = values[0], values[1], values[2]
            self.m11, self.m22, self.m12 = values[3], values[4], values[5]
            self.v13, self.v23 = values[6], values[7]
            self.mass, self.weight = values[8], values[9]
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
        return com_ret(model.NamedAssign.ModifierArea.Delete(self.name))
    
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
        ret = com_ret(model.NamedAssign.ModifierArea.ChangeName(self.name, new_name))
        if ret == 0:
            self.name = new_name
        return ret
    
    @staticmethod
    def get_count(model) -> int:
        """Get the number of modifiers"""
        return model.NamedAssign.ModifierArea.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """Get all modifier names"""
        result = model.NamedAssign.ModifierArea.GetNameList(0, [])
        names = com_data(result, 1)
        if names:
            return list(names)
        return []
    
    @classmethod
    def get_by_name(cls, model, name: str) -> Optional["NamedAreaModifier"]:
        """Get a modifier by name"""
        mod = cls(name=name)
        ret = mod._get(model)
        if ret == 0:
            return mod
        return None
    
    @classmethod
    def get_all(cls, model) -> List["NamedAreaModifier"]:
        """Get all modifiers"""
        names = cls.get_name_list(model)
        result = []
        for name in names:
            mod = cls.get_by_name(model, name)
            if mod:
                result.append(mod)
        return result
