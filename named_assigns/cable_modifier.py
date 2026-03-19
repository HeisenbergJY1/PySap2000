# -*- coding: utf-8 -*-
"""
cable_modifier.py - 命名索单元修改器

对应 SAP2000 的 NamedAssign.ModifierCable API

创建可复用的索单元修改器定义，可被多个索单元引用。

SAP2000 API:
- NamedAssign.ModifierCable.ChangeName
- NamedAssign.ModifierCable.Count
- NamedAssign.ModifierCable.Delete
- NamedAssign.ModifierCable.GetModifiers
- NamedAssign.ModifierCable.GetNameList
- NamedAssign.ModifierCable.SetModifiers

修改器数组 (3个值):
- [0] area: 截面面积
- [1] mass: 质量
- [2] weight: 重量
"""

from dataclasses import dataclass
from typing import List, Optional, ClassVar
from PySap2000.com_helper import com_ret, com_data


@dataclass
class NamedCableModifier:
    """
    命名索单元修改器
    
    Attributes:
        name: 修改器名称
        area: 截面面积修改系数
        mass: 质量修改系数
        weight: 重量修改系数
    """
    name: str = ""
    area: float = 1.0
    mass: float = 1.0
    weight: float = 1.0
    
    _object_type: ClassVar[str] = "NamedAssign.ModifierCable"
    
    def to_list(self) -> List[float]:
        """转换为 API 需要的列表格式"""
        return [self.area, self.mass, self.weight]
    
    @classmethod
    def from_list(cls, name: str, values: List[float]) -> "NamedCableModifier":
        """从 API 返回的列表创建"""
        if len(values) >= 3:
            return cls(
                name=name,
                area=values[0], mass=values[1], weight=values[2]
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
        return com_ret(model.NamedAssign.ModifierCable.SetModifiers(
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
        result = model.NamedAssign.ModifierCable.GetModifiers(
            self.name, [0.0] * 3
        )
        
        values = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and values and len(values) >= 3:
            self.area = values[0]
            self.mass = values[1]
            self.weight = values[2]
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
        return com_ret(model.NamedAssign.ModifierCable.Delete(self.name))
    
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
        ret = com_ret(model.NamedAssign.ModifierCable.ChangeName(self.name, new_name))
        if ret == 0:
            self.name = new_name
        return ret
    
    @staticmethod
    def get_count(model) -> int:
        """获取修改器数量"""
        return model.NamedAssign.ModifierCable.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """获取所有修改器名称"""
        result = model.NamedAssign.ModifierCable.GetNameList(0, [])
        names = com_data(result, 1)
        if names:
            return list(names)
        return []
    
    @classmethod
    def get_by_name(cls, model, name: str) -> Optional["NamedCableModifier"]:
        """按名称获取修改器"""
        mod = cls(name=name)
        ret = mod._get(model)
        if ret == 0:
            return mod
        return None
    
    @classmethod
    def get_all(cls, model) -> List["NamedCableModifier"]:
        """获取所有修改器"""
        names = cls.get_name_list(model)
        result = []
        for name in names:
            mod = cls.get_by_name(model, name)
            if mod:
                result.append(mod)
        return result
