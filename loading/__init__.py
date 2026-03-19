# -*- coding: utf-8 -*-
"""
loading - 荷载模式、工况、组合和质量源

SAP2000 术语:
    LoadPattern - 荷载模式 (如 DEAD, LIVE)
    LoadCase - 荷载工况/分析工况 (如 线性静力、模态、反应谱)
    LoadCombination - 荷载组合
    MassSource - 质量源 (动力分析质量来源)
"""

from .load_pattern import LoadPattern, LoadPatternType
from .load_case import (
    LoadCase,
    LoadCaseType,
    LoadCaseLoad,
    ModalSubType,
    TimeHistorySubType,
    DesignTypeOption,
    # 创建函数
    create_static_linear_case,
    create_static_nonlinear_case,
    create_modal_eigen_case,
    create_modal_ritz_case,
    create_response_spectrum_case,
    create_buckling_case,
    create_direct_history_linear_case,
    create_direct_history_nonlinear_case,
    create_modal_history_linear_case,
    create_modal_history_nonlinear_case,
    create_steady_state_case,
    create_psd_case,
    create_moving_load_case,
    create_hyperstatic_case,
    create_static_linear_multistep_case,
    create_static_nonlinear_multistep_case,
    create_staged_construction_case,
    # 荷载设置函数
    get_static_linear_loads,
    set_static_linear_loads,
)
from .load_combination import (
    # 枚举
    ComboCaseType,
    ComboType,
    # 函数
    add_combo,
    add_design_default_combos,
    change_combo_name,
    get_combo_count,
    get_combo_case_count,
    delete_combo,
    delete_combo_case,
    get_combo_name_list,
    get_combo_case_list,
    set_combo_case_list,
    get_combo_note,
    set_combo_note,
    get_combo_type,
    set_combo_type,
)
from .mass_source import MassSource, MassSourceLoad

# 函数定义 (时程函数、反应谱函数)
from .functions import (
    # 枚举
    FuncType,
    Chinese2010SiteClass,
    Chinese2010DesignGroup,
    # 通用管理
    change_func_name,
    convert_func_to_user,
    get_func_count,
    delete_func,
    get_func_name_list,
    get_func_type,
    get_func_values,
    # 时程数据类
    CosineParams,
    RampParams,
    SawtoothParams,
    SineParams,
    TriangularParams,
    FromFileParams,
    # 反应谱数据类
    Chinese2010Params,
    # 时程函数
    get_func_th_cosine,
    set_func_th_cosine,
    get_func_th_from_file,
    set_func_th_from_file,
    get_func_th_ramp,
    set_func_th_ramp,
    get_func_th_sawtooth,
    set_func_th_sawtooth,
    get_func_th_sine,
    set_func_th_sine,
    get_func_th_triangular,
    set_func_th_triangular,
    get_func_th_user,
    set_func_th_user,
    get_func_th_user_periodic,
    set_func_th_user_periodic,
    # 反应谱函数
    get_func_rs_chinese_2010,
    set_func_rs_chinese_2010,
    get_func_rs_user,
    set_func_rs_user,
    get_func_rs_from_file,
    set_func_rs_from_file,
)

__all__ = [
    # 荷载模式
    "LoadPattern",
    "LoadPatternType",
    # 荷载工况
    "LoadCase",
    "LoadCaseType",
    "LoadCaseLoad",
    "ModalSubType",
    "TimeHistorySubType",
    "DesignTypeOption",
    # 工况创建函数
    "create_static_linear_case",
    "create_static_nonlinear_case",
    "create_modal_eigen_case",
    "create_modal_ritz_case",
    "create_response_spectrum_case",
    "create_buckling_case",
    "create_direct_history_linear_case",
    "create_direct_history_nonlinear_case",
    "create_modal_history_linear_case",
    "create_modal_history_nonlinear_case",
    "create_steady_state_case",
    "create_psd_case",
    "create_moving_load_case",
    "create_hyperstatic_case",
    "create_static_linear_multistep_case",
    "create_static_nonlinear_multistep_case",
    "create_staged_construction_case",
    # 荷载设置函数
    "get_static_linear_loads",
    "set_static_linear_loads",
    # 荷载组合
    "ComboCaseType",
    "ComboType",
    "add_combo",
    "add_design_default_combos",
    "change_combo_name",
    "get_combo_count",
    "get_combo_case_count",
    "delete_combo",
    "delete_combo_case",
    "get_combo_name_list",
    "get_combo_case_list",
    "set_combo_case_list",
    "get_combo_note",
    "set_combo_note",
    "get_combo_type",
    "set_combo_type",
    # 质量源
    "MassSource",
    "MassSourceLoad",
    # 函数定义 - 枚举
    "FuncType",
    "Chinese2010SiteClass",
    "Chinese2010DesignGroup",
    # 函数定义 - 通用管理
    "change_func_name",
    "convert_func_to_user",
    "get_func_count",
    "delete_func",
    "get_func_name_list",
    "get_func_type",
    "get_func_values",
    # 函数定义 - 时程数据类
    "CosineParams",
    "RampParams",
    "SawtoothParams",
    "SineParams",
    "TriangularParams",
    "FromFileParams",
    # 函数定义 - 反应谱数据类
    "Chinese2010Params",
    # 函数定义 - 时程函数
    "get_func_th_cosine",
    "set_func_th_cosine",
    "get_func_th_from_file",
    "set_func_th_from_file",
    "get_func_th_ramp",
    "set_func_th_ramp",
    "get_func_th_sawtooth",
    "set_func_th_sawtooth",
    "get_func_th_sine",
    "set_func_th_sine",
    "get_func_th_triangular",
    "set_func_th_triangular",
    "get_func_th_user",
    "set_func_th_user",
    "get_func_th_user_periodic",
    "set_func_th_user_periodic",
    # 函数定义 - 反应谱函数
    "get_func_rs_chinese_2010",
    "set_func_rs_chinese_2010",
    "get_func_rs_user",
    "set_func_rs_user",
    "get_func_rs_from_file",
    "set_func_rs_from_file",
]

# AI Agent 友好的 API 分类
LOADING_API_CATEGORIES = {
    "load_pattern": {
        "description": "荷载模式 (DEAD, LIVE 等)",
        "classes": ["LoadPattern"],
        "enums": ["LoadPatternType"],
    },
    "load_case": {
        "description": "荷载工况/分析工况",
        "classes": ["LoadCase", "LoadCaseLoad"],
        "enums": ["LoadCaseType", "ModalSubType", "TimeHistorySubType", "DesignTypeOption"],
        "functions": {
            "create": [
                "create_static_linear_case",
                "create_static_nonlinear_case",
                "create_modal_eigen_case",
                "create_modal_ritz_case",
                "create_response_spectrum_case",
                "create_buckling_case",
                "create_direct_history_linear_case",
                "create_direct_history_nonlinear_case",
                "create_modal_history_linear_case",
                "create_modal_history_nonlinear_case",
                "create_steady_state_case",
                "create_psd_case",
                "create_moving_load_case",
                "create_hyperstatic_case",
                "create_static_linear_multistep_case",
                "create_static_nonlinear_multistep_case",
                "create_staged_construction_case",
            ],
            "static_linear_loads": [
                "get_static_linear_loads",
                "set_static_linear_loads",
            ],
        },
    },
    "load_combination": {
        "description": "荷载组合",
        "classes": ["LoadCombination"],
    },
    "mass_source": {
        "description": "质量源 (动力分析质量来源)",
        "classes": ["MassSource", "MassSourceLoad"],
    },
    "functions_common": {
        "description": "函数通用管理 (创建、删除、查询)",
        "enums": ["FuncType"],
        "functions": [
            "change_func_name",
            "convert_func_to_user",
            "get_func_count",
            "delete_func",
            "get_func_name_list",
            "get_func_type",
            "get_func_values",
        ],
    },
    "functions_time_history": {
        "description": "时程函数 (正弦、余弦、斜坡、锯齿波、三角波、用户定义、从文件)",
        "classes": ["CosineParams", "RampParams", "SawtoothParams", "SineParams", "TriangularParams", "FromFileParams"],
        "functions": [
            "get_func_th_cosine", "set_func_th_cosine",
            "get_func_th_from_file", "set_func_th_from_file",
            "get_func_th_ramp", "set_func_th_ramp",
            "get_func_th_sawtooth", "set_func_th_sawtooth",
            "get_func_th_sine", "set_func_th_sine",
            "get_func_th_triangular", "set_func_th_triangular",
            "get_func_th_user", "set_func_th_user",
            "get_func_th_user_periodic", "set_func_th_user_periodic",
        ],
    },
    "functions_response_spectrum": {
        "description": "反应谱函数 (中国规范 GB 50011-2010、用户定义、从文件)",
        "enums": ["Chinese2010SiteClass", "Chinese2010DesignGroup"],
        "classes": ["Chinese2010Params"],
        "functions": [
            "get_func_rs_chinese_2010", "set_func_rs_chinese_2010",
            "get_func_rs_user", "set_func_rs_user",
            "get_func_rs_from_file", "set_func_rs_from_file",
        ],
    },
}
