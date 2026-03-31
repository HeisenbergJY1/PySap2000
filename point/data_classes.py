# -*- coding: utf-8 -*-
"""
data_classes.py - Data classes for point-related assignments.
"""

from dataclasses import dataclass
from typing import Optional
from .enums import PanelZonePropType, PanelZoneConnectivity, PanelZoneLocalAxisFrom


@dataclass
class PointConstraintAssignment:
    """Point constraint assignment data."""
    point_name: str
    constraint_name: str


@dataclass
class PointSpringData:
    """
    Point spring data.
    
    Attributes:
        point_name: Point name
        u1, u2, u3: Translational stiffness [F/L]
        r1, r2, r3: Rotational stiffness [FL/rad]
        is_local_csys: Whether local coordinates are used
    """
    point_name: str
    u1: float = 0.0
    u2: float = 0.0
    u3: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0
    is_local_csys: bool = False


@dataclass
class PointMassData:
    """
    Point mass data.
    
    Attributes:
        point_name: Point name
        m1, m2, m3: Translational mass
        mr1, mr2, mr3: Rotational inertia
        is_local_csys: Whether local coordinates are used
    """
    point_name: str
    m1: float = 0.0
    m2: float = 0.0
    m3: float = 0.0
    mr1: float = 0.0
    mr2: float = 0.0
    mr3: float = 0.0
    is_local_csys: bool = True


@dataclass
class PanelZoneData:
    """
    Panel-zone data.
    
    Attributes:
        prop_type: Property type
        thickness: Doubler-plate thickness
        k1, k2: Spring stiffness values
        link_prop: Link property name
        connectivity: Connectivity type
        local_axis_from: Local-axis source
        local_axis_angle: Local-axis angle
    """
    prop_type: PanelZonePropType = PanelZonePropType.ELASTIC_FROM_COLUMN
    thickness: float = 0.0
    k1: float = 0.0
    k2: float = 0.0
    link_prop: str = ""
    connectivity: PanelZoneConnectivity = PanelZoneConnectivity.BEAMS_TO_OTHER
    local_axis_from: PanelZoneLocalAxisFrom = PanelZoneLocalAxisFrom.FROM_COLUMN
    local_axis_angle: float = 0.0
