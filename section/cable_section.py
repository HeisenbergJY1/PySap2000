# -*- coding: utf-8 -*-
"""
cable_section.py - Cable section property definitions.
Wraps SAP2000 `PropCable`.

This module defines cable section properties themselves. Use the `cable`
module to assign those properties to cable objects.

Usage:
    from section import CableSection
    
    # Get a cable section
    cable = CableSection.get_by_name(model, "C1")
    print(f"Material: {cable.material}, area: {cable.area}")
    
    # Create a cable section
    cable = CableSection(name="C1", material="A416Gr270", area=0.001)
    cable._create(model)
    
    # Set modifiers
    cable.set_modifiers(model, area_modifier=1.0, mass_modifier=1.5, weight_modifier=1.5)
"""

from dataclasses import dataclass, field
from typing import Optional, List, ClassVar

from PySap2000.com_helper import com_ret, com_data


@dataclass
class CableSection:
    """
    Cable section property wrapper for SAP2000 `PropCable`.
    
    Attributes:
        name: Section name
        material: Material name
        area: Section area [L^2]
        
        # Modifiers (default `1.0`)
        area_modifier: Area modifier
        mass_modifier: Mass modifier
        weight_modifier: Weight modifier
        
        # Optional properties
        color: Display color
        notes: Notes
        guid: Globally unique identifier
    """
    
    # Identifier
    name: str = ""
    
    # Core properties
    material: str = ""
    area: float = 0.0
    
    # Modifiers (default `1.0`)
    area_modifier: float = 1.0
    mass_modifier: float = 1.0
    weight_modifier: float = 1.0
    
    # Optional properties
    color: int = -1
    notes: str = ""
    guid: Optional[str] = None
    
    # Class metadata
    _object_type: ClassVar[str] = "PropCable"

    # ==================== Public helpers ====================
    
    @classmethod
    def get_by_name(cls, model, name: str) -> 'CableSection':
        """
        Get a cable section by name.
        
        Args:
            model: SAP2000 SapModel object
            name: Section name
            
        Returns:
            Populated `CableSection` instance.
            
        Example:
            cable = CableSection.get_by_name(model, "C1")
            print(f"Area: {cable.area}")
        """
        prop = cls(name=name)
        prop._get(model)
        return prop
    
    @classmethod
    def get_all(cls, model) -> List['CableSection']:
        """
        Get all cable sections.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            List of `CableSection`.
        """
        names = cls.get_name_list(model)
        props = []
        for name in names:
            try:
                prop = cls.get_by_name(model, name)
                props.append(prop)
            except Exception:
                pass
        return props
    
    @staticmethod
    def get_count(model) -> int:
        """Get the total number of cable sections."""
        return model.PropCable.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """Get the list of cable section names."""
        result = model.PropCable.GetNameList(0, [])
        names = com_data(result, 1)
        return list(names) if names else []

    def set_modifiers(self, model, area_modifier: float = None, 
                      mass_modifier: float = None, 
                      weight_modifier: float = None) -> int:
        """
        Set cable section modifiers.
        
        Args:
            model: SAP2000 SapModel object
            area_modifier: Area modifier (default `1.0`)
            mass_modifier: Mass modifier (default `1.0`)
            weight_modifier: Weight modifier (default `1.0`)
            
        Returns:
            `0` if successful, non-zero otherwise.
        """
        if area_modifier is not None:
            self.area_modifier = area_modifier
        if mass_modifier is not None:
            self.mass_modifier = mass_modifier
        if weight_modifier is not None:
            self.weight_modifier = weight_modifier
        
        modifiers = [self.area_modifier, self.mass_modifier, self.weight_modifier]
        return model.PropCable.SetModifiers(self.name, modifiers)
    
    def get_modifiers(self, model) -> 'CableSection':
        """Get cable section modifiers."""
        result = model.PropCable.GetModifiers(self.name, [0.0, 0.0, 0.0])
        modifiers = com_data(result, 0)
        if isinstance(modifiers, (list, tuple)) and len(modifiers) >= 3:
            self.area_modifier = modifiers[0]
            self.mass_modifier = modifiers[1]
            self.weight_modifier = modifiers[2]
        return self
    
    def change_name(self, model, new_name: str) -> int:
        """Rename the cable section."""
        ret = model.PropCable.ChangeName(self.name, new_name)
        if ret == 0:
            self.name = new_name
        return ret

    # ==================== Internal helpers ====================
    
    def _get(self, model) -> 'CableSection':
        """Load cable section data from SAP2000."""
        result = model.PropCable.GetProp(self.name)
        
        if com_data(result, 0) is not None and com_data(result, 5) is not None:
            self.material = com_data(result, 0, default="") or ""
            self.area = com_data(result, 1, default=0.0)
            self.color = com_data(result, 2, default=-1)
            self.notes = com_data(result, 3, default="") or ""
            self.guid = com_data(result, 4) or None
            ret = com_data(result, 5, default=-1)
            
            if ret != 0:
                from PySap2000.exceptions import SectionError
                raise SectionError(f"Cable section {self.name} does not exist")
        else:
            from PySap2000.exceptions import SectionError
            raise SectionError(f"Failed to get cable section {self.name}")
        
        self.get_modifiers(model)
        return self
    
    def _create(self, model) -> int:
        """Create the cable section in SAP2000."""
        from PySap2000.logger import get_logger
        _log = get_logger("cable_section")
        if self.name:
            try:
                existing = self.get_name_list(model)
                if self.name in existing:
                    _log.warning(f"CableSection '{self.name}' already exists, skipped")
                    return -1
            except Exception:
                pass
        if self.material:
            result = model.PropMaterial.GetNameList(0, [])
            mat_names_data = com_data(result, 1)
            mat_names = list(mat_names_data) if mat_names_data else []
            if self.material not in mat_names:
                _log.warning(f"Material '{self.material}' not found")
        
        return model.PropCable.SetProp(
            self.name, self.material, self.area,
            self.color, self.notes, self.guid or ""
        )
    
    def _delete(self, model) -> int:
        """Delete the cable section."""
        return model.PropCable.Delete(self.name)
    
    def _update(self, model) -> int:
        """Update the cable section."""
        return self._create(model)

    @property
    def standard_name(self) -> str:
        """
        Get a normalized section name.
        
        Cable sections use an equivalent diameter naming style:
        - `CAB32` means an equivalent diameter of about 32 mm
        
        Note: Call this when units are `N-mm-C` so `area` is in mm^2.
        
        Returns:
            Normalized section name.
            
        Example:
            cable = CableSection.get_by_name(model, "Cable1")
            print(cable.standard_name)  # "Φ32"
        """
        import math
        
        if self.area > 0:
            # Compute equivalent diameter from area (assuming a circular section).
            # area = π * (d/2)² => d = 2 * sqrt(area / π)
            diameter = 2 * math.sqrt(self.area / math.pi)
            return f"CAB{diameter:.0f}"
        
        # If area is zero, return the original name.
        return self.name
