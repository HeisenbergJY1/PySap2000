# -*- coding: utf-8 -*-
"""
loading - Load patterns, cases, combinations, and mass sources.

SAP2000 terms:
    LoadPattern - load pattern (for example `DEAD`, `LIVE`)
    LoadCase - load case / analysis case (for example linear static, modal, response spectrum)
    LoadCombination - load combination
    MassSource - mass source used in dynamic analysis
"""

from .load_pattern import LoadPattern, LoadPatternType
from .load_case import (
    LoadCase,
    LoadCaseType,
    LoadCaseLoad,
    ModalSubType,
    TimeHistorySubType,
    DesignTypeOption,
    # Creation helpers
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
    # Load-setting helpers
    get_static_linear_loads,
    set_static_linear_loads,
)
from .load_combination import (
    # Enums
    ComboCaseType,
    ComboType,
    # Functions
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

# Function definitions (time-history and response-spectrum functions)
from .functions import (
    # Enums
    FuncType,
    Chinese2010SiteClass,
    Chinese2010DesignGroup,
    # Common management
    change_func_name,
    convert_func_to_user,
    get_func_count,
    delete_func,
    get_func_name_list,
    get_func_type,
    get_func_values,
    # Time-history data classes
    CosineParams,
    RampParams,
    SawtoothParams,
    SineParams,
    TriangularParams,
    FromFileParams,
    # Response-spectrum data classes
    Chinese2010Params,
    # Time-history functions
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
    # Response-spectrum functions
    get_func_rs_chinese_2010,
    set_func_rs_chinese_2010,
    get_func_rs_user,
    set_func_rs_user,
    get_func_rs_from_file,
    set_func_rs_from_file,
)

__all__ = [
    # Load patterns
    "LoadPattern",
    "LoadPatternType",
    # Load cases
    "LoadCase",
    "LoadCaseType",
    "LoadCaseLoad",
    "ModalSubType",
    "TimeHistorySubType",
    "DesignTypeOption",
    # Load case creation helpers
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
    # Load-setting helpers
    "get_static_linear_loads",
    "set_static_linear_loads",
    # Load combinations
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
    # Mass sources
    "MassSource",
    "MassSourceLoad",
    # Function definitions - enums
    "FuncType",
    "Chinese2010SiteClass",
    "Chinese2010DesignGroup",
    # Function definitions - common management
    "change_func_name",
    "convert_func_to_user",
    "get_func_count",
    "delete_func",
    "get_func_name_list",
    "get_func_type",
    "get_func_values",
    # Function definitions - time-history data classes
    "CosineParams",
    "RampParams",
    "SawtoothParams",
    "SineParams",
    "TriangularParams",
    "FromFileParams",
    # Function definitions - response-spectrum data classes
    "Chinese2010Params",
    # Function definitions - time-history functions
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
    # Function definitions - response-spectrum functions
    "get_func_rs_chinese_2010",
    "set_func_rs_chinese_2010",
    "get_func_rs_user",
    "set_func_rs_user",
    "get_func_rs_from_file",
    "set_func_rs_from_file",
]

# API categories for discoverability
LOADING_API_CATEGORIES = {
    "load_pattern": {
        "description": "Load patterns such as DEAD and LIVE",
        "classes": ["LoadPattern"],
        "enums": ["LoadPatternType"],
    },
    "load_case": {
        "description": "Load cases and analysis cases",
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
        "description": "Load combinations",
        "classes": ["LoadCombination"],
    },
    "mass_source": {
        "description": "Mass sources used in dynamic analysis",
        "classes": ["MassSource", "MassSourceLoad"],
    },
    "functions_common": {
        "description": "Common function management such as rename, delete, and query",
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
        "description": "Time-history functions including sine, cosine, ramp, sawtooth, triangular, user-defined, and file-based",
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
        "description": "Response-spectrum functions including GB 50011-2010, user-defined, and file-based",
        "enums": ["Chinese2010SiteClass", "Chinese2010DesignGroup"],
        "classes": ["Chinese2010Params"],
        "functions": [
            "get_func_rs_chinese_2010", "set_func_rs_chinese_2010",
            "get_func_rs_user", "set_func_rs_user",
            "get_func_rs_from_file", "set_func_rs_from_file",
        ],
    },
}
