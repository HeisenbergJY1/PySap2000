# -*- coding: utf-8 -*-
"""
design/chinese_2010.py - GB 50017-2010 (Chinese steel design) helpers.

Python wrapper for `SapModel.DesignSteel.Chinese_2010`.
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, Tuple, Union

from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


class FramingType(IntEnum):
    """Lateral system / framing type."""
    PROGRAM_DEFAULT = 0     # Use preference default
    SMF = 1                 # Special moment frame (sidesway allowed)
    CBF = 2                 # Concentrically braced frame
    EBF = 3                 # Eccentrically braced frame
    NMF = 4                 # Moment frame (sidesway prevented)


class ElementType(IntEnum):
    """Member classification."""
    PROGRAM_DETERMINED = 0  # Program determined
    COLUMN = 1              # Column
    BEAM = 2                # Beam
    BRACE = 3               # Brace
    TRUSS = 4               # Truss


class SeismicDesignGrade(IntEnum):
    """Seismic design category / grade."""
    GRADE_I = 1             # Grade I
    GRADE_II = 2            # Grade II
    GRADE_III = 3           # Grade III
    GRADE_IV = 4            # Grade IV
    NON_SEISMIC = 5         # Non-seismic


class MultiResponseDesign(IntEnum):
    """Multi-load-case design strategy."""
    ENVELOPES = 1           # Envelope
    STEP_BY_STEP = 2        # Step-by-step
    LAST_STEP = 3           # Last step only
    ENVELOPES_ALL = 4       # Envelope all
    STEP_BY_STEP_ALL = 5    # Step-by-step all


class DeflectionCheckType(IntEnum):
    """Deflection check mode."""
    PROGRAM_DEFAULT = 0     # Program default
    RATIO = 1               # Deflection ratio (L/value)
    ABSOLUTE = 2            # Absolute deflection
    BOTH = 3                # Both ratio and absolute


class OverwriteItem(IntEnum):
    """Overwrite item index (1–51)."""
    FRAMING_TYPE = 1
    ELEMENT_TYPE = 2
    IS_TRANSFER_COLUMN = 3
    SEISMIC_MAGNIFICATION = 4
    IS_ROLLED_SECTION = 5
    IS_FLANGE_CUT_BY_GAS = 6
    IS_BOTH_END_PINNED = 7
    IGNORE_BT_CHECK = 8
    CLASSIFY_AS_FLEXO_COMPRESSION = 9
    IS_BEAM_TOP_LOADED = 10
    CONSIDER_DEFLECTION = 11
    DEFLECTION_CHECK_TYPE = 12
    DL_DEFLECTION_RATIO = 13
    SDL_LL_DEFLECTION_RATIO = 14
    LL_DEFLECTION_RATIO = 15
    TOTAL_DEFLECTION_RATIO = 16
    TOTAL_CAMBER_RATIO = 17
    DL_DEFLECTION_ABS = 18
    SDL_LL_DEFLECTION_ABS = 19
    LL_DEFLECTION_ABS = 20
    TOTAL_DEFLECTION_ABS = 21
    TOTAL_CAMBER_ABS = 22
    SPECIFIED_CAMBER = 23
    NET_AREA_RATIO = 24
    LIVE_LOAD_REDUCTION = 25
    UNBRACED_RATIO_MAJOR = 26
    UNBRACED_RATIO_MINOR_LTB = 27
    MUE_MAJOR = 28
    MUE_MINOR = 29
    BETA_M_MAJOR = 30
    BETA_M_MINOR = 31
    BETA_T_MAJOR = 32
    BETA_T_MINOR = 33
    PHI_MAJOR = 34
    PHI_MINOR = 35
    PHI_B_MAJOR = 36
    PHI_B_MINOR = 37
    GAMMA_MAJOR = 38
    GAMMA_MINOR = 39
    ETA_SECTION = 40
    ETA_BC = 41
    DELTA_MAJOR = 42
    DELTA_MINOR = 43
    FY = 44
    F_ALLOWABLE = 45
    FV_ALLOWABLE = 46
    CONSIDER_FICTITIOUS_SHEAR = 47
    DC_RATIO_LIMIT = 48
    DUAL_SYSTEM_FACTOR = 49
    LOR_COMPRESSION = 50
    LR_TENSION = 51


class PreferenceItem(IntEnum):
    """Preference item index (1–15)."""
    FRAMING_TYPE = 1
    GAMMA0 = 2
    IGNORE_BT_CHECK = 3
    CLASSIFY_AS_FLEXO_COMPRESSION = 4
    CONSIDER_DEFLECTION = 5
    DL_DEFLECTION_RATIO = 6
    SDL_LL_DEFLECTION_RATIO = 7
    LL_DEFLECTION_RATIO = 8
    TOTAL_DEFLECTION_RATIO = 9
    TOTAL_CAMBER_RATIO = 10
    PATTERN_LIVE_LOAD_FACTOR = 11
    DC_RATIO_LIMIT = 12
    MULTI_RESPONSE_DESIGN = 13
    IS_TALL_BUILDING = 14
    SEISMIC_DESIGN_GRADE = 15


@dataclass
class OverwriteResult:
    """Result of reading an overwrite value.

    Attributes:
        value: Overwrite numeric value
        prog_det: Whether the value is program-determined
    """
    value: float
    prog_det: bool


# ============================================================================
# Preferences
# ============================================================================

def get_chinese_2010_preference(model, item: Union[PreferenceItem, int]) -> float:
    """Get a GB 50017-2010 preference value.

    Args:
        model: SAP2000 SapModel object
        item: Preference index (1–15)

    Returns:
        Preference value.
    """
    result = model.DesignSteel.Chinese_2010.GetPreference(int(item), 0.0)
    return com_data(result, 0, 0.0)


def set_chinese_2010_preference(model, item: Union[PreferenceItem, int], value: float) -> int:
    """Set a GB 50017-2010 preference value.

    Args:
        model: SAP2000 SapModel object
        item: Preference index (1–15)
        value: Value to assign

    Returns:
        `0` on success, non-zero on failure.
    """
    ret = model.DesignSteel.Chinese_2010.SetPreference(int(item), value)
    return com_ret(ret)


# ============================================================================
# Overwrites
# ============================================================================

def get_chinese_2010_overwrite(
    model,
    name: str,
    item: Union[OverwriteItem, int]
) -> OverwriteResult:
    """Read a GB 50017-2010 overwrite for a frame object.

    Args:
        model: SAP2000 SapModel object
        name: Frame object name
        item: Overwrite index (1–51)

    Returns:
        Value and program-determined flag.
    """
    result = model.DesignSteel.Chinese_2010.GetOverwrite(name, int(item), 0.0, False)
    value = com_data(result, 0)
    prog_det = com_data(result, 1)
    if value is not None and prog_det is not None:
        return OverwriteResult(value=value, prog_det=bool(prog_det))
    return OverwriteResult(value=0.0, prog_det=True)


def set_chinese_2010_overwrite(
    model,
    name: str,
    item: Union[OverwriteItem, int],
    value: float,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """Set a GB 50017-2010 overwrite value.

    Args:
        model: SAP2000 SapModel object
        name: Object name, group name, or ignored depending on `item_type`
        item: Overwrite index (1–51)
        value: Overwrite value
        item_type: Object selection mode

    Returns:
        `0` on success, non-zero on failure.
    """
    ret = model.DesignSteel.Chinese_2010.SetOverwrite(name, int(item), value, int(item_type))
    return com_ret(ret)


# ============================================================================
# Convenience setters — common preferences
# ============================================================================

def set_chinese_2010_framing_type(model, framing_type: FramingType) -> int:
    """Set global framing type."""
    return set_chinese_2010_preference(model, PreferenceItem.FRAMING_TYPE, float(framing_type))


def set_chinese_2010_gamma0(model, gamma0: float) -> int:
    """Set importance factor γ0."""
    return set_chinese_2010_preference(model, PreferenceItem.GAMMA0, gamma0)


def set_chinese_2010_seismic_grade(model, grade: SeismicDesignGrade) -> int:
    """Set seismic design grade."""
    return set_chinese_2010_preference(model, PreferenceItem.SEISMIC_DESIGN_GRADE, float(grade))


def set_chinese_2010_dc_ratio_limit(model, ratio: float) -> int:
    """Set demand-to-capacity ratio limit."""
    return set_chinese_2010_preference(model, PreferenceItem.DC_RATIO_LIMIT, ratio)


def set_chinese_2010_tall_building(model, is_tall: bool) -> int:
    """Set tall-building flag."""
    return set_chinese_2010_preference(model, PreferenceItem.IS_TALL_BUILDING, 1.0 if is_tall else 0.0)


# ============================================================================
# Convenience setters — common overwrites
# ============================================================================

def set_chinese_2010_element_type(
    model,
    name: str,
    element_type: ElementType,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """Set member element type overwrite."""
    return set_chinese_2010_overwrite(model, name, OverwriteItem.ELEMENT_TYPE, float(element_type), item_type)


def set_chinese_2010_mue_factors(
    model,
    name: str,
    mue_major: float,
    mue_minor: float,
    item_type: ItemType = ItemType.OBJECT
) -> Tuple[int, int]:
    """Set effective length factors μ (major and minor).

    Args:
        model: SAP2000 SapModel object
        name: Object name
        mue_major: Major-axis effective length factor
        mue_minor: Minor-axis effective length factor
        item_type: Object selection mode

    Returns:
        Tuple of SAP2000 return codes ``(major, minor)``.
    """
    ret1 = set_chinese_2010_overwrite(model, name, OverwriteItem.MUE_MAJOR, mue_major, item_type)
    ret2 = set_chinese_2010_overwrite(model, name, OverwriteItem.MUE_MINOR, mue_minor, item_type)
    return ret1, ret2


def set_chinese_2010_unbraced_ratios(
    model,
    name: str,
    ratio_major: float,
    ratio_minor: float,
    item_type: ItemType = ItemType.OBJECT
) -> Tuple[int, int]:
    """Set unbraced length ratios (major flexure and minor LTB).

    Args:
        model: SAP2000 SapModel object
        name: Object name
        ratio_major: Major-axis unbraced length ratio
        ratio_minor: Minor-axis LTB unbraced length ratio
        item_type: Object selection mode

    Returns:
        Tuple of SAP2000 return codes ``(major, minor)``.
    """
    ret1 = set_chinese_2010_overwrite(model, name, OverwriteItem.UNBRACED_RATIO_MAJOR, ratio_major, item_type)
    ret2 = set_chinese_2010_overwrite(model, name, OverwriteItem.UNBRACED_RATIO_MINOR_LTB, ratio_minor, item_type)
    return ret1, ret2
