# -*- coding: utf-8 -*-
"""
frame_section.py - Frame section property definitions.
Wraps SAP2000 `PropFrame`.

This module defines frame section properties themselves rather than assigning
them to frame objects. Use the `frame` module for section assignments.

Usage:
    from section import FrameSection, FrameSectionType
    
    # Get a section
    section = FrameSection.get_by_name(model, "W14X22")
    print(f"Type: {section.type_name}, material: {section.material}")
    
    # Create a rectangular section
    rect = FrameSection(
        name="R1",
        property_type=FrameSectionType.RECTANGULAR,
        material="4000Psi",
        height=0.5,
        width=0.3
    )
    rect._create(model)
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, ClassVar
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class FrameSectionType(IntEnum):
    """Frame section type corresponding to SAP2000 `eFramePropType`."""
    I_SECTION = 1
    CHANNEL = 2
    T_SECTION = 3
    ANGLE = 4
    DOUBLE_ANGLE = 5
    BOX = 6
    PIPE = 7
    RECTANGULAR = 8
    CIRCLE = 9
    GENERAL = 10
    DOUBLE_CHANNEL = 11
    SD = 13
    VARIABLE = 14
    COLD_C = 17
    COLD_Z = 19
    COLD_L = 20
    COLD_HAT = 22
    BUILTUP_I_COVERPLATE = 23
    PRECAST_I = 24
    PRECAST_U = 25


SECTION_TYPE_NAMES: Dict[FrameSectionType, str] = {
    FrameSectionType.I_SECTION: "I-section",
    FrameSectionType.CHANNEL: "Channel",
    FrameSectionType.T_SECTION: "T-section",
    FrameSectionType.ANGLE: "Angle",
    FrameSectionType.DOUBLE_ANGLE: "Double angle",
    FrameSectionType.BOX: "Box",
    FrameSectionType.PIPE: "Pipe",
    FrameSectionType.RECTANGULAR: "Rectangular",
    FrameSectionType.CIRCLE: "Circle",
    FrameSectionType.GENERAL: "General",
    FrameSectionType.DOUBLE_CHANNEL: "Double channel",
    FrameSectionType.SD: "Section Designer",
    FrameSectionType.VARIABLE: "Variable",
    FrameSectionType.COLD_C: "Cold-formed C",
    FrameSectionType.COLD_Z: "Cold-formed Z",
    FrameSectionType.COLD_L: "Cold-formed L",
    FrameSectionType.COLD_HAT: "Cold-formed hat",
    FrameSectionType.BUILTUP_I_COVERPLATE: "Built-up I with cover plate",
    FrameSectionType.PRECAST_I: "Precast I girder",
    FrameSectionType.PRECAST_U: "Precast U girder",
}


@dataclass
class FrameSection:
    """Frame section property wrapper for SAP2000 `PropFrame`."""
    
    name: str = ""
    property_type: Optional[FrameSectionType] = None
    type_name: str = ""
    material: str = ""
    height: float = 0.0
    width: float = 0.0
    flange_thickness: float = 0.0
    web_thickness: float = 0.0
    bottom_flange_width: float = 0.0
    bottom_flange_thickness: float = 0.0
    fillet_radius: float = 0.0
    outer_diameter: float = 0.0
    wall_thickness: float = 0.0
    back_to_back_distance: float = 0.0
    mirror_about_2: bool = False
    mirror_about_3: bool = False
    color: int = -1
    notes: str = ""
    guid: Optional[str] = None
    file_name: str = ""
    
    # Nonprismatic section properties
    np_num_segments: int = 0                          # Number of nonprismatic segments
    np_start_secs: List[str] = field(default_factory=list)   # Start section name for each segment
    np_end_secs: List[str] = field(default_factory=list)     # End section name for each segment
    np_lengths: List[float] = field(default_factory=list)    # Segment lengths
    np_length_types: List[int] = field(default_factory=list) # Length type (1=variable, 2=absolute)
    np_ei33: List[int] = field(default_factory=list)         # EI33 variation (1=linear, 2=parabolic, 3=cubic)
    np_ei22: List[int] = field(default_factory=list)         # EI22 variation
    
    # Section properties from `GetSectProps`
    area: float = 0.0           # Area [L^2]
    as2: float = 0.0            # Shear area about local-2 [L^2]
    as3: float = 0.0            # Shear area about local-3 [L^2]
    torsion: float = 0.0        # Torsional constant [L^4]
    i22: float = 0.0            # Moment of inertia about local-2 [L^4]
    i33: float = 0.0            # Moment of inertia about local-3 [L^4]
    s22: float = 0.0            # Section modulus about local-2 [L^3]
    s33: float = 0.0            # Section modulus about local-3 [L^3]
    z22: float = 0.0            # Plastic modulus about local-2 [L^3]
    z33: float = 0.0            # Plastic modulus about local-3 [L^3]
    r22: float = 0.0            # Radius of gyration about local-2 [L]
    r33: float = 0.0            # Radius of gyration about local-3 [L]
    
    # Computed unit weight
    _weight_per_meter: float = 0.0
    
    _object_type: ClassVar[str] = "PropFrame"
    
    @property
    def weight_per_meter(self) -> float:
        """Unit weight per length in `kg/m`."""
        return self._weight_per_meter

    @classmethod
    def get_by_name(cls, model, name: str) -> 'FrameSection':
        """Get a section by name."""
        prop = cls(name=name)
        prop._get(model)
        return prop

    @classmethod
    def get_all(cls, model) -> List['FrameSection']:
        """Get all sections."""
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
        """Get the total number of sections."""
        return model.PropFrame.Count()
    
    @staticmethod
    def get_name_list(model, property_type: FrameSectionType = None) -> List[str]:
        """Get the list of section names."""
        if property_type is not None:
            result = model.PropFrame.GetNameList(property_type.value)
        else:
            result = model.PropFrame.GetNameList()
        names = com_data(result, 1)
        return list(names) if names else []

    def _get(self, model) -> 'FrameSection':
        """Load section data from SAP2000."""
        result = model.PropFrame.GetTypeOAPI(self.name)
        type_val = com_data(result, 0)
        ret = com_ret(result)
        if type_val is None:
            from PySap2000.exceptions import SectionError
            raise SectionError(f"Failed to get section type for {self.name}")
        if ret != 0:
            from PySap2000.exceptions import SectionError
            raise SectionError(f"Section {self.name} does not exist")
        try:
            self.property_type = FrameSectionType(type_val)
            self.type_name = SECTION_TYPE_NAMES.get(self.property_type, f"Unknown type ({type_val})")
        except ValueError:
            self.property_type = None
            self.type_name = f"Unknown type ({type_val})"
        self._get_properties_by_type(model)
        # If material is empty, try a generic fallback getter.
        if not self.material:
            self._get_material_fallback(model)
        # Load section properties.
        self._get_sect_props(model)
        # Compute unit weight.
        self._calculate_weight_per_meter(model)
        return self
    
    def _get_properties_by_type(self, model):
        """Load type-specific properties."""
        if self.property_type == FrameSectionType.RECTANGULAR:
            self._get_rectangle(model)
        elif self.property_type == FrameSectionType.CIRCLE:
            self._get_circle(model)
        elif self.property_type == FrameSectionType.PIPE:
            self._get_pipe(model)
        elif self.property_type == FrameSectionType.BOX:
            self._get_box(model)
        elif self.property_type == FrameSectionType.I_SECTION:
            self._get_isection(model)
        elif self.property_type == FrameSectionType.ANGLE:
            self._get_angle(model)
        elif self.property_type == FrameSectionType.CHANNEL:
            self._get_channel(model)
        elif self.property_type == FrameSectionType.T_SECTION:
            self._get_tee(model)
        elif self.property_type == FrameSectionType.DOUBLE_ANGLE:
            self._get_dbl_angle(model)
        elif self.property_type == FrameSectionType.DOUBLE_CHANNEL:
            self._get_dbl_channel(model)
        elif self.property_type == FrameSectionType.GENERAL:
            self._get_general(model)
        elif self.property_type == FrameSectionType.SD:
            self._get_sd_section(model)
        elif self.property_type == FrameSectionType.VARIABLE:
            self._get_nonprismatic(model)

    def _get_sect_props(self, model) -> None:
        """
        Load section properties from SAP2000.

        Calls `PropFrame.GetSectProps` to obtain area, inertia, and related properties.
        """
        try:
            result = model.PropFrame.GetSectProps(
                self.name, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            )
            if com_data(result, 0) is not None:
                self.area = com_data(result, 0, default=0.0)
                self.as2 = com_data(result, 1, default=0.0)
                self.as3 = com_data(result, 2, default=0.0)
                self.torsion = com_data(result, 3, default=0.0)
                self.i22 = com_data(result, 4, default=0.0)
                self.i33 = com_data(result, 5, default=0.0)
                self.s22 = com_data(result, 6, default=0.0)
                self.s33 = com_data(result, 7, default=0.0)
                self.z22 = com_data(result, 8, default=0.0)
                self.z33 = com_data(result, 9, default=0.0)
                self.r22 = com_data(result, 10, default=0.0)
                self.r33 = com_data(result, 11, default=0.0)
        except Exception:
            # Keep default values if the API call fails.
            pass

    def _calculate_weight_per_meter(self, model) -> float:
        """
        Compute unit weight per length in `kg/m`.
        
        weight_per_meter = area × density
        
        If the current units are not `N-m-C`, units are switched temporarily.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            Unit weight per length in `kg/m`, or `0.0` if the material is unavailable.
        """
        if not self.material:
            self._weight_per_meter = 0.0
            return 0.0
        
        try:
            from PySap2000.global_parameters.units import Units, UnitSystem
            
            current_units = Units.get_present_units(model)
            need_switch = current_units != UnitSystem.N_M_C
            
            if need_switch:
                Units.set_present_units(model, UnitSystem.N_M_C)
            
            try:
                # Get section area in m^2.
                result = model.PropFrame.GetSectProps(
                    self.name, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0
                )
                area_m2 = com_data(result, 0, default=0.0)
                
                # Get material density in kg/m^3.
                result = model.PropMaterial.GetWeightAndMass(self.material)
                density_kg_m3 = com_data(result, 1, default=0.0)
                
                if area_m2 > 0 and density_kg_m3 > 0:
                    self._weight_per_meter = area_m2 * density_kg_m3
                else:
                    self._weight_per_meter = 0.0
            finally:
                if need_switch:
                    Units.set_present_units(model, current_units)
            
        except Exception:
            self._weight_per_meter = 0.0
        
        return self._weight_per_meter

    def _get_rectangle(self, model):
        result = model.PropFrame.GetRectangle(self.name)
        if com_data(result, 0) is not None:
            self.file_name = com_data(result, 0, default="") or ""
            self.material = com_data(result, 1, default="") or ""
            self.height = com_data(result, 2, default=0.0)
            self.width = com_data(result, 3, default=0.0)
            self.color = com_data(result, 4, default=-1)
            self.notes = com_data(result, 5, default="") or ""
            self.guid = com_data(result, 6) or None
    
    def _get_circle(self, model):
        result = model.PropFrame.GetCircle(self.name)
        if com_data(result, 0) is not None:
            self.file_name = com_data(result, 0, default="") or ""
            self.material = com_data(result, 1, default="") or ""
            self.outer_diameter = com_data(result, 2, default=0.0)
            self.color = com_data(result, 3, default=-1)
            self.notes = com_data(result, 4, default="") or ""
            self.guid = com_data(result, 5) or None
    
    def _get_pipe(self, model):
        result = model.PropFrame.GetPipe(self.name)
        if com_data(result, 0) is not None:
            self.file_name = com_data(result, 0, default="") or ""
            self.material = com_data(result, 1, default="") or ""
            self.outer_diameter = com_data(result, 2, default=0.0)
            self.wall_thickness = com_data(result, 3, default=0.0)
            self.color = com_data(result, 4, default=-1)
            self.notes = com_data(result, 5, default="") or ""
            self.guid = com_data(result, 6) or None

    def _get_box(self, model):
        result = model.PropFrame.GetTube_1(self.name)
        if com_data(result, 0) is not None:
            self.file_name = com_data(result, 0, default="") or ""
            self.material = com_data(result, 1, default="") or ""
            self.height = com_data(result, 2, default=0.0)
            self.width = com_data(result, 3, default=0.0)
            self.flange_thickness = com_data(result, 4, default=0.0)
            self.web_thickness = com_data(result, 5, default=0.0)
            self.bottom_flange_thickness = com_data(result, 6, default=0.0)
            self.color = com_data(result, 7, default=-1)
            self.notes = com_data(result, 8, default="") or ""
            self.guid = com_data(result, 9) or None
    
    def _get_isection(self, model):
        result = model.PropFrame.GetISection_1(self.name)
        if com_data(result, 0) is not None:
            self.file_name = com_data(result, 0, default="") or ""
            self.material = com_data(result, 1, default="") or ""
            self.height = com_data(result, 2, default=0.0)
            self.width = com_data(result, 3, default=0.0)
            self.flange_thickness = com_data(result, 4, default=0.0)
            self.web_thickness = com_data(result, 5, default=0.0)
            self.bottom_flange_width = com_data(result, 6, default=0.0)
            self.bottom_flange_thickness = com_data(result, 7, default=0.0)
            self.fillet_radius = com_data(result, 8, default=0.0)
            self.color = com_data(result, 9, default=-1)
            self.notes = com_data(result, 10, default="") or ""
            self.guid = com_data(result, 11) or None

    def _get_angle(self, model):
        result = model.PropFrame.GetAngle_1(self.name)
        if com_data(result, 0) is not None:
            self.file_name = com_data(result, 0, default="") or ""
            self.material = com_data(result, 1, default="") or ""
            self.height = com_data(result, 2, default=0.0)
            self.width = com_data(result, 3, default=0.0)
            self.flange_thickness = com_data(result, 4, default=0.0)
            self.web_thickness = com_data(result, 5, default=0.0)
            self.fillet_radius = com_data(result, 6, default=0.0)
            self.color = com_data(result, 7, default=-1)
            self.notes = com_data(result, 8, default="") or ""
            self.guid = com_data(result, 9) or None

    def _get_channel(self, model):
        result = model.PropFrame.GetChannel_2(self.name)
        if com_data(result, 0) is not None:
            self.file_name = com_data(result, 0, default="") or ""
            self.material = com_data(result, 1, default="") or ""
            self.height = com_data(result, 2, default=0.0)
            self.width = com_data(result, 3, default=0.0)
            self.flange_thickness = com_data(result, 4, default=0.0)
            self.web_thickness = com_data(result, 5, default=0.0)
            self.fillet_radius = com_data(result, 6, default=0.0)
            self.mirror_about_2 = com_data(result, 7, default=False)
            self.color = com_data(result, 8, default=-1)
            self.notes = com_data(result, 9, default="") or ""
            self.guid = com_data(result, 10) or None

    def _get_tee(self, model):
        result = model.PropFrame.GetTee_1(self.name)
        if com_data(result, 0) is not None:
            self.file_name = com_data(result, 0, default="") or ""
            self.material = com_data(result, 1, default="") or ""
            self.height = com_data(result, 2, default=0.0)
            self.width = com_data(result, 3, default=0.0)
            self.flange_thickness = com_data(result, 4, default=0.0)
            self.web_thickness = com_data(result, 5, default=0.0)
            self.fillet_radius = com_data(result, 6, default=0.0)
            self.mirror_about_3 = com_data(result, 7, default=False)
            self.color = com_data(result, 8, default=-1)
            self.notes = com_data(result, 9, default="") or ""
            self.guid = com_data(result, 10) or None

    def _get_dbl_angle(self, model):
        result = model.PropFrame.GetDblAngle_2(self.name)
        if com_data(result, 0) is not None:
            self.file_name = com_data(result, 0, default="") or ""
            self.material = com_data(result, 1, default="") or ""
            self.height = com_data(result, 2, default=0.0)
            self.width = com_data(result, 3, default=0.0)
            self.flange_thickness = com_data(result, 4, default=0.0)
            self.web_thickness = com_data(result, 5, default=0.0)
            self.back_to_back_distance = com_data(result, 6, default=0.0)
            self.fillet_radius = com_data(result, 7, default=0.0)
            self.mirror_about_3 = com_data(result, 8, default=False)
            self.color = com_data(result, 9, default=-1)
            self.notes = com_data(result, 10, default="") or ""
            self.guid = com_data(result, 11) or None

    def _get_dbl_channel(self, model):
        result = model.PropFrame.GetDblChannel_1(self.name)
        if com_data(result, 0) is not None:
            self.file_name = com_data(result, 0, default="") or ""
            self.material = com_data(result, 1, default="") or ""
            self.height = com_data(result, 2, default=0.0)
            self.width = com_data(result, 3, default=0.0)
            self.flange_thickness = com_data(result, 4, default=0.0)
            self.web_thickness = com_data(result, 5, default=0.0)
            self.back_to_back_distance = com_data(result, 6, default=0.0)
            self.fillet_radius = com_data(result, 7, default=0.0)
            self.color = com_data(result, 8, default=-1)
            self.notes = com_data(result, 9, default="") or ""
            self.guid = com_data(result, 10) or None

    def _get_general(self, model):
        """Load a `GENERAL` section."""
        try:
            result = model.PropFrame.GetGeneral(
                self.name, "", "", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "", ""
            )
            if com_data(result, 0) is not None:
                self.file_name = com_data(result, 0, default="") or ""
                self.material = com_data(result, 1, default="") or ""
                self.height = com_data(result, 2, default=0.0)
                self.width = com_data(result, 3, default=0.0)
        except Exception:
            pass

    def _get_sd_section(self, model):
        """Load an `SD` (Section Designer) section."""
        try:
            # Section Designer sections use `GetSDSection` for basic info.
            # GetSDSection(Name, MatProp, NumberItems, ShapeName[], MyType[], DesignType, Color, Notes, GUID)
            result = model.PropFrame.GetSDSection(
                self.name, "", 0, [], [], 0, 0, "", ""
            )
            mat = com_data(result, 0)
            if mat is not None:
                self.material = mat or ""  # `MatProp` is at index 0.
                # `NumberItems` is at index 1; the rest follow.
        except Exception:
            # Fall back to the generic material getter.
            self._get_material_fallback(model)

    def _get_nonprismatic(self, model):
        """
        Load a nonprismatic section.
        
        API: PropFrame.GetNonPrismatic(Name, NumberItems, StartSec[], EndSec[],
             MyLength[], MyType[], EI33[], EI22[], Color, Notes, GUID)
        """
        try:
            result = model.PropFrame.GetNonPrismatic(
                self.name, 0, [], [], [], [], [], [], 0, "", ""
            )
            if com_data(result, 0) is not None:
                self.np_num_segments = com_data(result, 0, default=0)
                self.np_start_secs = list(com_data(result, 1, default=[])) if com_data(result, 1) else []
                self.np_end_secs = list(com_data(result, 2, default=[])) if com_data(result, 2) else []
                self.np_lengths = list(com_data(result, 3, default=[])) if com_data(result, 3) else []
                self.np_length_types = list(com_data(result, 4, default=[])) if com_data(result, 4) else []
                self.np_ei33 = list(com_data(result, 5, default=[])) if com_data(result, 5) else []
                self.np_ei22 = list(com_data(result, 6, default=[])) if com_data(result, 6) else []
                
                # Try to inherit the material from the first start section.
                if self.np_start_secs and not self.material:
                    try:
                        sub = FrameSection.get_by_name(model, self.np_start_secs[0])
                        self.material = sub.material
                    except Exception:
                        pass
        except Exception:
            self._get_material_fallback(model)

    def _get_material_fallback(self, model):
        """Generic last-resort material getter."""
        # Try multiple APIs to recover the material name.
        methods = [
            # Method 1: `GetGeneral` for GENERAL sections.
            lambda: model.PropFrame.GetGeneral(
                self.name, "", "", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "", ""
            ),
            # Method 2: `GetSDSection` for Section Designer sections.
            lambda: model.PropFrame.GetSDSection(
                self.name, "", 0, [], [], 0, 0, "", ""
            ),
        ]
        
        for method in methods:
            try:
                result = method()
                mat_1 = com_data(result, 1)
                mat_0 = com_data(result, 0)
                mat = mat_1 if mat_1 else (mat_0 if mat_0 else "")
                if mat and isinstance(mat, str) and mat.strip():
                    self.material = mat
                    return
            except Exception:
                continue

    def _create(self, model) -> int:
        """Create the section in SAP2000."""
        from PySap2000.logger import get_logger
        _log = get_logger("frame_section")
        if self.name:
            try:
                existing = self.get_name_list(model)
                if self.name in existing:
                    _log.warning(f"FrameSection '{self.name}' already exists, skipped")
                    return -1
            except Exception:
                pass
        if self.property_type is None:
            from PySap2000.exceptions import SectionError
            raise SectionError("Section property_type is required")
        if self.property_type == FrameSectionType.RECTANGULAR:
            return self._create_rectangle(model)
        elif self.property_type == FrameSectionType.CIRCLE:
            return self._create_circle(model)
        elif self.property_type == FrameSectionType.PIPE:
            return self._create_pipe(model)
        elif self.property_type == FrameSectionType.BOX:
            return self._create_box(model)
        elif self.property_type == FrameSectionType.I_SECTION:
            return self._create_isection(model)
        elif self.property_type == FrameSectionType.ANGLE:
            return self._create_angle(model)
        elif self.property_type == FrameSectionType.CHANNEL:
            return self._create_channel(model)
        elif self.property_type == FrameSectionType.T_SECTION:
            return self._create_tee(model)
        elif self.property_type == FrameSectionType.DOUBLE_ANGLE:
            return self._create_dbl_angle(model)
        elif self.property_type == FrameSectionType.DOUBLE_CHANNEL:
            return self._create_dbl_channel(model)
        elif self.property_type == FrameSectionType.VARIABLE:
            return self._create_nonprismatic(model)
        else:
            from PySap2000.exceptions import SectionError
            raise SectionError(f"Unsupported section type for creation: {self.property_type.name}")
    
    def _create_rectangle(self, model) -> int:
        return model.PropFrame.SetRectangle(
            self.name, self.material, self.height, self.width,
            self.color, self.notes, self.guid or "")
    
    def _create_circle(self, model) -> int:
        return model.PropFrame.SetCircle(
            self.name, self.material, self.outer_diameter,
            self.color, self.notes, self.guid or "")
    
    def _create_pipe(self, model) -> int:
        return model.PropFrame.SetPipe(
            self.name, self.material, self.outer_diameter, self.wall_thickness,
            self.color, self.notes, self.guid or "")

    def _create_box(self, model) -> int:
        return model.PropFrame.SetTube_1(
            self.name, self.material, self.height, self.width,
            self.flange_thickness, self.web_thickness, self.flange_thickness,
            self.color, self.notes, self.guid or "")
    
    def _create_isection(self, model) -> int:
        t2b = self.bottom_flange_width or self.width
        tfb = self.bottom_flange_thickness or self.flange_thickness
        return model.PropFrame.SetISection_1(
            self.name, self.material, self.height, self.width,
            self.flange_thickness, self.web_thickness, t2b, tfb, self.fillet_radius,
            self.color, self.notes, self.guid or "")

    def _create_angle(self, model) -> int:
        return model.PropFrame.SetAngle_1(
            self.name, self.material, self.height, self.width,
            self.flange_thickness, self.web_thickness, self.fillet_radius,
            self.color, self.notes, self.guid or "")

    def _create_channel(self, model) -> int:
        return model.PropFrame.SetChannel_2(
            self.name, self.material, self.height, self.width,
            self.flange_thickness, self.web_thickness, self.fillet_radius, self.mirror_about_2,
            self.color, self.notes, self.guid or "")

    def _create_tee(self, model) -> int:
        return model.PropFrame.SetTee_1(
            self.name, self.material, self.height, self.width,
            self.flange_thickness, self.web_thickness, self.fillet_radius, self.mirror_about_3,
            self.color, self.notes, self.guid or "")

    def _create_dbl_angle(self, model) -> int:
        return model.PropFrame.SetDblAngle_2(
            self.name, self.material, self.height, self.width,
            self.flange_thickness, self.web_thickness, self.back_to_back_distance, self.fillet_radius,
            self.mirror_about_3, self.color, self.notes, self.guid or "")

    def _create_dbl_channel(self, model) -> int:
        return model.PropFrame.SetDblChannel_1(
            self.name, self.material, self.height, self.width,
            self.flange_thickness, self.web_thickness, self.back_to_back_distance, self.fillet_radius,
            self.color, self.notes, self.guid or "")
    
    def _create_nonprismatic(self, model) -> int:
        """
        Create a nonprismatic section.
        
        API: PropFrame.SetNonPrismatic(Name, NumberItems, StartSec[], EndSec[],
             MyLength[], MyType[], EI33[], EI22[])
        """
        if not self.np_start_secs or not self.np_end_secs:
            from PySap2000.exceptions import SectionError
            raise SectionError("Nonprismatic sections must define `np_start_secs` and `np_end_secs`")
        return model.PropFrame.SetNonPrismatic(
            self.name, self.np_num_segments,
            self.np_start_secs, self.np_end_secs,
            self.np_lengths, self.np_length_types,
            self.np_ei33, self.np_ei22
        )
    
    def _delete(self, model) -> int:
        """Delete the section."""
        return model.PropFrame.Delete(self.name)
    
    def _update(self, model) -> int:
        """Update the section."""
        return self._create(model)

    @property
    def standard_name(self) -> str:
        """
        Get a normalized section name.

        Generated from section type and dimensions:
        - `H` - I-section (`height x width x web x flange`)
        - `C` - channel (`height x width x web x flange`)
        - `T` - tee (`height x width x web x flange`)
        - `L` - angle (`height x width x thickness`)
        - `2L` - double angle (`height x width x thickness x spacing`)
        - `B` - box (`height x width x web x flange`)
        - `P` - pipe (`diameter x wall`)
        - `R` - rectangular (`height x width`)
        - `D` - circular (`diameter`)
        - `2C` - double channel (`height x width x thickness x spacing`)
        
        Returns:
            Normalized section name, or the original name if it cannot be normalized.
            
        Example:
            section = FrameSection.get_by_name(model, "FSEC1")
            print(section.standard_name)  # "H400x200x8x13"
        """
        if self.property_type == FrameSectionType.I_SECTION:
            return f"H{self.height:.0f}x{self.width:.0f}x{self.web_thickness:.0f}x{self.flange_thickness:.0f}"
        
        elif self.property_type == FrameSectionType.CHANNEL:
            return f"C{self.height:.0f}x{self.width:.0f}x{self.web_thickness:.0f}x{self.flange_thickness:.0f}"
        
        elif self.property_type == FrameSectionType.T_SECTION:
            return f"T{self.height:.0f}x{self.width:.0f}x{self.web_thickness:.0f}x{self.flange_thickness:.0f}"
        
        elif self.property_type == FrameSectionType.ANGLE:
            # Angle thickness is stored in `flange_thickness`.
            return f"L{self.height:.0f}x{self.width:.0f}x{self.flange_thickness:.0f}"
        
        elif self.property_type == FrameSectionType.DOUBLE_ANGLE:
            return f"2L{self.height:.0f}x{self.width:.0f}x{self.flange_thickness:.0f}x{self.back_to_back_distance:.0f}"
        
        elif self.property_type == FrameSectionType.BOX:
            return f"B{self.height:.0f}x{self.width:.0f}x{self.web_thickness:.0f}x{self.flange_thickness:.0f}"
        
        elif self.property_type == FrameSectionType.PIPE:
            return f"P{self.outer_diameter:.0f}x{self.wall_thickness:.0f}"
        
        elif self.property_type == FrameSectionType.RECTANGULAR:
            return f"R{self.height:.0f}x{self.width:.0f}"
        
        elif self.property_type == FrameSectionType.CIRCLE:
            return f"D{self.outer_diameter:.0f}"
        
        elif self.property_type == FrameSectionType.DOUBLE_CHANNEL:
            return f"2C{self.height:.0f}x{self.width:.0f}x{self.flange_thickness:.0f}x{self.back_to_back_distance:.0f}"
        
        # Fall back to the original name if normalization is not possible.
        return self.name
