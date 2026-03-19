# -*- coding: utf-8 -*-
"""
load_case.py - 荷载工况定义

对应 SAP2000 的 LoadCases API

荷载工况（Load Case）是分析工况，定义了如何分析结构。
每种工况类型有不同的子类型和参数设置。

SAP2000 API 结构:
- LoadCases (基础 API)
  - ChangeName, Count, Delete, GetNameList_1, GetTypeOAPI_2, SetDesignType
- LoadCases.StaticLinear (线性静力)
- LoadCases.StaticNonlinear (非线性静力)
- LoadCases.ModalEigen (特征值模态)
- LoadCases.ModalRitz (Ritz 模态)
- LoadCases.ResponseSpectrum (反应谱)
- LoadCases.DirHistLinear (直接积分线性时程)
- LoadCases.DirHistNonlinear (直接积分非线性时程)
- LoadCases.ModHistLinear (模态线性时程)
- LoadCases.ModHistNonlinear (模态非线性时程)
- LoadCases.Buckling (屈曲)
- LoadCases.SteadyState (稳态)
- LoadCases.PSD (功率谱密度)
- LoadCases.MovingLoad (移动荷载)
- LoadCases.Hyperstatic (超静定)
- LoadCases.StaticLinearMultistep (多步线性静力)
- LoadCases.StaticNonlinearMultistep (多步非线性静力)
- LoadCases.StaticNonlinearStaged (分阶段施工)

Usage:
    from PySap2000.loading import LoadCase, LoadCaseType
    
    # 获取所有荷载工况
    all_cases = LoadCase.get_all(model)
    
    # 按类型获取
    static_cases = LoadCase.get_name_list(model, LoadCaseType.LINEAR_STATIC)
    
    # 获取工况信息
    case = LoadCase.get_by_name(model, "DEAD")
    print(f"Type: {case.case_type.name}")
"""

from dataclasses import dataclass, field
from typing import List, Optional, ClassVar, Union, Tuple
from enum import IntEnum

from .load_pattern import LoadPatternType
from PySap2000.com_helper import com_ret, com_data


class LoadCaseType(IntEnum):
    """
    荷载工况类型
    
    对应 SAP2000 的 eLoadCaseType 枚举
    """
    LINEAR_STATIC = 1               # 线性静力
    NONLINEAR_STATIC = 2            # 非线性静力
    MODAL = 3                       # 模态
    RESPONSE_SPECTRUM = 4           # 反应谱
    LINEAR_HISTORY = 5              # 模态线性时程
    NONLINEAR_HISTORY = 6           # 模态非线性时程
    LINEAR_DYNAMIC = 7              # 直接积分线性时程
    NONLINEAR_DYNAMIC = 8           # 直接积分非线性时程
    MOVING_LOAD = 9                 # 移动荷载
    BUCKLING = 10                   # 屈曲
    STEADY_STATE = 11               # 稳态
    POWER_SPECTRAL_DENSITY = 12     # 功率谱密度
    LINEAR_STATIC_MULTISTEP = 13    # 多步线性静力
    HYPERSTATIC = 14                # 超静定
    EXTERNAL_RESULTS = 15           # 外部结果
    STAGED_CONSTRUCTION = 16        # 分阶段施工
    NONLINEAR_STATIC_MULTISTEP = 17 # 多步非线性静力


class ModalSubType(IntEnum):
    """
    模态工况子类型
    
    仅适用于 LoadCaseType.MODAL
    """
    EIGEN = 1   # 特征值模态
    RITZ = 2    # Ritz 模态


class TimeHistorySubType(IntEnum):
    """
    时程工况子类型
    
    仅适用于 LoadCaseType.LINEAR_HISTORY
    """
    TRANSIENT = 1   # 瞬态
    PERIODIC = 2    # 周期


class DesignTypeOption(IntEnum):
    """
    设计类型选项
    """
    PROGRAM_DETERMINED = 0  # 程序自动确定
    USER_SPECIFIED = 1      # 用户指定


@dataclass
class LoadCaseLoad:
    """
    荷载工况中的单个荷载定义
    
    用于 StaticLinear 等工况的荷载设置
    
    Attributes:
        load_type: "Load" (荷载模式) 或 "Accel" (加速度)
        load_name: 荷载模式名称 或 方向 (UX, UY, UZ, RX, RY, RZ)
        scale_factor: 比例系数
    """
    load_type: str = "Load"     # "Load" or "Accel"
    load_name: str = ""         # Pattern name or direction
    scale_factor: float = 1.0


@dataclass
class LoadCase:
    """
    荷载工况定义
    
    对应 SAP2000 的 LoadCases
    
    这是一个基础类，提供所有工况类型的通用操作。
    具体工况类型的详细设置需要通过对应的子 API 进行。
    
    Attributes:
        name: 工况名称
        case_type: 工况类型 (LoadCaseType)
        sub_type: 子类型 (仅 Modal 和 LinearHistory 有效)
        design_type: 设计类型 (LoadPatternType)
        design_type_option: 设计类型选项
        is_auto: 是否自动创建
    """
    name: str = ""
    case_type: LoadCaseType = LoadCaseType.LINEAR_STATIC
    sub_type: int = 0
    design_type: LoadPatternType = LoadPatternType.DEAD
    design_type_option: DesignTypeOption = DesignTypeOption.PROGRAM_DETERMINED
    is_auto: bool = False
    
    _object_type: ClassVar[str] = "LoadCases"

    
    def _get(self, model) -> int:
        """
        从模型获取荷载工况数据
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
        """
        result = model.LoadCases.GetTypeOAPI_2(
            self.name, 0, 0, 0, 0, 0
        )
        
        try:
            self.case_type = LoadCaseType(com_data(result, 0, 1))
        except ValueError:
            self.case_type = LoadCaseType.LINEAR_STATIC
        
        self.sub_type = com_data(result, 1, 0)
        
        try:
            self.design_type = LoadPatternType(com_data(result, 2, 8))
        except ValueError:
            self.design_type = LoadPatternType.OTHER
        
        try:
            self.design_type_option = DesignTypeOption(com_data(result, 3, 0))
        except ValueError:
            self.design_type_option = DesignTypeOption.PROGRAM_DETERMINED
        
        self.is_auto = bool(com_data(result, 4, False))
        ret = com_ret(result)
        
        return ret
    
    def _delete(self, model) -> int:
        """
        删除荷载工况
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
        """
        return model.LoadCases.Delete(self.name)
    
    def change_name(self, model, new_name: str) -> int:
        """
        重命名荷载工况
        
        Args:
            model: SapModel 对象
            new_name: 新名称
            
        Returns:
            0 表示成功
        """
        ret = model.LoadCases.ChangeName(self.name, new_name)
        if ret == 0:
            self.name = new_name
        return ret
    
    def set_design_type(
        self, 
        model, 
        design_type_option: DesignTypeOption,
        design_type: LoadPatternType = LoadPatternType.DEAD
    ) -> int:
        """
        设置设计类型
        
        Args:
            model: SapModel 对象
            design_type_option: 设计类型选项 (程序确定/用户指定)
            design_type: 设计类型 (仅当 design_type_option=USER_SPECIFIED 时有效)
            
        Returns:
            0 表示成功
        """
        ret = model.LoadCases.SetDesignType(
            self.name,
            int(design_type_option),
            int(design_type)
        )
        if ret == 0:
            self.design_type_option = design_type_option
            if design_type_option == DesignTypeOption.USER_SPECIFIED:
                self.design_type = design_type
        return ret
    
    @staticmethod
    def get_count(model, case_type: Optional[LoadCaseType] = None) -> int:
        """
        获取荷载工况数量
        
        Args:
            model: SapModel 对象
            case_type: 工况类型 (可选，不指定则返回所有类型的总数)
            
        Returns:
            荷载工况数量
        """
        if case_type is None:
            return model.LoadCases.Count()
        else:
            return model.LoadCases.Count(int(case_type))
    
    @staticmethod
    def get_name_list(
        model, 
        case_type: Optional[LoadCaseType] = None
    ) -> List[str]:
        """
        获取荷载工况名称列表
        
        Args:
            model: SapModel 对象
            case_type: 工况类型 (可选，不指定则返回所有类型)
            
        Returns:
            荷载工况名称列表
        """
        if case_type is None:
            result = model.LoadCases.GetNameList_1(0, [])
        else:
            result = model.LoadCases.GetNameList_1(0, [], int(case_type))
        
        names = com_data(result, 1)
        if names:
            return list(names)
        return []
    
    @classmethod
    def get_by_name(cls, model, name: str) -> Optional["LoadCase"]:
        """
        按名称获取荷载工况
        
        Args:
            model: SapModel 对象
            name: 工况名称
            
        Returns:
            LoadCase 对象，如果不存在返回 None
        """
        case = cls(name=name)
        ret = case._get(model)
        if ret == 0:
            return case
        return None
    
    @classmethod
    def get_all(
        cls, 
        model, 
        case_type: Optional[LoadCaseType] = None
    ) -> List["LoadCase"]:
        """
        获取所有荷载工况
        
        Args:
            model: SapModel 对象
            case_type: 工况类型 (可选，不指定则返回所有类型)
            
        Returns:
            LoadCase 对象列表
        """
        names = cls.get_name_list(model, case_type)
        result = []
        for name in names:
            case = cls.get_by_name(model, name)
            if case:
                result.append(case)
        return result
    
    def get_modal_sub_type(self) -> Optional[ModalSubType]:
        """
        获取模态子类型
        
        仅当 case_type == MODAL 时有效
        
        Returns:
            ModalSubType 或 None
        """
        if self.case_type == LoadCaseType.MODAL and self.sub_type in (1, 2):
            return ModalSubType(self.sub_type)
        return None
    
    def get_time_history_sub_type(self) -> Optional[TimeHistorySubType]:
        """
        获取时程子类型
        
        仅当 case_type == LINEAR_HISTORY 时有效
        
        Returns:
            TimeHistorySubType 或 None
        """
        if self.case_type == LoadCaseType.LINEAR_HISTORY and self.sub_type in (1, 2):
            return TimeHistorySubType(self.sub_type)
        return None


# =============================================================================
# 静力工况创建函数
# =============================================================================

def create_static_linear_case(model, name: str) -> int:
    """
    创建线性静力工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.StaticLinear.SetCase(name)


def create_static_nonlinear_case(model, name: str) -> int:
    """
    创建非线性静力工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.StaticNonlinear.SetCase(name)


# =============================================================================
# 模态工况创建函数
# =============================================================================

def create_modal_eigen_case(model, name: str) -> int:
    """
    创建特征值模态工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.ModalEigen.SetCase(name)


def create_modal_ritz_case(model, name: str) -> int:
    """
    创建 Ritz 模态工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.ModalRitz.SetCase(name)


# =============================================================================
# 动力工况创建函数
# =============================================================================

def create_response_spectrum_case(model, name: str) -> int:
    """
    创建反应谱工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.ResponseSpectrum.SetCase(name)


def create_buckling_case(model, name: str) -> int:
    """
    创建屈曲工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.Buckling.SetCase(name)


# =============================================================================
# 时程工况创建函数
# =============================================================================

def create_direct_history_linear_case(model, name: str) -> int:
    """
    创建直接积分线性时程工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.DirHistLinear.SetCase(name)


def create_direct_history_nonlinear_case(model, name: str) -> int:
    """
    创建直接积分非线性时程工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.DirHistNonlinear.SetCase(name)


def create_modal_history_linear_case(model, name: str) -> int:
    """
    创建模态线性时程工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.ModHistLinear.SetCase(name)


def create_modal_history_nonlinear_case(model, name: str) -> int:
    """
    创建模态非线性时程工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.ModHistNonlinear.SetCase(name)


# =============================================================================
# 其他工况创建函数
# =============================================================================

def create_steady_state_case(model, name: str) -> int:
    """
    创建稳态工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.SteadyState.SetCase(name)


def create_psd_case(model, name: str) -> int:
    """
    创建功率谱密度工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.PSD.SetCase(name)


def create_moving_load_case(model, name: str) -> int:
    """
    创建移动荷载工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.MovingLoad.SetCase(name)


def create_hyperstatic_case(model, name: str) -> int:
    """
    创建超静定工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.Hyperstatic.SetCase(name)


# =============================================================================
# 多步工况创建函数
# =============================================================================

def create_static_linear_multistep_case(model, name: str) -> int:
    """
    创建多步线性静力工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.StaticLinearMultistep.SetCase(name)


def create_static_nonlinear_multistep_case(model, name: str) -> int:
    """
    创建多步非线性静力工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.StaticNonlinearMultistep.SetCase(name)


def create_staged_construction_case(model, name: str) -> int:
    """
    创建分阶段施工工况
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        0 表示成功
    """
    return model.LoadCases.StaticNonlinearStaged.SetCase(name)


# =============================================================================
# 静力工况荷载设置函数
# =============================================================================

def get_static_linear_loads(
    model, 
    name: str
) -> Tuple[List[LoadCaseLoad], int]:
    """
    获取线性静力工况的荷载数据
    
    Args:
        model: SapModel 对象
        name: 工况名称
        
    Returns:
        (荷载列表, 返回码)
    """
    result = model.LoadCases.StaticLinear.GetLoads(name, 0, [], [], [])
    
    loads = []
    num_loads = com_data(result, 0, 0)
    load_types = com_data(result, 1) or []
    load_names = com_data(result, 2) or []
    scale_factors = com_data(result, 3) or []
    ret = com_ret(result)
    
    if ret == 0 and num_loads > 0:
        for i in range(num_loads):
            load = LoadCaseLoad(
                load_type=load_types[i] if i < len(load_types) else "Load",
                load_name=load_names[i] if i < len(load_names) else "",
                scale_factor=scale_factors[i] if i < len(scale_factors) else 1.0
            )
            loads.append(load)
        return loads, ret
    
    return [], -1


def set_static_linear_loads(
    model, 
    name: str, 
    loads: List[LoadCaseLoad]
) -> int:
    """
    设置线性静力工况的荷载数据
    
    Args:
        model: SapModel 对象
        name: 工况名称
        loads: 荷载列表
        
    Returns:
        0 表示成功
    """
    if not loads:
        return -1
    
    num_loads = len(loads)
    load_types = [load.load_type for load in loads]
    load_names = [load.load_name for load in loads]
    scale_factors = [load.scale_factor for load in loads]
    
    return model.LoadCases.StaticLinear.SetLoads(
        name, num_loads, load_types, load_names, scale_factors
    )
