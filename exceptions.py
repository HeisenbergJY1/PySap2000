# -*- coding: utf-8 -*-
"""
exceptions.py - 统一异常定义
参考 dlubal.api.common.exceptions

Usage:
    from PySap2000.exceptions import PointError, FrameError, AnalysisError
    
    try:
        point = Point.get_by_name(model, "invalid")
    except PointError as e:
        print(f"Point error: {e}")
"""

import warnings
from functools import wraps


def _deprecated_class(cls, replacement: str):
    """为弃用的类添加警告"""
    original_init = cls.__init__
    
    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        warnings.warn(
            f"{cls.__name__} is deprecated. Use {replacement} instead.",
            DeprecationWarning,
            stacklevel=2
        )
        original_init(self, *args, **kwargs)
    
    cls.__init__ = new_init
    return cls


class PySap2000Error(Exception):
    """PySap2000 基础异常类"""
    pass


class ConnectionError(PySap2000Error):
    """连接 SAP2000 失败"""
    pass


class ObjectError(PySap2000Error):
    """对象操作错误"""
    pass


class NodeError(ObjectError):
    """
    [DEPRECATED] 节点相关错误
    
    请使用 PointError 替代
    """
    pass

NodeError = _deprecated_class(NodeError, "PointError")


class PointError(ObjectError):
    """Point 相关错误"""
    pass


class MemberError(ObjectError):
    """
    [DEPRECATED] 杆件相关错误
    
    请使用 FrameError 替代
    """
    pass

MemberError = _deprecated_class(MemberError, "FrameError")


class FrameError(ObjectError):
    """Frame 相关错误"""
    pass


class SurfaceError(ObjectError):
    """面单元相关错误"""
    pass


class AreaError(ObjectError):
    """Area 相关错误"""
    pass


class CableError(ObjectError):
    """Cable 相关错误"""
    pass


class LinkError(ObjectError):
    """Link 相关错误"""
    pass


class MaterialError(ObjectError):
    """材料相关错误"""
    pass


class SectionError(ObjectError):
    """截面相关错误"""
    pass


class LoadError(ObjectError):
    """荷载相关错误"""
    pass


class AnalysisError(PySap2000Error):
    """分析相关错误"""
    pass


class ResultError(PySap2000Error):
    """结果获取错误"""
    pass
