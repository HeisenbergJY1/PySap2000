# -*- coding: utf-8 -*-
"""
results - Analysis result helpers.

Wraps the SAP2000 `Results` API for extracting analysis output.

SAP2000 API structure:
- `Results.Setup`: output-selection settings
- `Results`: result extraction

Usage:
    from PySap2000.results import (
        # Output setup
        deselect_all_cases_and_combos,
        set_case_selected_for_output,
        select_cases_for_output,
        # Joint results
        get_joint_displ,
        get_joint_react,
        # Frame results
        get_frame_force,
        # Base reactions
        get_base_react,
        # Modal results
        get_modal_period,
        # Enums
        ItemTypeElm,
    )

    # Typical workflow
    deselect_all_cases_and_combos(model)
    set_case_selected_for_output(model, "DEAD")

    displ = get_joint_displ(model, "ALL", ItemTypeElm.GROUP_ELM)
    forces = get_frame_force(model, "1", ItemTypeElm.OBJECT_ELM)
"""

from .enums import ItemTypeElm

# =============================================================================
# Data classes
# =============================================================================
from .data_classes import (
    # Joint results
    JointDisplResult,
    JointReactResult,
    JointDisplAbsResult,
    JointAccResult,
    JointAccAbsResult,
    JointVelResult,
    JointVelAbsResult,
    JointRespSpecResult,
    # Frame results
    FrameForceResult,
    FrameJointForceResult,
    # Base reactions
    BaseReactResult,
    BaseReactWithCentroidResult,
    # Modal results
    ModalPeriodResult,
    ModeShapeResult,
    ModalMassRatioResult,
    ModalLoadParticipationRatioResult,
    ModalParticipationFactorResult,
    # Area results
    AreaForceShellResult,
    AreaJointForcePlaneResult,
    AreaJointForceShellResult,
    AreaStrainShellResult,
    AreaStrainShellLayeredResult,
    AreaStressPlaneResult,
    AreaStressShellResult,
    AreaStressShellLayeredResult,
    # Link results
    LinkDeformationResult,
    LinkForceResult,
    LinkJointForceResult,
    # Solid results
    SolidJointForceResult,
    SolidStrainResult,
    SolidStressResult,
    # Miscellaneous results
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
# Output setup functions
# =============================================================================
from .setup import (
    # Case/combo selection
    deselect_all_cases_and_combos,
    set_case_selected_for_output,
    get_case_selected_for_output,
    set_combo_selected_for_output,
    get_combo_selected_for_output,
    select_cases_for_output,
    select_combos_for_output,
    # Base reaction location
    get_option_base_react_loc,
    set_option_base_react_loc,
    # Buckling mode
    get_option_buckling_mode,
    set_option_buckling_mode,
    # Direct-integration time history
    get_option_direct_hist,
    set_option_direct_hist,
    # Modal time history
    get_option_modal_hist,
    set_option_modal_hist,
    # Mode shape
    get_option_mode_shape,
    set_option_mode_shape,
    # Multi-step static
    get_option_multi_step_static,
    set_option_multi_step_static,
    # Multi-valued combo
    get_option_multi_valued_combo,
    set_option_multi_valued_combo,
    # Nonlinear static
    get_option_nl_static,
    set_option_nl_static,
    # Power spectral density
    get_option_psd,
    set_option_psd,
    # Steady-state
    get_option_steady_state,
    set_option_steady_state,
    # Section cuts
    get_section_cut_selected_for_output,
    set_section_cut_selected_for_output,
    select_all_section_cuts_for_output,
)

# =============================================================================
# Joint result functions
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
# Frame result functions
# =============================================================================
from .frame_results import (
    get_frame_force,
    get_frame_joint_force,
)

# =============================================================================
# Base reaction functions
# =============================================================================
from .base_react import (
    get_base_react,
)

# =============================================================================
# Modal result functions
# =============================================================================
from .modal_results import (
    get_modal_period,
    get_mode_shape,
    get_modal_participating_mass_ratios,
    get_modal_load_participation_ratios,
    get_modal_participation_factors,
)

# =============================================================================
# Area result functions
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
# Link result functions
# =============================================================================
from .link_results import (
    get_link_deformation,
    get_link_force,
    get_link_joint_force,
)

# =============================================================================
# Solid result functions
# =============================================================================
from .solid_results import (
    get_solid_joint_force,
    get_solid_strain,
    get_solid_stress,
)

# =============================================================================
# Miscellaneous result functions
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
    # Enums
    "ItemTypeElm",
    # Data classes - joints
    "JointDisplResult",
    "JointReactResult",
    "JointDisplAbsResult",
    "JointAccResult",
    "JointAccAbsResult",
    "JointVelResult",
    "JointVelAbsResult",
    "JointRespSpecResult",
    # Data classes - frames
    "FrameForceResult",
    "FrameJointForceResult",
    # Data classes - base reactions
    "BaseReactResult",
    "BaseReactWithCentroidResult",
    # Data classes - modal
    "ModalPeriodResult",
    "ModeShapeResult",
    "ModalMassRatioResult",
    "ModalLoadParticipationRatioResult",
    "ModalParticipationFactorResult",
    # Data classes - areas
    "AreaForceShellResult",
    "AreaJointForcePlaneResult",
    "AreaJointForceShellResult",
    "AreaStrainShellResult",
    "AreaStrainShellLayeredResult",
    "AreaStressPlaneResult",
    "AreaStressShellResult",
    "AreaStressShellLayeredResult",
    # Data classes - links
    "LinkDeformationResult",
    "LinkForceResult",
    "LinkJointForceResult",
    # Data classes - solids
    "SolidJointForceResult",
    "SolidStrainResult",
    "SolidStressResult",
    # Data classes - miscellaneous
    "AssembledJointMassResult",
    "BucklingFactorResult",
    "GeneralizedDisplResult",
    "PanelZoneDeformationResult",
    "PanelZoneForceResult",
    "SectionCutAnalysisResult",
    "SectionCutDesignResult",
    "StepLabelResult",
    # Output setup
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
    # Joint results
    "get_joint_displ",
    "get_joint_displ_abs",
    "get_joint_react",
    "get_joint_acc",
    "get_joint_acc_abs",
    "get_joint_vel",
    "get_joint_vel_abs",
    "get_joint_resp_spec",
    # Frame results
    "get_frame_force",
    "get_frame_joint_force",
    # Base reactions
    "get_base_react",
    "get_base_react_with_centroid",
    # Modal results
    "get_modal_period",
    "get_mode_shape",
    "get_modal_participating_mass_ratios",
    "get_modal_load_participation_ratios",
    "get_modal_participation_factors",
    # Area results
    "get_area_force_shell",
    "get_area_joint_force_plane",
    "get_area_joint_force_shell",
    "get_area_strain_shell",
    "get_area_strain_shell_layered",
    "get_area_stress_plane",
    "get_area_stress_shell",
    "get_area_stress_shell_layered",
    # Link results
    "get_link_deformation",
    "get_link_force",
    "get_link_joint_force",
    # Solid results
    "get_solid_joint_force",
    "get_solid_strain",
    "get_solid_stress",
    # Miscellaneous results
    "get_assembled_joint_mass",
    "get_buckling_factor",
    "get_generalized_displ",
    "get_panel_zone_deformation",
    "get_panel_zone_force",
    "get_section_cut_analysis",
    "get_section_cut_design",
    "get_step_label",
]
