# -*- coding: utf-8 -*-
"""
design/data_classes.py - Design module dataclasses.

Dataclasses for steel, concrete, aluminum, and cold-formed design output.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .enums import RatioType, ColumnDesignOption


# ============================================================================
# Shared dataclasses
# ============================================================================

@dataclass
class VerifyPassedResult:
    """Generic design verification summary.

    Attributes:
        total_count: Total objects that failed checks or were not checked
        failed_count: Objects that failed design checks
        unchecked_count: Objects not yet checked
        frame_names: Names of objects that failed or were not checked
    """
    total_count: int
    failed_count: int
    unchecked_count: int
    frame_names: List[str] = field(default_factory=list)

    @property
    def all_passed(self) -> bool:
        """Whether every object passed."""
        return self.total_count == 0


# ============================================================================
# Shared summary row for steel / aluminum / cold-formed
# ============================================================================

@dataclass
class SteelSummaryResult:
    """Steel design summary row.

    Attributes:
        frame_name: Frame object name
        ratio: Controlling stress or strength ratio
        ratio_type: Ratio type (1–6)
        location: Location of controlling response measured from joint I
        combo_name: Controlling load combination name
        error_summary: Error summary text
        warning_summary: Warning summary text
    """
    frame_name: str
    ratio: float
    ratio_type: RatioType
    location: float
    combo_name: str
    error_summary: str = ""
    warning_summary: str = ""

    @property
    def passed(self) -> bool:
        """Whether the design check passes (ratio <= 1.0)."""
        return self.ratio <= 1.0

    @property
    def ratio_type_name(self) -> str:
        """Human-readable ratio type label."""
        names = {
            RatioType.PMM: "PMM",
            RatioType.MAJOR_SHEAR: "Major Shear",
            RatioType.MINOR_SHEAR: "Minor Shear",
            RatioType.MAJOR_BEAM_COLUMN: "Major Beam-Column",
            RatioType.MINOR_BEAM_COLUMN: "Minor Beam-Column",
            RatioType.OTHER: "Other",
        }
        return names.get(self.ratio_type, "Unknown")


# Aluminum and cold-formed reuse the same row layout as steel
AluminumSummaryResult = SteelSummaryResult
ColdFormedSummaryResult = SteelSummaryResult


# ============================================================================
# Concrete design dataclasses
# ============================================================================

@dataclass
class ConcreteBeamResult:
    """Concrete beam design summary row.

    Attributes:
        frame_name: Frame object name
        location: Distance from joint I along the member
        top_combo: Load combination controlling top longitudinal steel
        top_area: Top longitudinal steel area (flexure)
        bot_combo: Load combination controlling bottom longitudinal steel
        bot_area: Bottom longitudinal steel area (flexure)
        vmajor_combo: Load combination controlling shear
        vmajor_area: Major-axis shear stirrup area per unit length
        tl_combo: Load combination controlling torsion longitudinal steel
        tl_area: Torsion longitudinal steel area
        tt_combo: Load combination controlling torsion stirrups
        tt_area: Torsion stirrup area per unit length
        error_summary: Error summary text
        warning_summary: Warning summary text
    """
    frame_name: str
    location: float
    top_combo: str
    top_area: float
    bot_combo: str
    bot_area: float
    vmajor_combo: str
    vmajor_area: float
    tl_combo: str = ""
    tl_area: float = 0.0
    tt_combo: str = ""
    tt_area: float = 0.0
    error_summary: str = ""
    warning_summary: str = ""


@dataclass
class ConcreteColumnResult:
    """Concrete column design summary row.

    Attributes:
        frame_name: Frame object name
        design_option: Check vs. design mode
        location: Distance from joint I along the member
        pmm_combo: Load combination controlling PMM
        pmm_area: PMM longitudinal steel area (when ``design_option`` is DESIGN)
        pmm_ratio: PMM stress ratio (when ``design_option`` is CHECK)
        vmajor_combo: Load combination controlling major-axis shear
        av_major: Major-axis shear stirrup area per unit length
        vminor_combo: Load combination controlling minor-axis shear
        av_minor: Minor-axis shear stirrup area per unit length
        error_summary: Error summary text
        warning_summary: Warning summary text
    """
    frame_name: str
    design_option: ColumnDesignOption
    location: float
    pmm_combo: str
    pmm_area: float
    pmm_ratio: float
    vmajor_combo: str
    av_major: float
    vminor_combo: str
    av_minor: float
    error_summary: str = ""
    warning_summary: str = ""

    @property
    def passed(self) -> bool:
        """In CHECK mode, whether the stress ratio is acceptable (<= 1.0)."""
        if self.design_option == ColumnDesignOption.CHECK:
            return self.pmm_ratio <= 1.0
        return True


@dataclass
class ConcreteJointResult:
    """Concrete joint design summary row.

    Attributes:
        frame_name: Frame object name
        js_ratio_major_combo: Load combination controlling major-axis joint shear ratio
        js_ratio_major: Major-axis joint shear ratio
        js_ratio_minor_combo: Load combination controlling minor-axis joint shear ratio
        js_ratio_minor: Minor-axis joint shear ratio
        bcc_ratio_major_combo: Load combination controlling major-axis beam-column capacity ratio
        bcc_ratio_major: Major-axis beam-column capacity ratio
        bcc_ratio_minor_combo: Load combination controlling minor-axis beam-column capacity ratio
        bcc_ratio_minor: Minor-axis beam-column capacity ratio
        error_summary: Error summary text
        warning_summary: Warning summary text
    """
    frame_name: str
    js_ratio_major_combo: str
    js_ratio_major: float
    js_ratio_minor_combo: str
    js_ratio_minor: float
    bcc_ratio_major_combo: str
    bcc_ratio_major: float
    bcc_ratio_minor_combo: str
    bcc_ratio_minor: float
    error_summary: str = ""
    warning_summary: str = ""
