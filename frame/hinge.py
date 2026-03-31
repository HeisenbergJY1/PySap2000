# -*- coding: utf-8 -*-
"""
hinge.py - Frame end-release data object.

Wraps SAP2000 `FrameObj.SetReleases`.

Usage:
    from frame import FrameHinge, FrameHingeType

    # Use a preset hinge type
    hinge = FrameHinge(type=FrameHingeType.BOTH_HINGED)
    hinge.apply(model, frame_no=1)

    # Use custom releases
    hinge = FrameHinge(
        release_i=(False, False, False, False, True, True),
        release_j=(False, False, False, True, True, True)
    )
    hinge.apply_to_list(model, frames=[1, 2, 3])
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Union, ClassVar
from enum import IntEnum


class FrameHingeType(IntEnum):
    """
    Preset frame hinge types.

    Corresponds to commonly used end-release combinations in SAP2000.
    """
    BOTH_FIXED = 0      # Fixed at both ends
    I_END_HINGED = 1    # Hinged at the I-end (release R2, R3)
    J_END_HINGED = 2    # Hinged at the J-end (release R2, R3)
    BOTH_HINGED = 3     # Hinged at both ends
    I_END_PINNED = 4    # Pinned at the I-end (release R1, R2, R3)
    J_END_PINNED = 5    # Pinned at the J-end (release R1, R2, R3)
    BOTH_PINNED = 6     # Pinned at both ends


# Release tuples for each hinge type: (U1, U2, U3, R1, R2, R3)
HINGE_RELEASES = {
    FrameHingeType.BOTH_FIXED: (
        (False, False, False, False, False, False),
        (False, False, False, False, False, False)
    ),
    FrameHingeType.I_END_HINGED: (
        (False, False, False, False, True, True),
        (False, False, False, False, False, False)
    ),
    FrameHingeType.J_END_HINGED: (
        (False, False, False, False, False, False),
        (False, False, False, False, True, True)
    ),
    FrameHingeType.BOTH_HINGED: (
        (False, False, False, False, True, True),
        (False, False, False, False, True, True)
    ),
    FrameHingeType.I_END_PINNED: (
        (False, False, False, True, True, True),
        (False, False, False, False, False, False)
    ),
    FrameHingeType.J_END_PINNED: (
        (False, False, False, False, False, False),
        (False, False, False, True, True, True)
    ),
    FrameHingeType.BOTH_PINNED: (
        (False, False, False, True, True, True),
        (False, False, False, True, True, True)
    ),
}


@dataclass
class FrameHinge:
    """
    Frame end-release data object.

    Wraps SAP2000 `FrameObj.SetReleases`.
    """
    
    no: int = None
    type: FrameHingeType = FrameHingeType.BOTH_FIXED
    release_i: Tuple[bool, ...] = field(default=None)
    release_j: Tuple[bool, ...] = field(default=None)
    partial_fixity_i: Tuple[float, ...] = field(default=None, repr=False)
    partial_fixity_j: Tuple[float, ...] = field(default=None, repr=False)
    comment: str = ""
    
    _object_type: ClassVar[str] = "FrameHinge"
    
    def __post_init__(self):
        if self.release_i is None or self.release_j is None:
            releases = HINGE_RELEASES.get(self.type, ((False,)*6, (False,)*6))
            if self.release_i is None:
                self.release_i = releases[0]
            if self.release_j is None:
                self.release_j = releases[1]
        if self.partial_fixity_i is None:
            self.partial_fixity_i = (0.0,) * 6
        if self.partial_fixity_j is None:
            self.partial_fixity_j = (0.0,) * 6
    
    def apply(self, model, frame_no: Union[int, str]) -> int:
        """Apply the hinge definition to a single frame."""
        return model.FrameObj.SetReleases(
            str(frame_no),
            list(self.release_i),
            list(self.release_j),
            list(self.partial_fixity_i),
            list(self.partial_fixity_j)
        )
    
    def apply_to_list(self, model, frames: List[Union[int, str]]) -> int:
        """Apply the hinge definition to multiple frames."""
        ret = 0
        for frame in frames:
            result = self.apply(model, frame)
            if result != 0:
                ret = result
        return ret
    
    @classmethod
    def get_from_frame(cls, model, frame_no: Union[int, str]) -> 'FrameHinge':
        """Create a hinge object from an existing frame assignment."""
        result = model.FrameObj.GetReleases(str(frame_no))
        hinge = cls()
        if len(result) >= 4:
            hinge.release_i = tuple(result[0])
            hinge.release_j = tuple(result[1])
            hinge.partial_fixity_i = tuple(result[2])
            hinge.partial_fixity_j = tuple(result[3])
            hinge.type = cls._infer_type(hinge.release_i, hinge.release_j)
        return hinge
    
    @staticmethod
    def _infer_type(release_i: Tuple, release_j: Tuple) -> FrameHingeType:
        for hinge_type, (expected_i, expected_j) in HINGE_RELEASES.items():
            if tuple(release_i) == expected_i and tuple(release_j) == expected_j:
                return hinge_type
        return FrameHingeType.BOTH_FIXED
    
    def clear(self, model, frame_no: Union[int, str]) -> int:
        """Clear all end releases on the frame."""
        return model.FrameObj.SetReleases(
            str(frame_no), [False]*6, [False]*6, [0.0]*6, [0.0]*6
        )
