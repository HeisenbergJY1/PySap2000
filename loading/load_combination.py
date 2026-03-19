# -*- coding: utf-8 -*-
"""
load_combination.py - 荷载组合

SAP2000 RespCombo API 封装

SAP2000 API:
- RespCombo.Add - 添加组合
- RespCombo.AddDesignDefaultCombos - 添加设计默认组合
- RespCombo.ChangeName - 修改名称
- RespCombo.Count - 组合数量
- RespCombo.CountCase - 组合中工况数量
- RespCombo.Delete - 删除组合
- RespCombo.DeleteCase - 删除组合中的工况
- RespCombo.GetCaseList_1 - 获取工况列表
- RespCombo.GetNameList - 获取名称列表
- RespCombo.GetNote - 获取备注
- RespCombo.GetTypeOAPI - 获取组合类型
- RespCombo.SetCaseList_1 - 设置工况列表
- RespCombo.SetNote - 设置备注
- RespCombo.SetTypeOAPI - 设置组合类型
"""

from typing import List, Tuple
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class ComboCaseType(IntEnum):
    """
    组合中工况类型
    
    SAP2000 API: eCNameType
    """
    LOAD_CASE = 0       # 荷载工况
    LOAD_COMBO = 1      # 荷载组合


class ComboType(IntEnum):
    """
    组合类型
    
    SAP2000 API: eComboType
    """
    LINEAR_ADD = 0      # 线性叠加
    ENVELOPE = 1        # 包络
    ABS_ADD = 2         # 绝对值叠加
    SRSS = 3            # 平方和开方
    RANGE = 4           # 范围


# =============================================================================
# 组合管理函数
# =============================================================================

def add_combo(model, name: str, combo_type: ComboType = ComboType.LINEAR_ADD) -> int:
    """
    添加荷载组合
    
    Args:
        model: SapModel 对象
        name: 组合名称
        combo_type: 组合类型
        
    Returns:
        0 表示成功
    """
    return model.RespCombo.Add(name, int(combo_type))


def add_design_default_combos(
    model,
    design_steel: bool = True,
    design_concrete: bool = True,
    design_aluminum: bool = True,
    design_cold_formed: bool = True
) -> int:
    """
    添加设计默认组合
    
    Args:
        model: SapModel 对象
        design_steel: 是否添加钢结构设计组合
        design_concrete: 是否添加混凝土设计组合
        design_aluminum: 是否添加铝结构设计组合
        design_cold_formed: 是否添加冷弯型钢设计组合
        
    Returns:
        0 表示成功
    """
    return model.RespCombo.AddDesignDefaultCombos(
        design_steel, design_concrete, design_aluminum, design_cold_formed
    )


def change_combo_name(model, old_name: str, new_name: str) -> int:
    """
    修改组合名称
    
    Args:
        model: SapModel 对象
        old_name: 原名称
        new_name: 新名称
        
    Returns:
        0 表示成功
    """
    return model.RespCombo.ChangeName(old_name, new_name)


def get_combo_count(model) -> int:
    """
    获取组合数量
    
    Args:
        model: SapModel 对象
        
    Returns:
        组合数量
    """
    result = model.RespCombo.Count()
    count = com_data(result, 0)
    return count if count is not None else result


def get_combo_case_count(model, name: str) -> int:
    """
    获取组合中工况数量
    
    Args:
        model: SapModel 对象
        name: 组合名称
        
    Returns:
        工况数量
    """
    result = model.RespCombo.CountCase(name)
    count = com_data(result, 0)
    return count if count is not None else result


def delete_combo(model, name: str) -> int:
    """
    删除组合
    
    Args:
        model: SapModel 对象
        name: 组合名称
        
    Returns:
        0 表示成功
    """
    return model.RespCombo.Delete(name)


def delete_combo_case(model, name: str, case_type: ComboCaseType, case_name: str) -> int:
    """
    从组合中删除工况
    
    Args:
        model: SapModel 对象
        name: 组合名称
        case_type: 工况类型 (LOAD_CASE 或 LOAD_COMBO)
        case_name: 要删除的工况/组合名称
        
    Returns:
        0 表示成功
    """
    return model.RespCombo.DeleteCase(name, int(case_type), case_name)


def get_combo_name_list(model) -> List[str]:
    """
    获取所有组合名称列表
    
    Args:
        model: SapModel 对象
        
    Returns:
        组合名称列表
    """
    result = model.RespCombo.GetNameList(0, [])
    names = com_data(result, 1)
    if names:
        return list(names)
    return []


# =============================================================================
# 工况列表函数
# =============================================================================

def get_combo_case_list(model, name: str) -> Tuple[List[ComboCaseType], List[str], List[float]]:
    """
    获取组合中的工况列表
    
    Args:
        model: SapModel 对象
        name: 组合名称
        
    Returns:
        (case_types, case_names, scale_factors) 元组
        - case_types: 工况类型列表
        - case_names: 工况名称列表
        - scale_factors: 比例系数列表
    """
    result = model.RespCombo.GetCaseList_1(name, 0, [], [], [])
    num = com_data(result, 0, 0)
    case_types = com_data(result, 1)
    case_names = com_data(result, 2)
    scale_factors = com_data(result, 3)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        types = [ComboCaseType(t) for t in case_types] if case_types else []
        names = list(case_names) if case_names else []
        factors = list(scale_factors) if scale_factors else []
        return (types, names, factors)
    return ([], [], [])


def set_combo_case_list(
    model,
    name: str,
    case_type: ComboCaseType,
    case_name: str,
    scale_factor: float
) -> int:
    """
    向组合添加工况
    
    Args:
        model: SapModel 对象
        name: 组合名称
        case_type: 工况类型 (LOAD_CASE 或 LOAD_COMBO)
        case_name: 工况/组合名称
        scale_factor: 比例系数
        
    Returns:
        0 表示成功
    """
    return model.RespCombo.SetCaseList_1(name, int(case_type), case_name, 0, scale_factor)


# =============================================================================
# 备注函数
# =============================================================================

def get_combo_note(model, name: str) -> str:
    """
    获取组合备注
    
    Args:
        model: SapModel 对象
        name: 组合名称
        
    Returns:
        备注文本
    """
    result = model.RespCombo.GetNote(name, "")
    note = com_data(result, 0)
    return note if note else ""


def set_combo_note(model, name: str, note: str) -> int:
    """
    设置组合备注
    
    Args:
        model: SapModel 对象
        name: 组合名称
        note: 备注文本
        
    Returns:
        0 表示成功
    """
    return model.RespCombo.SetNote(name, note)


# =============================================================================
# 类型函数
# =============================================================================

def get_combo_type(model, name: str) -> ComboType:
    """
    获取组合类型
    
    Args:
        model: SapModel 对象
        name: 组合名称
        
    Returns:
        组合类型
    """
    result = model.RespCombo.GetTypeOAPI(name, 0)
    type_val = com_data(result, 0)
    if type_val is not None:
        return ComboType(type_val)
    return ComboType.LINEAR_ADD


def set_combo_type(model, name: str, combo_type: ComboType) -> int:
    """
    设置组合类型
    
    Args:
        model: SapModel 对象
        name: 组合名称
        combo_type: 组合类型
        
    Returns:
        0 表示成功
    """
    return model.RespCombo.SetTypeOAPI(name, int(combo_type))
