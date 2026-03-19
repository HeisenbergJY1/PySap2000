# -*- coding: utf-8 -*-
"""
modifier.py - Cable 修改系数

SAP2000 API:
- CableObj.SetModifiers(Name, Value, ItemType)
- CableObj.GetModifiers(Name, Value)
- CableObj.DeleteModifiers(Name, ItemType)

修改系数数组 Value[3]:
- Value[0]: 截面面积修改系数
- Value[1]: 质量修改系数
- Value[2]: 重量修改系数
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Union
from enum import IntEnum
from PySap2000.com_helper import com_ret, com_data


class CableItemType(IntEnum):
    """Cable 操作对象类型"""
    OBJECT = 0              # 单个对象
    GROUP = 1               # 组
    SELECTED_OBJECTS = 2    # 选中对象


@dataclass
class CableModifiers:
    """
    Cable 修改系数数据类
    
    Attributes:
        area: 截面面积修改系数 (默认 1.0)
        mass: 质量修改系数 (默认 1.0)
        weight: 重量修改系数 (默认 1.0)
    """
    area: float = 1.0
    mass: float = 1.0
    weight: float = 1.0
    
    def to_list(self) -> List[float]:
        """转换为 API 需要的列表格式"""
        return [self.area, self.mass, self.weight]
    
    @classmethod
    def from_list(cls, values: List[float]) -> 'CableModifiers':
        """从 API 返回的列表创建"""
        if len(values) >= 3:
            return cls(area=values[0], mass=values[1], weight=values[2])
        return cls()


def set_cable_modifiers(
    model,
    cable_name: str,
    modifiers: Union[CableModifiers, Tuple[float, float, float]],
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    设置 Cable 修改系数
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
        modifiers: 修改系数 (CableModifiers 或 (area, mass, weight) 元组)
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        # 使用 CableModifiers
        set_cable_modifiers(model, "1", CableModifiers(area=1.5, mass=1.2))
        
        # 使用元组
        set_cable_modifiers(model, "1", (1.5, 1.2, 1.0))
    """
    if isinstance(modifiers, CableModifiers):
        values = modifiers.to_list()
    else:
        values = list(modifiers)
    
    return model.CableObj.SetModifiers(str(cable_name), values, int(item_type))


def get_cable_modifiers(model, cable_name: str) -> Optional[CableModifiers]:
    """
    获取 Cable 修改系数
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
    
    Returns:
        CableModifiers 对象，失败返回 None
    
    Example:
        modifiers = get_cable_modifiers(model, "1")
        if modifiers:
            print(f"面积系数: {modifiers.area}")
    """
    try:
        result = model.CableObj.GetModifiers(str(cable_name), [0.0, 0.0, 0.0])
        values = com_data(result, 0)
        ret = com_ret(result)
        if ret == 0 and values:
            return CableModifiers.from_list(list(values))
    except Exception:
        pass
    return None


def delete_cable_modifiers(
    model,
    cable_name: str,
    item_type: CableItemType = CableItemType.OBJECT
) -> int:
    """
    删除 Cable 修改系数（恢复默认值 1.0）
    
    Args:
        model: SapModel 对象
        cable_name: Cable 名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.CableObj.DeleteModifiers(str(cable_name), int(item_type))
