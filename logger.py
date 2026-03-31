# -*- coding: utf-8 -*-
"""
logger.py - Unified logging helpers.

Provides logging utilities for PySap2000 with configurable levels and outputs.

Usage:
    from PySap2000.logger import logger, setup_logger
    
    # Use the default logger
    logger.info("Connected to SAP2000")
    logger.debug("Creating point at (0, 0, 0)")
    logger.error("Failed to create frame")
    
    # Use custom logging configuration
    setup_logger(level="DEBUG", log_file="pysap2000.log")
"""

import logging
import sys
from typing import Optional
from pathlib import Path
from logging.handlers import RotatingFileHandler


# Create the package logger.
logger = logging.getLogger("pysap2000")

# Default formats
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
SIMPLE_FORMAT = "%(levelname)s: %(message)s"


class ColoredFormatter(logging.Formatter):
    """
    Log formatter with ANSI colors for terminal output.
    """
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, '')
        message = super().format(record)
        return f"{color}{message}{self.RESET}" if color else message


def setup_logger(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None,
    use_colors: bool = True,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Configure the PySap2000 logger.

    Args:
        level: Logging level
        log_file: Optional log file path
        format_string: Optional log format override
        use_colors: Whether to use ANSI colors in terminal output
        max_bytes: Maximum size of a single log file
        backup_count: Number of rotated log files to keep

    Returns:
        The configured logger

    Example:
        # Development mode: show DEBUG output
        setup_logger(level="DEBUG")

        # Production mode: write to a rotating file
        setup_logger(level="INFO", log_file="app.log", max_bytes=10*1024*1024, backup_count=5)
    """
    # Clear existing handlers
    logger.handlers.clear()

    # Configure log level
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # Resolve format
    fmt = format_string or DEFAULT_FORMAT

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    if use_colors and sys.stdout.isatty():
        console_handler.setFormatter(ColoredFormatter(fmt))
    else:
        console_handler.setFormatter(logging.Formatter(fmt))

    logger.addHandler(console_handler)

    # Rotating file handler, when requested
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(file_handler)

    # Prevent propagation to the root logger
    logger.propagate = False

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Return a child logger.
    
    Args:
        name: Child logger name
        
    Returns:
        A child logger inheriting the package logger configuration
        
    Example:
        from PySap2000.logger import get_logger
        
        logger = get_logger("application")  # pysap2000.application
        logger.info("Application started")
    """
    return logging.getLogger(f"pysap2000.{name}")


# Default configuration: INFO level, console only
if not logger.handlers:
    setup_logger(level="INFO")
