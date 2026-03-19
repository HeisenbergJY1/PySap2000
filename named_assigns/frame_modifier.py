# -*- coding: utf-8 -*-
"""
frame_modifier.py - 命名杆件修改器

对应 SAP2000 的 NamedAssign.ModifierFrame API

创建可复用的杆件修改器定义，可被多个杆件引用。

SAP2000 API:
- NamedAssign.ModifierFrame.ChangeName
- NamedAssign.ModifierFrame.Count
- NamedAssign.ModifierFrame.Delete
- NamedAssign.ModifierFrame.GetModifiers
- NamedAssign.ModifierFrame.GetNameList
- NamedAssign.ModifierFrame.SetModifiers

修改器数组 (8个值):
- [0] area: 截面面积 (A)
- [1] shear_2: 局部2方向剪切面积 (As2)
- [2] shear_3: 局部3方向剪切面积 (As3)
- [3] torsion: 扭转常数 (J)
- [4] inertia_22: 局部2轴惯性矩 (I22)
- [5] inertia_33: 局部3轴惯性矩 (I33)
- [6] mass: 质量
- [7] weight: 重量
"""

from dataclasses import dataclass
from typing import List, Optional, ClassVar
from PySap2000.com_helper import com_ret, com_data


@dataclass
class NamedFrameModifier:
    """
    命名杆件修改器
    
    Attributes:
        name: 修改器名称
        area: 截面面积修改系数 (A)
        shear_2: 局部2方向剪切面积修改系数 (As2)
        shear_3: 局部3方向剪切面积修改系数 (As3)
        torsion: 扭转常数修改系数 (J)
        inertia_22: 局部2轴惯性矩修改系数 (I22)
        inertia_33: 局部3轴惯性矩修改系数 (I33)
        mass: 质量修改系数
        weight: 重量修改系数
    """
    name: str = ""
    area: float = 1.0
    shear_2: float = 1.0
    shear_3: float = 1.0
    torsion: float = 1.0
    inertia_22: float = 1.0
    inertia_33: float = 1.0
    mass: float = 1.0
    weight: float = 1.0
    
    _object_type: ClassVar[str] = "NamedAssign.ModifierFrame"
    
    def to_list(self) -> List[float]:
        """转换为 API 需要的列表格式"""
        return [
            self.area, self.shear_2, self.shear_3, self.torsion,
            self.inertia_22, self.inertia_33, self.mass, self.weight
        ]
    
    @classmethod
    def from_list(cls, name: str, values: List[float]) -> "NamedFrameModifier":
        """从 API 返回的列表创建"""
        if len(values) >= 8:
            return cls(
                name=name,
                area=values[0], shear_2=values[1], shear_3=values[2],
                torsion=values[3], inertia_22=values[4], inertia_33=values[5],
                mass=values[6], weight=values[7]
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
        return com_ret(model.NamedAssign.ModifierFrame.SetModifiers(
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
        result = model.NamedAssign.ModifierFrame.GetModifiers(
            self.name, [0.0] * 8
        )
        
        values = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and values and len(values) >= 8:
            self.area = values[0]
            self.shear_2 = values[1]
            self.shear_3 = values[2]
            self.torsion = values[3]
            self.inertia_22 = values[4]
            self.inertia_33 = values[5]
            self.mass = values[6]
            self.weight = values[7]
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
        return com_ret(model.NamedAssign.ModifierFrame.Delete(self.name))
    
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
        ret = com_ret(model.NamedAssign.ModifierFrame.ChangeName(self.name, new_name))
        if ret == 0:
            self.name = new_name
        return ret
    
    @staticmethod
    def get_count(model) -> int:
        """获取修改器数量"""
        return model.NamedAssign.ModifierFrame.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """获取所有修改器名称"""
        result = model.NamedAssign.ModifierFrame.GetNameList(0, [])
        names = com_data(result, 1)
        if names:
            return list(names)
        return []
    
    @classmethod
    def get_by_name(cls, model, name: str) -> Optional["NamedFrameModifier"]:
        """按名称获取修改器"""
        mod = cls(name=name)
        ret = mod._get(model)
        if ret == 0:
            return mod
        return None
    
    @classmethod
    def get_all(cls, model) -> List["NamedFrameModifier"]:
        """获取所有修改器"""
        names = cls.get_name_list(model)
        result = []
        for name in names:
            mod = cls.get_by_name(model, name)
            if mod:
                result.append(mod)
        return result
