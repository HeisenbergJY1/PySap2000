# -*- coding: utf-8 -*-
"""
load_pattern.py - 荷载模式定义

对应 SAP2000 的 LoadPatterns API

荷载模式是定义荷载的基础，如 DEAD（恒载）、LIVE（活载）等。
每个荷载模式可以自动创建对应的线性静力荷载工况。

SAP2000 API:
- LoadPatterns.Add - 添加荷载模式
- LoadPatterns.ChangeName - 重命名荷载模式
- LoadPatterns.Count - 获取荷载模式数量
- LoadPatterns.Delete - 删除荷载模式
- LoadPatterns.GetLoadType - 获取荷载类型
- LoadPatterns.GetNameList - 获取所有荷载模式名称
- LoadPatterns.GetSelfWtMultiplier - 获取自重系数
- LoadPatterns.SetLoadType - 设置荷载类型
- LoadPatterns.SetSelfWtMultiplier - 设置自重系数

Usage:
    from PySap2000.loading import LoadPattern, LoadPatternType
    
    # 创建荷载模式
    dead = LoadPattern(
        name="DEAD",
        load_type=LoadPatternType.DEAD,
        self_weight_multiplier=1.0
    )
    dead._create(model)
    
    # 获取荷载模式
    lp = LoadPattern.get_by_name(model, "DEAD")
    print(f"Type: {lp.load_type.name}, SW: {lp.self_weight_multiplier}")
    
    # 获取所有荷载模式
    all_patterns = LoadPattern.get_all(model)
"""

from dataclasses import dataclass
from typing import List, Optional, ClassVar, Union
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class LoadPatternType(IntEnum):
    """
    荷载模式类型
    
    对应 SAP2000 的 eLoadPatternType 枚举
    """
    DEAD = 1                        # 恒载
    SUPERDEAD = 2                   # 超恒载
    LIVE = 3                        # 活载
    REDUCELIVE = 4                  # 可折减活载
    QUAKE = 5                       # 地震
    WIND = 6                        # 风载
    SNOW = 7                        # 雪载
    OTHER = 8                       # 其他
    MOVE = 9                        # 移动荷载
    TEMPERATURE = 10                # 温度
    ROOFLIVE = 11                   # 屋面活载
    NOTIONAL = 12                   # 名义荷载
    PATTERNLIVE = 13                # 模式活载
    WAVE = 14                       # 波浪
    BRAKING = 15                    # 制动力
    CENTRIFUGAL = 16                # 离心力
    FRICTION = 17                   # 摩擦力
    ICE = 18                        # 冰载
    WINDONLIVELOAD = 19             # 活载上的风
    HORIZONTALEARTHPRESSURE = 20    # 水平土压力
    VERTICALEARTHPRESSURE = 21      # 垂直土压力
    EARTHSURCHARGE = 22             # 土超载
    DOWNDRAG = 23                   # 下拉力
    VEHICLECOLLISION = 24           # 车辆碰撞
    VESSELCOLLISION = 25            # 船舶碰撞
    TEMPERATUREGRADIENT = 26        # 温度梯度
    SETTLEMENT = 27                 # 沉降
    SHRINKAGE = 28                  # 收缩
    CREEP = 29                      # 徐变
    WATERLOADPRESSURE = 30          # 水压力
    LIVELOADSURCHARGE = 31          # 活载超载
    LOCKEDINFORCES = 32             # 锁定力
    PEDESTRIANLL = 33               # 人行活载
    PRESTRESS = 34                  # 预应力
    HYPERSTATIC = 35                # 超静定
    BOUYANCY = 36                   # 浮力
    STREAMFLOW = 37                 # 水流
    IMPACT = 38                     # 冲击
    CONSTRUCTION = 39               # 施工


@dataclass
class LoadPattern:
    """
    荷载模式定义
    
    对应 SAP2000 的 LoadPatterns
    
    Attributes:
        name: 荷载模式名称
        load_type: 荷载类型 (LoadPatternType)
        self_weight_multiplier: 自重系数
        add_load_case: 创建时是否自动创建对应的线性静力工况
    """
    name: str = ""
    load_type: LoadPatternType = LoadPatternType.OTHER
    self_weight_multiplier: float = 0.0
    add_load_case: bool = True
    
    _object_type: ClassVar[str] = "LoadPatterns"
    
    def _create(self, model) -> int:
        """
        创建荷载模式
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功，-1 表示已存在
        """
        # 检查是否已存在
        if self.name:
            try:
                existing = self.get_name_list(model)
                if self.name in existing:
                    return -1
            except Exception:
                pass
        
        result = model.LoadPatterns.Add(
            self.name,
            int(self.load_type),
            self.self_weight_multiplier,
            self.add_load_case
        )
        return com_ret(result)
    
    def _get(self, model) -> int:
        """
        从模型获取荷载模式数据
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
        """
        # 获取荷载类型
        result = model.LoadPatterns.GetLoadType(self.name, 0)
        try:
            self.load_type = LoadPatternType(com_data(result, 0, 0))
        except ValueError:
            self.load_type = LoadPatternType.OTHER
        ret1 = com_ret(result)
        
        # 获取自重系数
        result = model.LoadPatterns.GetSelfWtMultiplier(self.name, 0.0)
        self.self_weight_multiplier = com_data(result, 0, 0.0)
        ret2 = com_ret(result)
        
        return 0 if ret1 == 0 and ret2 == 0 else -1
    
    def _delete(self, model) -> int:
        """
        删除荷载模式
        
        注意: 不能删除被荷载工况引用的荷载模式，也不能删除唯一的荷载模式
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
        """
        return model.LoadPatterns.Delete(self.name)
    
    def change_name(self, model, new_name: str) -> int:
        """
        重命名荷载模式
        
        Args:
            model: SapModel 对象
            new_name: 新名称
            
        Returns:
            0 表示成功
        """
        ret = model.LoadPatterns.ChangeName(self.name, new_name)
        if ret == 0:
            self.name = new_name
        return ret
    
    def set_load_type(self, model, load_type: LoadPatternType) -> int:
        """
        设置荷载类型
        
        Args:
            model: SapModel 对象
            load_type: 荷载类型
            
        Returns:
            0 表示成功
        """
        ret = model.LoadPatterns.SetLoadType(self.name, int(load_type))
        if ret == 0:
            self.load_type = load_type
        return ret
    
    def set_self_weight_multiplier(self, model, multiplier: float) -> int:
        """
        设置自重系数
        
        Args:
            model: SapModel 对象
            multiplier: 自重系数
            
        Returns:
            0 表示成功
        """
        ret = model.LoadPatterns.SetSelfWtMultiplier(self.name, multiplier)
        if ret == 0:
            self.self_weight_multiplier = multiplier
        return ret
    
    @staticmethod
    def get_count(model) -> int:
        """
        获取荷载模式数量
        
        Args:
            model: SapModel 对象
            
        Returns:
            荷载模式数量
        """
        return model.LoadPatterns.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """
        获取所有荷载模式名称
        
        Args:
            model: SapModel 对象
            
        Returns:
            荷载模式名称列表
        """
        result = model.LoadPatterns.GetNameList(0, [])
        names = com_data(result, 1)
        if names:
            return list(names)
        return []
    
    @classmethod
    def get_by_name(cls, model, name: str) -> Optional["LoadPattern"]:
        """
        按名称获取荷载模式
        
        Args:
            model: SapModel 对象
            name: 荷载模式名称
            
        Returns:
            LoadPattern 对象，如果不存在返回 None
        """
        lp = cls(name=name)
        ret = lp._get(model)
        if ret == 0:
            return lp
        return None
    
    @classmethod
    def get_all(cls, model) -> List["LoadPattern"]:
        """
        获取所有荷载模式
        
        Args:
            model: SapModel 对象
            
        Returns:
            LoadPattern 对象列表
        """
        names = cls.get_name_list(model)
        result = []
        for name in names:
            lp = cls.get_by_name(model, name)
            if lp:
                result.append(lp)
        return result
