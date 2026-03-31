# -*- coding: utf-8 -*-
"""
element_geometry.py - Element geometry descriptions

Defines element geometry information (nodes, section, direction, etc.) without depending on any rendering library.

Optimization: supports `orjson` (if installed), with 5-10x faster JSON serialization/deserialization.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import json

# Try using `orjson` (a faster JSON library)
try:
    import orjson
    _USE_ORJSON = True
except ImportError:
    _USE_ORJSON = False


@dataclass
class Point3D:
    """3D point"""
    x: float
    y: float
    z: float
    
    def to_list(self) -> List[float]:
        return [self.x, self.y, self.z]
    
    def to_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "z": self.z}


@dataclass
class ElementGeometry:
    """Base element geometry class"""
    name: str
    point_i: Point3D  # Start point
    point_j: Point3D  # End point
    section_name: str
    material: str = ""
    group: str = ""
    
    def length(self) -> float:
        """Compute element length"""
        dx = self.point_j.x - self.point_i.x
        dy = self.point_j.y - self.point_i.y
        dz = self.point_j.z - self.point_i.z
        return (dx**2 + dy**2 + dz**2) ** 0.5
    
    def direction_vector(self) -> Tuple[float, float, float]:
        """Compute normalized element direction vector"""
        length = self.length()
        if length == 0:
            return (0, 0, 1)
        dx = (self.point_j.x - self.point_i.x) / length
        dy = (self.point_j.y - self.point_i.y) / length
        dz = (self.point_j.z - self.point_i.z) / length
        return (dx, dy, dz)
    
    def to_dict(self) -> dict:
        """Convert to a dictionary (JSON-serializable)."""
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
    """Frame element geometry"""
    section_type: str = ""  # Circle, Rect, I, etc.
    section_params: dict = field(default_factory=dict)  # Section parameters
    local_axis_angle: float = 0.0  # Local coordinate system rotation angle (degrees)
    
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
    """Cable element geometry"""
    diameter: float = 0.0  # Diameter (m)
    area: float = 0.0  # Area (m^2)
    section_type: str = "Circle"  # Cable section type (default: circle)
    section_params: dict = field(default_factory=dict)  # Section parameters
    
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
    """Complete 3D model data"""
    elements: List[ElementGeometry] = field(default_factory=list)
    model_name: str = ""
    units: str = "m"  # Units
    
    def add_element(self, element: ElementGeometry):
        """Add an element"""
        self.elements.append(element)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "model_name": self.model_name,
            "units": self.units,
            "element_count": len(self.elements),
            "elements": [elem.to_dict() for elem in self.elements],
        }
    
    def to_json(self, filepath: str = None, indent: bool = True) -> str:
        """
        Export as JSON
        
        If `orjson` is installed, use it for serialization (5-10x faster).
        
        Args:
            filepath: Output file path (optional)
            indent: Whether to format output (default: `True`)
            
        Returns:
            JSON string
        """
        data = self.to_dict()
        
        if _USE_ORJSON:
            # Use `orjson` (faster)
            option = orjson.OPT_INDENT_2 if indent else 0
            json_bytes = orjson.dumps(data, option=option)
            json_str = json_bytes.decode('utf-8')
        else:
            # Fallback to the standard library
            json_str = json.dumps(data, indent=2 if indent else None, ensure_ascii=False)
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Model3D':
        """
        Load from JSON
        
        If `orjson` is installed, use it for deserialization (5-10x faster).
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
