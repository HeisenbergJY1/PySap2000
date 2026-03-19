# -*- coding: utf-8 -*-
"""
model_settings.py - 模型设置
包含自由度、合并容差、坐标系统等模型级设置

API Reference:
    - Analyze.GetActiveDOF(DOF[]) -> Long
    - Analyze.SetActiveDOF(DOF[]) -> Long
    - GetMergeTol(MergeTol) -> Long
    - SetMergeTol(MergeTol) -> Long
    - GetPresentCoordSystem() -> String
    - SetPresentCoordSystem(CSys) -> Long

Usage:
    from PySap2000.global_parameters import ModelSettings, ActiveDOF
    
    # 获取活动自由度
    dof = ModelSettings.get_active_dof(model)
    
    # 设置为2D平面问题 (UX, UZ, RY)
    ModelSettings.set_active_dof(model, ActiveDOF.XZ_PLANE)
    
    # 设置合并容差
    ModelSettings.set_merge_tolerance(model, 0.01)
"""

from dataclasses import dataclass
from typing import Tuple, List
from enum import IntEnum
from PySap2000.com_helper import com_ret, com_data


class ActiveDOF(IntEnum):
    """
    预设自由度配置
    """
    FULL_3D = 0          # 完整3D (UX, UY, UZ, RX, RY, RZ)
    XZ_PLANE = 1         # XZ平面 (UX, UZ, RY)
    XY_PLANE = 2         # XY平面 (UX, UY, RZ)
    SPACE_TRUSS = 3      # 空间桁架 (UX, UY, UZ)
    PLANE_TRUSS_XZ = 4   # 平面桁架XZ (UX, UZ)
    PLANE_TRUSS_XY = 5   # 平面桁架XY (UX, UY)
    GRID = 6             # 网格 (UZ, RX, RY)


# 预设自由度配置映射
DOF_PRESETS = {
    ActiveDOF.FULL_3D: (True, True, True, True, True, True),
    ActiveDOF.XZ_PLANE: (True, False, True, False, True, False),
    ActiveDOF.XY_PLANE: (True, True, False, False, False, True),
    ActiveDOF.SPACE_TRUSS: (True, True, True, False, False, False),
    ActiveDOF.PLANE_TRUSS_XZ: (True, False, True, False, False, False),
    ActiveDOF.PLANE_TRUSS_XY: (True, True, False, False, False, False),
    ActiveDOF.GRID: (False, False, True, True, True, False),
}


@dataclass
class DOFState:
    """
    自由度状态
    
    Attributes:
        ux: X方向平动
        uy: Y方向平动
        uz: Z方向平动
        rx: 绕X轴转动
        ry: 绕Y轴转动
        rz: 绕Z轴转动
    """
    ux: bool = True
    uy: bool = True
    uz: bool = True
    rx: bool = True
    ry: bool = True
    rz: bool = True
    
    def to_tuple(self) -> Tuple[bool, ...]:
        """转换为元组"""
        return (self.ux, self.uy, self.uz, self.rx, self.ry, self.rz)
    
    def to_list(self) -> List[bool]:
        """转换为列表"""
        return [self.ux, self.uy, self.uz, self.rx, self.ry, self.rz]
    
    @classmethod
    def from_tuple(cls, dof: Tuple[bool, ...]) -> 'DOFState':
        """从元组创建"""
        return cls(
            ux=dof[0] if len(dof) > 0 else True,
            uy=dof[1] if len(dof) > 1 else True,
            uz=dof[2] if len(dof) > 2 else True,
            rx=dof[3] if len(dof) > 3 else True,
            ry=dof[4] if len(dof) > 4 else True,
            rz=dof[5] if len(dof) > 5 else True,
        )
    
    @classmethod
    def from_preset(cls, preset: ActiveDOF) -> 'DOFState':
        """从预设创建"""
        dof = DOF_PRESETS.get(preset, (True,) * 6)
        return cls.from_tuple(dof)


class ModelSettings:
    """
    模型设置管理类
    
    提供模型级设置的静态方法
    """
    
    # ==================== 自由度设置 ====================
    
    @staticmethod
    def get_active_dof(model) -> DOFState:
        """
        获取活动自由度
        
        API: Analyze.GetActiveDOF(DOF[]) -> Long
        
        Returns:
            DOFState 对象
        """
        result = model.Analyze.GetActiveDOF([False]*6)
        dof = com_data(result, 0, None)
        if dof and len(dof) >= 6:
            return DOFState.from_tuple(tuple(dof))
        return DOFState()
    
    @staticmethod
    def set_active_dof(
        model, 
        dof: ActiveDOF = None,
        custom_dof: Tuple[bool, ...] = None
    ) -> int:
        """
        设置活动自由度
        
        API: Analyze.SetActiveDOF(DOF[]) -> Long
        
        Args:
            model: SapModel 对象
            dof: 预设自由度配置
            custom_dof: 自定义自由度 (UX, UY, UZ, RX, RY, RZ)
            
        Returns:
            0 表示成功
        """
        if custom_dof is not None:
            dof_list = list(custom_dof)
            if len(dof_list) < 6:
                dof_list.extend([False] * (6 - len(dof_list)))
        elif dof is not None:
            dof_list = list(DOF_PRESETS.get(dof, (True,) * 6))
        else:
            dof_list = [True] * 6
        
        result = model.Analyze.SetActiveDOF(dof_list)
        return com_ret(result)
    
    @staticmethod
    def set_2d_xz_plane(model) -> int:
        """设置为XZ平面2D分析"""
        return ModelSettings.set_active_dof(model, ActiveDOF.XZ_PLANE)
    
    @staticmethod
    def set_2d_xy_plane(model) -> int:
        """设置为XY平面2D分析"""
        return ModelSettings.set_active_dof(model, ActiveDOF.XY_PLANE)
    
    @staticmethod
    def set_3d_full(model) -> int:
        """设置为完整3D分析"""
        return ModelSettings.set_active_dof(model, ActiveDOF.FULL_3D)
    
    # ==================== 合并容差 ====================
    
    @staticmethod
    def get_merge_tolerance(model) -> float:
        """
        获取自动合并容差
        
        API: GetMergeTol(MergeTol) -> Long
        
        Returns:
            合并容差 [L]
        """
        result = model.GetMergeTol(0.0)
        val = com_data(result, 0, None)
        if val is not None:
            return val
        return result if isinstance(result, float) else 0.0
    
    @staticmethod
    def set_merge_tolerance(model, tolerance: float) -> int:
        """
        设置自动合并容差
        
        API: SetMergeTol(MergeTol) -> Long
        
        Args:
            model: SapModel 对象
            tolerance: 合并容差 [L]
            
        Returns:
            0 表示成功
        """
        return model.SetMergeTol(tolerance)
    
    # ==================== 坐标系统 ====================
    
    @staticmethod
    def get_present_coord_system(model) -> str:
        """
        获取当前坐标系统
        
        API: GetPresentCoordSystem() -> String
        
        Returns:
            坐标系统名称
        """
        return model.GetPresentCoordSystem()
    
    @staticmethod
    def set_present_coord_system(model, csys: str) -> int:
        """
        设置当前坐标系统
        
        API: SetPresentCoordSystem(CSys) -> Long
        
        Args:
            model: SapModel 对象
            csys: 坐标系统名称
            
        Returns:
            0 表示成功
        """
        return model.SetPresentCoordSystem(csys)
    
    # ==================== 模型锁定 ====================
    
    @staticmethod
    def is_model_locked(model) -> bool:
        """
        检查模型是否锁定
        
        API: GetModelIsLocked() -> Boolean
        """
        return model.GetModelIsLocked()
    
    @staticmethod
    def set_model_locked(model, locked: bool) -> int:
        """
        设置模型锁定状态
        
        API: SetModelIsLocked(Locked) -> Long
        """
        return model.SetModelIsLocked(locked)
    
    @staticmethod
    def unlock_model(model) -> int:
        """解锁模型"""
        return ModelSettings.set_model_locked(model, False)
    
    @staticmethod
    def lock_model(model) -> int:
        """锁定模型"""
        return ModelSettings.set_model_locked(model, True)
    
    # ==================== 模型文件信息 ====================
    
    @staticmethod
    def get_model_filename(model) -> str:
        """
        获取模型文件名
        
        API: GetModelFilename() -> String
        """
        return model.GetModelFilename()
    
    @staticmethod
    def get_model_filepath(model) -> str:
        """
        获取模型文件路径
        
        API: GetModelFilepath() -> String
        """
        return model.GetModelFilepath()
