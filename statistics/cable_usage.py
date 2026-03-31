# -*- coding: utf-8 -*-
"""
cable_usage.py - cable-usage statistics

Provides model-level cable-usage statistics with support for:
- Calculate total cable usage
- Grouped statistics by section/material/group
- Compute a selected cable subset

Formula:
- total = Σ(cable.weight) (kg)
- cable.weight = weight_per_meter × length (kg)
- weight_per_meter = area × density (kg/m)

Usage:
    from statistics import CableUsage, get_cable_usage
    
    # Method 1: use the convenience function
    total = get_cable_usage(model)
    by_section = get_cable_usage(model, group_by="section")
    
    # Method 2: use the `CableUsage` class
    usage = CableUsage.calculate(model)
    print(f"Total cable usage: {usage.total} kg")
    
    # Group by section
    usage = CableUsage.calculate(model, group_by="section")
    for section, weight in usage.by_section.items():
        print(f"{section}: {weight} kg")
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union


@dataclass
class CableUsage:
    """
    Cable-usage statistics result
    
    Attributes:
        total: Total cable usage (kg)
        by_section: Cable usage grouped by section name
        by_material: Cable usage grouped by material name
        by_group: Cable usage grouped by SAP2000 group name
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
        Compute cable usage (direct API retrieval for unit consistency)
        
        Args:
            model: SapModel object
            group_by: Grouping mode ("section", "material", "group")
            cable_names: Cable names to include; `None` means all cables
            
        Returns:
            `CableUsage` object
        """
        from global_parameters.units import Units, UnitSystem
        
        result = cls()
        
        # Switch to N-m-C units (to keep API return units consistent)
        original_units = Units.get_present_units(model)
        Units.set_present_units(model, UnitSystem.N_M_C)
        
        try:
            # 1. Get all cable names
            ret = model.CableObj.GetNameList(0, [])
            if not isinstance(ret, (list, tuple)) or len(ret) < 2 or not ret[1]:
                return result
            all_cable_names = list(ret[1])
            
            # 2. Determine cables to include
            target_cables = set(cable_names) if cable_names else set(all_cable_names)
            
            # 3. Batch-read lengths and sections from tables (faster)
            cable_length = {}  # cable_name -> length (m)
            cable_section = {}  # cable_name -> section_name
            
            # Get lengths
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
            
            # Get section assignments
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
            
            # 4. Cache: section -> (area m², material name)
            section_cache = {}
            
            # 5. Cache: material -> density kg/m³
            material_cache = {}
            
            # 6. Compute each cable weight
            cable_data = []  # [(name, section, material, weight), ...]
            
            for cname in target_cables:
                length_m = cable_length.get(cname, 0.0)
                section_name = cable_section.get(cname, "")
                
                if not section_name or length_m <= 0:
                    continue
                
                # Get section info (with cache)
                if section_name not in section_cache:
                    # PropCable.GetProp returns: [MatProp, Area, Color, Notes, GUID, ret]
                    # Note: under N-m-C units, `Area` is in m²
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
                
                # Get material density (with cache)
                if mat_name and mat_name not in material_cache:
                    # GetWeightAndMass returns: [Weight, Mass, ret]
                    # Under N-m-C units: `Weight=N/m³`, `Mass=kg/m³`
                    ret = model.PropMaterial.GetWeightAndMass(mat_name)
                    if isinstance(ret, (list, tuple)) and len(ret) >= 2:
                        density = float(ret[1]) if ret[1] else 0.0  # kg/m³
                        # Check whether density is reasonable (steel is about `7850 kg/m³`)
                        # If density is too small, this may be a unit issue; try correcting it
                        if density < 100:  # density lower than `100 kg/m³` is unrealistic
                            density = density * 1000  # likely in `t/m³`; convert to `kg/m³`
                        material_cache[mat_name] = density
                    else:
                        material_cache[mat_name] = 0.0
                
                density = material_cache.get(mat_name, 0.0)
                
                # Compute weight: area (m²) x density (kg/m³) x length (m) = kg
                weight = area * density * length_m if area > 0 and density > 0 else 0.0
                cable_data.append((cname, section_name, mat_name, weight))
            
            # 7. Calculate total cable usage
            result.total = sum(w for _, _, _, w in cable_data)
            
            # 8. Aggregate by grouping mode
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
        """Group by SAP2000 group"""
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
    Convenience function to get cable usage
    
    Args:
        model: SapModel object
        group_by: Grouping mode; `None` returns total, `"section"/"material"/"group"` returns grouped dict
        cable_names: Cable names to include; `None` means all cables
        
    Returns:
        - When `group_by=None`, returns total cable usage (`float`)
        - When `group_by` is set, returns grouped dict (`Dict[str, float]`)
        
    Example:
        # Get total cable usage
        total = get_cable_usage(model)
        print(f"Total cable usage: {total} kg")
        
        # Group by section
        by_section = get_cable_usage(model, group_by="section")
        for section, weight in by_section.items():
            print(f"{section}: {weight} kg")
        
        # Selected cables
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
