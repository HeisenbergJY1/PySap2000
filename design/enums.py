# -*- coding: utf-8 -*-
"""
design/enums.py - 设计模块枚举

结构设计相关枚举类型（钢结构、混凝土、铝结构、冷弯薄壁钢）。
"""

from enum import IntEnum


# ============================================================================
# 通用枚举
# ============================================================================

class ItemType(IntEnum):
    """对象选择类型
    
    用于指定设计结果的对象范围。
    """
    OBJECT = 0          # 单个对象
    GROUP = 1           # 组
    SELECTED_OBJECTS = 2  # 选中的对象


class RatioType(IntEnum):
    """钢结构/铝结构/冷弯设计应力比类型
    
    控制应力比或承载力比的类型。
    注意：铝结构和冷弯只有 1, 3, 4 三种类型。
    """
    NONE = 0                    # 无/未知
    PMM = 1                     # 轴力-弯矩组合
    MAJOR_SHEAR = 2             # 主剪力（仅钢结构）
    MINOR_SHEAR = 3             # 次剪力（钢结构）/ 主剪力（铝/冷弯）
    MAJOR_BEAM_COLUMN = 4       # 主轴梁柱承载力比（钢结构）/ 次剪力（铝/冷弯）
    MINOR_BEAM_COLUMN = 5       # 次轴梁柱承载力比（仅钢结构）
    OTHER = 6                   # 其他（仅钢结构）


class ColumnDesignOption(IntEnum):
    """混凝土柱设计选项"""
    CHECK = 1       # 验算
    DESIGN = 2      # 设计


# ============================================================================
# 钢结构设计枚举
# ============================================================================

class SteelDesignCode(IntEnum):
    """钢结构设计规范
    
    SAP2000 支持的钢结构设计规范代码。
    注意：API 使用字符串名称，此枚举用于类型安全和代码提示。
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


# 规范代码名称映射（API 使用字符串）
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

# 反向映射：字符串名称 -> 枚举
STEEL_CODE_FROM_NAME = {v: k for k, v in STEEL_CODE_NAMES.items()}


# ============================================================================
# 混凝土设计枚举
# ============================================================================

class ConcreteDesignCode(IntEnum):
    """混凝土框架设计规范"""
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
    """混凝土壳设计规范"""
    ACI_350_20 = 1
    EUROCODE_2_2004 = 2


CONCRETE_SHELL_CODE_NAMES = {
    ConcreteShellDesignCode.ACI_350_20: "ACI 350-20",
    ConcreteShellDesignCode.EUROCODE_2_2004: "Eurocode 2-2004",
}

CONCRETE_SHELL_CODE_FROM_NAME = {v: k for k, v in CONCRETE_SHELL_CODE_NAMES.items()}


# ============================================================================
# 铝结构设计枚举
# ============================================================================

class AluminumDesignCode(IntEnum):
    """铝结构设计规范"""
    AA_ASD_2000 = 1
    AA_LRFD_2000 = 2


ALUMINUM_CODE_NAMES = {
    AluminumDesignCode.AA_ASD_2000: "AA-ASD 2000",
    AluminumDesignCode.AA_LRFD_2000: "AA-LRFD 2000",
}

ALUMINUM_CODE_FROM_NAME = {v: k for k, v in ALUMINUM_CODE_NAMES.items()}


# ============================================================================
# 冷弯薄壁钢设计枚举
# ============================================================================

class ColdFormedDesignCode(IntEnum):
    """冷弯薄壁钢设计规范"""
    AISI_ASD96 = 1
    AISI_LRFD96 = 2


COLD_FORMED_CODE_NAMES = {
    ColdFormedDesignCode.AISI_ASD96: "AISI-ASD96",
    ColdFormedDesignCode.AISI_LRFD96: "AISI-LRFD96",
}

COLD_FORMED_CODE_FROM_NAME = {v: k for k, v in COLD_FORMED_CODE_NAMES.items()}
