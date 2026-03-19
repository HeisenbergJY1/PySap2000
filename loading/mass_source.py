# -*- coding: utf-8 -*-
"""
mass_source.py - 质量源定义

对应 SAP2000 的 SourceMass API

质量源用于定义动力分析中的质量来源，可以包括：
- 单元自重 (MassFromElements)
- 指定质量 (MassFromMasses)
- 荷载模式 (MassFromLoads)

SAP2000 API:
- SourceMass.SetMassSource - 创建/修改质量源
- SourceMass.GetMassSource - 获取质量源数据
- SourceMass.GetNameList - 获取所有质量源名称
- SourceMass.Count - 获取质量源数量
- SourceMass.ChangeName - 重命名质量源
- SourceMass.Delete - 删除质量源
- SourceMass.GetDefault - 获取默认质量源
- SourceMass.SetDefault - 设置默认质量源

Usage:
    from PySap2000.loading import MassSource, MassSourceLoad
    
    # 创建质量源
    ms = MassSource(
        name="MyMassSource",
        mass_from_elements=True,
        mass_from_masses=True,
        mass_from_loads=True,
        is_default=True,
        loads=[MassSourceLoad("DEAD", 1.0), MassSourceLoad("SDL", 0.5)]
    )
    ms._create(model)
    
    # 获取质量源
    ms = MassSource.get_by_name(model, "MSSSRC1")
    
    # 获取默认质量源
    default_name = MassSource.get_default_name(model)
"""

from dataclasses import dataclass, field
from typing import List, Optional, ClassVar, Union

from PySap2000.com_helper import com_ret, com_data


@dataclass
class MassSourceLoad:
    """
    质量源中的荷载模式定义
    
    Attributes:
        load_pattern: 荷载模式名称
        scale_factor: 比例系数
    """
    load_pattern: str
    scale_factor: float = 1.0


@dataclass
class MassSource:
    """
    质量源定义
    
    用于定义动力分析中的质量来源
    
    Attributes:
        name: 质量源名称
        mass_from_elements: 是否包含单元自重
        mass_from_masses: 是否包含指定质量
        mass_from_loads: 是否包含荷载模式
        is_default: 是否为默认质量源
        loads: 荷载模式列表 (仅当 mass_from_loads=True 时有效)
    """
    name: str = ""
    mass_from_elements: bool = True
    mass_from_masses: bool = True
    mass_from_loads: bool = False
    is_default: bool = False
    loads: List[MassSourceLoad] = field(default_factory=list)
    
    _object_type: ClassVar[str] = "SourceMass"
    
    def _create(self, model) -> int:
        """
        创建或修改质量源
        
        如果同名质量源已存在，则会被覆盖
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
        """
        num_loads = len(self.loads)
        load_patterns = [ld.load_pattern for ld in self.loads] if self.loads else []
        scale_factors = [ld.scale_factor for ld in self.loads] if self.loads else []
        
        return model.SourceMass.SetMassSource(
            self.name,
            self.mass_from_elements,
            self.mass_from_masses,
            self.mass_from_loads,
            self.is_default,
            num_loads,
            load_patterns,
            scale_factors
        )
    
    def _get(self, model) -> int:
        """
        从模型获取质量源数据
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
        """
        result = model.SourceMass.GetMassSource(
            self.name, False, False, False, False, 0, [], []
        )
        
        self.mass_from_elements = com_data(result, 0, False)
        self.mass_from_masses = com_data(result, 1, False)
        self.mass_from_loads = com_data(result, 2, False)
        self.is_default = com_data(result, 3, False)
        num_loads = com_data(result, 4, 0)
        load_patterns = com_data(result, 5) or []
        scale_factors = com_data(result, 6) or []
        ret = com_ret(result)
        
        self.loads = []
        if num_loads > 0 and load_patterns and scale_factors:
            for i in range(num_loads):
                self.loads.append(MassSourceLoad(
                    load_pattern=load_patterns[i],
                    scale_factor=scale_factors[i]
                ))
        
        return ret if ret is not None else -1
    
    def _delete(self, model) -> int:
        """
        删除质量源
        
        注意: 不能删除默认质量源
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
        """
        return model.SourceMass.Delete(self.name)
    
    def change_name(self, model, new_name: str) -> int:
        """
        重命名质量源
        
        Args:
            model: SapModel 对象
            new_name: 新名称
            
        Returns:
            0 表示成功
        """
        ret = model.SourceMass.ChangeName(self.name, new_name)
        if ret == 0:
            self.name = new_name
        return ret
    
    def set_as_default(self, model) -> int:
        """
        设置为默认质量源
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
        """
        ret = model.SourceMass.SetDefault(self.name)
        if ret == 0:
            self.is_default = True
        return ret
    
    @staticmethod
    def get_count(model) -> int:
        """
        获取质量源数量
        
        Args:
            model: SapModel 对象
            
        Returns:
            质量源数量
        """
        return model.SourceMass.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """
        获取所有质量源名称
        
        Args:
            model: SapModel 对象
            
        Returns:
            质量源名称列表
        """
        result = model.SourceMass.GetNameList(0, [])
        names = com_data(result, 1)
        if names:
            return list(names)
        return []
    
    @staticmethod
    def get_default_name(model) -> str:
        """
        获取默认质量源名称
        
        Args:
            model: SapModel 对象
            
        Returns:
            默认质量源名称
        """
        result = model.SourceMass.GetDefault("")
        name = com_data(result, 0)
        return name if name else ""
    
    @classmethod
    def get_by_name(cls, model, name: str) -> Optional["MassSource"]:
        """
        按名称获取质量源
        
        Args:
            model: SapModel 对象
            name: 质量源名称
            
        Returns:
            MassSource 对象，如果不存在返回 None
        """
        ms = cls(name=name)
        ret = ms._get(model)
        if ret == 0:
            return ms
        return None
    
    @classmethod
    def get_all(cls, model) -> List["MassSource"]:
        """
        获取所有质量源
        
        Args:
            model: SapModel 对象
            
        Returns:
            MassSource 对象列表
        """
        names = cls.get_name_list(model)
        result = []
        for name in names:
            ms = cls.get_by_name(model, name)
            if ms:
                result.append(ms)
        return result
    
    @classmethod
    def get_default(cls, model) -> Optional["MassSource"]:
        """
        获取默认质量源
        
        Args:
            model: SapModel 对象
            
        Returns:
            默认 MassSource 对象
        """
        name = cls.get_default_name(model)
        if name:
            return cls.get_by_name(model, name)
        return None
    
    def add_load(self, load_pattern: str, scale_factor: float = 1.0) -> None:
        """
        添加荷载模式到质量源
        
        Args:
            load_pattern: 荷载模式名称
            scale_factor: 比例系数
        """
        self.loads.append(MassSourceLoad(load_pattern, scale_factor))
        self.mass_from_loads = True
    
    def clear_loads(self) -> None:
        """清除所有荷载模式"""
        self.loads = []
