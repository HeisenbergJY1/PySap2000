# -*- coding: utf-8 -*-
"""
data_classes.py - Area-related data classes.

Wraps data structures used by the SAP2000 `AreaObj` API.

Note: Load-related data classes have been moved to `loads/area_load.py`.
"""

from dataclasses import dataclass
from typing import Optional, List, Tuple

from .enums import (
    AreaSpringType, AreaSimpleSpringType, AreaSpringLocalOneType,
    AreaMeshType, AreaThicknessType, AreaOffsetType, PlaneRefVectorOption
)


# ==================== Property Data Classes ====================

@dataclass
class AreaSpringData:
    """Area spring data."""
    spring_type: AreaSpringType = AreaSpringType.SIMPLE_SPRING
    stiffness: float = 0.0
    simple_spring_type: AreaSimpleSpringType = AreaSimpleSpringType.TENSION_COMPRESSION
    link_prop: str = ""
    face: int = -1
    local_one_type: AreaSpringLocalOneType = AreaSpringLocalOneType.PARALLEL_TO_LOCAL_AXIS
    direction: int = 3
    outward: bool = True
    vector: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    angle: float = 0.0


@dataclass
class AreaAutoMeshData:
    """Automatic meshing settings for an area object."""
    mesh_type: AreaMeshType = AreaMeshType.NO_MESH
    n1: int = 2                          # Number of divisions in direction 1
    n2: int = 2                          # Number of divisions in direction 2
    max_size1: float = 0.0               # Maximum size in direction 1
    max_size2: float = 0.0               # Maximum size in direction 2
    point_on_edge_from_line: bool = False
    point_on_edge_from_point: bool = False
    extend_cookie_cut_lines: bool = False
    rotation: float = 0.0
    max_size_general: float = 0.0
    local_axes_on_edge: bool = False
    local_axes_on_face: bool = False
    restraints_on_edge: bool = False
    restraints_on_face: bool = False
    group: str = "ALL"
    sub_mesh: bool = False
    sub_mesh_size: float = 0.0


@dataclass
class AreaLocalAxesData:
    """Area local-axis data."""
    area_name: str = ""
    angle: float = 0.0        # Local-axis rotation angle [deg]
    advanced: bool = False    # Whether advanced settings are enabled


@dataclass
class AreaLocalAxesAdvancedData:
    """Advanced local-axis settings for an area object."""
    active: bool = False
    plane2: int = 31  # 31=3-1 plane, 32=3-2 plane
    pl_vect_opt: PlaneRefVectorOption = PlaneRefVectorOption.COORDINATE_DIRECTION
    pl_csys: str = "Global"
    pl_dir: Tuple[int, int] = (1, 2)  # Primary and secondary directions
    pl_pt: Tuple[str, str] = ("", "")  # Two point names
    pl_vect: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # User vector


@dataclass
class AreaThicknessData:
    """Area thickness override data."""
    thickness_type: AreaThicknessType = AreaThicknessType.NO_OVERWRITE
    thickness_pattern: str = ""
    thickness_pattern_sf: float = 1.0
    thickness: Optional[List[float]] = None


@dataclass
class AreaOffsetData:
    """Area offset data."""
    offset_type: AreaOffsetType = AreaOffsetType.NO_OFFSET
    offset_pattern: str = ""
    offset_pattern_sf: float = 1.0
    offsets: Optional[List[float]] = None


@dataclass
class AreaModifierData:
    """Area modifier data with 10 values."""
    f11: float = 1.0    # Membrane stiffness f11
    f22: float = 1.0    # Membrane stiffness f22
    f12: float = 1.0    # Membrane stiffness f12
    m11: float = 1.0    # Bending stiffness m11
    m22: float = 1.0    # Bending stiffness m22
    m12: float = 1.0    # Bending stiffness m12
    v13: float = 1.0    # Shear stiffness v13
    v23: float = 1.0    # Shear stiffness v23
    mass: float = 1.0   # Mass modifier
    weight: float = 1.0 # Weight modifier
    
    def to_list(self) -> List[float]:
        """Return modifier values as a list."""
        return [self.f11, self.f22, self.f12, self.m11, self.m22,
                self.m12, self.v13, self.v23, self.mass, self.weight]
    
    @classmethod
    def from_list(cls, values: List[float]) -> 'AreaModifierData':
        """Create an instance from a list."""
        if len(values) >= 10:
            return cls(
                f11=values[0], f22=values[1], f12=values[2],
                m11=values[3], m22=values[4], m12=values[5],
                v13=values[6], v23=values[7],
                mass=values[8], weight=values[9]
            )
        return cls()


@dataclass
class AreaMassData:
    """Area mass data."""
    area_name: str           # Area object name
    mass_per_area: float     # Mass per unit area
