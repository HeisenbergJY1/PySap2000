# -*- coding: utf-8 -*-
"""
group.py - 组定义数据对象

对应 SAP2000 的 GroupDef API

这是组的定义和管理模块，用于:
- 创建/删除/重命名组
- 获取组属性
- 获取组内所有对象
- 清空组内对象

注意: 将对象添加到组请使用 types_for_xxx/xx_group.py

SAP2000 API:
- SetGroup(Name, color, SpecifiedForSelection, ...) - 创建/修改组
- GetGroup(Name, color, SpecifiedForSelection, ...) - 获取组属性
- GetNameList(NumberNames, MyName[]) - 获取所有组名称
- GetAssignments(Name, NumberItems, ObjectType[], ObjectName[]) - 获取组内对象
- Count() - 获取组数量
- Delete(Name) - 删除组 (不能删除 "ALL")
- ChangeName(Name, NewName) - 重命名组 (不能重命名 "ALL")
- Clear(Name) - 清空组内对象

Usage:
    from PySap2000.group import Group, GroupObjectType
    
    # 创建组
    group = Group(name="Beams", for_steel_design=True)
    group._create(model)
    
    # 获取组
    group = Group.get_by_name(model, "Beams")
    print(f"颜色: {group.color}")
    
    # 获取组内所有对象
    assignments = group.get_assignments(model)
    for obj_type, obj_name in assignments:
        print(f"{GroupObjectType(obj_type).name}: {obj_name}")
    
    # 清空组
    group.clear(model)
    
    # 重命名组
    group.change_name(model, "NewName")
    
    # 删除组
    group._delete(model)
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, ClassVar

from .enums import GroupObjectType
from PySap2000.com_helper import com_data


@dataclass
class GroupAssignment:
    """
    组内对象分配
    
    Attributes:
        object_type: 对象类型 (GroupObjectType)
        object_name: 对象名称
    """
    object_type: GroupObjectType
    object_name: str


@dataclass
class Group:
    """
    组定义数据对象
    
    对应 SAP2000 的 GroupDef
    
    Attributes:
        name: 组名称
        color: 显示颜色 (-1 表示自动选择)
        for_selection: 用于选择
        for_section_cut: 用于截面切割定义
        for_steel_design: 用于钢结构设计组
        for_concrete_design: 用于混凝土设计组
        for_aluminum_design: 用于铝结构设计组
        for_cold_formed_design: 用于冷弯型钢设计组
        for_static_nl_stage: 用于非线性静力分析阶段
        for_bridge_output: 用于桥梁响应输出
        for_auto_seismic_output: 用于自动地震荷载输出
        for_auto_wind_output: 用于自动风荷载输出
        for_mass_and_weight: 用于质量和重量报告
    """
    
    # 必填属性
    name: str = ""
    
    # 显示颜色
    color: int = -1
    
    # 用途标志 (默认值与 SAP2000 API 一致)
    for_selection: bool = True
    for_section_cut: bool = True
    for_steel_design: bool = True
    for_concrete_design: bool = True
    for_aluminum_design: bool = True
    for_cold_formed_design: bool = True
    for_static_nl_stage: bool = True
    for_bridge_output: bool = True
    for_auto_seismic_output: bool = False
    for_auto_wind_output: bool = False
    for_mass_and_weight: bool = True
    
    # 类属性
    _object_type: ClassVar[str] = "GroupDef"
    
    # ==================== 核心 CRUD 方法 ====================
    
    def _create(self, model) -> int:
        """
        在 SAP2000 中创建或修改组
        
        如果组已存在则修改，否则创建新组
        
        Returns:
            0 表示成功
        """
        return model.GroupDef.SetGroup(
            self.name,
            self.color,
            self.for_selection,
            self.for_section_cut,
            self.for_steel_design,
            self.for_concrete_design,
            self.for_aluminum_design,
            self.for_cold_formed_design,
            self.for_static_nl_stage,
            self.for_bridge_output,
            self.for_auto_seismic_output,
            self.for_auto_wind_output,
            self.for_mass_and_weight
        )
    
    def _get(self, model) -> 'Group':
        """
        从 SAP2000 获取组数据
        
        Returns:
            self
        """
        result = model.GroupDef.GetGroup(
            self.name,
            0,      # color
            False,  # SpecifiedForSelection
            False,  # SpecifiedForSectionCutDefinition
            False,  # SpecifiedForSteelDesign
            False,  # SpecifiedForConcreteDesign
            False,  # SpecifiedForAluminumDesign
            False,  # SpecifiedForColdFormedDesign
            False,  # SpecifiedForStaticNLActiveStage
            False,  # SpecifiedForBridgeResponseOutput
            False,  # SpecifiedForAutoSeismicOutput
            False,  # SpecifiedForAutoWindOutput
            False   # SpecifiedForMassAndWeight
        )
        
        color = com_data(result, 0)
        if color is not None:
            self.color = com_data(result, 0, -1)
            self.for_selection = com_data(result, 1, True)
            self.for_section_cut = com_data(result, 2, True)
            self.for_steel_design = com_data(result, 3, True)
            self.for_concrete_design = com_data(result, 4, True)
            self.for_aluminum_design = com_data(result, 5, True)
            self.for_cold_formed_design = com_data(result, 6, True)
            self.for_static_nl_stage = com_data(result, 7, True)
            self.for_bridge_output = com_data(result, 8, True)
            self.for_auto_seismic_output = com_data(result, 9, False)
            self.for_auto_wind_output = com_data(result, 10, False)
            self.for_mass_and_weight = com_data(result, 11, True)
            # result[12] 是返回码
        
        return self
    
    def _delete(self, model) -> int:
        """
        从 SAP2000 删除组
        
        注意: 不能删除 "ALL" 组
        
        Returns:
            0 表示成功
        """
        return model.GroupDef.Delete(self.name)
    
    # ==================== 静态方法 ====================
    
    @staticmethod
    def get_count(model) -> int:
        """
        获取组总数
        
        Returns:
            组数量
        """
        return model.GroupDef.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """
        获取所有组名称列表
        
        Returns:
            组名称列表
        """
        result = model.GroupDef.GetNameList(0, [])
        num_names = com_data(result, 0, 0)
        if num_names > 0 and com_data(result, 1):
            return list(com_data(result, 1))
        return []
    
    # ==================== 类方法 ====================
    
    @classmethod
    def get_by_name(cls, model, name: str) -> 'Group':
        """
        获取指定名称的组
        
        Args:
            model: SapModel 对象
            name: 组名称
            
        Returns:
            Group 对象
            
        Example:
            group = Group.get_by_name(model, "Beams")
            print(f"用于钢结构设计: {group.for_steel_design}")
        """
        group = cls(name=name)
        group._get(model)
        return group
    
    @classmethod
    def get_all(cls, model, names: List[str] = None) -> List['Group']:
        """
        获取所有组
        
        Args:
            model: SapModel 对象
            names: 组名称列表，None 表示获取全部
            
        Returns:
            Group 对象列表
            
        Example:
            groups = Group.get_all(model)
            for g in groups:
                print(f"{g.name}: color={g.color}")
        """
        if names is None:
            names = cls.get_name_list(model)
        return [cls.get_by_name(model, name) for name in names]
    
    # ==================== 实例方法 ====================
    
    def change_name(self, model, new_name: str) -> int:
        """
        重命名组
        
        注意: 不能重命名 "ALL" 组
        
        Args:
            model: SapModel 对象
            new_name: 新名称
            
        Returns:
            0 表示成功
            
        Example:
            group.change_name(model, "NewGroupName")
        """
        ret = model.GroupDef.ChangeName(self.name, new_name)
        if ret == 0:
            self.name = new_name
        return ret
    
    def clear(self, model) -> int:
        """
        清空组内所有对象
        
        移除组内所有对象分配，但保留组定义
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
            
        Example:
            group.clear(model)
        """
        return model.GroupDef.Clear(self.name)
    
    def get_assignments(self, model) -> List[GroupAssignment]:
        """
        获取组内所有对象
        
        Args:
            model: SapModel 对象
            
        Returns:
            GroupAssignment 列表
            
        Example:
            assignments = group.get_assignments(model)
            for a in assignments:
                print(f"{a.object_type.name}: {a.object_name}")
        """
        result = model.GroupDef.GetAssignments(self.name, 0, [], [])
        
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            obj_types = com_data(result, 1)
            obj_names = com_data(result, 2)
            if obj_types and obj_names:
                return [
                    GroupAssignment(
                        object_type=GroupObjectType(obj_types[i]),
                        object_name=obj_names[i]
                    )
                    for i in range(num_items)
                ]
        
        return []
    
    def get_assignments_raw(self, model) -> List[Tuple[int, str]]:
        """
        获取组内所有对象 (原始格式)
        
        Args:
            model: SapModel 对象
            
        Returns:
            (object_type, object_name) 元组列表
            
        Example:
            assignments = group.get_assignments_raw(model)
            for obj_type, obj_name in assignments:
                print(f"Type {obj_type}: {obj_name}")
        """
        result = model.GroupDef.GetAssignments(self.name, 0, [], [])
        
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            obj_types = com_data(result, 1)
            obj_names = com_data(result, 2)
            if obj_types and obj_names:
                return [(obj_types[i], obj_names[i]) for i in range(num_items)]
        
        return []
    
    def get_member_count(self, model) -> int:
        """
        获取组内对象数量
        
        Args:
            model: SapModel 对象
            
        Returns:
            对象数量
        """
        result = model.GroupDef.GetAssignments(self.name, 0, [], [])
        return com_data(result, 0, 0)
    
    def get_members_by_type(
        self, 
        model, 
        object_type: GroupObjectType
    ) -> List[str]:
        """
        获取组内指定类型的对象
        
        Args:
            model: SapModel 对象
            object_type: 对象类型
            
        Returns:
            对象名称列表
            
        Example:
            # 获取组内所有杆件
            frames = group.get_members_by_type(model, GroupObjectType.FRAME)
        """
        assignments = self.get_assignments_raw(model)
        return [name for obj_type, name in assignments if obj_type == int(object_type)]
    
    # ==================== 便捷方法 ====================
    
    def get_points(self, model) -> List[str]:
        """获取组内所有节点"""
        return self.get_members_by_type(model, GroupObjectType.POINT)
    
    def get_frames(self, model) -> List[str]:
        """获取组内所有杆件"""
        return self.get_members_by_type(model, GroupObjectType.FRAME)
    
    def get_cables(self, model) -> List[str]:
        """获取组内所有索"""
        return self.get_members_by_type(model, GroupObjectType.CABLE)
    
    def get_tendons(self, model) -> List[str]:
        """获取组内所有预应力筋"""
        return self.get_members_by_type(model, GroupObjectType.TENDON)
    
    def get_areas(self, model) -> List[str]:
        """获取组内所有面"""
        return self.get_members_by_type(model, GroupObjectType.AREA)
    
    def get_solids(self, model) -> List[str]:
        """获取组内所有实体"""
        return self.get_members_by_type(model, GroupObjectType.SOLID)
    
    def get_links(self, model) -> List[str]:
        """获取组内所有连接单元"""
        return self.get_members_by_type(model, GroupObjectType.LINK)
