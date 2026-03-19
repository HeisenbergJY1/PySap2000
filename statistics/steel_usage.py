# -*- coding: utf-8 -*-
"""
steel_usage.py - 用钢量统计

提供模型级别的用钢量统计功能，支持:
- 计算总用钢量
- 按截面/材料/组分组统计
- 指定杆件子集计算

计算公式:
- total = Σ(frame.weight) (kg)
- frame.weight = weight_per_meter × length (kg)
- weight_per_meter = area × density (kg/m)

Usage:
    from statistics import SteelUsage, get_steel_usage
    
    # 方式1: 使用便捷函数
    total = get_steel_usage(model)
    by_section = get_steel_usage(model, group_by="section")
    
    # 方式2: 使用 SteelUsage 类
    usage = SteelUsage.calculate(model)
    print(f"总用钢量: {usage.total} kg")
    
    # 按截面分组
    usage = SteelUsage.calculate(model, group_by="section")
    for section, weight in usage.by_section.items():
        print(f"{section}: {weight} kg")
    
    # 指定杆件
    usage = SteelUsage.calculate(model, frame_names=["1", "2", "3"])
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union


@dataclass
class SteelUsage:
    """
    用钢量统计结果
    
    Attributes:
        total: 总用钢量 (kg)
        by_section: 按截面名称分组的用钢量
        by_material: 按材料名称分组的用钢量
        by_group: 按 SAP2000 组名称分组的用钢量
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
        frame_names: Optional[List[str]] = None
    ) -> 'SteelUsage':
        """
        计算用钢量 (使用表格批量获取，速度最快)
        
        Args:
            model: SapModel 对象
            group_by: 分组方式 ("section", "material", "group")
            frame_names: 指定杆件名称列表，None 表示所有杆件
            
        Returns:
            SteelUsage 对象
        """
        from global_parameters.units import Units, UnitSystem
        
        result = cls()
        
        # 切换到 N-m-C 单位
        original_units = Units.get_present_units(model)
        Units.set_present_units(model, UnitSystem.N_M_C)
        
        try:
            # 1. 从表格批量获取杆件长度 (Connectivity - Frame)
            frame_length = {}  # frame_name -> length (m)
            ret = model.DatabaseTables.GetTableForDisplayArray(
                "Connectivity - Frame", ["Frame", "Length"], "", 0, [], 0, []
            )
            if isinstance(ret, (list, tuple)) and len(ret) >= 5 and ret[5] == 0:
                fields = list(ret[2])
                num_records = ret[3]
                data = ret[4]
                num_fields = len(fields)
                
                frame_idx = fields.index("Frame") if "Frame" in fields else -1
                length_idx = fields.index("Length") if "Length" in fields else -1
                
                if frame_idx >= 0 and length_idx >= 0:
                    for i in range(num_records):
                        base = i * num_fields
                        fname = data[base + frame_idx]
                        length_str = data[base + length_idx]
                        if fname and length_str:
                            frame_length[fname] = float(length_str)
            
            # 2. 从表格批量获取杆件截面和材料覆盖 (Frame Section Assignments)
            frame_section = {}  # frame_name -> section_name
            frame_mat_overwrite = {}  # frame_name -> material_overwrite (非Default时有效)
            ret = model.DatabaseTables.GetTableForDisplayArray(
                "Frame Section Assignments", ["Frame", "AnalSect", "MatProp"], "", 0, [], 0, []
            )
            if isinstance(ret, (list, tuple)) and len(ret) >= 5 and ret[5] == 0:
                fields = list(ret[2])
                num_records = ret[3]
                data = ret[4]
                num_fields = len(fields)
                
                frame_idx = fields.index("Frame") if "Frame" in fields else -1
                section_idx = fields.index("AnalSect") if "AnalSect" in fields else -1
                matprop_idx = fields.index("MatProp") if "MatProp" in fields else -1
                
                if frame_idx >= 0 and section_idx >= 0:
                    for i in range(num_records):
                        base = i * num_fields
                        fname = data[base + frame_idx]
                        section = data[base + section_idx]
                        if fname and section:
                            frame_section[fname] = section
                        # 获取材料覆盖 (非Default时使用覆盖材料)
                        if matprop_idx >= 0:
                            mat_overwrite = data[base + matprop_idx]
                            if mat_overwrite and mat_overwrite != "Default":
                                frame_mat_overwrite[fname] = mat_overwrite
            
            # 3. 缓存: 截面 -> (面积, 材料名)
            section_cache = {}
            
            # 4. 缓存: 材料 -> 密度
            material_cache = {}
            
            # 5. 确定要计算的杆件
            if frame_names is None:
                frame_names = list(frame_length.keys())
            
            target_frames = set(frame_names) if frame_names else set()
            
            # 6. 计算每根杆件的重量
            frame_data = []  # [(name, section, material, weight), ...]
            
            for fname in target_frames:
                length_m = frame_length.get(fname, 0.0)
                section_name = frame_section.get(fname, "")
                
                if not section_name or length_m <= 0:
                    continue
                
                # 获取截面信息 (带缓存)
                if section_name not in section_cache:
                    # 获取截面面积
                    ret = model.PropFrame.GetSectProps(
                        section_name, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0
                    )
                    area = ret[0] if isinstance(ret, (list, tuple)) and len(ret) >= 1 else 0.0
                    
                    # 获取截面材料
                    section_mat = cls._get_section_material(model, section_name)
                    section_cache[section_name] = (area, section_mat)
                
                area, section_mat = section_cache[section_name]
                
                # 优先使用材料覆盖，否则使用截面材料
                mat_name = frame_mat_overwrite.get(fname, section_mat)
                
                # 获取材料密度 (带缓存)
                if mat_name and mat_name not in material_cache:
                    ret = model.PropMaterial.GetWeightAndMass(mat_name)
                    if isinstance(ret, (list, tuple)) and len(ret) >= 2:
                        material_cache[mat_name] = ret[1]  # kg/m³
                    else:
                        material_cache[mat_name] = 0.0
                
                density = material_cache.get(mat_name, 0.0)
                
                # 计算重量
                weight = area * density * length_m if area > 0 and density > 0 else 0.0
                frame_data.append((fname, section_name, mat_name, weight))
            
            # 7. 计算总用钢量
            result.total = sum(w for _, _, _, w in frame_data)
            
            # 8. 按分组方式统计
            if group_by == "section":
                for _, section, _, weight in frame_data:
                    if section not in result.by_section:
                        result.by_section[section] = 0.0
                    result.by_section[section] += weight
                    
            elif group_by == "material":
                for _, _, mat, weight in frame_data:
                    mat_key = mat or "Unknown"
                    if mat_key not in result.by_material:
                        result.by_material[mat_key] = 0.0
                    result.by_material[mat_key] += weight
                    
            elif group_by == "group":
                result.by_group = cls._group_by_group_fast(model, 
                    [(n, s, w) for n, s, _, w in frame_data])
                
        finally:
            Units.set_present_units(model, original_units)
        
        return result
    
    @staticmethod
    def _get_section_material(model, section_name: str) -> str:
        """获取截面的材料名称"""
        try:
            # 先获取截面类型
            ret = model.PropFrame.GetTypeOAPI(section_name)
            if not isinstance(ret, (list, tuple)) or len(ret) < 1:
                return ""
            sec_type = ret[0]
            
            # 根据类型调用对应的获取方法
            if sec_type == 8:  # RECTANGULAR
                ret = model.PropFrame.GetRectangle(section_name)
            elif sec_type == 9:  # CIRCLE
                ret = model.PropFrame.GetCircle(section_name)
            elif sec_type == 7:  # PIPE
                ret = model.PropFrame.GetPipe(section_name)
            elif sec_type == 6:  # BOX
                ret = model.PropFrame.GetTube_1(section_name)
            elif sec_type == 1:  # I_SECTION
                ret = model.PropFrame.GetISection_1(section_name)
            elif sec_type == 4:  # ANGLE
                ret = model.PropFrame.GetAngle_1(section_name)
            elif sec_type == 2:  # CHANNEL
                ret = model.PropFrame.GetChannel_2(section_name)
            elif sec_type == 3:  # T_SECTION
                ret = model.PropFrame.GetTee_1(section_name)
            elif sec_type == 5:  # DOUBLE_ANGLE
                ret = model.PropFrame.GetDblAngle_2(section_name)
            elif sec_type == 11:  # DOUBLE_CHANNEL
                ret = model.PropFrame.GetDblChannel_1(section_name)
            else:
                return ""
            
            if isinstance(ret, (list, tuple)) and len(ret) >= 2:
                return ret[1] or ""
        except Exception:
            pass
        return ""
    
    @staticmethod
    def _group_by_group_fast(model, frame_data) -> Dict[str, float]:
        """按组分组统计"""
        from group.group import Group
        
        result: Dict[str, float] = {}
        frame_weights = {name: weight for name, _, weight in frame_data}
        
        group_names = Group.get_name_list(model)
        for group_name in group_names:
            try:
                group = Group.get_by_name(model, group_name)
                group_frames = group.get_frames(model)
                group_weight = sum(
                    frame_weights.get(fname, 0.0)
                    for fname in group_frames
                    if fname in frame_weights
                )
                if group_weight > 0:
                    result[group_name] = group_weight
            except Exception:
                pass
        
        return result


def get_steel_usage(
    model,
    group_by: Optional[str] = None,
    frame_names: Optional[List[str]] = None
) -> Union[float, Dict[str, float]]:
    """
    获取用钢量的便捷函数
    
    Args:
        model: SapModel 对象
        group_by: 分组方式，None 返回总量，"section"/"material"/"group" 返回分组字典
        frame_names: 指定杆件名称列表，None 表示所有杆件
        
    Returns:
        - 当 group_by=None 时，返回总用钢量 (float)
        - 当 group_by 指定时，返回分组字典 (Dict[str, float])
        
    Example:
        # 获取总用钢量
        total = get_steel_usage(model)
        print(f"总用钢量: {total} kg")
        
        # 按截面分组
        by_section = get_steel_usage(model, group_by="section")
        for section, weight in by_section.items():
            print(f"{section}: {weight} kg")
        
        # 指定杆件
        weight = get_steel_usage(model, frame_names=["1", "2"])
    """
    usage = SteelUsage.calculate(model, group_by=group_by, frame_names=frame_names)
    
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
