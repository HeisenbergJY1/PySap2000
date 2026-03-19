# -*- coding: utf-8 -*-
"""
results - 分析结果模块

SAP2000 的 Results API，用于提取分析结果。

SAP2000 API 结构:
- Results.Setup - 输出选择设置
- Results - 结果提取

Usage:
    from PySap2000.results import (
        # 输出设置
        deselect_all_cases_and_combos,
        set_case_selected_for_output,
        select_cases_for_output,
        # 节点结果
        get_joint_displ,
        get_joint_react,
        # 框架结果
        get_frame_force,
        # 基底反力
        get_base_react,
        # 模态结果
        get_modal_period,
        # 枚举
        ItemTypeElm,
    )
    
    # 典型工作流
    deselect_all_cases_and_combos(model)
    set_case_selected_for_output(model, "DEAD")
    
    displ = get_joint_displ(model, "ALL", ItemTypeElm.GROUP_ELM)
    forces = get_frame_force(model, "1", ItemTypeElm.OBJECT_ELM)
"""

from .enums import ItemTypeElm

# =============================================================================
# 数据类
# =============================================================================
from .data_classes import (
    # 节点结果
    JointDisplResult,
    JointReactResult,
    JointDisplAbsResult,
    JointAccResult,
    JointAccAbsResult,
    JointVelResult,
    JointVelAbsResult,
    JointRespSpecResult,
    # 框架结果
    FrameForceResult,
    FrameJointForceResult,
    # 基底反力
    BaseReactResult,
    BaseReactWithCentroidResult,
    # 模态结果
    ModalPeriodResult,
    ModeShapeResult,
    ModalMassRatioResult,
    ModalLoadParticipationRatioResult,
    ModalParticipationFactorResult,
    # 面单元结果
    AreaForceShellResult,
    AreaJointForcePlaneResult,
    AreaJointForceShellResult,
    AreaStrainShellResult,
    AreaStrainShellLayeredResult,
    AreaStressPlaneResult,
    AreaStressShellResult,
    AreaStressShellLayeredResult,
    # 连接单元结果
    LinkDeformationResult,
    LinkForceResult,
    LinkJointForceResult,
    # 实体单元结果
    SolidJointForceResult,
    SolidStrainResult,
    SolidStressResult,
    # 杂项结果
    AssembledJointMassResult,
    BucklingFactorResult,
    GeneralizedDisplResult,
    PanelZoneDeformationResult,
    PanelZoneForceResult,
    SectionCutAnalysisResult,
    SectionCutDesignResult,
    StepLabelResult,
)

# =============================================================================
# 输出设置函数
# =============================================================================
from .setup import (
    # 工况/组合选择
    deselect_all_cases_and_combos,
    set_case_selected_for_output,
    get_case_selected_for_output,
    set_combo_selected_for_output,
    get_combo_selected_for_output,
    select_cases_for_output,
    select_combos_for_output,
    # 基底反力位置
    get_option_base_react_loc,
    set_option_base_react_loc,
    # 屈曲模态
    get_option_buckling_mode,
    set_option_buckling_mode,
    # 直接积分时程
    get_option_direct_hist,
    set_option_direct_hist,
    # 模态时程
    get_option_modal_hist,
    set_option_modal_hist,
    # 振型
    get_option_mode_shape,
    set_option_mode_shape,
    # 多步静力
    get_option_multi_step_static,
    set_option_multi_step_static,
    # 多值组合
    get_option_multi_valued_combo,
    set_option_multi_valued_combo,
    # 非线性静力
    get_option_nl_static,
    set_option_nl_static,
    # 功率谱密度
    get_option_psd,
    set_option_psd,
    # 稳态
    get_option_steady_state,
    set_option_steady_state,
    # 截面切割
    get_section_cut_selected_for_output,
    set_section_cut_selected_for_output,
    select_all_section_cuts_for_output,
)

# =============================================================================
# 节点结果函数
# =============================================================================
from .joint_results import (
    get_joint_displ,
    get_joint_displ_abs,
    get_joint_react,
    get_joint_acc,
    get_joint_acc_abs,
    get_joint_vel,
    get_joint_vel_abs,
    get_joint_resp_spec,
)

# =============================================================================
# 框架结果函数
# =============================================================================
from .frame_results import (
    get_frame_force,
    get_frame_joint_force,
)

# =============================================================================
# 基底反力函数
# =============================================================================
from .base_react import (
    get_base_react,
)

# =============================================================================
# 模态结果函数
# =============================================================================
from .modal_results import (
    get_modal_period,
    get_mode_shape,
    get_modal_participating_mass_ratios,
    get_modal_load_participation_ratios,
    get_modal_participation_factors,
)

# =============================================================================
# 面单元结果函数
# =============================================================================
from .area_results import (
    get_area_force_shell,
    get_area_joint_force_plane,
    get_area_joint_force_shell,
    get_area_strain_shell,
    get_area_strain_shell_layered,
    get_area_stress_plane,
    get_area_stress_shell,
    get_area_stress_shell_layered,
)

# =============================================================================
# 连接单元结果函数
# =============================================================================
from .link_results import (
    get_link_deformation,
    get_link_force,
    get_link_joint_force,
)

# =============================================================================
# 实体单元结果函数
# =============================================================================
from .solid_results import (
    get_solid_joint_force,
    get_solid_strain,
    get_solid_stress,
)

# =============================================================================
# 杂项结果函数
# =============================================================================
from .misc_results import (
    get_assembled_joint_mass,
    get_base_react_with_centroid,
    get_buckling_factor,
    get_generalized_displ,
    get_panel_zone_deformation,
    get_panel_zone_force,
    get_section_cut_analysis,
    get_section_cut_design,
    get_step_label,
)


__all__ = [
    # 枚举
    "ItemTypeElm",
    # 数据类 - 节点
    "JointDisplResult",
    "JointReactResult",
    "JointDisplAbsResult",
    "JointAccResult",
    "JointAccAbsResult",
    "JointVelResult",
    "JointVelAbsResult",
    "JointRespSpecResult",
    # 数据类 - 框架
    "FrameForceResult",
    "FrameJointForceResult",
    # 数据类 - 基底反力
    "BaseReactResult",
    "BaseReactWithCentroidResult",
    # 数据类 - 模态
    "ModalPeriodResult",
    "ModeShapeResult",
    "ModalMassRatioResult",
    "ModalLoadParticipationRatioResult",
    "ModalParticipationFactorResult",
    # 数据类 - 面单元
    "AreaForceShellResult",
    "AreaJointForcePlaneResult",
    "AreaJointForceShellResult",
    "AreaStrainShellResult",
    "AreaStrainShellLayeredResult",
    "AreaStressPlaneResult",
    "AreaStressShellResult",
    "AreaStressShellLayeredResult",
    # 数据类 - 连接单元
    "LinkDeformationResult",
    "LinkForceResult",
    "LinkJointForceResult",
    # 数据类 - 实体单元
    "SolidJointForceResult",
    "SolidStrainResult",
    "SolidStressResult",
    # 数据类 - 杂项
    "AssembledJointMassResult",
    "BucklingFactorResult",
    "GeneralizedDisplResult",
    "PanelZoneDeformationResult",
    "PanelZoneForceResult",
    "SectionCutAnalysisResult",
    "SectionCutDesignResult",
    "StepLabelResult",
    # 输出设置
    "deselect_all_cases_and_combos",
    "set_case_selected_for_output",
    "get_case_selected_for_output",
    "set_combo_selected_for_output",
    "get_combo_selected_for_output",
    "select_cases_for_output",
    "select_combos_for_output",
    "get_option_base_react_loc",
    "set_option_base_react_loc",
    "get_option_buckling_mode",
    "set_option_buckling_mode",
    "get_option_direct_hist",
    "set_option_direct_hist",
    "get_option_modal_hist",
    "set_option_modal_hist",
    "get_option_mode_shape",
    "set_option_mode_shape",
    "get_option_multi_step_static",
    "set_option_multi_step_static",
    "get_option_multi_valued_combo",
    "set_option_multi_valued_combo",
    "get_option_nl_static",
    "set_option_nl_static",
    "get_option_psd",
    "set_option_psd",
    "get_option_steady_state",
    "set_option_steady_state",
    "get_section_cut_selected_for_output",
    "set_section_cut_selected_for_output",
    "select_all_section_cuts_for_output",
    # 节点结果
    "get_joint_displ",
    "get_joint_displ_abs",
    "get_joint_react",
    "get_joint_acc",
    "get_joint_acc_abs",
    "get_joint_vel",
    "get_joint_vel_abs",
    "get_joint_resp_spec",
    # 框架结果
    "get_frame_force",
    "get_frame_joint_force",
    # 基底反力
    "get_base_react",
    "get_base_react_with_centroid",
    # 模态结果
    "get_modal_period",
    "get_mode_shape",
    "get_modal_participating_mass_ratios",
    "get_modal_load_participation_ratios",
    "get_modal_participation_factors",
    # 面单元结果
    "get_area_force_shell",
    "get_area_joint_force_plane",
    "get_area_joint_force_shell",
    "get_area_strain_shell",
    "get_area_strain_shell_layered",
    "get_area_stress_plane",
    "get_area_stress_shell",
    "get_area_stress_shell_layered",
    # 连接单元结果
    "get_link_deformation",
    "get_link_force",
    "get_link_joint_force",
    # 实体单元结果
    "get_solid_joint_force",
    "get_solid_strain",
    "get_solid_stress",
    # 杂项结果
    "get_assembled_joint_mass",
    "get_buckling_factor",
    "get_generalized_displ",
    "get_panel_zone_deformation",
    "get_panel_zone_force",
    "get_section_cut_analysis",
    "get_section_cut_design",
    "get_step_label",
]
