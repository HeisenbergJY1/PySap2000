# -*- coding: utf-8 -*-
"""
units.py - 单位系统
对应 SAP2000 的 eUnits 枚举

API Reference:
    - GetPresentUnits() -> eUnits
    - SetPresentUnits(Units) -> Long
    - GetDatabaseUnits() -> eUnits

Usage:
    from PySap2000.global_parameters import Units, UnitSystem
    
    # 获取当前单位
    current_units = Units.get_present_units(model)
    
    # 设置单位为 kN-m
    Units.set_present_units(model, UnitSystem.KN_M_C)
    
    # 获取数据库单位
    db_units = Units.get_database_units(model)
"""

from enum import IntEnum
from typing import Optional


class UnitSystem(IntEnum):
    """
    单位系统枚举
    对应 SAP2000 的 eUnits
    
    命名规则: 力_长度_温度
    F = Fahrenheit (华氏度)
    C = Celsius (摄氏度)
    """
    LB_IN_F = 1       # lb, in, F
    LB_FT_F = 2       # lb, ft, F
    KIP_IN_F = 3      # Kip, in, F
    KIP_FT_F = 4      # Kip, ft, F
    KN_MM_C = 5       # KN, mm, C
    KN_M_C = 6        # KN, m, C
    KGF_MM_C = 7      # Kgf, mm, C
    KGF_M_C = 8       # Kgf, m, C
    N_MM_C = 9        # N, mm, C
    N_M_C = 10        # N, m, C
    TON_MM_C = 11     # Tonf, mm, C
    TON_M_C = 12      # Tonf, m, C
    KN_CM_C = 13      # KN, cm, C
    KGF_CM_C = 14     # Kgf, cm, C
    N_CM_C = 15       # N, cm, C
    TON_CM_C = 16     # Tonf, cm, C


# 单位系统描述
UNIT_DESCRIPTIONS = {
    UnitSystem.LB_IN_F: "lb-in-F",
    UnitSystem.LB_FT_F: "lb-ft-F",
    UnitSystem.KIP_IN_F: "kip-in-F",
    UnitSystem.KIP_FT_F: "kip-ft-F",
    UnitSystem.KN_MM_C: "kN-mm-C",
    UnitSystem.KN_M_C: "kN-m-C",
    UnitSystem.KGF_MM_C: "kgf-mm-C",
    UnitSystem.KGF_M_C: "kgf-m-C",
    UnitSystem.N_MM_C: "N-mm-C",
    UnitSystem.N_M_C: "N-m-C",
    UnitSystem.TON_MM_C: "tonf-mm-C",
    UnitSystem.TON_M_C: "tonf-m-C",
    UnitSystem.KN_CM_C: "kN-cm-C",
    UnitSystem.KGF_CM_C: "kgf-cm-C",
    UnitSystem.N_CM_C: "N-cm-C",
    UnitSystem.TON_CM_C: "tonf-cm-C",
}


class Units:
    """
    单位系统管理类
    
    提供获取和设置 SAP2000 单位系统的静态方法
    """
    
    @staticmethod
    def get_present_units(model) -> UnitSystem:
        """
        获取当前显示单位
        
        API: GetPresentUnits() -> eUnits
        
        Returns:
            当前单位系统
        """
        result = model.GetPresentUnits()
        return UnitSystem(result)
    
    @staticmethod
    def set_present_units(model, units: UnitSystem) -> int:
        """
        设置当前显示单位
        
        API: SetPresentUnits(Units) -> Long
        
        Args:
            model: SapModel 对象
            units: 单位系统
            
        Returns:
            0 表示成功
        """
        return model.SetPresentUnits(units)
    
    @staticmethod
    def get_database_units(model) -> UnitSystem:
        """
        获取数据库单位
        
        所有数据在模型内部以此单位存储，需要时转换为当前显示单位
        
        API: GetDatabaseUnits() -> eUnits
        
        Returns:
            数据库单位系统
        """
        result = model.GetDatabaseUnits()
        return UnitSystem(result)
    
    @staticmethod
    def get_unit_description(units: UnitSystem) -> str:
        """
        获取单位系统的中文描述
        
        Args:
            units: 单位系统
            
        Returns:
            中文描述字符串
        """
        return UNIT_DESCRIPTIONS.get(units, str(units))
    
    @staticmethod
    def get_force_unit(units: UnitSystem) -> str:
        """获取力单位"""
        force_map = {
            UnitSystem.LB_IN_F: "lb",
            UnitSystem.LB_FT_F: "lb",
            UnitSystem.KIP_IN_F: "kip",
            UnitSystem.KIP_FT_F: "kip",
            UnitSystem.KN_MM_C: "kN",
            UnitSystem.KN_M_C: "kN",
            UnitSystem.KGF_MM_C: "kgf",
            UnitSystem.KGF_M_C: "kgf",
            UnitSystem.N_MM_C: "N",
            UnitSystem.N_M_C: "N",
            UnitSystem.TON_MM_C: "tonf",
            UnitSystem.TON_M_C: "tonf",
            UnitSystem.KN_CM_C: "kN",
            UnitSystem.KGF_CM_C: "kgf",
            UnitSystem.N_CM_C: "N",
            UnitSystem.TON_CM_C: "tonf",
        }
        return force_map.get(units, "")
    
    @staticmethod
    def get_length_unit(units: UnitSystem) -> str:
        """获取长度单位"""
        length_map = {
            UnitSystem.LB_IN_F: "in",
            UnitSystem.LB_FT_F: "ft",
            UnitSystem.KIP_IN_F: "in",
            UnitSystem.KIP_FT_F: "ft",
            UnitSystem.KN_MM_C: "mm",
            UnitSystem.KN_M_C: "m",
            UnitSystem.KGF_MM_C: "mm",
            UnitSystem.KGF_M_C: "m",
            UnitSystem.N_MM_C: "mm",
            UnitSystem.N_M_C: "m",
            UnitSystem.TON_MM_C: "mm",
            UnitSystem.TON_M_C: "m",
            UnitSystem.KN_CM_C: "cm",
            UnitSystem.KGF_CM_C: "cm",
            UnitSystem.N_CM_C: "cm",
            UnitSystem.TON_CM_C: "cm",
        }
        return length_map.get(units, "")
    
    @staticmethod
    def get_temp_unit(units: UnitSystem) -> str:
        """获取温度单位"""
        if units.value <= 4:
            return "°F"
        return "°C"
