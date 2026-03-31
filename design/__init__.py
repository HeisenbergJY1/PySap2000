# -*- coding: utf-8 -*-
"""
design - Structural design helpers.

Wraps SAP2000 design APIs for steel, concrete, aluminum, and cold-formed members.

- `DesignSteel` — steel design (`SapModel.DesignSteel`)
- `DesignConcrete` — concrete frame design (`SapModel.DesignConcrete`)
- `DesignConcreteShell` — concrete shell design (`SapModel.DesignConcreteShell`)
- `DesignAluminum` — aluminum design (`SapModel.DesignAluminum`)
- `DesignColdFormed` — cold-formed steel design (`SapModel.DesignColdFormed`)

Usage:
    from PySap2000.design import (
        # Steel
        set_steel_code, start_steel_design, get_steel_summary_results,
        SteelDesignCode, ItemType,
        # Concrete
        set_concrete_code, start_concrete_design,
        get_concrete_summary_results_beam, get_concrete_summary_results_column,
        ConcreteDesignCode,
        # Aluminum
        set_aluminum_code, start_aluminum_design, get_aluminum_summary_results,
        AluminumDesignCode,
        # Cold-formed
        set_cold_formed_code, start_cold_formed_design, get_cold_formed_summary_results,
        ColdFormedDesignCode,
    )
"""

# ============================================================================
# Shared enums
# ============================================================================
from .enums import (
    ItemType,
    RatioType,
    ColumnDesignOption,
    # Steel
    SteelDesignCode, STEEL_CODE_NAMES, STEEL_CODE_FROM_NAME,
    # Concrete
    ConcreteDesignCode, CONCRETE_CODE_NAMES, CONCRETE_CODE_FROM_NAME,
    ConcreteShellDesignCode, CONCRETE_SHELL_CODE_NAMES, CONCRETE_SHELL_CODE_FROM_NAME,
    # Aluminum
    AluminumDesignCode, ALUMINUM_CODE_NAMES, ALUMINUM_CODE_FROM_NAME,
    # Cold-formed
    ColdFormedDesignCode, COLD_FORMED_CODE_NAMES, COLD_FORMED_CODE_FROM_NAME,
)

# ============================================================================
# Dataclasses
# ============================================================================
from .data_classes import (
    SteelSummaryResult,
    AluminumSummaryResult,
    ColdFormedSummaryResult,
    VerifyPassedResult,
    ConcreteBeamResult,
    ConcreteColumnResult,
    ConcreteJointResult,
)

# ============================================================================
# Steel design
# ============================================================================
from .steel import (
    get_steel_code,
    set_steel_code,
    start_steel_design,
    delete_steel_results,
    get_steel_results_available,
    get_steel_summary_results,
    get_steel_design_group,
    set_steel_design_group,
    get_steel_design_section,
    set_steel_design_section,
    set_steel_auto_select_null,
    get_steel_combo_strength,
    set_steel_combo_strength,
    get_steel_combo_deflection,
    set_steel_combo_deflection,
    get_steel_combo_auto_generate,
    set_steel_combo_auto_generate,
    reset_steel_overwrites,
    verify_steel_passed,
    verify_steel_sections,
)

# ============================================================================
# Steel — GB 50017-2010 (Chinese_2010)
# ============================================================================
from .chinese_2010 import (
    # Enums
    FramingType,
    ElementType,
    SeismicDesignGrade,
    MultiResponseDesign,
    DeflectionCheckType,
    OverwriteItem,
    PreferenceItem,
    # Dataclasses
    OverwriteResult,
    # Core API
    get_chinese_2010_preference,
    set_chinese_2010_preference,
    get_chinese_2010_overwrite,
    set_chinese_2010_overwrite,
    # Shortcuts
    set_chinese_2010_framing_type,
    set_chinese_2010_gamma0,
    set_chinese_2010_seismic_grade,
    set_chinese_2010_dc_ratio_limit,
    set_chinese_2010_tall_building,
    set_chinese_2010_element_type,
    set_chinese_2010_mue_factors,
    set_chinese_2010_unbraced_ratios,
)

# ============================================================================
# Concrete frame design
# ============================================================================
from .concrete import (
    get_concrete_code,
    set_concrete_code,
    start_concrete_design,
    delete_concrete_results,
    get_concrete_results_available,
    get_concrete_combo_strength,
    set_concrete_combo_strength,
    get_concrete_combo_auto_generate,
    set_concrete_combo_auto_generate,
    get_concrete_design_group,
    set_concrete_design_group,
    get_concrete_design_section,
    set_concrete_design_section,
    reset_concrete_overwrites,
    verify_concrete_passed,
    verify_concrete_sections,
    get_concrete_summary_results_beam,
    get_concrete_summary_results_column,
    get_concrete_summary_results_joint,
)

# ============================================================================
# Concrete shell design
# ============================================================================
from .concrete_shell import (
    get_concrete_shell_code,
    set_concrete_shell_code,
    start_concrete_shell_design,
    delete_concrete_shell_results,
)

# ============================================================================
# Aluminum design
# ============================================================================
from .aluminum import (
    get_aluminum_code,
    set_aluminum_code,
    start_aluminum_design,
    delete_aluminum_results,
    get_aluminum_results_available,
    get_aluminum_combo_strength,
    set_aluminum_combo_strength,
    get_aluminum_combo_deflection,
    set_aluminum_combo_deflection,
    get_aluminum_combo_auto_generate,
    set_aluminum_combo_auto_generate,
    get_aluminum_design_group,
    set_aluminum_design_group,
    get_aluminum_design_section,
    set_aluminum_design_section,
    set_aluminum_auto_select_null,
    reset_aluminum_overwrites,
    verify_aluminum_passed,
    verify_aluminum_sections,
    get_aluminum_summary_results,
)

# ============================================================================
# Cold-formed steel design
# ============================================================================
from .cold_formed import (
    get_cold_formed_code,
    set_cold_formed_code,
    start_cold_formed_design,
    delete_cold_formed_results,
    get_cold_formed_results_available,
    get_cold_formed_combo_strength,
    set_cold_formed_combo_strength,
    get_cold_formed_combo_deflection,
    set_cold_formed_combo_deflection,
    get_cold_formed_combo_auto_generate,
    set_cold_formed_combo_auto_generate,
    get_cold_formed_design_group,
    set_cold_formed_design_group,
    get_cold_formed_design_section,
    set_cold_formed_design_section,
    set_cold_formed_auto_select_null,
    reset_cold_formed_overwrites,
    verify_cold_formed_passed,
    verify_cold_formed_sections,
    get_cold_formed_summary_results,
)

# ============================================================================
# __all__
# ============================================================================
__all__ = [
    # --- Shared enums ---
    "ItemType", "RatioType", "ColumnDesignOption",
    # --- Shared dataclasses ---
    "VerifyPassedResult",
    # === Steel ===
    "SteelDesignCode", "STEEL_CODE_NAMES", "STEEL_CODE_FROM_NAME",
    "SteelSummaryResult",
    "get_steel_code", "set_steel_code",
    "start_steel_design", "delete_steel_results", "get_steel_results_available",
    "get_steel_summary_results",
    "get_steel_design_group", "set_steel_design_group",
    "get_steel_design_section", "set_steel_design_section", "set_steel_auto_select_null",
    "get_steel_combo_strength", "set_steel_combo_strength",
    "get_steel_combo_deflection", "set_steel_combo_deflection",
    "get_steel_combo_auto_generate", "set_steel_combo_auto_generate",
    "reset_steel_overwrites", "verify_steel_passed", "verify_steel_sections",
    # Steel - GB 50017-2010
    "FramingType", "ElementType", "SeismicDesignGrade",
    "MultiResponseDesign", "DeflectionCheckType",
    "OverwriteItem", "PreferenceItem", "OverwriteResult",
    "get_chinese_2010_preference", "set_chinese_2010_preference",
    "get_chinese_2010_overwrite", "set_chinese_2010_overwrite",
    "set_chinese_2010_framing_type", "set_chinese_2010_gamma0",
    "set_chinese_2010_seismic_grade", "set_chinese_2010_dc_ratio_limit",
    "set_chinese_2010_tall_building", "set_chinese_2010_element_type",
    "set_chinese_2010_mue_factors", "set_chinese_2010_unbraced_ratios",
    # === Concrete frame ===
    "ConcreteDesignCode", "CONCRETE_CODE_NAMES", "CONCRETE_CODE_FROM_NAME",
    "ConcreteBeamResult", "ConcreteColumnResult", "ConcreteJointResult",
    "get_concrete_code", "set_concrete_code",
    "start_concrete_design", "delete_concrete_results", "get_concrete_results_available",
    "get_concrete_combo_strength", "set_concrete_combo_strength",
    "get_concrete_combo_auto_generate", "set_concrete_combo_auto_generate",
    "get_concrete_design_group", "set_concrete_design_group",
    "get_concrete_design_section", "set_concrete_design_section",
    "reset_concrete_overwrites", "verify_concrete_passed", "verify_concrete_sections",
    "get_concrete_summary_results_beam", "get_concrete_summary_results_column",
    "get_concrete_summary_results_joint",
    # === Concrete shell ===
    "ConcreteShellDesignCode", "CONCRETE_SHELL_CODE_NAMES", "CONCRETE_SHELL_CODE_FROM_NAME",
    "get_concrete_shell_code", "set_concrete_shell_code",
    "start_concrete_shell_design", "delete_concrete_shell_results",
    # === Aluminum ===
    "AluminumDesignCode", "ALUMINUM_CODE_NAMES", "ALUMINUM_CODE_FROM_NAME",
    "AluminumSummaryResult",
    "get_aluminum_code", "set_aluminum_code",
    "start_aluminum_design", "delete_aluminum_results", "get_aluminum_results_available",
    "get_aluminum_combo_strength", "set_aluminum_combo_strength",
    "get_aluminum_combo_deflection", "set_aluminum_combo_deflection",
    "get_aluminum_combo_auto_generate", "set_aluminum_combo_auto_generate",
    "get_aluminum_design_group", "set_aluminum_design_group",
    "get_aluminum_design_section", "set_aluminum_design_section",
    "set_aluminum_auto_select_null",
    "reset_aluminum_overwrites", "verify_aluminum_passed", "verify_aluminum_sections",
    "get_aluminum_summary_results",
    # === Cold-formed steel ===
    "ColdFormedDesignCode", "COLD_FORMED_CODE_NAMES", "COLD_FORMED_CODE_FROM_NAME",
    "ColdFormedSummaryResult",
    "get_cold_formed_code", "set_cold_formed_code",
    "start_cold_formed_design", "delete_cold_formed_results", "get_cold_formed_results_available",
    "get_cold_formed_combo_strength", "set_cold_formed_combo_strength",
    "get_cold_formed_combo_deflection", "set_cold_formed_combo_deflection",
    "get_cold_formed_combo_auto_generate", "set_cold_formed_combo_auto_generate",
    "get_cold_formed_design_group", "set_cold_formed_design_group",
    "get_cold_formed_design_section", "set_cold_formed_design_section",
    "set_cold_formed_auto_select_null",
    "reset_cold_formed_overwrites", "verify_cold_formed_passed", "verify_cold_formed_sections",
    "get_cold_formed_summary_results",
]

# ============================================================================
# API categories for discoverability
# ============================================================================
DESIGN_API_CATEGORIES = {
    # ---- Steel ----
    "steel_code": {
        "description": "Steel design code selection",
        "functions": ["get_steel_code", "set_steel_code"],
        "enums": ["SteelDesignCode"],
        "api_path": "DesignSteel.GetCode/SetCode",
    },
    "steel_design": {
        "description": "Steel design execution",
        "functions": ["start_steel_design", "delete_steel_results", "get_steel_results_available"],
        "api_path": "DesignSteel.StartDesign/DeleteResults/GetResultsAvailable",
    },
    "steel_results": {
        "description": "Steel design results",
        "functions": ["get_steel_summary_results", "verify_steel_passed", "verify_steel_sections"],
        "classes": ["SteelSummaryResult", "VerifyPassedResult"],
        "enums": ["RatioType", "ItemType"],
        "api_path": "DesignSteel.GetSummaryResults/VerifyPassed/VerifySections",
    },
    "steel_group": {
        "description": "Steel design groups",
        "functions": ["get_steel_design_group", "set_steel_design_group"],
        "api_path": "DesignSteel.GetGroup/SetGroup",
    },
    "steel_section": {
        "description": "Steel design sections",
        "functions": ["get_steel_design_section", "set_steel_design_section", "set_steel_auto_select_null"],
        "api_path": "DesignSteel.GetDesignSection/SetDesignSection/SetAutoSelectNull",
    },
    "steel_combo": {
        "description": "Steel design combinations",
        "functions": [
            "get_steel_combo_strength", "set_steel_combo_strength",
            "get_steel_combo_deflection", "set_steel_combo_deflection",
            "get_steel_combo_auto_generate", "set_steel_combo_auto_generate",
        ],
        "api_path": "DesignSteel.GetComboStrength/SetComboStrength/GetComboDeflection/SetComboDeflection/GetComboAutoGenerate/SetComboAutoGenerate",
    },
    "steel_overwrites": {
        "description": "Steel design overwrites",
        "functions": ["reset_steel_overwrites"],
        "api_path": "DesignSteel.ResetOverwrites",
    },
    "chinese_2010_preference": {
        "description": "GB 50017-2010 preference values",
        "functions": [
            "get_chinese_2010_preference", "set_chinese_2010_preference",
            "set_chinese_2010_framing_type", "set_chinese_2010_gamma0",
            "set_chinese_2010_seismic_grade", "set_chinese_2010_dc_ratio_limit",
            "set_chinese_2010_tall_building",
        ],
        "enums": ["PreferenceItem", "FramingType", "SeismicDesignGrade", "MultiResponseDesign"],
        "api_path": "DesignSteel.Chinese_2010.GetPreference/SetPreference",
    },
    "chinese_2010_overwrite": {
        "description": "GB 50017-2010 overwrite values",
        "functions": [
            "get_chinese_2010_overwrite", "set_chinese_2010_overwrite",
            "set_chinese_2010_element_type", "set_chinese_2010_mue_factors",
            "set_chinese_2010_unbraced_ratios",
        ],
        "classes": ["OverwriteResult"],
        "enums": ["OverwriteItem", "ElementType", "DeflectionCheckType"],
        "api_path": "DesignSteel.Chinese_2010.GetOverwrite/SetOverwrite",
    },
    # ---- Concrete frame ----
    "concrete_code": {
        "description": "Concrete frame design code selection",
        "functions": ["get_concrete_code", "set_concrete_code"],
        "enums": ["ConcreteDesignCode"],
        "api_path": "DesignConcrete.GetCode/SetCode",
    },
    "concrete_design": {
        "description": "Concrete frame design execution",
        "functions": ["start_concrete_design", "delete_concrete_results", "get_concrete_results_available"],
        "api_path": "DesignConcrete.StartDesign/DeleteResults/GetResultsAvailable",
    },
    "concrete_results": {
        "description": "Concrete frame design results for beams, columns, and joints",
        "functions": [
            "get_concrete_summary_results_beam",
            "get_concrete_summary_results_column",
            "get_concrete_summary_results_joint",
            "verify_concrete_passed", "verify_concrete_sections",
        ],
        "classes": ["ConcreteBeamResult", "ConcreteColumnResult", "ConcreteJointResult", "VerifyPassedResult"],
        "enums": ["ColumnDesignOption", "ItemType"],
        "api_path": "DesignConcrete.GetSummaryResultsBeam/GetSummaryResultsColumn/GetSummaryResultsJoint/VerifyPassed/VerifySections",
    },
    "concrete_group": {
        "description": "Concrete design groups",
        "functions": ["get_concrete_design_group", "set_concrete_design_group"],
        "api_path": "DesignConcrete.GetGroup/SetGroup",
    },
    "concrete_section": {
        "description": "Concrete design sections",
        "functions": ["get_concrete_design_section", "set_concrete_design_section"],
        "api_path": "DesignConcrete.GetDesignSection/SetDesignSection",
    },
    "concrete_combo": {
        "description": "Concrete design combinations",
        "functions": [
            "get_concrete_combo_strength", "set_concrete_combo_strength",
            "get_concrete_combo_auto_generate", "set_concrete_combo_auto_generate",
        ],
        "api_path": "DesignConcrete.GetComboStrength/SetComboStrength/GetComboAutoGenerate/SetComboAutoGenerate",
    },
    "concrete_overwrites": {
        "description": "Concrete design overwrites",
        "functions": ["reset_concrete_overwrites"],
        "api_path": "DesignConcrete.ResetOverwrites",
    },
    # ---- Concrete shell ----
    "concrete_shell_code": {
        "description": "Concrete shell design code selection",
        "functions": ["get_concrete_shell_code", "set_concrete_shell_code"],
        "enums": ["ConcreteShellDesignCode"],
        "api_path": "DesignConcreteShell.GetCode/SetCode",
    },
    "concrete_shell_design": {
        "description": "Concrete shell design execution",
        "functions": ["start_concrete_shell_design", "delete_concrete_shell_results"],
        "api_path": "DesignConcreteShell.StartDesign/DeleteResults",
    },
    # ---- Aluminum ----
    "aluminum_code": {
        "description": "Aluminum design code selection",
        "functions": ["get_aluminum_code", "set_aluminum_code"],
        "enums": ["AluminumDesignCode"],
        "api_path": "DesignAluminum.GetCode/SetCode",
    },
    "aluminum_design": {
        "description": "Aluminum design execution",
        "functions": ["start_aluminum_design", "delete_aluminum_results", "get_aluminum_results_available"],
        "api_path": "DesignAluminum.StartDesign/DeleteResults/GetResultsAvailable",
    },
    "aluminum_results": {
        "description": "Aluminum design results",
        "functions": ["get_aluminum_summary_results", "verify_aluminum_passed", "verify_aluminum_sections"],
        "classes": ["AluminumSummaryResult", "VerifyPassedResult"],
        "api_path": "DesignAluminum.GetSummaryResults/VerifyPassed/VerifySections",
    },
    "aluminum_group": {
        "description": "Aluminum design groups",
        "functions": ["get_aluminum_design_group", "set_aluminum_design_group"],
        "api_path": "DesignAluminum.GetGroup/SetGroup",
    },
    "aluminum_section": {
        "description": "Aluminum design sections",
        "functions": ["get_aluminum_design_section", "set_aluminum_design_section", "set_aluminum_auto_select_null"],
        "api_path": "DesignAluminum.GetDesignSection/SetDesignSection/SetAutoSelectNull",
    },
    "aluminum_combo": {
        "description": "Aluminum design combinations",
        "functions": [
            "get_aluminum_combo_strength", "set_aluminum_combo_strength",
            "get_aluminum_combo_deflection", "set_aluminum_combo_deflection",
            "get_aluminum_combo_auto_generate", "set_aluminum_combo_auto_generate",
        ],
        "api_path": "DesignAluminum.GetComboStrength/SetComboStrength/GetComboDeflection/SetComboDeflection/GetComboAutoGenerate/SetComboAutoGenerate",
    },
    "aluminum_overwrites": {
        "description": "Aluminum design overwrites",
        "functions": ["reset_aluminum_overwrites"],
        "api_path": "DesignAluminum.ResetOverwrites",
    },
    # ---- Cold-formed steel ----
    "cold_formed_code": {
        "description": "Cold-formed steel design code selection",
        "functions": ["get_cold_formed_code", "set_cold_formed_code"],
        "enums": ["ColdFormedDesignCode"],
        "api_path": "DesignColdFormed.GetCode/SetCode",
    },
    "cold_formed_design": {
        "description": "Cold-formed steel design execution",
        "functions": ["start_cold_formed_design", "delete_cold_formed_results", "get_cold_formed_results_available"],
        "api_path": "DesignColdFormed.StartDesign/DeleteResults/GetResultsAvailable",
    },
    "cold_formed_results": {
        "description": "Cold-formed steel design results",
        "functions": ["get_cold_formed_summary_results", "verify_cold_formed_passed", "verify_cold_formed_sections"],
        "classes": ["ColdFormedSummaryResult", "VerifyPassedResult"],
        "api_path": "DesignColdFormed.GetSummaryResults/VerifyPassed/VerifySections",
    },
    "cold_formed_group": {
        "description": "Cold-formed steel design groups",
        "functions": ["get_cold_formed_design_group", "set_cold_formed_design_group"],
        "api_path": "DesignColdFormed.GetGroup/SetGroup",
    },
    "cold_formed_section": {
        "description": "Cold-formed steel design sections",
        "functions": ["get_cold_formed_design_section", "set_cold_formed_design_section", "set_cold_formed_auto_select_null"],
        "api_path": "DesignColdFormed.GetDesignSection/SetDesignSection/SetAutoSelectNull",
    },
    "cold_formed_combo": {
        "description": "Cold-formed steel design combinations",
        "functions": [
            "get_cold_formed_combo_strength", "set_cold_formed_combo_strength",
            "get_cold_formed_combo_deflection", "set_cold_formed_combo_deflection",
            "get_cold_formed_combo_auto_generate", "set_cold_formed_combo_auto_generate",
        ],
        "api_path": "DesignColdFormed.GetComboStrength/SetComboStrength/GetComboDeflection/SetComboDeflection/GetComboAutoGenerate/SetComboAutoGenerate",
    },
    "cold_formed_overwrites": {
        "description": "Cold-formed steel design overwrites",
        "functions": ["reset_cold_formed_overwrites"],
        "api_path": "DesignColdFormed.ResetOverwrites",
    },
}
