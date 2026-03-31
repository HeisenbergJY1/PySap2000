# -*- coding: utf-8 -*-
"""
retry.py - Retry decorator for COM calls.

Provides simple retry logic for transient COM failures.

Usage:
    from PySap2000.utils.retry import retry_on_com_error

    @retry_on_com_error(max_retries=3, delay=1.0)
    def unstable_operation(model):
        return model.Analyze.RunAnalysis()
"""

from functools import wraps
import time
from typing import Callable, TypeVar
from PySap2000.logger import get_logger

_logger = get_logger("retry")

T = TypeVar('T')


def retry_on_com_error(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 1.0
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Retry a callable when a COM call fails.

    Args:
        max_retries: Maximum number of attempts
        delay: Initial delay in seconds
        backoff: Delay multiplier applied after each retry

    Returns:
        Decorator function

    Example:
        @retry_on_com_error(max_retries=3, delay=1.0)
        def run_analysis(model):
            return model.Analyze.RunAnalysis()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            current_delay = delay
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        _logger.warning(
                            f"{func.__name__} failed (attempt {attempt + 1}/{max_retries}): {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        _logger.error(
                            f"{func.__name__} failed after {max_retries} attempts: {e}"
                        )

            raise last_exception

        return wrapper
    return decorator
