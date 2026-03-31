# -*- coding: utf-8 -*-
"""
data_classes.py - Frame-related data classes.

Wraps input and output data used by the SAP2000 `FrameObj` API.

Note: Load-related data classes have been moved to `loads/frame_load.py`.
"""

from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass
class FrameReleaseData:
    """
    Frame end-release data.
    
    Attributes:
        frame_name: Frame object name
        release_i: I-end release tuple `(U1, U2, U3, R1, R2, R3)`
        release_j: J-end release tuple `(U1, U2, U3, R1, R2, R3)`
        start_value: I-end partial-fixity stiffness values
        end_value: J-end partial-fixity stiffness values
    """
    frame_name: str
    release_i: Tuple[bool, bool, bool, bool, bool, bool] = (False,) * 6
    release_j: Tuple[bool, bool, bool, bool, bool, bool] = (False,) * 6
    start_value: Tuple[float, ...] = (0.0,) * 6
    end_value: Tuple[float, ...] = (0.0,) * 6


@dataclass
class FrameModifierData:
    """
    Frame section modifier data.

    The 8 modifier values all default to `1.0`:
        [0] = area modifier (`A`)
        [1] = local-2 shear-area modifier (`As2`)
        [2] = local-3 shear-area modifier (`As3`)
        [3] = torsional constant modifier (`J`)
        [4] = local-2 inertia modifier (`I22`)
        [5] = local-3 inertia modifier (`I33`)
        [6] = mass modifier
        [7] = weight modifier
    """
    frame_name: str
    area: float = 1.0       # A
    shear_2: float = 1.0    # As2
    shear_3: float = 1.0    # As3
    torsion: float = 1.0    # J
    inertia_22: float = 1.0 # I22
    inertia_33: float = 1.0 # I33
    mass: float = 1.0       # Mass
    weight: float = 1.0     # Weight
    
    def to_tuple(self) -> Tuple[float, ...]:
        """Return the modifier values as a tuple."""
        return (
            self.area, self.shear_2, self.shear_3, self.torsion,
            self.inertia_22, self.inertia_33, self.mass, self.weight
        )
    
    @classmethod
    def from_tuple(cls, frame_name: str, values: Tuple[float, ...]) -> 'FrameModifierData':
        """Create an instance from a modifier tuple."""
        return cls(
            frame_name=frame_name,
            area=values[0] if len(values) > 0 else 1.0,
            shear_2=values[1] if len(values) > 1 else 1.0,
            shear_3=values[2] if len(values) > 2 else 1.0,
            torsion=values[3] if len(values) > 3 else 1.0,
            inertia_22=values[4] if len(values) > 4 else 1.0,
            inertia_33=values[5] if len(values) > 5 else 1.0,
            mass=values[6] if len(values) > 6 else 1.0,
            weight=values[7] if len(values) > 7 else 1.0,
        )


@dataclass
class FrameLocalAxesData:
    """
    Frame local-axis data.
    
    Attributes:
        frame_name: Frame object name
        angle: Rotation angle of local axes 2 and 3 about positive local axis 1 [deg]
        advanced: Whether advanced local-axis options are enabled
    """
    frame_name: str
    angle: float = 0.0
    advanced: bool = False


@dataclass
class FrameLocalAxesAdvancedData:
    """
    Advanced frame local-axis data.
    
    Attributes:
        active: Whether advanced local-axis options are active
        plane2: `12` for the 1-2 plane, `13` for the 1-3 plane
        pl_vect_opt: Plane reference-vector option
            (`1`=coordinate direction, `2`=two points, `3`=user vector)
        pl_csys: Coordinate system name
        pl_dir: Primary and secondary directions
        pl_pt: Names of the two reference points
        pl_vect: User-defined reference vector
    """
    active: bool = False
    plane2: int = 12
    pl_vect_opt: int = 1
    pl_csys: str = "Global"
    pl_dir: Tuple[int, int] = (1, 2)
    pl_pt: Tuple[str, str] = ("", "")
    pl_vect: Tuple[float, float, float] = (0.0, 0.0, 0.0)


@dataclass
class FrameMassData:
    """
    Frame mass data.
    
    Attributes:
        frame_name: Frame object name
        mass_per_length: Mass per unit length [M/L]
    """
    frame_name: str
    mass_per_length: float = 0.0


@dataclass
class FrameSectionNonPrismaticData:
    """
    Nonprismatic frame section assignment data.

    Matches the return data of `FrameObj.GetSectionNonPrismatic`.
    
    Attributes:
        frame_name: Frame object name
        prop_name: Nonprismatic property name
        total_length: Assumed total nonprismatic length.
            Use `0` to match the frame length.
        rel_start_loc: Relative distance from the I-end to the nonprismatic
            start location. Only used when `total_length > 0`.
    """
    frame_name: str
    prop_name: str = ""
    total_length: float = 0.0
    rel_start_loc: float = 0.0
