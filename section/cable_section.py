# -*- coding: utf-8 -*-
"""
cable_section.py - 缆索截面属性定义
对应 SAP2000 的 PropCable

本模块用于定义截面属性（是什么），而非分配截面到缆索（怎么用）。
截面分配功能请使用 types_for_cables 模块。

Usage:
    from section import CableSection
    
    # 获取缆索截面
    cable = CableSection.get_by_name(model, "C1")
    print(f"材料: {cable.material}, 面积: {cable.area}")
    
    # 创建缆索截面
    cable = CableSection(name="C1", material="A416Gr270", area=0.001)
    cable._create(model)
    
    # 设置修改系数
    cable.set_modifiers(model, area_modifier=1.0, mass_modifier=1.5, weight_modifier=1.5)
"""

from dataclasses import dataclass, field
from typing import Optional, List, ClassVar

from PySap2000.com_helper import com_ret, com_data


@dataclass
class CableSection:
    """
    缆索截面属性 - 对应 SAP2000 PropCable
    
    Attributes:
        name: 截面名称
        material: 材料名称
        area: 截面面积 [L²]
        
        # 修改系数(默认值为1.0)
        area_modifier: 截面面积修改系数
        mass_modifier: 质量修改系数
        weight_modifier: 重量修改系数
        
        # 可选属性
        color: 显示颜色
        notes: 备注
        guid: 全局唯一标识符
    """
    
    # 标识
    name: str = ""
    
    # 属性
    material: str = ""
    area: float = 0.0
    
    # 修改系数(默认值为1.0)
    area_modifier: float = 1.0
    mass_modifier: float = 1.0
    weight_modifier: float = 1.0
    
    # 可选属性
    color: int = -1
    notes: str = ""
    guid: Optional[str] = None
    
    # 类属性
    _object_type: ClassVar[str] = "PropCable"

    # ==================== 公开方法 ====================
    
    @classmethod
    def get_by_name(cls, model, name: str) -> 'CableSection':
        """
        获取指定名称的缆索截面
        
        Args:
            model: SapModel 对象
            name: 截面名称
            
        Returns:
            填充了数据的 CableSection 对象
            
        Example:
            cable = CableSection.get_by_name(model, "C1")
            print(f"面积: {cable.area}")
        """
        prop = cls(name=name)
        prop._get(model)
        return prop
    
    @classmethod
    def get_all(cls, model) -> List['CableSection']:
        """
        获取所有缆索截面
        
        Args:
            model: SapModel 对象
            
        Returns:
            CableSection 对象列表
        """
        names = cls.get_name_list(model)
        props = []
        for name in names:
            try:
                prop = cls.get_by_name(model, name)
                props.append(prop)
            except Exception:
                pass
        return props
    
    @staticmethod
    def get_count(model) -> int:
        """获取缆索截面总数"""
        return model.PropCable.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """获取缆索截面名称列表"""
        result = model.PropCable.GetNameList(0, [])
        names = com_data(result, 1)
        return list(names) if names else []

    def set_modifiers(self, model, area_modifier: float = None, 
                      mass_modifier: float = None, 
                      weight_modifier: float = None) -> int:
        """
        设置缆索截面修改系数
        
        Args:
            model: SapModel 对象
            area_modifier: 截面面积修改系数(默认1.0)
            mass_modifier: 质量修改系数(默认1.0)
            weight_modifier: 重量修改系数(默认1.0)
            
        Returns:
            0 表示成功，非0 表示失败
        """
        if area_modifier is not None:
            self.area_modifier = area_modifier
        if mass_modifier is not None:
            self.mass_modifier = mass_modifier
        if weight_modifier is not None:
            self.weight_modifier = weight_modifier
        
        modifiers = [self.area_modifier, self.mass_modifier, self.weight_modifier]
        return model.PropCable.SetModifiers(self.name, modifiers)
    
    def get_modifiers(self, model) -> 'CableSection':
        """获取缆索截面修改系数"""
        result = model.PropCable.GetModifiers(self.name, [0.0, 0.0, 0.0])
        modifiers = com_data(result, 0)
        if isinstance(modifiers, (list, tuple)) and len(modifiers) >= 3:
            self.area_modifier = modifiers[0]
            self.mass_modifier = modifiers[1]
            self.weight_modifier = modifiers[2]
        return self
    
    def change_name(self, model, new_name: str) -> int:
        """修改缆索截面名称"""
        ret = model.PropCable.ChangeName(self.name, new_name)
        if ret == 0:
            self.name = new_name
        return ret

    # ==================== 内部方法 ====================
    
    def _get(self, model) -> 'CableSection':
        """从 SAP2000 获取缆索截面数据"""
        result = model.PropCable.GetProp(self.name)
        
        if com_data(result, 0) is not None and com_data(result, 5) is not None:
            self.material = com_data(result, 0, default="") or ""
            self.area = com_data(result, 1, default=0.0)
            self.color = com_data(result, 2, default=-1)
            self.notes = com_data(result, 3, default="") or ""
            self.guid = com_data(result, 4) or None
            ret = com_data(result, 5, default=-1)
            
            if ret != 0:
                from exceptions import SectionError
                raise SectionError(f"缆索截面 {self.name} 不存在")
        else:
            from exceptions import SectionError
            raise SectionError(f"获取缆索截面 {self.name} 失败")
        
        self.get_modifiers(model)
        return self
    
    def _create(self, model) -> int:
        """在 SAP2000 中创建缆索截面"""
        from PySap2000.logger import get_logger
        _log = get_logger("cable_section")
        if self.name:
            try:
                existing = self.get_name_list(model)
                if self.name in existing:
                    _log.warning(f"CableSection '{self.name}' already exists, skipped")
                    return -1
            except Exception:
                pass
        if self.material:
            result = model.PropMaterial.GetNameList(0, [])
            mat_names_data = com_data(result, 1)
            mat_names = list(mat_names_data) if mat_names_data else []
            if self.material not in mat_names:
                _log.warning(f"Material '{self.material}' not found")
        
        return model.PropCable.SetProp(
            self.name, self.material, self.area,
            self.color, self.notes, self.guid or ""
        )
    
    def _delete(self, model) -> int:
        """删除缆索截面"""
        return model.PropCable.Delete(self.name)
    
    def _update(self, model) -> int:
        """更新缆索截面"""
        return self._create(model)

    @property
    def standard_name(self) -> str:
        """
        获取标准化截面名称
        
        索截面使用 Φ + 等效直径:
        - Φ32 表示等效直径 32mm 的索
        
        注意: 调用前需确保单位为 N-mm-C，这样 area 单位是 mm²
        
        Returns:
            标准化的截面名称，格式为 Φ + 直径(mm)
            
        Example:
            cable = CableSection.get_by_name(model, "Cable1")
            print(cable.standard_name)  # "Φ32"
        """
        import math
        
        if self.area > 0:
            # 根据面积计算等效直径 (假设圆形截面)
            # area = π * (d/2)² => d = 2 * sqrt(area / π)
            diameter = 2 * math.sqrt(self.area / math.pi)
            return f"CAB{diameter:.0f}"
        
        # 面积为 0，返回原名称
        return self.name
