# -*- coding: utf-8 -*-
"""
response_spectrum.py - 反应谱函数

SAP2000 Func.FuncRS API 封装（中国规范相关）

SAP2000 API:
- Func.FuncRS.GetChinese2010 / SetChinese2010 - 中国GB 50011-2010规范
- Func.FuncRS.GetUser / SetUser - 用户定义反应谱
- Func.FuncRS.GetFromFile_1 / SetFromFile_1 - 从文件读取
"""

from typing import List, Tuple
from dataclasses import dataclass
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class Chinese2010SiteClass(IntEnum):
    """
    中国规范场地类别
    
    GB 50011-2010
    """
    I_0 = 0     # I0类
    I_1 = 1     # I1类
    II = 2      # II类
    III = 3     # III类
    IV = 4      # IV类


class Chinese2010DesignGroup(IntEnum):
    """
    中国规范设计地震分组
    
    GB 50011-2010
    """
    GROUP_1 = 0     # 第一组
    GROUP_2 = 1     # 第二组
    GROUP_3 = 2     # 第三组


@dataclass
class Chinese2010Params:
    """
    中国GB 50011-2010反应谱参数
    
    Attributes:
        alpha_max: 地震影响系数最大值
        site_class: 场地类别
        design_group: 设计地震分组
        period_time_discount: 周期折减系数
        damping_ratio: 阻尼比
    """
    alpha_max: float = 0.0
    site_class: Chinese2010SiteClass = Chinese2010SiteClass.II
    design_group: Chinese2010DesignGroup = Chinese2010DesignGroup.GROUP_1
    period_time_discount: float = 1.0
    damping_ratio: float = 0.05


# =============================================================================
# 中国规范 GB 50011-2010
# =============================================================================

def get_func_rs_chinese_2010(model, name: str) -> Chinese2010Params:
    """
    获取中国GB 50011-2010反应谱函数参数
    
    Args:
        model: SapModel 对象
        name: 函数名称
        
    Returns:
        Chinese2010Params 参数对象
    """
    result = model.Func.FuncRS.GetChinese2010(name, 0.0, 0, 0, 0.0, 0.0)
    alpha_max = com_data(result, 0)
    if alpha_max is not None:
        return Chinese2010Params(
            alpha_max=alpha_max,
            site_class=Chinese2010SiteClass(com_data(result, 1, 2)),
            design_group=Chinese2010DesignGroup(com_data(result, 2, 0)),
            period_time_discount=com_data(result, 3, 1.0),
            damping_ratio=com_data(result, 4, 0.05),
        )
    return Chinese2010Params()


def set_func_rs_chinese_2010(
    model,
    name: str,
    alpha_max: float,
    site_class: Chinese2010SiteClass,
    design_group: Chinese2010DesignGroup,
    period_time_discount: float = 1.0,
    damping_ratio: float = 0.05
) -> int:
    """
    设置中国GB 50011-2010反应谱函数
    
    Args:
        model: SapModel 对象
        name: 函数名称
        alpha_max: 地震影响系数最大值
        site_class: 场地类别
        design_group: 设计地震分组
        period_time_discount: 周期折减系数
        damping_ratio: 阻尼比
        
    Returns:
        0 表示成功
        
    Example:
        set_func_rs_chinese_2010(
            model, "RS-X",
            alpha_max=0.08,
            site_class=Chinese2010SiteClass.II,
            design_group=Chinese2010DesignGroup.GROUP_1,
            damping_ratio=0.05
        )
    """
    return model.Func.FuncRS.SetChinese2010(
        name,
        alpha_max,
        int(site_class),
        int(design_group),
        period_time_discount,
        damping_ratio
    )


# =============================================================================
# 用户定义反应谱
# =============================================================================

def get_func_rs_user(model, name: str) -> Tuple[List[float], List[float], float]:
    """
    获取用户定义反应谱函数数据
    
    Args:
        model: SapModel 对象
        name: 函数名称
        
    Returns:
        (periods, values, damping_ratio) 元组
        - periods: 周期列表 [s]
        - values: 谱值列表
        - damping_ratio: 阻尼比
    """
    result = model.Func.FuncRS.GetUser(name, 0, [], [], 0.0)
    num = com_data(result, 0, 0)
    periods = com_data(result, 1)
    values = com_data(result, 2)
    damping = com_data(result, 3, 0.05)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        return (
            list(periods) if periods else [],
            list(values) if values else [],
            damping
        )
    return ([], [], 0.05)


def set_func_rs_user(
    model,
    name: str,
    periods: List[float],
    values: List[float],
    damping_ratio: float = 0.05
) -> int:
    """
    设置用户定义反应谱函数
    
    Args:
        model: SapModel 对象
        name: 函数名称
        periods: 周期列表 [s]
        values: 谱值列表
        damping_ratio: 阻尼比
        
    Returns:
        0 表示成功
    """
    num = len(periods)
    return model.Func.FuncRS.SetUser(name, num, periods, values, damping_ratio)


# =============================================================================
# 从文件读取
# =============================================================================

def get_func_rs_from_file(model, name: str) -> Tuple[str, int, int, float]:
    """
    获取从文件读取的反应谱函数参数
    
    Args:
        model: SapModel 对象
        name: 函数名称
        
    Returns:
        (file_name, header_lines, prefix_chars, damping_ratio) 元组
    """
    result = model.Func.FuncRS.GetFromFile_1(name, "", 0, 0, 0.0)
    file_name = com_data(result, 0)
    if file_name is not None:
        return (
            file_name if file_name else "",
            com_data(result, 1, 0),
            com_data(result, 2, 0),
            com_data(result, 3, 0.05),
        )
    return ("", 0, 0, 0.05)


def set_func_rs_from_file(
    model,
    name: str,
    file_name: str,
    header_lines: int = 0,
    prefix_chars: int = 0,
    damping_ratio: float = 0.05
) -> int:
    """
    从文件设置反应谱函数
    
    Args:
        model: SapModel 对象
        name: 函数名称
        file_name: 文件路径
        header_lines: 头部跳过行数
        prefix_chars: 每行前缀跳过字符数
        damping_ratio: 阻尼比
        
    Returns:
        0 表示成功
    """
    return model.Func.FuncRS.SetFromFile_1(
        name, file_name, header_lines, prefix_chars, damping_ratio
    )
