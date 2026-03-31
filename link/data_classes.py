# -*- coding: utf-8 -*-
"""
data_classes.py - Link data classes.

Stores structured data for link object properties.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class LinkLocalAxesData:
    """Link local-axis data."""
    link_name: str = ""
    angle: float = 0.0
    advanced: bool = False


@dataclass
class LinkLocalAxesAdvancedData:
    """
    Advanced link local-axis data.
    
    Attributes:
        link_name: Link object name
        active: Whether advanced local axes are enabled
        ax_vect_opt: Axis vector option (`1`=coordinate direction,
            `2`=two points, `3`=user vector)
        ax_csys: Axis coordinate system
        ax_dir: Axis direction array `[primary, secondary]`
        ax_pt: Axis reference point array `[pt1, pt2]`
        ax_vect: Axis vector `[x, y, z]`
        plane2: Plane-2 definition (`12` or `13`)
        pl_vect_opt: Plane vector option
        pl_csys: Plane coordinate system
        pl_dir: Plane direction array `[primary, secondary]`
        pl_pt: Plane reference point array `[pt1, pt2]`
        pl_vect: Plane vector `[x, y, z]`
    """
    link_name: str = ""
    active: bool = False
    ax_vect_opt: int = 1
    ax_csys: str = "Global"
    ax_dir: List[int] = field(default_factory=lambda: [0, 0])
    ax_pt: List[str] = field(default_factory=lambda: ["", ""])
    ax_vect: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    plane2: int = 12
    pl_vect_opt: int = 1
    pl_csys: str = "Global"
    pl_dir: List[int] = field(default_factory=lambda: [0, 0])
    pl_pt: List[str] = field(default_factory=lambda: ["", ""])
    pl_vect: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
