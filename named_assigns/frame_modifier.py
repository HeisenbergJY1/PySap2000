# -*- coding: utf-8 -*-
"""
frame_modifier.py - Named frame modifiers

Wraps SAP2000 `NamedAssign.ModifierFrame`.

Creates reusable frame modifier definitions that can be referenced by multiple frame objects.

SAP2000 API:
- NamedAssign.ModifierFrame.ChangeName
- NamedAssign.ModifierFrame.Count
- NamedAssign.ModifierFrame.Delete
- NamedAssign.ModifierFrame.GetModifiers
- NamedAssign.ModifierFrame.GetNameList
- NamedAssign.ModifierFrame.SetModifiers

Modifier array (8 values):
- [0] area: Section area (`A`)
- [1] shear_2: Local-2 shear area (`As2`)
- [2] shear_3: Local-3 shear area (`As3`)
- [3] torsion: Torsional constant (`J`)
- [4] inertia_22: Moment of inertia about local-2 (`I22`)
- [5] inertia_33: Moment of inertia about local-3 (`I33`)
- [6] mass: Mass
- [7] weight: Weight
"""

from dataclasses import dataclass
from typing import List, Optional, ClassVar
from PySap2000.com_helper import com_ret, com_data


@dataclass
class NamedFrameModifier:
    """
    Named frame modifier
    
    Attributes:
        name: Modifier name
        area: Section area modifier (`A`)
        shear_2: Local-2 shear area modifier (`As2`)
        shear_3: Local-3 shear area modifier (`As3`)
        torsion: Torsional constant modifier (`J`)
        inertia_22: Local-2 inertia modifier (`I22`)
        inertia_33: Local-3 inertia modifier (`I33`)
        mass: Mass modifier
        weight: Weight modifier
    """
    name: str = ""
    area: float = 1.0
    shear_2: float = 1.0
    shear_3: float = 1.0
    torsion: float = 1.0
    inertia_22: float = 1.0
    inertia_33: float = 1.0
    mass: float = 1.0
    weight: float = 1.0
    
    _object_type: ClassVar[str] = "NamedAssign.ModifierFrame"
    
    def to_list(self) -> List[float]:
        """Convert to the list format required by the API"""
        return [
            self.area, self.shear_2, self.shear_3, self.torsion,
            self.inertia_22, self.inertia_33, self.mass, self.weight
        ]
    
    @classmethod
    def from_list(cls, name: str, values: List[float]) -> "NamedFrameModifier":
        """Build from the list returned by the API"""
        if len(values) >= 8:
            return cls(
                name=name,
                area=values[0], shear_2=values[1], shear_3=values[2],
                torsion=values[3], inertia_22=values[4], inertia_33=values[5],
                mass=values[6], weight=values[7]
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
        return com_ret(model.NamedAssign.ModifierFrame.SetModifiers(
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
        result = model.NamedAssign.ModifierFrame.GetModifiers(
            self.name, [0.0] * 8
        )
        
        values = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and values and len(values) >= 8:
            self.area = values[0]
            self.shear_2 = values[1]
            self.shear_3 = values[2]
            self.torsion = values[3]
            self.inertia_22 = values[4]
            self.inertia_33 = values[5]
            self.mass = values[6]
            self.weight = values[7]
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
        return com_ret(model.NamedAssign.ModifierFrame.Delete(self.name))
    
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
        ret = com_ret(model.NamedAssign.ModifierFrame.ChangeName(self.name, new_name))
        if ret == 0:
            self.name = new_name
        return ret
    
    @staticmethod
    def get_count(model) -> int:
        """Get the number of modifiers"""
        return model.NamedAssign.ModifierFrame.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """Get all modifier names"""
        result = model.NamedAssign.ModifierFrame.GetNameList(0, [])
        names = com_data(result, 1)
        if names:
            return list(names)
        return []
    
    @classmethod
    def get_by_name(cls, model, name: str) -> Optional["NamedFrameModifier"]:
        """Get a modifier by name"""
        mod = cls(name=name)
        ret = mod._get(model)
        if ret == 0:
            return mod
        return None
    
    @classmethod
    def get_all(cls, model) -> List["NamedFrameModifier"]:
        """Get all modifiers"""
        names = cls.get_name_list(model)
        result = []
        for name in names:
            mod = cls.get_by_name(model, name)
            if mod:
                result.append(mod)
        return result
