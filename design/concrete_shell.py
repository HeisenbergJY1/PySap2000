# -*- coding: utf-8 -*-
"""
design/concrete_shell.py - 混凝土壳设计函数

SAP2000 DesignConcreteShell API 的 Python 封装。
API 路径: SapModel.DesignConcreteShell
"""

from typing import Union

from .enums import (
    ConcreteShellDesignCode, CONCRETE_SHELL_CODE_NAMES,
)
from PySap2000.com_helper import com_ret, com_data


def get_concrete_shell_code(model) -> str:
    """获取当前混凝土壳设计规范

    Args:
        model: SapModel 对象

    Returns:
        规范名称字符串
    """
    result = model.DesignConcreteShell.GetCode("")
    return com_data(result, 0, "")


def set_concrete_shell_code(model, code: Union[ConcreteShellDesignCode, str]) -> int:
    """设置混凝土壳设计规范

    Args:
        model: SapModel 对象
        code: 规范枚举或规范名称字符串

    Returns:
        0 表示成功，非 0 表示失败
    """
    if isinstance(code, ConcreteShellDesignCode):
        code_name = CONCRETE_SHELL_CODE_NAMES.get(code, "Eurocode 2-2004")
    else:
        code_name = code
    ret = model.DesignConcreteShell.SetCode(code_name)
    return com_ret(ret)


def start_concrete_shell_design(model) -> int:
    """开始混凝土壳设计

    Args:
        model: SapModel 对象

    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignConcreteShell.StartDesign()
    return com_ret(ret)


def delete_concrete_shell_results(model) -> int:
    """删除所有混凝土壳设计结果

    Args:
        model: SapModel 对象

    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignConcreteShell.DeleteResults()
    return com_ret(ret)
