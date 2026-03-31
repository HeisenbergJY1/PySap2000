# -*- coding: utf-8 -*-
"""deprecation.py - Deprecation decorator helpers."""

import warnings
from functools import wraps


def deprecated(reason: str = ""):
    """
    Mark a function as deprecated.
    
    Args:
        reason: Deprecation reason or migration hint
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated. {reason}",
                DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator
