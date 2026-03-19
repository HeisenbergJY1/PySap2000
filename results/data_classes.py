# -*- coding: utf-8 -*-
"""
data_classes.py - 分析结果数据类

SAP2000 Analysis Results API 的数据类定义
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class JointDisplResult:
    """
    节点位移结果
    
    SAP2000 API: Results.JointDispl
    
    Attributes:
        obj: 点对象名称
        elm: 点元素名称
        load_case: 工况或组合名称
        step_type: 步骤类型
        step_num: 步骤号
        u1: 局部1方向位移 [L]
        u2: 局部2方向位移 [L]
        u3: 局部3方向位移 [L]
        r1: 绕局部1轴转角 [rad]
        r2: 绕局部2轴转角 [rad]
        r3: 绕局部3轴转角 [rad]
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
    节点反力结果
    
    SAP2000 API: Results.JointReact
    
    Attributes:
        obj: 点对象名称
        elm: 点元素名称
        load_case: 工况或组合名称
        step_type: 步骤类型
        step_num: 步骤号
        f1: 局部1方向反力 [F]
        f2: 局部2方向反力 [F]
        f3: 局部3方向反力 [F]
        m1: 绕局部1轴反力矩 [FL]
        m2: 绕局部2轴反力矩 [FL]
        m3: 绕局部3轴反力矩 [FL]
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
    框架单元内力结果
    
    SAP2000 API: Results.FrameForce
    
    Attributes:
        obj: 线对象名称
        obj_sta: 从对象I端到结果位置的距离 [L]
        elm: 线元素名称
        elm_sta: 从元素I端到结果位置的距离 [L]
        load_case: 工况或组合名称
        step_type: 步骤类型
        step_num: 步骤号
        p: 轴力 [F]
        v2: 局部2方向剪力 [F]
        v3: 局部3方向剪力 [F]
        t: 扭矩 [FL]
        m2: 绕局部2轴弯矩 [FL]
        m3: 绕局部3轴弯矩 [FL]
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
    基底反力结果
    
    SAP2000 API: Results.BaseReact
    
    Attributes:
        load_case: 工况或组合名称
        step_type: 步骤类型
        step_num: 步骤号
        fx: 全局X方向反力 [F]
        fy: 全局Y方向反力 [F]
        fz: 全局Z方向反力 [F]
        mx: 绕全局X轴反力矩 [FL]
        my: 绕全局Y轴反力矩 [FL]
        mz: 绕全局Z轴反力矩 [FL]
        gx: 反力报告点全局X坐标 [L]
        gy: 反力报告点全局Y坐标 [L]
        gz: 反力报告点全局Z坐标 [L]
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
    模态周期结果
    
    SAP2000 API: Results.ModalPeriod
    
    Attributes:
        load_case: 模态工况名称
        step_type: 步骤类型 (总是 "Mode")
        step_num: 振型号
        period: 周期 [s]
        frequency: 频率 [1/s]
        circ_freq: 圆频率 [rad/s]
        eigenvalue: 特征值 [rad²/s²]
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
    振型结果
    
    SAP2000 API: Results.ModeShape
    
    Attributes:
        obj: 点对象名称
        elm: 点元素名称
        load_case: 模态工况名称
        step_type: 步骤类型 (总是 "Mode")
        step_num: 振型号
        u1: 局部1方向位移 [L]
        u2: 局部2方向位移 [L]
        u3: 局部3方向位移 [L]
        r1: 绕局部1轴转角 [rad]
        r2: 绕局部2轴转角 [rad]
        r3: 绕局部3轴转角 [rad]
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
    模态参与质量比结果
    
    SAP2000 API: Results.ModalParticipatingMassRatios
    
    Attributes:
        load_case: 模态工况名称
        step_type: 步骤类型 (总是 "Mode")
        step_num: 振型号
        period: 周期 [s]
        ux: UX方向参与质量比
        uy: UY方向参与质量比
        uz: UZ方向参与质量比
        sum_ux: UX方向累计参与质量比
        sum_uy: UY方向累计参与质量比
        sum_uz: UZ方向累计参与质量比
        rx: RX方向参与质量比
        ry: RY方向参与质量比
        rz: RZ方向参与质量比
        sum_rx: RX方向累计参与质量比
        sum_ry: RY方向累计参与质量比
        sum_rz: RZ方向累计参与质量比
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
    壳单元内力结果
    
    SAP2000 API: Results.AreaForceShell
    
    Attributes:
        obj: 面对象名称
        elm: 面元素名称
        point_elm: 结果报告点元素名称
        load_case: 工况或组合名称
        step_type: 步骤类型
        step_num: 步骤号
        f11: 膜力F11 [F/L]
        f22: 膜力F22 [F/L]
        f12: 膜剪力F12 [F/L]
        f_max: 最大主膜力 [F/L]
        f_min: 最小主膜力 [F/L]
        f_angle: 最大主膜力方向角 [deg]
        f_vm: Von Mises膜力 [F/L]
        m11: 弯矩M11 [FL/L]
        m22: 弯矩M22 [FL/L]
        m12: 扭矩M12 [FL/L]
        m_max: 最大主弯矩 [FL/L]
        m_min: 最小主弯矩 [FL/L]
        m_angle: 最大主弯矩方向角 [deg]
        v13: 横向剪力V13 [F/L]
        v23: 横向剪力V23 [F/L]
        v_max: 最大横向剪力 [F/L]
        v_angle: 最大横向剪力方向角 [deg]
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
# 面单元附加结果
# =============================================================================

@dataclass
class AreaJointForcePlaneResult:
    """
    平面单元节点力结果
    
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
    壳单元节点力结果
    
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
    壳单元应变结果
    
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
    分层壳单元应变结果
    
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
    平面单元应力结果
    
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
    壳单元应力结果
    
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
    分层壳单元应力结果
    
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
# 节点附加结果
# =============================================================================

@dataclass
class AssembledJointMassResult:
    """
    组装节点质量结果
    
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
    带质心的基底反力结果
    
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
    屈曲因子结果
    
    SAP2000 API: Results.BucklingFactor
    """
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    factor: float = 0.0


@dataclass
class FrameJointForceResult:
    """
    框架节点力结果
    
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
    广义位移结果
    
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
    节点加速度结果
    
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
    节点绝对加速度结果
    
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
    节点绝对位移结果
    
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
    节点反应谱结果
    
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
    节点速度结果
    
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
    节点绝对速度结果
    
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
# 连接单元结果
# =============================================================================

@dataclass
class LinkDeformationResult:
    """
    连接单元变形结果
    
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
    连接单元内力结果
    
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
    连接单元节点力结果
    
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
# 模态附加结果
# =============================================================================

@dataclass
class ModalLoadParticipationRatioResult:
    """
    模态荷载参与比结果
    
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
    模态参与因子结果
    
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
# 节点域结果
# =============================================================================

@dataclass
class PanelZoneDeformationResult:
    """
    节点域变形结果
    
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
    节点域内力结果
    
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
# 截面切割结果
# =============================================================================

@dataclass
class SectionCutAnalysisResult:
    """
    截面切割分析结果
    
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
    截面切割设计结果
    
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
# 实体单元结果
# =============================================================================

@dataclass
class SolidJointForceResult:
    """
    实体单元节点力结果
    
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
    实体单元应变结果
    
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
    实体单元应力结果
    
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
# 步骤标签
# =============================================================================

@dataclass
class StepLabelResult:
    """
    步骤标签结果
    
    SAP2000 API: Results.StepLabel
    """
    load_case: str = ""
    step_num: int = 0
    label: str = ""
