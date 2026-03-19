# -*- coding: utf-8 -*-
"""
design/data_classes.py - 设计模块数据类

结构设计相关数据类（钢结构、混凝土、铝结构、冷弯薄壁钢）。
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .enums import RatioType, ColumnDesignOption


# ============================================================================
# 通用数据类
# ============================================================================

@dataclass
class VerifyPassedResult:
    """设计验证结果（通用）
    
    Attributes:
        total_count: 未通过或未检查的对象总数
        failed_count: 未通过设计检查的对象数
        unchecked_count: 尚未检查的对象数
        frame_names: 未通过或未检查的对象名称列表
    """
    total_count: int
    failed_count: int
    unchecked_count: int
    frame_names: List[str] = field(default_factory=list)
    
    @property
    def all_passed(self) -> bool:
        """是否全部通过"""
        return self.total_count == 0


# ============================================================================
# 钢结构 / 铝结构 / 冷弯薄壁钢 通用汇总结果
# ============================================================================

@dataclass
class SteelSummaryResult:
    """钢结构设计汇总结果
    
    Attributes:
        frame_name: 框架对象名称
        ratio: 控制应力比或承载力比
        ratio_type: 应力比类型 (1-6)
        location: 控制位置距 I 端的距离
        combo_name: 控制组合名称
        error_summary: 错误信息
        warning_summary: 警告信息
    """
    frame_name: str
    ratio: float
    ratio_type: RatioType
    location: float
    combo_name: str
    error_summary: str = ""
    warning_summary: str = ""
    
    @property
    def passed(self) -> bool:
        """是否通过设计检查（应力比 <= 1.0）"""
        return self.ratio <= 1.0
    
    @property
    def ratio_type_name(self) -> str:
        """应力比类型名称"""
        names = {
            RatioType.PMM: "PMM",
            RatioType.MAJOR_SHEAR: "Major Shear",
            RatioType.MINOR_SHEAR: "Minor Shear",
            RatioType.MAJOR_BEAM_COLUMN: "Major Beam-Column",
            RatioType.MINOR_BEAM_COLUMN: "Minor Beam-Column",
            RatioType.OTHER: "Other",
        }
        return names.get(self.ratio_type, "Unknown")


# 铝结构和冷弯薄壁钢的汇总结果格式与钢结构相同
AluminumSummaryResult = SteelSummaryResult
ColdFormedSummaryResult = SteelSummaryResult


# ============================================================================
# 混凝土设计数据类
# ============================================================================

@dataclass
class ConcreteBeamResult:
    """混凝土梁设计汇总结果
    
    Attributes:
        frame_name: 框架对象名称
        location: 距 I 端的距离
        top_combo: 控制顶部纵筋的组合名称
        top_area: 顶部纵筋面积（弯矩）
        bot_combo: 控制底部纵筋的组合名称
        bot_area: 底部纵筋面积（弯矩）
        vmajor_combo: 控制剪力的组合名称
        vmajor_area: 主剪力箍筋面积/单位长度
        tl_combo: 控制扭转纵筋的组合名称
        tl_area: 扭转纵筋面积
        tt_combo: 控制扭转箍筋的组合名称
        tt_area: 扭转箍筋面积/单位长度
        error_summary: 错误信息
        warning_summary: 警告信息
    """
    frame_name: str
    location: float
    top_combo: str
    top_area: float
    bot_combo: str
    bot_area: float
    vmajor_combo: str
    vmajor_area: float
    tl_combo: str = ""
    tl_area: float = 0.0
    tt_combo: str = ""
    tt_area: float = 0.0
    error_summary: str = ""
    warning_summary: str = ""


@dataclass
class ConcreteColumnResult:
    """混凝土柱设计汇总结果
    
    Attributes:
        frame_name: 框架对象名称
        design_option: 设计选项（验算/设计）
        location: 距 I 端的距离
        pmm_combo: 控制 PMM 的组合名称
        pmm_area: PMM 纵筋面积（design_option=DESIGN 时有效）
        pmm_ratio: PMM 应力比（design_option=CHECK 时有效）
        vmajor_combo: 控制主剪力的组合名称
        av_major: 主剪力箍筋面积/单位长度
        vminor_combo: 控制次剪力的组合名称
        av_minor: 次剪力箍筋面积/单位长度
        error_summary: 错误信息
        warning_summary: 警告信息
    """
    frame_name: str
    design_option: ColumnDesignOption
    location: float
    pmm_combo: str
    pmm_area: float
    pmm_ratio: float
    vmajor_combo: str
    av_major: float
    vminor_combo: str
    av_minor: float
    error_summary: str = ""
    warning_summary: str = ""
    
    @property
    def passed(self) -> bool:
        """验算模式下是否通过（应力比 <= 1.0）"""
        if self.design_option == ColumnDesignOption.CHECK:
            return self.pmm_ratio <= 1.0
        return True


@dataclass
class ConcreteJointResult:
    """混凝土节点设计汇总结果
    
    Attributes:
        frame_name: 框架对象名称
        js_ratio_major_combo: 主轴节点剪力比控制组合
        js_ratio_major: 主轴节点剪力比
        js_ratio_minor_combo: 次轴节点剪力比控制组合
        js_ratio_minor: 次轴节点剪力比
        bcc_ratio_major_combo: 主轴梁柱承载力比控制组合
        bcc_ratio_major: 主轴梁柱承载力比
        bcc_ratio_minor_combo: 次轴梁柱承载力比控制组合
        bcc_ratio_minor: 次轴梁柱承载力比
        error_summary: 错误信息
        warning_summary: 警告信息
    """
    frame_name: str
    js_ratio_major_combo: str
    js_ratio_major: float
    js_ratio_minor_combo: str
    js_ratio_minor: float
    bcc_ratio_major_combo: str
    bcc_ratio_major: float
    bcc_ratio_minor_combo: str
    bcc_ratio_minor: float
    error_summary: str = ""
    warning_summary: str = ""
