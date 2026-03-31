# -*- coding: utf-8 -*-
"""
config.py - Centralized configuration management.

This module stores project-wide configuration and supports environment-variable
overrides.

Usage:
    from PySap2000.config import config
    
    # Read config values
    print(config.default_units)
    print(config.agent.max_history_rounds)
    
    # Update config values
    config.log_level = "DEBUG"
    
    # Override values with environment variables
    # export PYSAP_LOG_LEVEL=DEBUG
    # export PYSAP_AGENT_MAX_HISTORY=20
"""

import os
from dataclasses import dataclass, field
from typing import Optional, List
from pathlib import Path


def _get_env(key: str, default: str = "") -> str:
    """Return an environment variable with the `PYSAP_` prefix."""
    return os.environ.get(f"PYSAP_{key}", default)


def _get_env_int(key: str, default: int) -> int:
    """Read an integer environment variable."""
    value = _get_env(key)
    return int(value) if value.isdigit() else default


def _get_env_bool(key: str, default: bool) -> bool:
    """Read a boolean environment variable."""
    value = _get_env(key).lower()
    if value in ("true", "1", "yes"):
        return True
    elif value in ("false", "0", "no"):
        return False
    return default


def _get_env_float(key: str, default: float) -> float:
    """Read a float environment variable."""
    value = _get_env(key)
    try:
        return float(value) if value else default
    except ValueError:
        return default


@dataclass
class AgentConfig:
    """Configuration for agent-related features."""
    
    # Model configuration
    default_provider: str = "qwen"
    default_model: str = "qwen-plus"
    temperature: float = 0.1
    max_tokens: int = 4096
    
    # Conversation configuration
    max_history_rounds: int = 10
    enable_tool_selector: bool = True
    enable_rag: bool = True
    
    # Safety configuration
    require_confirmation: bool = True
    pending_timeout: int = 300  # seconds
    
    # Documentation path
    docs_path: str = "docs/CSI_AI_Ready_Texts"
    
    def __post_init__(self):
        """Load values from environment variables."""
        self.default_provider = _get_env("AGENT_PROVIDER", self.default_provider)
        self.default_model = _get_env("AGENT_MODEL", self.default_model)
        self.temperature = _get_env_float("AGENT_TEMPERATURE", self.temperature)
        self.max_tokens = _get_env_int("AGENT_MAX_TOKENS", self.max_tokens)
        self.max_history_rounds = _get_env_int("AGENT_MAX_HISTORY", self.max_history_rounds)
        self.require_confirmation = _get_env_bool("AGENT_REQUIRE_CONFIRM", self.require_confirmation)
        self.pending_timeout = _get_env_int("AGENT_PENDING_TIMEOUT", self.pending_timeout)


@dataclass
class VisualizationConfig:
    """Visualization-related configuration."""
    
    # Default colors
    point_color: str = "#FF0000"
    frame_color: str = "#0066CC"
    area_color: str = "#00CC66"
    cable_color: str = "#FF6600"
    
    # Rendering configuration
    default_opacity: float = 0.8
    show_grid: bool = True
    show_axes: bool = True
    
    # Export configuration
    default_format: str = "html"  # html, json, gltf
    embed_viewer: bool = True
    
    def __post_init__(self):
        """Load values from environment variables."""
        self.point_color = _get_env("VIS_POINT_COLOR", self.point_color)
        self.frame_color = _get_env("VIS_FRAME_COLOR", self.frame_color)
        self.area_color = _get_env("VIS_AREA_COLOR", self.area_color)


@dataclass
class ConnectionConfig:
    """SAP2000 connection configuration."""
    
    # Connection mode
    attach_to_instance: bool = True
    program_path: str = ""
    
    # Timeout configuration
    connection_timeout: int = 30  # seconds
    operation_timeout: int = 60   # seconds
    
    # Retry configuration
    max_retries: int = 3
    retry_delay: float = 1.0  # seconds
    
    # Default units
    default_units: int = 6  # kN_m_C
    
    def __post_init__(self):
        """Load values from environment variables."""
        self.attach_to_instance = _get_env_bool("ATTACH_TO_INSTANCE", self.attach_to_instance)
        self.program_path = _get_env("SAP_PROGRAM_PATH", self.program_path)
        self.connection_timeout = _get_env_int("CONNECTION_TIMEOUT", self.connection_timeout)
        self.max_retries = _get_env_int("MAX_RETRIES", self.max_retries)


@dataclass
class PySap2000Config:
    """
    Main configuration object for PySap2000.

    All top-level config values live here and can be overridden through
    environment variables.

    Environment variable prefix: `PYSAP_`
    
    Example:
        # Set environment variables
        export PYSAP_LOG_LEVEL=DEBUG
        export PYSAP_AGENT_MAX_HISTORY=20
        
        # Use in code
        from PySap2000.config import config
        config.log_level = "INFO"
    """
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Debug mode
    debug: bool = False
    
    # Strict mode: raise instead of silently returning COM error codes
    strict_mode: bool = False
    
    # Nested config sections
    agent: AgentConfig = field(default_factory=AgentConfig)
    visualization: VisualizationConfig = field(default_factory=VisualizationConfig)
    connection: ConnectionConfig = field(default_factory=ConnectionConfig)
    
    def __post_init__(self):
        """Load values from environment variables."""
        self.log_level = _get_env("LOG_LEVEL", self.log_level)
        self.log_file = _get_env("LOG_FILE") or None
        self.debug = _get_env_bool("DEBUG", self.debug)
        self.strict_mode = _get_env_bool("STRICT_MODE", self.strict_mode)
    
    def to_dict(self) -> dict:
        """Convert the config object into a dictionary."""
        return {
            "log_level": self.log_level,
            "log_file": self.log_file,
            "debug": self.debug,
            "agent": {
                "default_provider": self.agent.default_provider,
                "default_model": self.agent.default_model,
                "temperature": self.agent.temperature,
                "max_history_rounds": self.agent.max_history_rounds,
                "require_confirmation": self.agent.require_confirmation,
            },
            "visualization": {
                "point_color": self.visualization.point_color,
                "frame_color": self.visualization.frame_color,
                "default_format": self.visualization.default_format,
            },
            "connection": {
                "attach_to_instance": self.connection.attach_to_instance,
                "connection_timeout": self.connection.connection_timeout,
                "default_units": self.connection.default_units,
            }
        }
    
    def update_from_dict(self, data: dict) -> None:
        """Update config values from a dictionary."""
        if "log_level" in data:
            self.log_level = data["log_level"]
        if "log_file" in data:
            self.log_file = data["log_file"]
        if "debug" in data:
            self.debug = data["debug"]
        
        if "agent" in data:
            agent_data = data["agent"]
            if "max_history_rounds" in agent_data:
                self.agent.max_history_rounds = agent_data["max_history_rounds"]
            if "temperature" in agent_data:
                self.agent.temperature = agent_data["temperature"]


# Global config instance
config = PySap2000Config()
