# -*- coding: utf-8 -*-
"""
com_helper.py - Utilities for handling COM return values.

When `comtypes` calls the SAP2000 COM API, the return value is usually a
tuple or list:
- the last element is the return code, where `0` means success
- preceding elements contain data

This module centralizes extraction logic so individual wrappers do not need to
repeat the same parsing and logging code.

Usage:
    from PySap2000.com_helper import com_ret, com_data

    # Extract the return code.
    ret = com_ret(model.FrameObj.Delete("1"))

    # Extract data.
    names = com_data(model.FrameObj.GetNameList(0, []), index=1, default=[])
"""

import sys
import logging
import os
from typing import Any

_log = logging.getLogger("pysap2000.com")


def com_ret(result, *, context: str = "") -> int:
    """
    Extract the return code from a COM result value.

    For tuple/list results, the return code is expected at `result[-1]`.
    If a scalar integer is returned, it is treated as the return code directly.
    When the return code is non-zero:
      - a warning is logged automatically
      - `PySap2000Error` is raised when `config.strict_mode` is enabled

    Args:
        result: Raw return value from a COM call
        context: Optional manual context description

    Returns:
        The return code, where `0` means success

    Raises:
        PySap2000Error: Raised when strict mode is enabled and the code is non-zero

    Example:
        ret = com_ret(model.FrameObj.Delete("1"))
        assert ret == 0
    """
    if isinstance(result, (list, tuple)):
        ret = result[-1] if result else -1
    else:
        ret = result

    if ret != 0:
        # `sys._getframe()` is much cheaper than `inspect.stack()` here.
        if context:
            caller_info = context
        else:
            try:
                frame = sys._getframe(1)
                filename = os.path.basename(frame.f_code.co_filename)
                func_name = frame.f_code.co_name
                caller_info = f"{filename}:{func_name}()"
            except (AttributeError, ValueError):
                caller_info = "<unknown>"

        msg = f"COM call failed: {caller_info}, return_code={ret}"
        _log.warning(msg)

        from PySap2000.config import config
        if config.strict_mode:
            from PySap2000.exceptions import PySap2000Error
            raise PySap2000Error(msg)

    return ret


def com_data(result, index: int = 0, default=None) -> Any:
    """
    Extract data from a specific position in a COM result value.

    Args:
        result: Raw return value from a COM call
        index: Position of the desired value, default `0`
        default: Value returned when extraction fails

    Returns:
        The extracted data item

    Example:
        result = model.FrameObj.GetNameList(0, [])
        names = com_data(result, index=1, default=[])
    """
    if isinstance(result, (list, tuple)) and len(result) > index:
        return result[index]
    return default
