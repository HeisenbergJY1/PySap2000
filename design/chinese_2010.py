# -*- coding: utf-8 -*-
"""
design/chinese_2010.py - 中国钢结构规范 GB 50017-2010 设计函数

SAP2000 DesignSteel.Chinese_2010 API 的 Python 封装。
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, Tuple, Union

from .enums import ItemType
from PySap2000.com_helper import com_ret, com_data


class FramingType(IntEnum):
    """结构体系类型"""
    PROGRAM_DEFAULT = 0     # 按首选项设置
    SMF = 1                 # 有侧移弯矩框架
    CBF = 2                 # 中心支撑框架
    EBF = 3                 # 偏心支撑框架
    NMF = 4                 # 无侧移弯矩框架


class ElementType(IntEnum):
    """构件类型"""
    PROGRAM_DETERMINED = 0  # 程序确定
    COLUMN = 1              # 柱
    BEAM = 2                # 梁
    BRACE = 3               # 支撑
    TRUSS = 4               # 桁架


class SeismicDesignGrade(IntEnum):
    """抗震设计等级"""
    GRADE_I = 1             # 一级
    GRADE_II = 2            # 二级
    GRADE_III = 3           # 三级
    GRADE_IV = 4            # 四级
    NON_SEISMIC = 5         # 非抗震


class MultiResponseDesign(IntEnum):
    """多工况设计方法"""
    ENVELOPES = 1           # 包络
    STEP_BY_STEP = 2        # 逐步
    LAST_STEP = 3           # 最后一步
    ENVELOPES_ALL = 4       # 包络-全部
    STEP_BY_STEP_ALL = 5    # 逐步-全部


class DeflectionCheckType(IntEnum):
    """挠度检查类型"""
    PROGRAM_DEFAULT = 0     # 程序默认
    RATIO = 1               # 相对值
    ABSOLUTE = 2            # 绝对值
    BOTH = 3                # 两者


class OverwriteItem(IntEnum):
    """覆盖项编号 (1-51)"""
    FRAMING_TYPE = 1                    # 结构体系类型
    ELEMENT_TYPE = 2                    # 构件类型
    IS_TRANSFER_COLUMN = 3              # 是否转换柱
    SEISMIC_MAGNIFICATION = 4           # 地震放大系数
    IS_ROLLED_SECTION = 5               # 是否轧制截面
    IS_FLANGE_CUT_BY_GAS = 6            # 翼缘是否气割
    IS_BOTH_END_PINNED = 7              # 两端是否铰接
    IGNORE_BT_CHECK = 8                 # 忽略宽厚比检查
    CLASSIFY_AS_FLEXO_COMPRESSION = 9   # 按压弯构件分类
    IS_BEAM_TOP_LOADED = 10             # 梁顶部是否受荷
    CONSIDER_DEFLECTION = 11            # 考虑挠度
    DEFLECTION_CHECK_TYPE = 12          # 挠度检查类型
    DL_DEFLECTION_RATIO = 13            # 恒载挠度限值 L/Value
    SDL_LL_DEFLECTION_RATIO = 14        # 附加恒载+活载挠度限值 L/Value
    LL_DEFLECTION_RATIO = 15            # 活载挠度限值 L/Value
    TOTAL_DEFLECTION_RATIO = 16         # 总荷载挠度限值 L/Value
    TOTAL_CAMBER_RATIO = 17             # 总起拱限值 L/Value
    DL_DEFLECTION_ABS = 18              # 恒载挠度限值 绝对值
    SDL_LL_DEFLECTION_ABS = 19          # 附加恒载+活载挠度限值 绝对值
    LL_DEFLECTION_ABS = 20              # 活载挠度限值 绝对值
    TOTAL_DEFLECTION_ABS = 21           # 总荷载挠度限值 绝对值
    TOTAL_CAMBER_ABS = 22               # 总起拱限值 绝对值
    SPECIFIED_CAMBER = 23               # 指定起拱值
    NET_AREA_RATIO = 24                 # 净面积与总面积比
    LIVE_LOAD_REDUCTION = 25            # 活载折减系数
    UNBRACED_RATIO_MAJOR = 26           # 主轴无支撑长度比
    UNBRACED_RATIO_MINOR_LTB = 27       # 次轴侧扭屈曲无支撑长度比
    MUE_MAJOR = 28                      # 主轴计算长度系数 μ
    MUE_MINOR = 29                      # 次轴计算长度系数 μ
    BETA_M_MAJOR = 30                   # 主轴等效弯矩系数 βm
    BETA_M_MINOR = 31                   # 次轴等效弯矩系数 βm
    BETA_T_MAJOR = 32                   # 主轴弯矩系数 βt
    BETA_T_MINOR = 33                   # 次轴弯矩系数 βt
    PHI_MAJOR = 34                      # 主轴轴心稳定系数 φ
    PHI_MINOR = 35                      # 次轴轴心稳定系数 φ
    PHI_B_MAJOR = 36                    # 主轴弯曲稳定系数 φb
    PHI_B_MINOR = 37                    # 次轴弯曲稳定系数 φb
    GAMMA_MAJOR = 38                    # 主轴塑性发展系数 γ
    GAMMA_MINOR = 39                    # 次轴塑性发展系数 γ
    ETA_SECTION = 40                    # 截面影响系数 η
    ETA_BC = 41                         # 梁柱承载力系数 η
    DELTA_MAJOR = 42                    # 主轴欧拉弯矩系数 δ
    DELTA_MINOR = 43                    # 次轴欧拉弯矩系数 δ
    FY = 44                             # 屈服强度 Fy
    F_ALLOWABLE = 45                    # 容许正应力 f
    FV_ALLOWABLE = 46                   # 容许剪应力 fv
    CONSIDER_FICTITIOUS_SHEAR = 47      # 考虑虚拟剪力
    DC_RATIO_LIMIT = 48                 # 需求/承载力比限值
    DUAL_SYSTEM_FACTOR = 49             # 双重体系放大系数
    LOR_COMPRESSION = 50                # 受压长细比限值 Lo/r
    LR_TENSION = 51                     # 受拉长细比限值 L/r


class PreferenceItem(IntEnum):
    """首选项编号 (1-15)"""
    FRAMING_TYPE = 1                    # 结构体系类型
    GAMMA0 = 2                          # 重要性系数 γ0
    IGNORE_BT_CHECK = 3                 # 忽略宽厚比检查
    CLASSIFY_AS_FLEXO_COMPRESSION = 4   # 按压弯构件分类
    CONSIDER_DEFLECTION = 5             # 考虑挠度
    DL_DEFLECTION_RATIO = 6             # 恒载挠度限值 L/Value
    SDL_LL_DEFLECTION_RATIO = 7         # 附加恒载+活载挠度限值 L/Value
    LL_DEFLECTION_RATIO = 8             # 活载挠度限值 L/Value
    TOTAL_DEFLECTION_RATIO = 9          # 总荷载挠度限值 L/Value
    TOTAL_CAMBER_RATIO = 10             # 总起拱限值 L/Value
    PATTERN_LIVE_LOAD_FACTOR = 11       # 活载不利布置系数
    DC_RATIO_LIMIT = 12                 # 需求/承载力比限值
    MULTI_RESPONSE_DESIGN = 13          # 多工况设计方法
    IS_TALL_BUILDING = 14               # 是否高层建筑
    SEISMIC_DESIGN_GRADE = 15           # 抗震设计等级


@dataclass
class OverwriteResult:
    """覆盖项获取结果
    
    Attributes:
        value: 覆盖值
        prog_det: 是否程序确定
    """
    value: float
    prog_det: bool


# ============================================================================
# Preference 首选项函数
# ============================================================================

def get_chinese_2010_preference(model, item: Union[PreferenceItem, int]) -> float:
    """获取中国规范首选项值
    
    Args:
        model: SapModel 对象
        item: 首选项编号 (1-15)
        
    Returns:
        首选项值
    """
    result = model.DesignSteel.Chinese_2010.GetPreference(int(item), 0.0)
    return com_data(result, 0, 0.0)


def set_chinese_2010_preference(model, item: Union[PreferenceItem, int], value: float) -> int:
    """设置中国规范首选项值
    
    Args:
        model: SapModel 对象
        item: 首选项编号 (1-15)
        value: 首选项值
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignSteel.Chinese_2010.SetPreference(int(item), value)
    return com_ret(ret)


# ============================================================================
# Overwrite 覆盖项函数
# ============================================================================

def get_chinese_2010_overwrite(
    model,
    name: str,
    item: Union[OverwriteItem, int]
) -> OverwriteResult:
    """获取中国规范覆盖项值
    
    Args:
        model: SapModel 对象
        name: 框架对象名称
        item: 覆盖项编号 (1-51)
        
    Returns:
        覆盖项结果（值和是否程序确定）
    """
    result = model.DesignSteel.Chinese_2010.GetOverwrite(name, int(item), 0.0, False)
    value = com_data(result, 0)
    prog_det = com_data(result, 1)
    if value is not None and prog_det is not None:
        return OverwriteResult(value=value, prog_det=bool(prog_det))
    return OverwriteResult(value=0.0, prog_det=True)


def set_chinese_2010_overwrite(
    model,
    name: str,
    item: Union[OverwriteItem, int],
    value: float,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """设置中国规范覆盖项值
    
    Args:
        model: SapModel 对象
        name: 对象名称、组名称或忽略（取决于 item_type）
        item: 覆盖项编号 (1-51)
        value: 覆盖值
        item_type: 对象选择类型
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    ret = model.DesignSteel.Chinese_2010.SetOverwrite(name, int(item), value, int(item_type))
    return com_ret(ret)


# ============================================================================
# 便捷函数 - 常用首选项
# ============================================================================

def set_chinese_2010_framing_type(model, framing_type: FramingType) -> int:
    """设置结构体系类型"""
    return set_chinese_2010_preference(model, PreferenceItem.FRAMING_TYPE, float(framing_type))


def set_chinese_2010_gamma0(model, gamma0: float) -> int:
    """设置重要性系数 γ0"""
    return set_chinese_2010_preference(model, PreferenceItem.GAMMA0, gamma0)


def set_chinese_2010_seismic_grade(model, grade: SeismicDesignGrade) -> int:
    """设置抗震设计等级"""
    return set_chinese_2010_preference(model, PreferenceItem.SEISMIC_DESIGN_GRADE, float(grade))


def set_chinese_2010_dc_ratio_limit(model, ratio: float) -> int:
    """设置需求/承载力比限值"""
    return set_chinese_2010_preference(model, PreferenceItem.DC_RATIO_LIMIT, ratio)


def set_chinese_2010_tall_building(model, is_tall: bool) -> int:
    """设置是否高层建筑"""
    return set_chinese_2010_preference(model, PreferenceItem.IS_TALL_BUILDING, 1.0 if is_tall else 0.0)


# ============================================================================
# 便捷函数 - 常用覆盖项
# ============================================================================

def set_chinese_2010_element_type(
    model,
    name: str,
    element_type: ElementType,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """设置构件类型"""
    return set_chinese_2010_overwrite(model, name, OverwriteItem.ELEMENT_TYPE, float(element_type), item_type)


def set_chinese_2010_mue_factors(
    model,
    name: str,
    mue_major: float,
    mue_minor: float,
    item_type: ItemType = ItemType.OBJECT
) -> Tuple[int, int]:
    """设置计算长度系数 μ
    
    Args:
        model: SapModel 对象
        name: 对象名称
        mue_major: 主轴计算长度系数
        mue_minor: 次轴计算长度系数
        item_type: 对象选择类型
        
    Returns:
        (主轴返回码, 次轴返回码)
    """
    ret1 = set_chinese_2010_overwrite(model, name, OverwriteItem.MUE_MAJOR, mue_major, item_type)
    ret2 = set_chinese_2010_overwrite(model, name, OverwriteItem.MUE_MINOR, mue_minor, item_type)
    return ret1, ret2


def set_chinese_2010_unbraced_ratios(
    model,
    name: str,
    ratio_major: float,
    ratio_minor: float,
    item_type: ItemType = ItemType.OBJECT
) -> Tuple[int, int]:
    """设置无支撑长度比
    
    Args:
        model: SapModel 对象
        name: 对象名称
        ratio_major: 主轴无支撑长度比
        ratio_minor: 次轴无支撑长度比（侧扭屈曲）
        item_type: 对象选择类型
        
    Returns:
        (主轴返回码, 次轴返回码)
    """
    ret1 = set_chinese_2010_overwrite(model, name, OverwriteItem.UNBRACED_RATIO_MAJOR, ratio_major, item_type)
    ret2 = set_chinese_2010_overwrite(model, name, OverwriteItem.UNBRACED_RATIO_MINOR_LTB, ratio_minor, item_type)
    return ret1, ret2
