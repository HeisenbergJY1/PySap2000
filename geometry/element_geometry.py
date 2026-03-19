# -*- coding: utf-8 -*-
"""
element_geometry.py - 单元几何描述

定义单元的几何信息（节点、截面、方向等），不依赖任何渲染库

优化：支持 orjson（如果已安装），JSON 序列化/反序列化速度提升 5-10 倍
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import json

# 尝试使用 orjson（更快的 JSON 库）
try:
    import orjson
    _USE_ORJSON = True
except ImportError:
    _USE_ORJSON = False


@dataclass
class Point3D:
    """三维点"""
    x: float
    y: float
    z: float
    
    def to_list(self) -> List[float]:
        return [self.x, self.y, self.z]
    
    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "z": self.z}


@dataclass
class ElementGeometry:
    """单元几何基类"""
    name: str
    point_i: Point3D  # 起点
    point_j: Point3D  # 终点
    section_name: str
    material: str = ""
    group: str = ""
    
    def length(self) -> float:
        """计算单元长度"""
        dx = self.point_j.x - self.point_i.x
        dy = self.point_j.y - self.point_i.y
        dz = self.point_j.z - self.point_i.z
        return (dx**2 + dy**2 + dz**2) ** 0.5
    
    def direction_vector(self) -> Tuple[float, float, float]:
        """计算单元方向向量（归一化）"""
        length = self.length()
        if length == 0:
            return (0, 0, 1)
        dx = (self.point_j.x - self.point_i.x) / length
        dy = (self.point_j.y - self.point_i.y) / length
        dz = (self.point_j.z - self.point_i.z) / length
        return (dx, dy, dz)
    
    def to_dict(self) -> dict:
        """转换为字典（可序列化为 JSON）"""
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "point_i": self.point_i.to_dict(),
            "point_j": self.point_j.to_dict(),
            "section_name": self.section_name,
            "material": self.material,
            "group": self.group,
            "length": self.length(),
        }


@dataclass
class FrameElement3D(ElementGeometry):
    """框架单元几何"""
    section_type: str = ""  # Circle, Rect, I, etc.
    section_params: dict = field(default_factory=dict)  # 截面参数
    local_axis_angle: float = 0.0  # 局部坐标系旋转角度（度）
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "section_type": self.section_type,
            "section_params": self.section_params,
            "local_axis_angle": self.local_axis_angle,
        })
        return data


@dataclass
class CableElement3D(ElementGeometry):
    """索单元几何"""
    diameter: float = 0.0  # 直径（米）
    area: float = 0.0  # 面积（平方米）
    section_type: str = "Circle"  # 索截面类型（默认圆形）
    section_params: dict = field(default_factory=dict)  # 截面参数
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "diameter": self.diameter,
            "area": self.area,
            "section_type": self.section_type,
            "section_params": self.section_params,
        })
        return data


@dataclass
class Model3D:
    """完整的三维模型数据"""
    elements: List[ElementGeometry] = field(default_factory=list)
    model_name: str = ""
    units: str = "m"  # 单位
    
    def add_element(self, element: ElementGeometry):
        """添加单元"""
        self.elements.append(element)
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "model_name": self.model_name,
            "units": self.units,
            "element_count": len(self.elements),
            "elements": [elem.to_dict() for elem in self.elements],
        }
    
    def to_json(self, filepath: str = None, indent: bool = True) -> str:
        """
        导出为 JSON
        
        如果安装了 orjson，使用 orjson 序列化（速度快 5-10 倍）
        
        Args:
            filepath: 输出文件路径（可选）
            indent: 是否格式化输出（默认 True）
            
        Returns:
            JSON 字符串
        """
        data = self.to_dict()
        
        if _USE_ORJSON:
            # 使用 orjson（更快）
            option = orjson.OPT_INDENT_2 if indent else 0
            json_bytes = orjson.dumps(data, option=option)
            json_str = json_bytes.decode('utf-8')
        else:
            # 回退到标准库
            json_str = json.dumps(data, indent=2 if indent else None, ensure_ascii=False)
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Model3D':
        """
        从 JSON 加载
        
        如果安装了 orjson，使用 orjson 反序列化（速度快 5-10 倍）
        """
        if _USE_ORJSON:
            data = orjson.loads(json_str)
        else:
            data = json.loads(json_str)
        model = cls(model_name=data.get("model_name", ""), units=data.get("units", "m"))
        
        for elem_data in data.get("elements", []):
            point_i = Point3D(**elem_data["point_i"])
            point_j = Point3D(**elem_data["point_j"])
            
            if elem_data["type"] == "FrameElement3D":
                elem = FrameElement3D(
                    name=elem_data["name"],
                    point_i=point_i,
                    point_j=point_j,
                    section_name=elem_data["section_name"],
                    material=elem_data.get("material", ""),
                    group=elem_data.get("group", ""),
                    section_type=elem_data.get("section_type", ""),
                    section_params=elem_data.get("section_params", {}),
                    local_axis_angle=elem_data.get("local_axis_angle", 0.0),
                )
            elif elem_data["type"] == "CableElement3D":
                elem = CableElement3D(
                    name=elem_data["name"],
                    point_i=point_i,
                    point_j=point_j,
                    section_name=elem_data["section_name"],
                    material=elem_data.get("material", ""),
                    group=elem_data.get("group", ""),
                    diameter=elem_data.get("diameter", 0.0),
                    area=elem_data.get("area", 0.0),
                    section_type=elem_data.get("section_type", "Circle"),
                    section_params=elem_data.get("section_params", {}),
                )
            else:
                elem = ElementGeometry(
                    name=elem_data["name"],
                    point_i=point_i,
                    point_j=point_j,
                    section_name=elem_data["section_name"],
                    material=elem_data.get("material", ""),
                    group=elem_data.get("group", ""),
                )
            
            model.add_element(elem)
        
        return model
