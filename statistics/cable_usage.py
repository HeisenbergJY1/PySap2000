# -*- coding: utf-8 -*-
"""
cable_usage.py - 用索量统计

提供模型级别的用索量统计功能，支持:
- 计算总用索量
- 按截面/材料/组分组统计
- 指定索单元子集计算

计算公式:
- total = Σ(cable.weight) (kg)
- cable.weight = weight_per_meter × length (kg)
- weight_per_meter = area × density (kg/m)

Usage:
    from statistics import CableUsage, get_cable_usage
    
    # 方式1: 使用便捷函数
    total = get_cable_usage(model)
    by_section = get_cable_usage(model, group_by="section")
    
    # 方式2: 使用 CableUsage 类
    usage = CableUsage.calculate(model)
    print(f"总用索量: {usage.total} kg")
    
    # 按截面分组
    usage = CableUsage.calculate(model, group_by="section")
    for section, weight in usage.by_section.items():
        print(f"{section}: {weight} kg")
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union


@dataclass
class CableUsage:
    """
    用索量统计结果
    
    Attributes:
        total: 总用索量 (kg)
        by_section: 按截面名称分组的用索量
        by_material: 按材料名称分组的用索量
        by_group: 按 SAP2000 组名称分组的用索量
    """
    
    total: float = 0.0
    by_section: Dict[str, float] = field(default_factory=dict)
    by_material: Dict[str, float] = field(default_factory=dict)
    by_group: Dict[str, float] = field(default_factory=dict)
    
    @classmethod
    def calculate(
        cls,
        model,
        group_by: Optional[str] = None,
        cable_names: Optional[List[str]] = None
    ) -> 'CableUsage':
        """
        计算用索量 (使用 API 直接获取，确保单位正确)
        
        Args:
            model: SapModel 对象
            group_by: 分组方式 ("section", "material", "group")
            cable_names: 指定索单元名称列表，None 表示所有索单元
            
        Returns:
            CableUsage 对象
        """
        from global_parameters.units import Units, UnitSystem
        
        result = cls()
        
        # 切换到 N-m-C 单位 (确保 API 返回值单位一致)
        original_units = Units.get_present_units(model)
        Units.set_present_units(model, UnitSystem.N_M_C)
        
        try:
            # 1. 获取所有 Cable 名称
            ret = model.CableObj.GetNameList(0, [])
            if not isinstance(ret, (list, tuple)) or len(ret) < 2 or not ret[1]:
                return result
            all_cable_names = list(ret[1])
            
            # 2. 确定要计算的索单元
            target_cables = set(cable_names) if cable_names else set(all_cable_names)
            
            # 3. 从表格批量获取长度和截面 (表格数据更快)
            cable_length = {}  # cable_name -> length (m)
            cable_section = {}  # cable_name -> section_name
            
            # 获取长度
            ret = model.DatabaseTables.GetTableForDisplayArray(
                "Connectivity - Cable", ["Cable", "Length"], "", 0, [], 0, []
            )
            if isinstance(ret, (list, tuple)) and len(ret) >= 5 and ret[5] == 0:
                fields = list(ret[2])
                num_records = ret[3]
                data = ret[4]
                num_fields = len(fields)
                
                cable_idx = fields.index("Cable") if "Cable" in fields else -1
                length_idx = fields.index("Length") if "Length" in fields else -1
                
                if cable_idx >= 0 and length_idx >= 0:
                    for i in range(num_records):
                        base = i * num_fields
                        cname = data[base + cable_idx]
                        length_str = data[base + length_idx]
                        if cname and length_str:
                            cable_length[cname] = float(length_str)
            
            # 获取截面分配
            ret = model.DatabaseTables.GetTableForDisplayArray(
                "Cable Section Assignments", ["Cable", "CableSect"], "", 0, [], 0, []
            )
            if isinstance(ret, (list, tuple)) and len(ret) >= 5 and ret[5] == 0:
                fields = list(ret[2])
                num_records = ret[3]
                data = ret[4]
                num_fields = len(fields)
                
                cable_idx = fields.index("Cable") if "Cable" in fields else -1
                sect_idx = fields.index("CableSect") if "CableSect" in fields else -1
                
                if cable_idx >= 0 and sect_idx >= 0:
                    for i in range(num_records):
                        base = i * num_fields
                        cname = data[base + cable_idx]
                        section = data[base + sect_idx]
                        if cname and section:
                            cable_section[cname] = section
            
            # 4. 缓存: 截面 -> (面积 m², 材料名)
            section_cache = {}
            
            # 5. 缓存: 材料 -> 密度 kg/m³
            material_cache = {}
            
            # 6. 计算每根索单元的重量
            cable_data = []  # [(name, section, material, weight), ...]
            
            for cname in target_cables:
                length_m = cable_length.get(cname, 0.0)
                section_name = cable_section.get(cname, "")
                
                if not section_name or length_m <= 0:
                    continue
                
                # 获取截面信息 (带缓存)
                if section_name not in section_cache:
                    # PropCable.GetProp 返回: [MatProp, Area, Color, Notes, GUID, ret]
                    # 注意: 在 N-m-C 单位下，Area 单位是 m²
                    ret = model.PropCable.GetProp(section_name, "", 0, 0)
                    if isinstance(ret, (list, tuple)) and len(ret) >= 2:
                        section_mat = ret[0] or ""
                        area = float(ret[1]) if ret[1] else 0.0  # m²
                    else:
                        section_mat = ""
                        area = 0.0
                    
                    section_cache[section_name] = (area, section_mat)
                
                area, section_mat = section_cache[section_name]
                mat_name = section_mat
                
                # 获取材料密度 (带缓存)
                if mat_name and mat_name not in material_cache:
                    # GetWeightAndMass 返回: [Weight, Mass, ret]
                    # 在 N-m-C 单位下: Weight=N/m³, Mass=kg/m³
                    ret = model.PropMaterial.GetWeightAndMass(mat_name)
                    if isinstance(ret, (list, tuple)) and len(ret) >= 2:
                        density = float(ret[1]) if ret[1] else 0.0  # kg/m³
                        # 检查密度是否合理 (钢材约 7850 kg/m³)
                        # 如果密度太小，可能是单位问题，尝试修正
                        if density < 100:  # 密度小于 100 kg/m³ 不合理
                            density = density * 1000  # 可能是 t/m³，转换为 kg/m³
                        material_cache[mat_name] = density
                    else:
                        material_cache[mat_name] = 0.0
                
                density = material_cache.get(mat_name, 0.0)
                
                # 计算重量: 面积(m²) × 密度(kg/m³) × 长度(m) = kg
                weight = area * density * length_m if area > 0 and density > 0 else 0.0
                cable_data.append((cname, section_name, mat_name, weight))
            
            # 7. 计算总用索量
            result.total = sum(w for _, _, _, w in cable_data)
            
            # 8. 按分组方式统计
            if group_by == "section":
                for _, section, _, weight in cable_data:
                    if section not in result.by_section:
                        result.by_section[section] = 0.0
                    result.by_section[section] += weight
                    
            elif group_by == "material":
                for _, _, mat, weight in cable_data:
                    mat_key = mat or "Unknown"
                    if mat_key not in result.by_material:
                        result.by_material[mat_key] = 0.0
                    result.by_material[mat_key] += weight
                    
            elif group_by == "group":
                result.by_group = cls._group_by_group_fast(model, 
                    [(n, s, w) for n, s, _, w in cable_data])
                
        finally:
            Units.set_present_units(model, original_units)
        
        return result
    
    @staticmethod
    def _group_by_group_fast(model, cable_data) -> Dict[str, float]:
        """按组分组统计"""
        from group.group import Group
        
        result: Dict[str, float] = {}
        cable_weights = {name: weight for name, _, weight in cable_data}
        
        group_names = Group.get_name_list(model)
        for group_name in group_names:
            try:
                group = Group.get_by_name(model, group_name)
                group_cables = group.get_cables(model)
                group_weight = sum(
                    cable_weights.get(cname, 0.0)
                    for cname in group_cables
                    if cname in cable_weights
                )
                if group_weight > 0:
                    result[group_name] = group_weight
            except Exception:
                pass
        
        return result


def get_cable_usage(
    model,
    group_by: Optional[str] = None,
    cable_names: Optional[List[str]] = None
) -> Union[float, Dict[str, float]]:
    """
    获取用索量的便捷函数
    
    Args:
        model: SapModel 对象
        group_by: 分组方式，None 返回总量，"section"/"material"/"group" 返回分组字典
        cable_names: 指定索单元名称列表，None 表示所有索单元
        
    Returns:
        - 当 group_by=None 时，返回总用索量 (float)
        - 当 group_by 指定时，返回分组字典 (Dict[str, float])
        
    Example:
        # 获取总用索量
        total = get_cable_usage(model)
        print(f"总用索量: {total} kg")
        
        # 按截面分组
        by_section = get_cable_usage(model, group_by="section")
        for section, weight in by_section.items():
            print(f"{section}: {weight} kg")
        
        # 指定索单元
        weight = get_cable_usage(model, cable_names=["1", "2"])
    """
    usage = CableUsage.calculate(model, group_by=group_by, cable_names=cable_names)
    
    if group_by is None:
        return usage.total
    elif group_by == "section":
        return usage.by_section
    elif group_by == "material":
        return usage.by_material
    elif group_by == "group":
        return usage.by_group
    else:
        return usage.total
