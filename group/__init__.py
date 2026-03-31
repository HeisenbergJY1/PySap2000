# -*- coding: utf-8 -*-
"""
group - Group definition helpers.

Provides helpers for managing SAP2000 group definitions via the `GroupDef` API.

Note:
    This package manages group definitions themselves, not assignments of
    objects into groups. For assignments, use each module's `group.py`:
    - `frame/group.py`
    - `link/group.py`
    - `area/group.py`
    - `point/` (via `Point.set_group_assign`)
    - `cable/group.py`

SAP2000 API:
- `GroupDef.SetGroup` - Create or update a group
- `GroupDef.GetGroup` - Get group properties
- `GroupDef.GetNameList` - Get all group names
- `GroupDef.GetAssignments` - Get all objects in a group
- `GroupDef.Count` - Get the group count
- `GroupDef.Delete` - Delete a group
- `GroupDef.ChangeName` - Rename a group
- `GroupDef.Clear` - Remove all objects from a group

Usage:
    from PySap2000.group import Group, GroupObjectType
    
    # Create a group
    group = Group(name="MyGroup")
    group._create(model)
    
    # Get a group
    group = Group.get_by_name(model, "MyGroup")
    
    # Get all objects in the group
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

# API categories for discoverability
GROUP_API_CATEGORIES = {
    "group_definition": {
        "description": "Group definition and management",
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
        "description": "Group-related enums",
        "items": ["GroupObjectType"],
    },
}
