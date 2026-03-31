# -*- coding: utf-8 -*-
"""
link_section.py - Link property definitions.
Wraps SAP2000 `PropLink`.

Usage:
    from section import LinkSection, LinkSectionType
    
    # Get a link property
    link = LinkSection.get_by_name(model, "L1")
    print(f"Type: {link.type_name}")
    
    # Create a linear link
    link = LinkSection(
        name="L1",
        section_type=LinkSectionType.LINEAR
    )
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, ClassVar
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class LinkSectionType(IntEnum):
    """Link property type corresponding to SAP2000 `eLinkPropType`."""
    LINEAR = 1                    # Linear
    DAMPER = 2                    # Damper
    GAP = 3                       # Gap
    HOOK = 4                      # Hook
    PLASTIC_WEN = 5               # Plastic (Wen)
    RUBBER_ISOLATOR = 6           # Rubber isolator
    FRICTION_ISOLATOR = 7         # Friction isolator
    MULTILINEAR_ELASTIC = 8       # Multilinear elastic
    MULTILINEAR_PLASTIC = 9       # Multilinear plastic
    TC_FRICTION_ISOLATOR = 10     # T/C friction isolator





# Human-readable link type names
LINK_TYPE_NAMES: Dict[LinkSectionType, str] = {
    LinkSectionType.LINEAR: "Linear",
    LinkSectionType.DAMPER: "Damper",
    LinkSectionType.GAP: "Gap",
    LinkSectionType.HOOK: "Hook",
    LinkSectionType.PLASTIC_WEN: "Plastic (Wen)",
    LinkSectionType.RUBBER_ISOLATOR: "Rubber isolator",
    LinkSectionType.FRICTION_ISOLATOR: "Friction isolator",
    LinkSectionType.MULTILINEAR_ELASTIC: "Multilinear elastic",
    LinkSectionType.MULTILINEAR_PLASTIC: "Multilinear plastic",
    LinkSectionType.TC_FRICTION_ISOLATOR: "T/C friction isolator",
}


@dataclass
class LinkSection:
    """
    Link property wrapper for SAP2000 `PropLink`.
    
    Attributes:
        name: Property name
        section_type: Property type
        type_name: Human-readable property type name
        dof: Active DOF flags `[U1, U2, U3, R1, R2, R3]`
        fixed: Fixed DOF flags
        stiffness: Effective stiffness `Ke`
        damping: Effective damping `Ce`
        dj2: Distance from U2 shear spring to the J end
        dj3: Distance from U3 shear spring to the J end
    """
    
    # Identifier
    name: str = ""
    
    # Type
    section_type: Optional[LinkSectionType] = None
    type_name: str = ""
    
    # Common properties
    dof: List[bool] = field(default_factory=lambda: [False] * 6)
    fixed: List[bool] = field(default_factory=lambda: [False] * 6)
    stiffness: List[float] = field(default_factory=lambda: [0.0] * 6)
    damping: List[float] = field(default_factory=lambda: [0.0] * 6)
    dj2: float = 0.0
    dj3: float = 0.0
    
    # Nonlinear properties
    nonlinear: List[bool] = field(default_factory=lambda: [False] * 6)
    k_initial: List[float] = field(default_factory=lambda: [0.0] * 6)
    
    # Damper properties
    c_nonlinear: List[float] = field(default_factory=lambda: [0.0] * 6)
    c_exponent: List[float] = field(default_factory=lambda: [1.0] * 6)
    
    # Gap / hook properties
    opening: List[float] = field(default_factory=lambda: [0.0] * 6)
    
    # Weight and mass properties
    weight: float = 0.0
    mass: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0
    
    # Coupling flags
    stiffness_coupled: bool = False
    damping_coupled: bool = False
    
    notes: str = ""
    guid: Optional[str] = None
    
    _object_type: ClassVar[str] = "PropLink"

    @classmethod
    def get_by_name(cls, model, name: str) -> 'LinkSection':
        """Get a link property by name."""
        prop = cls(name=name)
        prop._get(model)
        return prop
    
    @classmethod
    def get_all(cls, model) -> List['LinkSection']:
        """Get all link properties."""
        names = cls.get_name_list(model)
        return [cls.get_by_name(model, n) for n in names]
    
    @staticmethod
    def get_count(model) -> int:
        """Get the total number of link properties."""
        return model.PropLink.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """Get the list of link property names."""
        result = model.PropLink.GetNameList(0, [])
        names = com_data(result, 1)
        return list(names) if names else []

    def _get(self, model) -> 'LinkSection':
        """Load link property data from SAP2000."""
        result = model.PropLink.GetTypeOAPI(self.name)
        
        type_val = com_data(result, 0)
        ret = com_ret(result)
        if type_val is not None:
            if ret != 0:
                from PySap2000.exceptions import SectionError
                raise SectionError(f"Link property {self.name} does not exist")
            
            try:
                self.section_type = LinkSectionType(type_val)
                self.type_name = LINK_TYPE_NAMES.get(self.section_type, f"Unknown ({type_val})")
            except ValueError:
                self.section_type = None
                self.type_name = f"Unknown ({type_val})"
        
        # Load type-specific properties
        if self.section_type == LinkSectionType.LINEAR:
            self._get_linear(model)
        elif self.section_type == LinkSectionType.DAMPER:
            self._get_damper(model)
        elif self.section_type == LinkSectionType.GAP:
            self._get_gap(model)
        elif self.section_type == LinkSectionType.HOOK:
            self._get_hook(model)
        
        self._get_weight_and_mass(model)
        return self
    
    def _get_linear(self, model):
        result = model.PropLink.GetLinear(self.name)
        if com_data(result, 0) is not None:
            self.dof = list(com_data(result, 0, default=[])) or [False] * 6
            self.fixed = list(com_data(result, 1, default=[])) or [False] * 6
            self.stiffness = list(com_data(result, 2, default=[])) or [0.0] * 6
            self.damping = list(com_data(result, 3, default=[])) or [0.0] * 6
            self.dj2 = com_data(result, 4, default=0.0)
            self.dj3 = com_data(result, 5, default=0.0)
            self.stiffness_coupled = com_data(result, 6, default=False)
            self.damping_coupled = com_data(result, 7, default=False)
            self.notes = com_data(result, 8, default="") or ""
            self.guid = com_data(result, 9) or None
    
    def _get_damper(self, model):
        result = model.PropLink.GetDamper(self.name)
        if com_data(result, 0) is not None:
            self.dof = list(com_data(result, 0, default=[])) or [False] * 6
            self.fixed = list(com_data(result, 1, default=[])) or [False] * 6
            self.nonlinear = list(com_data(result, 2, default=[])) or [False] * 6
            self.stiffness = list(com_data(result, 3, default=[])) or [0.0] * 6
            self.damping = list(com_data(result, 4, default=[])) or [0.0] * 6
            self.k_initial = list(com_data(result, 5, default=[])) or [0.0] * 6
            self.c_nonlinear = list(com_data(result, 6, default=[])) or [0.0] * 6
            self.c_exponent = list(com_data(result, 7, default=[])) or [1.0] * 6
            self.dj2 = com_data(result, 8, default=0.0)
            self.dj3 = com_data(result, 9, default=0.0)
            self.notes = com_data(result, 10, default="") or ""
            self.guid = com_data(result, 11) or None
    
    def _get_gap(self, model):
        result = model.PropLink.GetGap(self.name)
        if com_data(result, 0) is not None:
            self.dof = list(com_data(result, 0, default=[])) or [False] * 6
            self.fixed = list(com_data(result, 1, default=[])) or [False] * 6
            self.nonlinear = list(com_data(result, 2, default=[])) or [False] * 6
            self.stiffness = list(com_data(result, 3, default=[])) or [0.0] * 6
            self.damping = list(com_data(result, 4, default=[])) or [0.0] * 6
            self.k_initial = list(com_data(result, 5, default=[])) or [0.0] * 6
            self.opening = list(com_data(result, 6, default=[])) or [0.0] * 6
            self.dj2 = com_data(result, 7, default=0.0)
            self.dj3 = com_data(result, 8, default=0.0)
            self.notes = com_data(result, 9, default="") or ""
            self.guid = com_data(result, 10) or None
    
    def _get_hook(self, model):
        result = model.PropLink.GetHook(self.name)
        if com_data(result, 0) is not None:
            self.dof = list(com_data(result, 0, default=[])) or [False] * 6
            self.fixed = list(com_data(result, 1, default=[])) or [False] * 6
            self.nonlinear = list(com_data(result, 2, default=[])) or [False] * 6
            self.stiffness = list(com_data(result, 3, default=[])) or [0.0] * 6
            self.damping = list(com_data(result, 4, default=[])) or [0.0] * 6
            self.k_initial = list(com_data(result, 5, default=[])) or [0.0] * 6
            self.opening = list(com_data(result, 6, default=[])) or [0.0] * 6
            self.dj2 = com_data(result, 7, default=0.0)
            self.dj3 = com_data(result, 8, default=0.0)
            self.notes = com_data(result, 9, default="") or ""
            self.guid = com_data(result, 10) or None
    
    def _get_weight_and_mass(self, model):
        result = model.PropLink.GetWeightAndMass(self.name)
        if com_data(result, 0) is not None:
            self.weight = com_data(result, 0, default=0.0)
            self.mass = com_data(result, 1, default=0.0)
            self.r1 = com_data(result, 2, default=0.0)
            self.r2 = com_data(result, 3, default=0.0)
            self.r3 = com_data(result, 4, default=0.0)

    def _create(self, model) -> int:
        """Create the link property in SAP2000."""
        from PySap2000.logger import get_logger
        _log = get_logger("link_section")
        if self.name:
            try:
                existing = self.get_name_list(model)
                if self.name in existing:
                    _log.warning(f"LinkSection '{self.name}' already exists, skipped")
                    return -1
            except Exception:
                pass
        if self.section_type == LinkSectionType.LINEAR:
            result = model.PropLink.SetLinear(
                self.name, self.dof, self.fixed, self.stiffness, self.damping,
                self.dj2, self.dj3, self.stiffness_coupled, self.damping_coupled,
                self.notes, self.guid or ""
            )
        elif self.section_type == LinkSectionType.DAMPER:
            result = model.PropLink.SetDamper(
                self.name, self.dof, self.fixed, self.nonlinear,
                self.stiffness, self.damping, self.k_initial,
                self.c_nonlinear, self.c_exponent, self.dj2, self.dj3,
                self.notes, self.guid or ""
            )
        elif self.section_type == LinkSectionType.GAP:
            result = model.PropLink.SetGap(
                self.name, self.dof, self.fixed, self.nonlinear,
                self.stiffness, self.damping, self.k_initial, self.opening,
                self.dj2, self.dj3, self.notes, self.guid or ""
            )
        elif self.section_type == LinkSectionType.HOOK:
            result = model.PropLink.SetHook(
                self.name, self.dof, self.fixed, self.nonlinear,
                self.stiffness, self.damping, self.k_initial, self.opening,
                self.dj2, self.dj3, self.notes, self.guid or ""
            )
        else:
            return -1
        return com_ret(result)
    
    def _delete(self, model) -> int:
        return model.PropLink.Delete(self.name)

