# -*- coding: utf-8 -*-
"""
design/enums.py - Design module enums

Enums for steel, concrete, aluminum, and cold-formed design.
"""

from enum import IntEnum


# ============================================================================
# Shared enums
# ============================================================================

class ItemType(IntEnum):
    """Object selection mode
    
    Scopes which objects are included in design result queries.
    """
    OBJECT = 0          # Single object
    GROUP = 1           # Group
    SELECTED_OBJECTS = 2  # Selected objects


class RatioType(IntEnum):
    """Stress or strength ratio type (steel / aluminum / cold-formed)
    
    Selects which ratio is reported as controlling.
    Aluminum and cold-formed design only use types 1, 3, and 4.
    """
    NONE = 0                    # None / unknown
    PMM = 1                     # Axial-flexural (PMM)
    MAJOR_SHEAR = 2             # Major-axis shear (steel only)
    MINOR_SHEAR = 3             # Minor shear (steel) or major shear (aluminum / cold-formed)
    MAJOR_BEAM_COLUMN = 4       # Major beam-column (steel) or minor shear (aluminum / cold-formed)
    MINOR_BEAM_COLUMN = 5       # Minor beam-column (steel only)
    OTHER = 6                   # Other (steel only)


class ColumnDesignOption(IntEnum):
    """Concrete column design mode"""
    CHECK = 1       # Check
    DESIGN = 2      # Design


# ============================================================================
# Steel design enums
# ============================================================================

class SteelDesignCode(IntEnum):
    """Steel design code identifiers.

    String names are used by the SAP2000 COM API; this enum aids typing and discovery.
    """
    AASHTO_LRFD_2007 = 1
    AISC_ASD89 = 2
    AISC_360_10 = 3
    AISC_360_05_IBC2006 = 4
    AISC_LRFD93 = 5
    API_RP2A_LRFD_97 = 6
    API_RP2A_WSD2000 = 7
    API_RP2A_WSD2014 = 8
    AS_4100_1998 = 9
    ASCE_10_97 = 10
    BS5950_2000 = 11
    CHINESE_2010 = 12
    CSA_S16_19 = 13
    CSA_S16_14 = 14
    CSA_S16_09 = 15
    EN1993_1_1_2005 = 16  # formerly EUROCODE 3-2005
    INDIAN_IS_800_2007 = 17
    ITALIAN_NTC_2008 = 18
    ITALIAN_UNI_10011 = 19
    KBC_2009 = 20
    NORSOK_N_004_2013 = 21
    NZS_3404_1997 = 22
    SP_16_13330_2011 = 23


# Code name strings used by the API
STEEL_CODE_NAMES = {
    SteelDesignCode.AASHTO_LRFD_2007: "AASHTO LRFD 2007",
    SteelDesignCode.AISC_ASD89: "AISC-ASD89",
    SteelDesignCode.AISC_360_10: "AISC 360-10",
    SteelDesignCode.AISC_360_05_IBC2006: "AISC360-05/IBC2006",
    SteelDesignCode.AISC_LRFD93: "AISC-LRFD93",
    SteelDesignCode.API_RP2A_LRFD_97: "API RP2A-LRFD 97",
    SteelDesignCode.API_RP2A_WSD2000: "API RP2A-WSD2000",
    SteelDesignCode.API_RP2A_WSD2014: "API RP2A-WSD2014",
    SteelDesignCode.AS_4100_1998: "AS 4100-1998",
    SteelDesignCode.ASCE_10_97: "ASCE 10-97",
    SteelDesignCode.BS5950_2000: "BS5950 2000",
    SteelDesignCode.CHINESE_2010: "Chinese 2010",
    SteelDesignCode.CSA_S16_19: "CSA S16-19",
    SteelDesignCode.CSA_S16_14: "CSA S16-14",
    SteelDesignCode.CSA_S16_09: "CSA-S16-09",
    SteelDesignCode.EN1993_1_1_2005: "EN1993-1-1:2005(formerlyEUROCODE3-2005)",
    SteelDesignCode.INDIAN_IS_800_2007: "Indian IS 800-2007",
    SteelDesignCode.ITALIAN_NTC_2008: "Italian NTC 2008",
    SteelDesignCode.ITALIAN_UNI_10011: "Italian UNI 10011",
    SteelDesignCode.KBC_2009: "KBC 2009",
    SteelDesignCode.NORSOK_N_004_2013: "Norsok N-004 2013",
    SteelDesignCode.NZS_3404_1997: "NZS 3404-1997",
    SteelDesignCode.SP_16_13330_2011: "SP 16.13330.2011",
}

# Reverse lookup: name string to enum
STEEL_CODE_FROM_NAME = {v: k for k, v in STEEL_CODE_NAMES.items()}


# ============================================================================
# Concrete design enums
# ============================================================================

class ConcreteDesignCode(IntEnum):
    """Concrete frame design code."""
    AASHTO_LRFD_2014 = 1
    AASHTO_LRFD_2012 = 2
    AASHTO_CONCRETE_07 = 3
    ACI_318_14 = 4
    ACI_318_11 = 5
    ACI_318_08_IBC2009 = 6
    AS_3600_09 = 7
    BS8110_97 = 8
    CHINESE_2010 = 9
    CSA_A23_3_14 = 10
    CSA_A23_3_04 = 11
    EUROCODE_2_2004 = 12
    HONG_KONG_CP_2013 = 13
    INDIAN_IS_456_2000 = 14
    ITALIAN_NTC_2008 = 15
    KBC_2009 = 16
    MEXICAN_RCDF_2004 = 17
    NZS_3101_2006 = 18
    SINGAPORE_CP_65_99 = 19
    SP_63_13330_2012 = 20
    TS_500_2000 = 21


CONCRETE_CODE_NAMES = {
    ConcreteDesignCode.AASHTO_LRFD_2014: "AASHTO LRFD 2014",
    ConcreteDesignCode.AASHTO_LRFD_2012: "AASHTO LRFD 2012",
    ConcreteDesignCode.AASHTO_CONCRETE_07: "AASHTO Concrete 07",
    ConcreteDesignCode.ACI_318_14: "ACI 318-14",
    ConcreteDesignCode.ACI_318_11: "ACI 318-11",
    ConcreteDesignCode.ACI_318_08_IBC2009: "ACI 318-08/IBC2009",
    ConcreteDesignCode.AS_3600_09: "AS 3600-09",
    ConcreteDesignCode.BS8110_97: "BS8110 97",
    ConcreteDesignCode.CHINESE_2010: "Chinese 2010",
    ConcreteDesignCode.CSA_A23_3_14: "CSA A23.3-14",
    ConcreteDesignCode.CSA_A23_3_04: "CSA A23.3-04",
    ConcreteDesignCode.EUROCODE_2_2004: "Eurocode 2-2004",
    ConcreteDesignCode.HONG_KONG_CP_2013: "Hong Kong CP 2013",
    ConcreteDesignCode.INDIAN_IS_456_2000: "Indian IS 456-2000",
    ConcreteDesignCode.ITALIAN_NTC_2008: "Italian NTC 2008",
    ConcreteDesignCode.KBC_2009: "KBC 2009",
    ConcreteDesignCode.MEXICAN_RCDF_2004: "Mexican RCDF 2004",
    ConcreteDesignCode.NZS_3101_2006: "NZS 3101:2006",
    ConcreteDesignCode.SINGAPORE_CP_65_99: "Singapore CP 65:99",
    ConcreteDesignCode.SP_63_13330_2012: "SP 63.13330.2012",
    ConcreteDesignCode.TS_500_2000: "TS 500-2000",
}

CONCRETE_CODE_FROM_NAME = {v: k for k, v in CONCRETE_CODE_NAMES.items()}


class ConcreteShellDesignCode(IntEnum):
    """Concrete shell design code."""
    ACI_350_20 = 1
    EUROCODE_2_2004 = 2


CONCRETE_SHELL_CODE_NAMES = {
    ConcreteShellDesignCode.ACI_350_20: "ACI 350-20",
    ConcreteShellDesignCode.EUROCODE_2_2004: "Eurocode 2-2004",
}

CONCRETE_SHELL_CODE_FROM_NAME = {v: k for k, v in CONCRETE_SHELL_CODE_NAMES.items()}


# ============================================================================
# Aluminum design enums
# ============================================================================

class AluminumDesignCode(IntEnum):
    """Aluminum design code."""
    AA_ASD_2000 = 1
    AA_LRFD_2000 = 2


ALUMINUM_CODE_NAMES = {
    AluminumDesignCode.AA_ASD_2000: "AA-ASD 2000",
    AluminumDesignCode.AA_LRFD_2000: "AA-LRFD 2000",
}

ALUMINUM_CODE_FROM_NAME = {v: k for k, v in ALUMINUM_CODE_NAMES.items()}


# ============================================================================
# Cold-formed steel design enums
# ============================================================================

class ColdFormedDesignCode(IntEnum):
    """Cold-formed steel design code."""
    AISI_ASD96 = 1
    AISI_LRFD96 = 2


COLD_FORMED_CODE_NAMES = {
    ColdFormedDesignCode.AISI_ASD96: "AISI-ASD96",
    ColdFormedDesignCode.AISI_LRFD96: "AISI-LRFD96",
}

COLD_FORMED_CODE_FROM_NAME = {v: k for k, v in COLD_FORMED_CODE_NAMES.items()}
