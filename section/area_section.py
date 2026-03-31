# -*- coding: utf-8 -*-
"""
area_section.py - Area section property definitions.
Wraps SAP2000 `PropArea`.

This module defines area section properties themselves rather than assigning
them to area objects. Use the `area` module for section assignments.

Includes three property families:
- `Shell`: thin shell, thick shell, thin plate, thick plate, membrane, layered shell
- `Plane`: plane stress and plane strain
- `Asolid`: axisymmetric solid

Usage:
    from section import AreaSection, AreaSectionType, ShellType
    
    # Get an area property
    prop = AreaSection.get_by_name(model, "SLAB1")
    print(f"Type: {prop.prop_type}, thickness: {prop.membrane_thickness}")
    
    # Create a shell section
    shell = AreaSection(
        name="SLAB1",
        shell_type=ShellType.SHELL_THIN,
        material="4000Psi",
        membrane_thickness=0.2
    )
    shell._create(model)
"""

from dataclasses import dataclass, field
from typing import Optional, List, ClassVar
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class AreaSectionType(IntEnum):
    """Area property type used by `GetNameList(..., PropType)`."""
    ALL = 0
    SHELL = 1
    PLANE = 2
    ASOLID = 3


class ShellType(IntEnum):
    """Shell type used by `GetShell_1(..., ShellType)`."""
    SHELL_THIN = 1
    SHELL_THICK = 2
    PLATE_THIN = 3
    PLATE_THICK = 4
    MEMBRANE = 5
    SHELL_LAYERED = 6


class PlaneType(IntEnum):
    """Plane type used by `GetPlane(..., MyType)`."""
    PLANE_STRESS = 1
    PLANE_STRAIN = 2


@dataclass
class AreaModifiers:
    """Area property modifiers (10 values)."""
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
    
    def to_list(self) -> List[float]:
        """Return modifiers as a list."""
        return [self.f11, self.f22, self.f12, self.m11, self.m22, 
                self.m12, self.v13, self.v23, self.mass, self.weight]
    
    @classmethod
    def from_list(cls, values: List[float]) -> 'AreaModifiers':
        """Build modifiers from a list."""
        if len(values) >= 10:
            return cls(
                f11=values[0], f22=values[1], f12=values[2],
                m11=values[3], m22=values[4], m12=values[5],
                v13=values[6], v23=values[7],
                mass=values[8], weight=values[9]
            )
        return cls()


@dataclass
class AreaSection:
    """Area section property wrapper for SAP2000 `PropArea`."""
    
    name: str = ""
    prop_type: Optional[AreaSectionType] = None
    shell_type: Optional[ShellType] = None
    plane_type: Optional[PlaneType] = None
    material: str = ""
    membrane_thickness: float = 0.0
    bending_thickness: float = 0.0
    material_angle: float = 0.0
    include_drilling_dof: bool = False
    incompatible_modes: bool = True
    arc_angle: float = 360.0
    color: int = -1
    notes: str = ""
    guid: Optional[str] = None
    _object_type: ClassVar[str] = "PropArea"

    @classmethod
    def get_by_name(cls, model, name: str) -> 'AreaSection':
        """Get an area property by name."""
        prop = cls(name=name)
        prop._get(model)
        return prop
    
    @classmethod
    def get_all(cls, model, prop_type: AreaSectionType = AreaSectionType.ALL) -> List['AreaSection']:
        """Get all area properties."""
        names = cls.get_name_list(model, prop_type)
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
        """Get the total number of area properties."""
        return model.PropArea.Count()
    
    @staticmethod
    def get_name_list(model, prop_type: AreaSectionType = AreaSectionType.ALL) -> List[str]:
        """Get the list of area property names."""
        result = model.PropArea.GetNameList(0, [], prop_type.value)
        names = com_data(result, 1)
        return list(names) if names else []
    
    def change_name(self, model, new_name: str) -> int:
        """Rename the property."""
        ret = model.PropArea.ChangeName(self.name, new_name)
        if ret == 0:
            self.name = new_name
        return ret
    
    def get_modifiers(self, model) -> AreaModifiers:
        """Get property modifiers."""
        result = model.PropArea.GetModifiers(self.name, [])
        values = com_data(result, 0)
        if values and len(values) >= 10:
            return AreaModifiers.from_list(list(values))
        return AreaModifiers()
    
    def set_modifiers(self, model, modifiers: AreaModifiers) -> int:
        """Set property modifiers."""
        return model.PropArea.SetModifiers(self.name, modifiers.to_list())

    def _get(self, model) -> 'AreaSection':
        """Load area property data from SAP2000."""
        result = model.PropArea.GetTypeOAPI(self.name)
        type_val = com_data(result, 0)
        ret = com_ret(result)
        if type_val is None:
            from PySap2000.exceptions import SectionError
            raise SectionError(f"Failed to get type for area property {self.name}")
        if ret != 0:
            from PySap2000.exceptions import SectionError
            raise SectionError(f"Area property {self.name} does not exist")
        try:
            self.prop_type = AreaSectionType(type_val)
        except ValueError:
            self.prop_type = AreaSectionType.SHELL
        
        if self.prop_type == AreaSectionType.SHELL:
            self._get_shell(model)
        elif self.prop_type == AreaSectionType.PLANE:
            self._get_plane(model)
        elif self.prop_type == AreaSectionType.ASOLID:
            self._get_asolid(model)
        return self
    
    def _get_shell(self, model):
        """Load shell property data."""
        result = model.PropArea.GetShell_1(self.name)
        if com_data(result, 0) is not None:
            try:
                self.shell_type = ShellType(com_data(result, 0))
            except ValueError:
                self.shell_type = ShellType.SHELL_THIN
            self.include_drilling_dof = com_data(result, 1, default=False)
            self.material = com_data(result, 2, default="") or ""
            self.material_angle = com_data(result, 3, default=0.0)
            self.membrane_thickness = com_data(result, 4, default=0.0)
            self.bending_thickness = com_data(result, 5, default=0.0)
            self.color = com_data(result, 6, default=-1)
            self.notes = com_data(result, 7, default="") or ""
            self.guid = com_data(result, 8) or None
    
    def _get_plane(self, model):
        """Load plane property data."""
        result = model.PropArea.GetPlane(self.name)
        if com_data(result, 0) is not None:
            try:
                self.plane_type = PlaneType(com_data(result, 0))
            except ValueError:
                self.plane_type = PlaneType.PLANE_STRESS
            self.material = com_data(result, 1, default="") or ""
            self.material_angle = com_data(result, 2, default=0.0)
            self.membrane_thickness = com_data(result, 3, default=0.0)
            self.incompatible_modes = com_data(result, 4, default=True)
            self.color = com_data(result, 5, default=-1)
            self.notes = com_data(result, 6, default="") or ""
            self.guid = com_data(result, 7) or None
    
    def _get_asolid(self, model):
        """Load axisymmetric solid property data."""
        result = model.PropArea.GetAsolid(self.name)
        if com_data(result, 0) is not None:
            self.material = com_data(result, 0, default="") or ""
            self.material_angle = com_data(result, 1, default=0.0)
            self.arc_angle = com_data(result, 2, default=360.0)
            self.incompatible_modes = com_data(result, 3, default=True)
            self.color = com_data(result, 4, default=-1)
            self.notes = com_data(result, 5, default="") or ""
            self.guid = com_data(result, 6) or None

    def _create(self, model) -> int:
        """Create the area property in SAP2000."""
        from PySap2000.logger import get_logger
        _log = get_logger("area_section")
        if self.name:
            try:
                existing = self.get_name_list(model)
                if self.name in existing:
                    _log.warning(f"AreaSection '{self.name}' already exists, skipped")
                    return -1
            except Exception:
                pass
        if self.shell_type is not None:
            return self._create_shell(model)
        elif self.plane_type is not None:
            return self._create_plane(model)
        elif self.prop_type == AreaSectionType.ASOLID:
            return self._create_asolid(model)
        else:
            self.shell_type = ShellType.SHELL_THIN
            return self._create_shell(model)
    
    def _create_shell(self, model) -> int:
        """Create a shell property."""
        return model.PropArea.SetShell_1(
            self.name,
            self.shell_type.value if self.shell_type else ShellType.SHELL_THIN.value,
            self.include_drilling_dof,
            self.material,
            self.material_angle,
            self.membrane_thickness,
            self.bending_thickness or self.membrane_thickness,
            self.color,
            self.notes,
            self.guid or ""
        )
    
    def _create_plane(self, model) -> int:
        """Create a plane property."""
        return model.PropArea.SetPlane(
            self.name,
            self.plane_type.value if self.plane_type else PlaneType.PLANE_STRESS.value,
            self.material,
            self.material_angle,
            self.membrane_thickness,
            self.incompatible_modes,
            self.color,
            self.notes,
            self.guid or ""
        )
    
    def _create_asolid(self, model) -> int:
        """Create an axisymmetric solid property."""
        return model.PropArea.SetAsolid(
            self.name,
            self.material,
            self.material_angle,
            self.arc_angle,
            self.incompatible_modes,
            self.color,
            self.notes,
            self.guid or ""
        )
    
    def _delete(self, model) -> int:
        """Delete the area property."""
        return model.PropArea.Delete(self.name)
    
    def _update(self, model) -> int:
        """Update the area property."""
        return self._create(model)
