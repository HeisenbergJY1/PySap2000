# -*- coding: utf-8 -*-
"""
functions - Function definition helpers.

Wraps the SAP2000 `Func` API and exposes various function definitions.

Submodules:
- `func_common`: common function management
- `time_history`: time-history functions
- `response_spectrum`: response-spectrum functions
"""

from .func_common import (
    FuncType,
    change_func_name,
    convert_func_to_user,
    get_func_count,
    delete_func,
    get_func_name_list,
    get_func_type,
    get_func_values,
)

from .time_history import (
    # Data classes
    CosineParams,
    RampParams,
    SawtoothParams,
    SineParams,
    TriangularParams,
    FromFileParams,
    # Cosine functions
    get_func_th_cosine,
    set_func_th_cosine,
    # File-based
    get_func_th_from_file,
    set_func_th_from_file,
    # Ramp functions
    get_func_th_ramp,
    set_func_th_ramp,
    # Sawtooth functions
    get_func_th_sawtooth,
    set_func_th_sawtooth,
    # Sine functions
    get_func_th_sine,
    set_func_th_sine,
    # Triangular functions
    get_func_th_triangular,
    set_func_th_triangular,
    # User-defined functions
    get_func_th_user,
    set_func_th_user,
    # User-defined periodic functions
    get_func_th_user_periodic,
    set_func_th_user_periodic,
)

from .response_spectrum import (
    # Enums
    Chinese2010SiteClass,
    Chinese2010DesignGroup,
    # Data classes
    Chinese2010Params,
    # Chinese code helpers
    get_func_rs_chinese_2010,
    set_func_rs_chinese_2010,
    # User-defined helpers
    get_func_rs_user,
    set_func_rs_user,
    # File-based helpers
    get_func_rs_from_file,
    set_func_rs_from_file,
)

__all__ = [
    # Enums
    "FuncType",
    "Chinese2010SiteClass",
    "Chinese2010DesignGroup",
    # Common management
    "change_func_name",
    "convert_func_to_user",
    "get_func_count",
    "delete_func",
    "get_func_name_list",
    "get_func_type",
    "get_func_values",
    # Time-history data classes
    "CosineParams",
    "RampParams",
    "SawtoothParams",
    "SineParams",
    "TriangularParams",
    "FromFileParams",
    # Response-spectrum data classes
    "Chinese2010Params",
    # Time-history functions
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
    # Response-spectrum functions
    "get_func_rs_chinese_2010",
    "set_func_rs_chinese_2010",
    "get_func_rs_user",
    "set_func_rs_user",
    "get_func_rs_from_file",
    "set_func_rs_from_file",
]
