# -*- coding: utf-8 -*-
"""
area_modifier.py - 命名面单元刚度修改器

对应 SAP2000 的 NamedAssign.ModifierArea API

创建可复用的面单元刚度修改器定义，可被多个面单元引用。

SAP2000 API:
- NamedAssign.ModifierArea.ChangeName
- NamedAssign.ModifierArea.Count
- NamedAssign.ModifierArea.Delete
- NamedAssign.ModifierArea.GetModifiers
- NamedAssign.ModifierArea.GetNameList
- NamedAssign.ModifierArea.SetModifiers

修改器数组 (10个值):
- [0] f11: 膜刚度 11
- [1] f22: 膜刚度 22
- [2] f12: 膜刚度 12
- [3] m11: 弯曲刚度 11
- [4] m22: 弯曲刚度 22
- [5] m12: 弯曲刚度 12
- [6] v13: 剪切刚度 13
- [7] v23: 剪切刚度 23
- [8] mass: 质量
- [9] weight: 重量
"""

from dataclasses import dataclass
from typing import List, Optional, ClassVar
from PySap2000.com_helper import com_ret, com_data


@dataclass
class NamedAreaModifier:
    """
    命名面单元刚度修改器
    
    Attributes:
        name: 修改器名称
        f11: 膜刚度 11 修改系数
        f22: 膜刚度 22 修改系数
        f12: 膜刚度 12 修改系数
        m11: 弯曲刚度 11 修改系数
        m22: 弯曲刚度 22 修改系数
        m12: 弯曲刚度 12 修改系数
        v13: 剪切刚度 13 修改系数
        v23: 剪切刚度 23 修改系数
        mass: 质量修改系数
        weight: 重量修改系数
    """
    name: str = ""
    f11: float = 1.0
    f22: float = 1.0
    f12: float = 1.0
    m11: float = 1.0
    m22: float = 1.0
    m12: float = 1.0
    v13: float = 1.0
    v23: float = 1.0
    mass: float = 1.0
    weight: float = 1.0
    
    _object_type: ClassVar[str] = "NamedAssign.ModifierArea"
    
    def to_list(self) -> List[float]:
        """转换为 API 需要的列表格式"""
        return [
            self.f11, self.f22, self.f12,
            self.m11, self.m22, self.m12,
            self.v13, self.v23,
            self.mass, self.weight
        ]
    
    @classmethod
    def from_list(cls, name: str, values: List[float]) -> "NamedAreaModifier":
        """从 API 返回的列表创建"""
        if len(values) >= 10:
            return cls(
                name=name,
                f11=values[0], f22=values[1], f12=values[2],
                m11=values[3], m22=values[4], m12=values[5],
                v13=values[6], v23=values[7],
                mass=values[8], weight=values[9]
            )
        return cls(name=name)
    
    def _create(self, model) -> int:
        """
        创建或更新命名修改器
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
        """
        from PySap2000.com_helper import com_ret
        return com_ret(model.NamedAssign.ModifierArea.SetModifiers(
            self.name, self.to_list()
        ))
    
    def _get(self, model) -> int:
        """
        从模型获取修改器数据
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
        """
        result = model.NamedAssign.ModifierArea.GetModifiers(
            self.name, [0.0] * 10
        )
        
        values = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and values and len(values) >= 10:
            self.f11, self.f22, self.f12 = values[0], values[1], values[2]
            self.m11, self.m22, self.m12 = values[3], values[4], values[5]
            self.v13, self.v23 = values[6], values[7]
            self.mass, self.weight = values[8], values[9]
        return ret if isinstance(ret, int) else -1
    
    def _delete(self, model) -> int:
        """
        删除命名修改器
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
        """
        from PySap2000.com_helper import com_ret
        return com_ret(model.NamedAssign.ModifierArea.Delete(self.name))
    
    def change_name(self, model, new_name: str) -> int:
        """
        重命名修改器
        
        Args:
            model: SapModel 对象
            new_name: 新名称
            
        Returns:
            0 表示成功
        """
        from PySap2000.com_helper import com_ret
        ret = com_ret(model.NamedAssign.ModifierArea.ChangeName(self.name, new_name))
        if ret == 0:
            self.name = new_name
        return ret
    
    @staticmethod
    def get_count(model) -> int:
        """获取修改器数量"""
        return model.NamedAssign.ModifierArea.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """获取所有修改器名称"""
        result = model.NamedAssign.ModifierArea.GetNameList(0, [])
        names = com_data(result, 1)
        if names:
            return list(names)
        return []
    
    @classmethod
    def get_by_name(cls, model, name: str) -> Optional["NamedAreaModifier"]:
        """按名称获取修改器"""
        mod = cls(name=name)
        ret = mod._get(model)
        if ret == 0:
            return mod
        return None
    
    @classmethod
    def get_all(cls, model) -> List["NamedAreaModifier"]:
        """获取所有修改器"""
        names = cls.get_name_list(model)
        result = []
        for name in names:
            mod = cls.get_by_name(model, name)
            if mod:
                result.append(mod)
        return result
