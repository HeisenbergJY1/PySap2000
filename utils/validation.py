# -*- coding: utf-8 -*-
"""
validation.py - Validation and sanitization helpers.

Provides light-weight validation helpers for names and numeric inputs.

Usage:
    from PySap2000.utils.validation import sanitize_name, validate_coordinate

    name = sanitize_name(user_input)
    x = validate_coordinate(x_value, "x")
"""

import re
from typing import Union


def sanitize_name(name: Union[str, int]) -> str:
    """
    Sanitize an object name.

    SAP2000 object names should contain only letters, digits, underscores,
    hyphens, and dots.

    Args:
        name: Raw input name

    Returns:
        Sanitized name

    Example:
        >>> sanitize_name("Frame<script>")
        'Framescript'
        >>> sanitize_name("Node-1.2")
        'Node-1.2'
    """
    name_str = str(name)
    # Keep only letters, digits, underscores, hyphens, and dots.
    return re.sub(r'[^\w\-.]', '', name_str)


def validate_coordinate(value: float, coord_name: str = "coordinate") -> float:
    """
    Validate a coordinate value.

    Args:
        value: Coordinate value
        coord_name: Coordinate label used in error messages

    Returns:
        Validated coordinate as float

    Raises:
        TypeError: Raised when the value is not numeric
        ValueError: Raised when the value is NaN or infinite
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{coord_name} must be numeric, got {type(value).__name__}")

    if value != value:  # NaN check
        raise ValueError(f"{coord_name} cannot be NaN")

    if abs(value) == float('inf'):
        raise ValueError(f"{coord_name} cannot be infinite")

    return float(value)


def validate_positive(value: Union[int, float], param_name: str = "value") -> Union[int, float]:
    """
    Validate that a value is positive.

    Args:
        value: Value to validate
        param_name: Parameter name

    Returns:
        The validated value

    Raises:
        ValueError: Raised when the value is not positive
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{param_name} must be numeric")

    if value <= 0:
        raise ValueError(f"{param_name} must be positive, got {value}")

    return value


def validate_range(
    value: Union[int, float],
    min_val: Union[int, float],
    max_val: Union[int, float],
    param_name: str = "value"
) -> Union[int, float]:
    """
    Validate that a value falls within a range.

    Args:
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        param_name: Parameter name

    Returns:
        The validated value

    Raises:
        ValueError: Raised when the value is outside the allowed range
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{param_name} must be numeric")

    if not (min_val <= value <= max_val):
        raise ValueError(
            f"{param_name} must be between {min_val} and {max_val}, got {value}"
        )

    return value
