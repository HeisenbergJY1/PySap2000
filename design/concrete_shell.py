# -*- coding: utf-8 -*-
"""
design/concrete_shell.py - Concrete shell design helpers

Python wrapper for the SAP2000 `DesignConcreteShell` API.
API path: `SapModel.DesignConcreteShell`
"""

from typing import Union

from .enums import (
    ConcreteShellDesignCode, CONCRETE_SHELL_CODE_NAMES,
)
from PySap2000.com_helper import com_ret, com_data


def get_concrete_shell_code(model) -> str:
    """Get the active concrete shell design code

    Args:
        model: SAP2000 SapModel object

    Returns:
        Code name string
    """
    result = model.DesignConcreteShell.GetCode("")
    return com_data(result, 0, "")


def set_concrete_shell_code(model, code: Union[ConcreteShellDesignCode, str]) -> int:
    """Set the concrete shell design code

    Args:
        model: SAP2000 SapModel object
        code: Code enum or code name string

    Returns:
        `0` on success, non-zero on failure
    """
    if isinstance(code, ConcreteShellDesignCode):
        code_name = CONCRETE_SHELL_CODE_NAMES.get(code, "Eurocode 2-2004")
    else:
        code_name = code
    ret = model.DesignConcreteShell.SetCode(code_name)
    return com_ret(ret)


def start_concrete_shell_design(model) -> int:
    """Run concrete shell design

    Args:
        model: SAP2000 SapModel object

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignConcreteShell.StartDesign()
    return com_ret(ret)


def delete_concrete_shell_results(model) -> int:
    """Delete all concrete shell design results

    Args:
        model: SAP2000 SapModel object

    Returns:
        `0` on success, non-zero on failure
    """
    ret = model.DesignConcreteShell.DeleteResults()
    return com_ret(ret)
