# -*- coding: utf-8 -*-
"""
design - 设计模块

SAP2000 的 Design API，用于结构设计。

支持四大设计类型：
- DesignSteel - 钢结构设计 (SapModel.DesignSteel)
- DesignConcrete - 混凝土框架设计 (SapModel.DesignConcrete)
- DesignConcreteShell - 混凝土壳设计 (SapModel.DesignConcreteShell)
- DesignAluminum - 铝结构设计 (SapModel.DesignAluminum)
- DesignColdFormed - 冷弯薄壁钢设计 (SapModel.DesignColdFormed)

Usage:
    from PySap2000.design import (
        # 钢结构
        set_steel_code, start_steel_design, get_steel_summary_results,
        SteelDesignCode, ItemType,
        # 混凝土
        set_concrete_code, start_concrete_design,
        get_concrete_summary_results_beam, get_concrete_summary_results_column,
        ConcreteDesignCode,
        # 铝结构
        set_aluminum_code, start_aluminum_design, get_aluminum_summary_results,
        AluminumDesignCode,
        # 冷弯薄壁钢
        set_cold_formed_code, start_cold_formed_design, get_cold_formed_summary_results,
        ColdFormedDesignCode,
    )
"""

# ============================================================================
# 通用枚举
# ============================================================================
from .enums import (
    ItemType,
    RatioType,
    ColumnDesignOption,
    # 钢结构
    SteelDesignCode, STEEL_CODE_NAMES, STEEL_CODE_FROM_NAME,
    # 混凝土
    ConcreteDesignCode, CONCRETE_CODE_NAMES, CONCRETE_CODE_FROM_NAME,
    ConcreteShellDesignCode, CONCRETE_SHELL_CODE_NAMES, CONCRETE_SHELL_CODE_FROM_NAME,
    # 铝结构
    AluminumDesignCode, ALUMINUM_CODE_NAMES, ALUMINUM_CODE_FROM_NAME,
    # 冷弯薄壁钢
    ColdFormedDesignCode, COLD_FORMED_CODE_NAMES, COLD_FORMED_CODE_FROM_NAME,
)

# ============================================================================
# 数据类
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
# 钢结构设计
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
# 钢结构 - 中国规范 GB 50017-2010
# ============================================================================
from .chinese_2010 import (
    # 枚举
    FramingType,
    ElementType,
    SeismicDesignGrade,
    MultiResponseDesign,
    DeflectionCheckType,
    OverwriteItem,
    PreferenceItem,
    # 数据类
    OverwriteResult,
    # 核心函数
    get_chinese_2010_preference,
    set_chinese_2010_preference,
    get_chinese_2010_overwrite,
    set_chinese_2010_overwrite,
    # 便捷函数
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
# 混凝土框架设计
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
# 混凝土壳设计
# ============================================================================
from .concrete_shell import (
    get_concrete_shell_code,
    set_concrete_shell_code,
    start_concrete_shell_design,
    delete_concrete_shell_results,
)

# ============================================================================
# 铝结构设计
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
# 冷弯薄壁钢设计
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
    # --- 通用枚举 ---
    "ItemType", "RatioType", "ColumnDesignOption",
    # --- 通用数据类 ---
    "VerifyPassedResult",
    # === 钢结构 ===
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
    # 钢结构 - 中国规范
    "FramingType", "ElementType", "SeismicDesignGrade",
    "MultiResponseDesign", "DeflectionCheckType",
    "OverwriteItem", "PreferenceItem", "OverwriteResult",
    "get_chinese_2010_preference", "set_chinese_2010_preference",
    "get_chinese_2010_overwrite", "set_chinese_2010_overwrite",
    "set_chinese_2010_framing_type", "set_chinese_2010_gamma0",
    "set_chinese_2010_seismic_grade", "set_chinese_2010_dc_ratio_limit",
    "set_chinese_2010_tall_building", "set_chinese_2010_element_type",
    "set_chinese_2010_mue_factors", "set_chinese_2010_unbraced_ratios",
    # === 混凝土框架 ===
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
    # === 混凝土壳 ===
    "ConcreteShellDesignCode", "CONCRETE_SHELL_CODE_NAMES", "CONCRETE_SHELL_CODE_FROM_NAME",
    "get_concrete_shell_code", "set_concrete_shell_code",
    "start_concrete_shell_design", "delete_concrete_shell_results",
    # === 铝结构 ===
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
    # === 冷弯薄壁钢 ===
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
# AI Agent 友好的 API 分类
# ============================================================================
DESIGN_API_CATEGORIES = {
    # ---- 钢结构 ----
    "steel_code": {
        "description": "钢结构设计规范",
        "functions": ["get_steel_code", "set_steel_code"],
        "enums": ["SteelDesignCode"],
        "api_path": "DesignSteel.GetCode/SetCode",
    },
    "steel_design": {
        "description": "钢结构设计执行",
        "functions": ["start_steel_design", "delete_steel_results", "get_steel_results_available"],
        "api_path": "DesignSteel.StartDesign/DeleteResults/GetResultsAvailable",
    },
    "steel_results": {
        "description": "钢结构设计结果",
        "functions": ["get_steel_summary_results", "verify_steel_passed", "verify_steel_sections"],
        "classes": ["SteelSummaryResult", "VerifyPassedResult"],
        "enums": ["RatioType", "ItemType"],
        "api_path": "DesignSteel.GetSummaryResults/VerifyPassed/VerifySections",
    },
    "steel_group": {
        "description": "钢结构设计组",
        "functions": ["get_steel_design_group", "set_steel_design_group"],
        "api_path": "DesignSteel.GetGroup/SetGroup",
    },
    "steel_section": {
        "description": "钢结构设计截面",
        "functions": ["get_steel_design_section", "set_steel_design_section", "set_steel_auto_select_null"],
        "api_path": "DesignSteel.GetDesignSection/SetDesignSection/SetAutoSelectNull",
    },
    "steel_combo": {
        "description": "钢结构设计组合",
        "functions": [
            "get_steel_combo_strength", "set_steel_combo_strength",
            "get_steel_combo_deflection", "set_steel_combo_deflection",
            "get_steel_combo_auto_generate", "set_steel_combo_auto_generate",
        ],
        "api_path": "DesignSteel.GetComboStrength/SetComboStrength/GetComboDeflection/SetComboDeflection/GetComboAutoGenerate/SetComboAutoGenerate",
    },
    "steel_overwrites": {
        "description": "钢结构设计覆盖",
        "functions": ["reset_steel_overwrites"],
        "api_path": "DesignSteel.ResetOverwrites",
    },
    "chinese_2010_preference": {
        "description": "中国钢结构规范 GB 50017-2010 首选项",
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
        "description": "中国钢结构规范 GB 50017-2010 覆盖项",
        "functions": [
            "get_chinese_2010_overwrite", "set_chinese_2010_overwrite",
            "set_chinese_2010_element_type", "set_chinese_2010_mue_factors",
            "set_chinese_2010_unbraced_ratios",
        ],
        "classes": ["OverwriteResult"],
        "enums": ["OverwriteItem", "ElementType", "DeflectionCheckType"],
        "api_path": "DesignSteel.Chinese_2010.GetOverwrite/SetOverwrite",
    },
    # ---- 混凝土框架 ----
    "concrete_code": {
        "description": "混凝土框架设计规范",
        "functions": ["get_concrete_code", "set_concrete_code"],
        "enums": ["ConcreteDesignCode"],
        "api_path": "DesignConcrete.GetCode/SetCode",
    },
    "concrete_design": {
        "description": "混凝土框架设计执行",
        "functions": ["start_concrete_design", "delete_concrete_results", "get_concrete_results_available"],
        "api_path": "DesignConcrete.StartDesign/DeleteResults/GetResultsAvailable",
    },
    "concrete_results": {
        "description": "混凝土框架设计结果（梁/柱/节点）",
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
        "description": "混凝土设计组",
        "functions": ["get_concrete_design_group", "set_concrete_design_group"],
        "api_path": "DesignConcrete.GetGroup/SetGroup",
    },
    "concrete_section": {
        "description": "混凝土设计截面",
        "functions": ["get_concrete_design_section", "set_concrete_design_section"],
        "api_path": "DesignConcrete.GetDesignSection/SetDesignSection",
    },
    "concrete_combo": {
        "description": "混凝土设计组合",
        "functions": [
            "get_concrete_combo_strength", "set_concrete_combo_strength",
            "get_concrete_combo_auto_generate", "set_concrete_combo_auto_generate",
        ],
        "api_path": "DesignConcrete.GetComboStrength/SetComboStrength/GetComboAutoGenerate/SetComboAutoGenerate",
    },
    "concrete_overwrites": {
        "description": "混凝土设计覆盖",
        "functions": ["reset_concrete_overwrites"],
        "api_path": "DesignConcrete.ResetOverwrites",
    },
    # ---- 混凝土壳 ----
    "concrete_shell_code": {
        "description": "混凝土壳设计规范",
        "functions": ["get_concrete_shell_code", "set_concrete_shell_code"],
        "enums": ["ConcreteShellDesignCode"],
        "api_path": "DesignConcreteShell.GetCode/SetCode",
    },
    "concrete_shell_design": {
        "description": "混凝土壳设计执行",
        "functions": ["start_concrete_shell_design", "delete_concrete_shell_results"],
        "api_path": "DesignConcreteShell.StartDesign/DeleteResults",
    },
    # ---- 铝结构 ----
    "aluminum_code": {
        "description": "铝结构设计规范",
        "functions": ["get_aluminum_code", "set_aluminum_code"],
        "enums": ["AluminumDesignCode"],
        "api_path": "DesignAluminum.GetCode/SetCode",
    },
    "aluminum_design": {
        "description": "铝结构设计执行",
        "functions": ["start_aluminum_design", "delete_aluminum_results", "get_aluminum_results_available"],
        "api_path": "DesignAluminum.StartDesign/DeleteResults/GetResultsAvailable",
    },
    "aluminum_results": {
        "description": "铝结构设计结果",
        "functions": ["get_aluminum_summary_results", "verify_aluminum_passed", "verify_aluminum_sections"],
        "classes": ["AluminumSummaryResult", "VerifyPassedResult"],
        "api_path": "DesignAluminum.GetSummaryResults/VerifyPassed/VerifySections",
    },
    "aluminum_group": {
        "description": "铝结构设计组",
        "functions": ["get_aluminum_design_group", "set_aluminum_design_group"],
        "api_path": "DesignAluminum.GetGroup/SetGroup",
    },
    "aluminum_section": {
        "description": "铝结构设计截面",
        "functions": ["get_aluminum_design_section", "set_aluminum_design_section", "set_aluminum_auto_select_null"],
        "api_path": "DesignAluminum.GetDesignSection/SetDesignSection/SetAutoSelectNull",
    },
    "aluminum_combo": {
        "description": "铝结构设计组合",
        "functions": [
            "get_aluminum_combo_strength", "set_aluminum_combo_strength",
            "get_aluminum_combo_deflection", "set_aluminum_combo_deflection",
            "get_aluminum_combo_auto_generate", "set_aluminum_combo_auto_generate",
        ],
        "api_path": "DesignAluminum.GetComboStrength/SetComboStrength/GetComboDeflection/SetComboDeflection/GetComboAutoGenerate/SetComboAutoGenerate",
    },
    "aluminum_overwrites": {
        "description": "铝结构设计覆盖",
        "functions": ["reset_aluminum_overwrites"],
        "api_path": "DesignAluminum.ResetOverwrites",
    },
    # ---- 冷弯薄壁钢 ----
    "cold_formed_code": {
        "description": "冷弯薄壁钢设计规范",
        "functions": ["get_cold_formed_code", "set_cold_formed_code"],
        "enums": ["ColdFormedDesignCode"],
        "api_path": "DesignColdFormed.GetCode/SetCode",
    },
    "cold_formed_design": {
        "description": "冷弯薄壁钢设计执行",
        "functions": ["start_cold_formed_design", "delete_cold_formed_results", "get_cold_formed_results_available"],
        "api_path": "DesignColdFormed.StartDesign/DeleteResults/GetResultsAvailable",
    },
    "cold_formed_results": {
        "description": "冷弯薄壁钢设计结果",
        "functions": ["get_cold_formed_summary_results", "verify_cold_formed_passed", "verify_cold_formed_sections"],
        "classes": ["ColdFormedSummaryResult", "VerifyPassedResult"],
        "api_path": "DesignColdFormed.GetSummaryResults/VerifyPassed/VerifySections",
    },
    "cold_formed_group": {
        "description": "冷弯薄壁钢设计组",
        "functions": ["get_cold_formed_design_group", "set_cold_formed_design_group"],
        "api_path": "DesignColdFormed.GetGroup/SetGroup",
    },
    "cold_formed_section": {
        "description": "冷弯薄壁钢设计截面",
        "functions": ["get_cold_formed_design_section", "set_cold_formed_design_section", "set_cold_formed_auto_select_null"],
        "api_path": "DesignColdFormed.GetDesignSection/SetDesignSection/SetAutoSelectNull",
    },
    "cold_formed_combo": {
        "description": "冷弯薄壁钢设计组合",
        "functions": [
            "get_cold_formed_combo_strength", "set_cold_formed_combo_strength",
            "get_cold_formed_combo_deflection", "set_cold_formed_combo_deflection",
            "get_cold_formed_combo_auto_generate", "set_cold_formed_combo_auto_generate",
        ],
        "api_path": "DesignColdFormed.GetComboStrength/SetComboStrength/GetComboDeflection/SetComboDeflection/GetComboAutoGenerate/SetComboAutoGenerate",
    },
    "cold_formed_overwrites": {
        "description": "冷弯薄壁钢设计覆盖",
        "functions": ["reset_cold_formed_overwrites"],
        "api_path": "DesignColdFormed.ResetOverwrites",
    },
}
