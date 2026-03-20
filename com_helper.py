# -*- coding: utf-8 -*-
"""
com_helper.py - COM 返回值处理工具

comtypes 调用 SAP2000 COM 接口时，返回值通常是 list 或 tuple：
- 返回码在最后一个元素，0 表示成功
- 数据在前面的元素中

这个模块提供统一的提取函数，避免每个方法都重复写判断逻辑。
当 COM 调用失败时，自动记录 warning 级别日志（包含调用者文件和函数名），方便排查。

Usage:
    from PySap2000.com_helper import com_ret, com_data

    # 提取返回码（失败时自动记日志，无需手动传名称）
    ret = com_ret(model.FrameObj.Delete("1"))

    # 提取数据
    names = com_data(model.FrameObj.GetNameList(0, []), index=1, default=[])
"""

import sys
import logging
import os
from typing import Any

_log = logging.getLogger("pysap2000.com")


def com_ret(result, *, context: str = "") -> int:
    """
    从 COM 返回值提取返回码（最后一个元素）

    comtypes 返回 list 或 tuple 时，返回码总在 result[-1]。
    如果返回的是单个值（int），直接返回。
    当返回码非零时：
      - 自动记录 warning 日志（包含调用者文件和函数名）
      - 若 config.strict_mode=True，抛出 PySap2000Error 异常

    Args:
        result: COM 调用的原始返回值
        context: 可选的手动上下文描述，为空时自动从调用栈获取

    Returns:
        返回码，0 表示成功

    Raises:
        PySap2000Error: strict_mode 开启且返回码非零时抛出

    Example:
        ret = com_ret(model.FrameObj.Delete("1"))
        assert ret == 0
    """
    if isinstance(result, (list, tuple)):
        ret = result[-1] if result else -1
    else:
        ret = result

    if ret != 0:
        # 用 sys._getframe 替代 inspect.stack()，性能提升 10x+
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

        msg = f"COM 调用失败: {caller_info}, 返回码={ret}"
        _log.warning(msg)

        from PySap2000.config import config
        if config.strict_mode:
            from PySap2000.exceptions import PySap2000Error
            raise PySap2000Error(msg)

    return ret


def com_data(result, index: int = 0, default=None) -> Any:
    """
    从 COM 返回值提取指定位置的数据

    Args:
        result: COM 调用的原始返回值
        index: 数据所在的索引位置，默认 0
        default: 提取失败时的默认值

    Returns:
        指定位置的数据

    Example:
        result = model.FrameObj.GetNameList(0, [])
        names = com_data(result, index=1, default=[])
    """
    if isinstance(result, (list, tuple)) and len(result) > index:
        return result[index]
    return default
