# -*- coding: utf-8 -*-
"""
data_classes.py - Analysis result data classes.

Data class definitions for the SAP2000 Analysis Results API.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class JointDisplResult:
    """
    Joint displacement result.
    
    SAP2000 API: Results.JointDispl
    
    Attributes:
        obj: Point object name
        elm: Point element name
        load_case: Load case or combination name
        step_type: Step type
        step_num: Step number
        u1: Displacement in local direction 1 [L]
        u2: Displacement in local direction 2 [L]
        u3: Displacement in local direction 3 [L]
        r1: Rotation about local axis 1 [rad]
        r2: Rotation about local axis 2 [rad]
        r3: Rotation about local axis 3 [rad]
    """
    obj: str = ""
    elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    u1: float = 0.0
    u2: float = 0.0
    u3: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0


@dataclass
class JointReactResult:
    """
    Joint reaction result.
    
    SAP2000 API: Results.JointReact
    
    Attributes:
        obj: Point object name
        elm: Point element name
        load_case: Load case or combination name
        step_type: Step type
        step_num: Step number
        f1: Reaction in local direction 1 [F]
        f2: Reaction in local direction 2 [F]
        f3: Reaction in local direction 3 [F]
        m1: Reaction moment about local axis 1 [FL]
        m2: Reaction moment about local axis 2 [FL]
        m3: Reaction moment about local axis 3 [FL]
    """
    obj: str = ""
    elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    f1: float = 0.0
    f2: float = 0.0
    f3: float = 0.0
    m1: float = 0.0
    m2: float = 0.0
    m3: float = 0.0


@dataclass
class FrameForceResult:
    """
    Frame element internal force result.
    
    SAP2000 API: Results.FrameForce
    
    Attributes:
        obj: Line object name
        obj_sta: Distance from the object's I-end to the result station [L]
        elm: Line element name
        elm_sta: Distance from the element's I-end to the result station [L]
        load_case: Load case or combination name
        step_type: Step type
        step_num: Step number
        p: Axial force [F]
        v2: Shear force in local direction 2 [F]
        v3: Shear force in local direction 3 [F]
        t: Torque [FL]
        m2: Bending moment about local axis 2 [FL]
        m3: Bending moment about local axis 3 [FL]
    """
    obj: str = ""
    obj_sta: float = 0.0
    elm: str = ""
    elm_sta: float = 0.0
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    p: float = 0.0
    v2: float = 0.0
    v3: float = 0.0
    t: float = 0.0
    m2: float = 0.0
    m3: float = 0.0


@dataclass
class BaseReactResult:
    """
    Base reaction result.
    
    SAP2000 API: Results.BaseReact
    
    Attributes:
        load_case: Load case or combination name
        step_type: Step type
        step_num: Step number
        fx: Reaction in global X [F]
        fy: Reaction in global Y [F]
        fz: Reaction in global Z [F]
        mx: Reaction moment about global X [FL]
        my: Reaction moment about global Y [FL]
        mz: Reaction moment about global Z [FL]
        gx: Global X coordinate of the reaction report point [L]
        gy: Global Y coordinate of the reaction report point [L]
        gz: Global Z coordinate of the reaction report point [L]
    """
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    fx: float = 0.0
    fy: float = 0.0
    fz: float = 0.0
    mx: float = 0.0
    my: float = 0.0
    mz: float = 0.0
    gx: float = 0.0
    gy: float = 0.0
    gz: float = 0.0


@dataclass
class ModalPeriodResult:
    """
    Modal period result.
    
    SAP2000 API: Results.ModalPeriod
    
    Attributes:
        load_case: Modal case name
        step_type: Step type, always `"Mode"`
        step_num: Mode number
        period: Period [s]
        frequency: Frequency [1/s]
        circ_freq: Circular frequency [rad/s]
        eigenvalue: Eigenvalue [rad^2/s^2]
    """
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    period: float = 0.0
    frequency: float = 0.0
    circ_freq: float = 0.0
    eigenvalue: float = 0.0


@dataclass
class ModeShapeResult:
    """
    Mode shape result.
    
    SAP2000 API: Results.ModeShape
    
    Attributes:
        obj: Point object name
        elm: Point element name
        load_case: Modal case name
        step_type: Step type, always `"Mode"`
        step_num: Mode number
        u1: Displacement in local direction 1 [L]
        u2: Displacement in local direction 2 [L]
        u3: Displacement in local direction 3 [L]
        r1: Rotation about local axis 1 [rad]
        r2: Rotation about local axis 2 [rad]
        r3: Rotation about local axis 3 [rad]
    """
    obj: str = ""
    elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    u1: float = 0.0
    u2: float = 0.0
    u3: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0


@dataclass
class ModalMassRatioResult:
    """
    Modal participating mass ratio result.
    
    SAP2000 API: Results.ModalParticipatingMassRatios
    
    Attributes:
        load_case: Modal case name
        step_type: Step type, always `"Mode"`
        step_num: Mode number
        period: Period [s]
        ux: Participating mass ratio in UX
        uy: Participating mass ratio in UY
        uz: Participating mass ratio in UZ
        sum_ux: Cumulative participating mass ratio in UX
        sum_uy: Cumulative participating mass ratio in UY
        sum_uz: Cumulative participating mass ratio in UZ
        rx: Participating mass ratio in RX
        ry: Participating mass ratio in RY
        rz: Participating mass ratio in RZ
        sum_rx: Cumulative participating mass ratio in RX
        sum_ry: Cumulative participating mass ratio in RY
        sum_rz: Cumulative participating mass ratio in RZ
    """
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    period: float = 0.0
    ux: float = 0.0
    uy: float = 0.0
    uz: float = 0.0
    sum_ux: float = 0.0
    sum_uy: float = 0.0
    sum_uz: float = 0.0
    rx: float = 0.0
    ry: float = 0.0
    rz: float = 0.0
    sum_rx: float = 0.0
    sum_ry: float = 0.0
    sum_rz: float = 0.0


@dataclass
class AreaForceShellResult:
    """
    Shell internal force result.
    
    SAP2000 API: Results.AreaForceShell
    
    Attributes:
        obj: Area object name
        elm: Area element name
        point_elm: Reporting point element name
        load_case: Load case or combination name
        step_type: Step type
        step_num: Step number
        f11: Membrane force F11 [F/L]
        f22: Membrane force F22 [F/L]
        f12: Membrane shear force F12 [F/L]
        f_max: Maximum principal membrane force [F/L]
        f_min: Minimum principal membrane force [F/L]
        f_angle: Direction angle of the maximum principal membrane force [deg]
        f_vm: Von Mises membrane force [F/L]
        m11: Bending moment M11 [FL/L]
        m22: Bending moment M22 [FL/L]
        m12: Twisting moment M12 [FL/L]
        m_max: Maximum principal bending moment [FL/L]
        m_min: Minimum principal bending moment [FL/L]
        m_angle: Direction angle of the maximum principal bending moment [deg]
        v13: Transverse shear force V13 [F/L]
        v23: Transverse shear force V23 [F/L]
        v_max: Maximum transverse shear force [F/L]
        v_angle: Direction angle of the maximum transverse shear force [deg]
    """
    obj: str = ""
    elm: str = ""
    point_elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    f11: float = 0.0
    f22: float = 0.0
    f12: float = 0.0
    f_max: float = 0.0
    f_min: float = 0.0
    f_angle: float = 0.0
    f_vm: float = 0.0
    m11: float = 0.0
    m22: float = 0.0
    m12: float = 0.0
    m_max: float = 0.0
    m_min: float = 0.0
    m_angle: float = 0.0
    v13: float = 0.0
    v23: float = 0.0
    v_max: float = 0.0
    v_angle: float = 0.0


# =============================================================================
# Additional area results
# =============================================================================

@dataclass
class AreaJointForcePlaneResult:
    """
    Plane element joint force result.
    
    SAP2000 API: Results.AreaJointForcePlane
    """
    obj: str = ""
    elm: str = ""
    point_elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    f1: float = 0.0
    f2: float = 0.0
    f3: float = 0.0
    m1: float = 0.0
    m2: float = 0.0
    m3: float = 0.0


@dataclass
class AreaJointForceShellResult:
    """
    Shell element joint force result.
    
    SAP2000 API: Results.AreaJointForceShell
    """
    obj: str = ""
    elm: str = ""
    point_elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    f1: float = 0.0
    f2: float = 0.0
    f3: float = 0.0
    m1: float = 0.0
    m2: float = 0.0
    m3: float = 0.0


@dataclass
class AreaStrainShellResult:
    """
    Shell strain result.
    
    SAP2000 API: Results.AreaStrainShell
    """
    obj: str = ""
    elm: str = ""
    point_elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    e11: float = 0.0
    e22: float = 0.0
    g12: float = 0.0
    e_max: float = 0.0
    e_min: float = 0.0
    e_angle: float = 0.0
    e_vm: float = 0.0
    g13: float = 0.0
    g23: float = 0.0
    g_max: float = 0.0
    g_angle: float = 0.0


@dataclass
class AreaStrainShellLayeredResult:
    """
    Layered shell strain result.
    
    SAP2000 API: Results.AreaStrainShellLayered
    """
    obj: str = ""
    elm: str = ""
    layer: str = ""
    int_pt_num: int = 0
    int_pt_loc: float = 0.0
    point_elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    e11: float = 0.0
    e22: float = 0.0
    g12: float = 0.0
    e_max: float = 0.0
    e_min: float = 0.0
    e_angle: float = 0.0
    e_vm: float = 0.0
    g13: float = 0.0
    g23: float = 0.0
    g_max: float = 0.0
    g_angle: float = 0.0


@dataclass
class AreaStressPlaneResult:
    """
    Plane element stress result.
    
    SAP2000 API: Results.AreaStressPlane
    """
    obj: str = ""
    elm: str = ""
    point_elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    s11: float = 0.0
    s22: float = 0.0
    s33: float = 0.0
    s12: float = 0.0
    s_max: float = 0.0
    s_min: float = 0.0
    s_angle: float = 0.0
    s_vm: float = 0.0


@dataclass
class AreaStressShellResult:
    """
    Shell stress result.
    
    SAP2000 API: Results.AreaStressShell
    """
    obj: str = ""
    elm: str = ""
    point_elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    s11_top: float = 0.0
    s22_top: float = 0.0
    s12_top: float = 0.0
    s_max_top: float = 0.0
    s_min_top: float = 0.0
    s_angle_top: float = 0.0
    s_vm_top: float = 0.0
    s11_bot: float = 0.0
    s22_bot: float = 0.0
    s12_bot: float = 0.0
    s_max_bot: float = 0.0
    s_min_bot: float = 0.0
    s_angle_bot: float = 0.0
    s_vm_bot: float = 0.0
    s13_avg: float = 0.0
    s23_avg: float = 0.0
    s_max_avg: float = 0.0
    s_angle_avg: float = 0.0


@dataclass
class AreaStressShellLayeredResult:
    """
    Layered shell stress result.
    
    SAP2000 API: Results.AreaStressShellLayered
    """
    obj: str = ""
    elm: str = ""
    layer: str = ""
    int_pt_num: int = 0
    int_pt_loc: float = 0.0
    point_elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    s11: float = 0.0
    s22: float = 0.0
    s12: float = 0.0
    s_max: float = 0.0
    s_min: float = 0.0
    s_angle: float = 0.0
    s_vm: float = 0.0
    s13: float = 0.0
    s23: float = 0.0
    s_max_shear: float = 0.0
    s_angle_shear: float = 0.0


# =============================================================================
# Additional joint results
# =============================================================================

@dataclass
class AssembledJointMassResult:
    """
    Assembled joint mass result.
    
    SAP2000 API: Results.AssembledJointMass_1
    """
    obj: str = ""
    elm: str = ""
    u1: float = 0.0
    u2: float = 0.0
    u3: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0


@dataclass
class BaseReactWithCentroidResult:
    """
    Base reaction result with centroid data.
    
    SAP2000 API: Results.BaseReactWithCentroid
    """
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    fx: float = 0.0
    fy: float = 0.0
    fz: float = 0.0
    mx: float = 0.0
    my: float = 0.0
    mz: float = 0.0
    gx: float = 0.0
    gy: float = 0.0
    gz: float = 0.0
    xcentroid_fx: float = 0.0
    ycentroid_fx: float = 0.0
    zcentroid_fx: float = 0.0
    xcentroid_fy: float = 0.0
    ycentroid_fy: float = 0.0
    zcentroid_fy: float = 0.0
    xcentroid_fz: float = 0.0
    ycentroid_fz: float = 0.0
    zcentroid_fz: float = 0.0


@dataclass
class BucklingFactorResult:
    """
    Buckling factor result.
    
    SAP2000 API: Results.BucklingFactor
    """
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    factor: float = 0.0


@dataclass
class FrameJointForceResult:
    """
    Frame joint force result.
    
    SAP2000 API: Results.FrameJointForce
    """
    obj: str = ""
    elm: str = ""
    point_elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    f1: float = 0.0
    f2: float = 0.0
    f3: float = 0.0
    m1: float = 0.0
    m2: float = 0.0
    m3: float = 0.0


@dataclass
class GeneralizedDisplResult:
    """
    Generalized displacement result.
    
    SAP2000 API: Results.GeneralizedDispl
    """
    name: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    dof_type: str = ""
    value: float = 0.0


@dataclass
class JointAccResult:
    """
    Joint acceleration result.
    
    SAP2000 API: Results.JointAcc
    """
    obj: str = ""
    elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    u1: float = 0.0
    u2: float = 0.0
    u3: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0


@dataclass
class JointAccAbsResult:
    """
    Absolute joint acceleration result.
    
    SAP2000 API: Results.JointAccAbs
    """
    obj: str = ""
    elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    u1: float = 0.0
    u2: float = 0.0
    u3: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0


@dataclass
class JointDisplAbsResult:
    """
    Absolute joint displacement result.
    
    SAP2000 API: Results.JointDisplAbs
    """
    obj: str = ""
    elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    u1: float = 0.0
    u2: float = 0.0
    u3: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0


@dataclass
class JointRespSpecResult:
    """
    Joint response spectrum result.
    
    SAP2000 API: Results.JointRespSpec
    """
    obj: str = ""
    elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    u1: float = 0.0
    u2: float = 0.0
    u3: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0


@dataclass
class JointVelResult:
    """
    Joint velocity result.
    
    SAP2000 API: Results.JointVel
    """
    obj: str = ""
    elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    u1: float = 0.0
    u2: float = 0.0
    u3: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0


@dataclass
class JointVelAbsResult:
    """
    Absolute joint velocity result.
    
    SAP2000 API: Results.JointVelAbs
    """
    obj: str = ""
    elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    u1: float = 0.0
    u2: float = 0.0
    u3: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0


# =============================================================================
# Link results
# =============================================================================

@dataclass
class LinkDeformationResult:
    """
    Link deformation result.
    
    SAP2000 API: Results.LinkDeformation
    """
    obj: str = ""
    elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    u1: float = 0.0
    u2: float = 0.0
    u3: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0


@dataclass
class LinkForceResult:
    """
    Link internal force result.
    
    SAP2000 API: Results.LinkForce
    """
    obj: str = ""
    elm: str = ""
    point_elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    p: float = 0.0
    v2: float = 0.0
    v3: float = 0.0
    t: float = 0.0
    m2: float = 0.0
    m3: float = 0.0


@dataclass
class LinkJointForceResult:
    """
    Link joint force result.
    
    SAP2000 API: Results.LinkJointForce
    """
    obj: str = ""
    elm: str = ""
    point_elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    f1: float = 0.0
    f2: float = 0.0
    f3: float = 0.0
    m1: float = 0.0
    m2: float = 0.0
    m3: float = 0.0


# =============================================================================
# Additional modal results
# =============================================================================

@dataclass
class ModalLoadParticipationRatioResult:
    """
    Modal load participation ratio result.
    
    SAP2000 API: Results.ModalLoadParticipationRatios
    """
    load_case: str = ""
    item_type: str = ""
    item: str = ""
    stat: float = 0.0
    dyn: float = 0.0


@dataclass
class ModalParticipationFactorResult:
    """
    Modal participation factor result.
    
    SAP2000 API: Results.ModalParticipationFactors
    """
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    period: float = 0.0
    ux: float = 0.0
    uy: float = 0.0
    uz: float = 0.0
    rx: float = 0.0
    ry: float = 0.0
    rz: float = 0.0
    modal_mass: float = 0.0
    modal_stiff: float = 0.0


# =============================================================================
# Panel zone results
# =============================================================================

@dataclass
class PanelZoneDeformationResult:
    """
    Panel zone deformation result.
    
    SAP2000 API: Results.PanelZoneDeformation
    """
    elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    u1: float = 0.0
    u2: float = 0.0
    u3: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0


@dataclass
class PanelZoneForceResult:
    """
    Panel zone force result.
    
    SAP2000 API: Results.PanelZoneForce
    """
    elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    p: float = 0.0
    v2: float = 0.0
    v3: float = 0.0
    t: float = 0.0
    m2: float = 0.0
    m3: float = 0.0


# =============================================================================
# Section-cut results
# =============================================================================

@dataclass
class SectionCutAnalysisResult:
    """
    Section-cut analysis result.
    
    SAP2000 API: Results.SectionCutAnalysis
    """
    name: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    f1: float = 0.0
    f2: float = 0.0
    f3: float = 0.0
    m1: float = 0.0
    m2: float = 0.0
    m3: float = 0.0


@dataclass
class SectionCutDesignResult:
    """
    Section-cut design result.
    
    SAP2000 API: Results.SectionCutDesign
    """
    name: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    p: float = 0.0
    v2: float = 0.0
    v3: float = 0.0
    t: float = 0.0
    m2: float = 0.0
    m3: float = 0.0


# =============================================================================
# Solid element results
# =============================================================================

@dataclass
class SolidJointForceResult:
    """
    Solid element joint force result.
    
    SAP2000 API: Results.SolidJointForce
    """
    obj: str = ""
    elm: str = ""
    point_elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    f1: float = 0.0
    f2: float = 0.0
    f3: float = 0.0
    m1: float = 0.0
    m2: float = 0.0
    m3: float = 0.0


@dataclass
class SolidStrainResult:
    """
    Solid element strain result.
    
    SAP2000 API: Results.SolidStrain
    """
    obj: str = ""
    elm: str = ""
    point_elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    e11: float = 0.0
    e22: float = 0.0
    e33: float = 0.0
    g12: float = 0.0
    g13: float = 0.0
    g23: float = 0.0
    e_max: float = 0.0
    e_mid: float = 0.0
    e_min: float = 0.0
    e_vm: float = 0.0
    dir_cos_max1: float = 0.0
    dir_cos_max2: float = 0.0
    dir_cos_max3: float = 0.0
    dir_cos_mid1: float = 0.0
    dir_cos_mid2: float = 0.0
    dir_cos_mid3: float = 0.0
    dir_cos_min1: float = 0.0
    dir_cos_min2: float = 0.0
    dir_cos_min3: float = 0.0


@dataclass
class SolidStressResult:
    """
    Solid element stress result.
    
    SAP2000 API: Results.SolidStress
    """
    obj: str = ""
    elm: str = ""
    point_elm: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    s11: float = 0.0
    s22: float = 0.0
    s33: float = 0.0
    s12: float = 0.0
    s13: float = 0.0
    s23: float = 0.0
    s_max: float = 0.0
    s_mid: float = 0.0
    s_min: float = 0.0
    s_vm: float = 0.0
    dir_cos_max1: float = 0.0
    dir_cos_max2: float = 0.0
    dir_cos_max3: float = 0.0
    dir_cos_mid1: float = 0.0
    dir_cos_mid2: float = 0.0
    dir_cos_mid3: float = 0.0
    dir_cos_min1: float = 0.0
    dir_cos_min2: float = 0.0
    dir_cos_min3: float = 0.0


# =============================================================================
# Step labels
# =============================================================================

@dataclass
class StepLabelResult:
    """
    Step label result.
    
    SAP2000 API: Results.StepLabel
    """
    load_case: str = ""
    step_num: int = 0
    label: str = ""
