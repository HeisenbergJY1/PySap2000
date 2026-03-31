# -*- coding: utf-8 -*-
"""
release.py - Frame end-release helpers.

Helpers for assigning and querying end releases on frame elements.

SAP2000 API:
- FrameObj.SetReleases(Name, II[], JJ[], StartValue[], EndValue[], ItemType)
- FrameObj.GetReleases(Name, II[], JJ[], StartValue[], EndValue[])
"""

from typing import Tuple, Optional
from .enums import ItemType, FrameReleaseType, RELEASE_PRESETS
from .data_classes import FrameReleaseData
from PySap2000.com_helper import com_ret, com_data


def set_frame_release(
    model,
    frame_name: str,
    release_type: FrameReleaseType,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Assign a predefined frame end-release preset.
    
    Args:
        model: `SapModel` object
        frame_name: Frame name
        release_type: Release preset
            - `BOTH_FIXED`: both ends fixed
            - `I_END_HINGED`: I-end hinged (R2 and R3 released)
            - `J_END_HINGED`: J-end hinged (R2 and R3 released)
            - `BOTH_HINGED`: both ends hinged
        item_type: Item scope
    
    Returns:
        `0` on success
    
    Example:
        # Set both ends as hinged
        set_frame_release(model, "1", FrameReleaseType.BOTH_HINGED)
        
        # Set the I-end as hinged
        set_frame_release(model, "1", FrameReleaseType.I_END_HINGED)
    """
    release_i, release_j = RELEASE_PRESETS.get(
        release_type, 
        ((False,)*6, (False,)*6)
    )
    
    result = model.FrameObj.SetReleases(
        str(frame_name),
        list(release_i),
        list(release_j),
        [0.0] * 6,
        [0.0] * 6,
        int(item_type)
    )
    return com_ret(result)


def set_frame_release_custom(
    model,
    frame_name: str,
    release_i: Tuple[bool, bool, bool, bool, bool, bool],
    release_j: Tuple[bool, bool, bool, bool, bool, bool],
    start_value: Tuple[float, ...] = None,
    end_value: Tuple[float, ...] = None,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    Assign custom end releases to a frame.
    
    Args:
        model: `SapModel` object
        frame_name: Frame name
        release_i: I-end release tuple `(U1, U2, U3, R1, R2, R3)`
            - `True`: release this degree of freedom
            - `False`: keep this degree of freedom fixed
        release_j: J-end release tuple
        start_value: Partial-fixity values for the I-end, optional
        end_value: Partial-fixity values for the J-end, optional
        item_type: Item scope
    
    Returns:
        `0` on success
    
    Example:
        # Release R2 and R3 at the I-end
        set_frame_release_custom(
            model, "1",
            (False, False, False, False, True, True),
            (False, False, False, False, False, False)
        )
        
        # Release torsion at both ends
        set_frame_release_custom(
            model, "1",
            (False, False, False, True, False, False),
            (False, False, False, True, False, False)
        )
    """
    if start_value is None:
        start_value = (0.0,) * 6
    if end_value is None:
        end_value = (0.0,) * 6
    
    return model.FrameObj.SetReleases(
        str(frame_name),
        list(release_i),
        list(release_j),
        list(start_value),
        list(end_value),
        int(item_type)
    )


def get_frame_release(
    model,
    frame_name: str
) -> Optional[FrameReleaseData]:
    """
    Return the end-release state of a frame.
    
    Args:
        model: `SapModel` object
        frame_name: Frame name
    
    Returns:
        `FrameReleaseData`, or `None` on failure
    
    Example:
        release = get_frame_release(model, "1")
        if release:
            print(f"I-end releases: {release.release_i}")
            print(f"J-end releases: {release.release_j}")
    """
    try:
        result = model.FrameObj.GetReleases(str(frame_name))
        ri = com_data(result, 0)
        rj = com_data(result, 1)
        if ri is not None:
            return FrameReleaseData(
                frame_name=str(frame_name),
                release_i=tuple(ri) if ri else (False,) * 6,
                release_j=tuple(rj) if rj else (False,) * 6,
                start_value=tuple(com_data(result, 2, [0.0]*6)),
                end_value=tuple(com_data(result, 3, [0.0]*6))
            )
    except Exception:
        pass
    return None


def get_frame_release_type(
    model,
    frame_name: str
) -> Optional[FrameReleaseType]:
    """
    Infer the release preset from the current frame release state.
    
    Args:
        model: `SapModel` object
        frame_name: Frame name
    
    Returns:
        Matching release preset, or `None` if no preset matches
    
    Example:
        release_type = get_frame_release_type(model, "1")
        if release_type == FrameReleaseType.BOTH_HINGED:
            print("This frame is hinged at both ends")
    """
    release = get_frame_release(model, frame_name)
    if release:
        for rtype, (expected_i, expected_j) in RELEASE_PRESETS.items():
            if release.release_i == expected_i and release.release_j == expected_j:
                return rtype
    return None


def is_frame_hinged(
    model,
    frame_name: str
) -> Tuple[bool, bool]:
    """
    Check whether each frame end behaves like a hinge.
    
    Args:
        model: `SapModel` object
        frame_name: Frame name
    
    Returns:
        Tuple `(i_end_hinged, j_end_hinged)`
    
    Example:
        i_hinged, j_hinged = is_frame_hinged(model, "1")
        if i_hinged:
            print("The I-end is hinged")
    """
    release = get_frame_release(model, frame_name)
    if release:
        # A hinge is inferred when both R2 and R3 are released.
        i_hinged = release.release_i[4] and release.release_i[5]
        j_hinged = release.release_j[4] and release.release_j[5]
        return (i_hinged, j_hinged)
    return (False, False)
