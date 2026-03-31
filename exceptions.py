# -*- coding: utf-8 -*-
"""
exceptions.py - Unified exception definitions.

Inspired by `dlubal.api.common.exceptions`.

Usage:
    from PySap2000.exceptions import PointError, FrameError, AnalysisError

    try:
        point = Point.get_by_name(model, "invalid")
    except PointError as e:
        print(f"Point error: {e}")
        print(f"Details: {e.details}")
"""

import warnings
from functools import wraps
from typing import Optional, Dict, Any


def _deprecated_class(cls, replacement: str):
    """Attach a deprecation warning to a legacy exception class."""
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
    """
    Base exception for PySap2000.

    Attributes:
        message: Error message
        details: Optional details dictionary
    """
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self):
        if self.details:
            detail_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({detail_str})"
        return self.message


class SAPConnectionError(PySap2000Error):
    """Raised when connecting to SAP2000 fails."""
    pass


# Backward-compatible alias. Deprecated; prefer SAPConnectionError.
ConnectionError = SAPConnectionError


class ConnectionTimeoutError(SAPConnectionError):
    """Raised when a SAP2000 connection attempt times out."""
    pass


class ConnectionLostError(SAPConnectionError):
    """Raised when an existing SAP2000 connection is lost."""
    pass


class SAP2000NotRunningError(SAPConnectionError):
    """Raised when SAP2000 is not running."""
    pass


class ObjectError(PySap2000Error):
    """Raised for object operation errors."""
    pass


class NodeError(ObjectError):
    """
    [DEPRECATED] Point-related error.

    Use PointError instead.
    """
    pass

NodeError = _deprecated_class(NodeError, "PointError")


class PointError(ObjectError):
    """Raised for point-related errors."""
    pass


class MemberError(ObjectError):
    """
    [DEPRECATED] Frame-related error.

    Use FrameError instead.
    """
    pass

MemberError = _deprecated_class(MemberError, "FrameError")


class FrameError(ObjectError):
    """Raised for frame-related errors."""
    pass


class SurfaceError(ObjectError):
    """Raised for surface-related errors."""
    pass


class AreaError(ObjectError):
    """Raised for area-related errors."""
    pass


class CableError(ObjectError):
    """Raised for cable-related errors."""
    pass


class LinkError(ObjectError):
    """Raised for link-related errors."""
    pass


class MaterialError(ObjectError):
    """Raised for material-related errors."""
    pass


class SectionError(ObjectError):
    """Raised for section-related errors."""
    pass


class LoadError(ObjectError):
    """Raised for load-related errors."""
    pass


class AnalysisError(PySap2000Error):
    """Raised for analysis-related errors."""
    pass


class ResultError(PySap2000Error):
    """Raised for result retrieval errors."""
    pass
