# -*- coding: utf-8 -*-
"""
group - 组定义模块

用于管理 SAP2000 中的组定义 (GroupDef API)

注意: 这是组的定义和管理模块，不是对象到组的分配。
对象到组的分配请使用:
- types_for_frames/frame_group.py
- types_for_links/link_group.py
- types_for_areas/area_group.py
- types_for_points/point_group.py
- types_for_cables/cable_group.py

SAP2000 API:
- GroupDef.SetGroup - 创建/修改组
- GroupDef.GetGroup - 获取组属性
- GroupDef.GetNameList - 获取所有组名称
- GroupDef.GetAssignments - 获取组内所有对象
- GroupDef.Count - 获取组数量
- GroupDef.Delete - 删除组
- GroupDef.ChangeName - 重命名组
- GroupDef.Clear - 清空组内对象

Usage:
    from PySap2000.group import Group, GroupObjectType
    
    # 创建组
    group = Group(name="MyGroup")
    group._create(model)
    
    # 获取组
    group = Group.get_by_name(model, "MyGroup")
    
    # 获取组内所有对象
    assignments = group.get_assignments(model)
    for obj_type, obj_name in assignments:
        print(f"{GroupObjectType(obj_type).name}: {obj_name}")
"""

from .group import Group, GroupAssignment
from .enums import GroupObjectType

__all__ = [
    "Group",
    "GroupAssignment",
    "GroupObjectType",
]

# AI Agent 友好的 API 分类
GROUP_API_CATEGORIES = {
    "group_definition": {
        "description": "组定义和管理",
        "class": "Group",
        "methods": [
            "_create",
            "_get", 
            "_delete",
            "get_count",
            "get_name_list",
            "get_by_name",
            "get_all",
            "change_name",
            "clear",
            "get_assignments",
        ],
    },
    "enums": {
        "description": "组相关枚举",
        "items": ["GroupObjectType"],
    },
}
