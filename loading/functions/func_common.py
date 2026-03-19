# -*- coding: utf-8 -*-
"""
func_common.py - 函数通用管理

SAP2000 Func API 封装

SAP2000 API:
- Func.ChangeName - 修改名称
- Func.ConvertToUser - 转换为用户定义
- Func.Count - 函数数量
- Func.Delete - 删除函数
- Func.GetNameList - 获取名称列表
- Func.GetTypeOAPI - 获取函数类型
- Func.GetValues - 获取函数值
"""

from typing import List, Tuple
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class FuncType(IntEnum):
    """
    函数类型
    
    SAP2000 API: eFuncType
    """
    RESPONSE_SPECTRUM = 0       # 反应谱
    TIME_HISTORY = 1            # 时程
    POWER_SPECTRAL_DENSITY = 2  # 功率谱密度
    STEADY_STATE = 3            # 稳态


# =============================================================================
# 函数管理
# =============================================================================

def change_func_name(model, old_name: str, new_name: str) -> int:
    """
    修改函数名称
    
    Args:
        model: SapModel 对象
        old_name: 原名称
        new_name: 新名称
        
    Returns:
        0 表示成功
    """
    return model.Func.ChangeName(old_name, new_name)


def convert_func_to_user(model, name: str) -> int:
    """
    将函数转换为用户定义类型
    
    Args:
        model: SapModel 对象
        name: 函数名称
        
    Returns:
        0 表示成功
    """
    return model.Func.ConvertToUser(name)


def get_func_count(model, func_type: FuncType = None) -> int:
    """
    获取函数数量
    
    Args:
        model: SapModel 对象
        func_type: 函数类型，None 表示所有类型
        
    Returns:
        函数数量
    """
    if func_type is None:
        result = model.Func.Count()
    else:
        result = model.Func.Count(int(func_type))
    
    count = com_data(result, 0)
    return count if count is not None else result


def delete_func(model, name: str) -> int:
    """
    删除函数
    
    Args:
        model: SapModel 对象
        name: 函数名称
        
    Returns:
        0 表示成功
    """
    return model.Func.Delete(name)


def get_func_name_list(model, func_type: FuncType = None) -> List[str]:
    """
    获取函数名称列表
    
    Args:
        model: SapModel 对象
        func_type: 函数类型，None 表示所有类型
        
    Returns:
        函数名称列表
    """
    if func_type is None:
        result = model.Func.GetNameList(0, [])
    else:
        result = model.Func.GetNameList(0, [], int(func_type))
    
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


def get_func_type(model, name: str) -> FuncType:
    """
    获取函数类型
    
    Args:
        model: SapModel 对象
        name: 函数名称
        
    Returns:
        函数类型
    """
    result = model.Func.GetTypeOAPI(name, 0, 0)
    type_val = com_data(result, 0)
    if type_val is not None:
        return FuncType(type_val)
    return FuncType.TIME_HISTORY


def get_func_values(model, name: str) -> Tuple[List[float], List[float]]:
    """
    获取函数值
    
    Args:
        model: SapModel 对象
        name: 函数名称
        
    Returns:
        (x_values, y_values) 元组
    """
    result = model.Func.GetValues(name, 0, [], [])
    num = com_data(result, 0, 0)
    x_values = com_data(result, 1)
    y_values = com_data(result, 2)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        return (
            list(x_values) if x_values else [],
            list(y_values) if y_values else []
        )
    return ([], [])
