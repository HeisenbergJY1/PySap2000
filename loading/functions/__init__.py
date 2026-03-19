# -*- coding: utf-8 -*-
"""
functions - 函数定义模块

SAP2000 Func API 封装，包含各类函数定义

子模块:
- func_common: 函数通用管理
- time_history: 时程函数
- response_spectrum: 反应谱函数
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
    # 数据类
    CosineParams,
    RampParams,
    SawtoothParams,
    SineParams,
    TriangularParams,
    FromFileParams,
    # 余弦函数
    get_func_th_cosine,
    set_func_th_cosine,
    # 从文件
    get_func_th_from_file,
    set_func_th_from_file,
    # 斜坡函数
    get_func_th_ramp,
    set_func_th_ramp,
    # 锯齿波函数
    get_func_th_sawtooth,
    set_func_th_sawtooth,
    # 正弦函数
    get_func_th_sine,
    set_func_th_sine,
    # 三角波函数
    get_func_th_triangular,
    set_func_th_triangular,
    # 用户定义函数
    get_func_th_user,
    set_func_th_user,
    # 用户周期函数
    get_func_th_user_periodic,
    set_func_th_user_periodic,
)

from .response_spectrum import (
    # 枚举
    Chinese2010SiteClass,
    Chinese2010DesignGroup,
    # 数据类
    Chinese2010Params,
    # 中国规范
    get_func_rs_chinese_2010,
    set_func_rs_chinese_2010,
    # 用户定义
    get_func_rs_user,
    set_func_rs_user,
    # 从文件
    get_func_rs_from_file,
    set_func_rs_from_file,
)

__all__ = [
    # 枚举
    "FuncType",
    "Chinese2010SiteClass",
    "Chinese2010DesignGroup",
    # 通用管理
    "change_func_name",
    "convert_func_to_user",
    "get_func_count",
    "delete_func",
    "get_func_name_list",
    "get_func_type",
    "get_func_values",
    # 时程数据类
    "CosineParams",
    "RampParams",
    "SawtoothParams",
    "SineParams",
    "TriangularParams",
    "FromFileParams",
    # 反应谱数据类
    "Chinese2010Params",
    # 时程函数
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
    # 反应谱函数
    "get_func_rs_chinese_2010",
    "set_func_rs_chinese_2010",
    "get_func_rs_user",
    "set_func_rs_user",
    "get_func_rs_from_file",
    "set_func_rs_from_file",
]
