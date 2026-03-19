# -*- coding: utf-8 -*-
"""
logger.py - 统一日志管理

提供 PySap2000 库的日志功能，支持多种日志级别和输出目标。

Usage:
    from PySap2000.logger import logger, setup_logger
    
    # 使用默认日志器
    logger.info("Connected to SAP2000")
    logger.debug("Creating point at (0, 0, 0)")
    logger.error("Failed to create frame")
    
    # 自定义日志配置
    setup_logger(level="DEBUG", log_file="pysap2000.log")
"""

import logging
import sys
from typing import Optional
from pathlib import Path


# 创建 PySap2000 专用日志器
logger = logging.getLogger("pysap2000")

# 默认格式
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
SIMPLE_FORMAT = "%(levelname)s: %(message)s"


class ColoredFormatter(logging.Formatter):
    """
    带颜色的日志格式化器（仅在终端有效）
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
    use_colors: bool = True
) -> logging.Logger:
    """
    配置 PySap2000 日志器
    
    Args:
        level: 日志级别 ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
        log_file: 日志文件路径（可选），如果提供则同时输出到文件
        format_string: 自定义日志格式
        use_colors: 是否在终端使用颜色
        
    Returns:
        配置好的日志器
        
    Example:
        # 开发模式：显示 DEBUG 级别
        setup_logger(level="DEBUG")
        
        # 生产模式：保存到文件
        setup_logger(level="INFO", log_file="app.log")
    """
    # 清除现有处理器
    logger.handlers.clear()
    
    # 设置日志级别
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # 设置格式
    fmt = format_string or DEFAULT_FORMAT
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    if use_colors and sys.stdout.isatty():
        console_handler.setFormatter(ColoredFormatter(fmt))
    else:
        console_handler.setFormatter(logging.Formatter(fmt))
    
    logger.addHandler(console_handler)
    
    # 文件处理器（如果指定）
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(file_handler)
    
    # 防止日志传播到根日志器
    logger.propagate = False
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    获取子日志器
    
    Args:
        name: 子日志器名称
        
    Returns:
        子日志器，会继承 pysap2000 日志器的配置
        
    Example:
        from PySap2000.logger import get_logger
        
        logger = get_logger("application")  # pysap2000.application
        logger.info("Application started")
    """
    return logging.getLogger(f"pysap2000.{name}")


# 默认配置：INFO 级别，仅控制台输出
if not logger.handlers:
    setup_logger(level="INFO")
