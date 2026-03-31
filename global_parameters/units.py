# -*- coding: utf-8 -*-
"""
units.py - Unit systems.

Maps to the SAP2000 `eUnits` enumeration.

API Reference:
    - GetPresentUnits() -> eUnits
    - SetPresentUnits(Units) -> Long
    - GetDatabaseUnits() -> eUnits

Usage:
    from PySap2000.global_parameters import Units, UnitSystem

    # Current display units
    current_units = Units.get_present_units(model)

    # Set units to kN-m-C
    Units.set_present_units(model, UnitSystem.KN_M_C)

    # Database storage units
    db_units = Units.get_database_units(model)
"""

from enum import IntEnum
from typing import Optional


class UnitSystem(IntEnum):
    """
    Unit system enumeration.

    Matches SAP2000 `eUnits`.

    Naming convention: force_length_temperature.
    - F: Fahrenheit
    - C: Celsius
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


# Human-readable unit system labels (short form)
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
    Helpers for reading and setting the SAP2000 unit system.
    """
    
    @staticmethod
    def get_present_units(model) -> UnitSystem:
        """
        Get the current display units.

        API: GetPresentUnits() -> eUnits

        Returns:
            Active `UnitSystem`.
        """
        result = model.GetPresentUnits()
        return UnitSystem(result)
    
    @staticmethod
    def set_present_units(model, units: UnitSystem) -> int:
        """
        Set the current display units.

        API: SetPresentUnits(Units) -> Long

        Args:
            model: SAP2000 SapModel object
            units: Target unit system

        Returns:
            `0` if successful.
        """
        return model.SetPresentUnits(units)
    
    @staticmethod
    def get_database_units(model) -> UnitSystem:
        """
        Get the database (internal storage) units.

        Model data is stored in this system and converted to display units when needed.

        API: GetDatabaseUnits() -> eUnits

        Returns:
            Database `UnitSystem`.
        """
        result = model.GetDatabaseUnits()
        return UnitSystem(result)
    
    @staticmethod
    def get_unit_description(units: UnitSystem) -> str:
        """
        Get a short label for the unit system (e.g. ``kN-m-C``).

        Args:
            units: Unit system

        Returns:
            Label string.
        """
        return UNIT_DESCRIPTIONS.get(units, str(units))
    
    @staticmethod
    def get_force_unit(units: UnitSystem) -> str:
        """Return the force unit symbol for the given system."""
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
        """Return the length unit symbol for the given system."""
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
        """Return the temperature unit symbol for the given system."""
        if units.value <= 4:
            return "°F"
        return "°C"
