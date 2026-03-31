# -*- coding: utf-8 -*-
"""
group.py - Group definition data objects

Wraps the SAP2000 `GroupDef` API.

This module manages group definitions and supports:
- Creating, deleting, and renaming groups
- Reading group properties
- Getting all objects assigned to a group
- Clearing all assignments from a group

Note: To assign objects into groups, use each module's `group.py` (for example `frame/group.py`).

SAP2000 API:
- `SetGroup(Name, color, SpecifiedForSelection, ...)` - Create or update a group
- GetGroup(Name, color, SpecifiedForSelection, ...) - Reading group properties
- `GetNameList(NumberNames, MyName[])` - Get all group names
- `GetAssignments(Name, NumberItems, ObjectType[], ObjectName[])` - Get group assignments
- `Count()` - Get the number of groups
- `Delete(Name)` - Delete a group (cannot delete `"ALL"`)
- `ChangeName(Name, NewName)` - Rename a group (cannot rename `"ALL"`)
- Clear(Name) - Clearing all assignments from a group

Usage:
    from PySap2000.group import Group, GroupObjectType
    
    # Create a group
    group = Group(name="Beams", for_steel_design=True)
    group._create(model)
    
    # Get a group
    group = Group.get_by_name(model, "Beams")
    print(f"Color: {group.color}")
    
    # Get all objects in the group
    assignments = group.get_assignments(model)
    for obj_type, obj_name in assignments:
        print(f"{GroupObjectType(obj_type).name}: {obj_name}")
    
    # Clear the group
    group.clear(model)
    
    # Rename the group
    group.change_name(model, "NewName")
    
    # Delete the group
    group._delete(model)
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, ClassVar

from .enums import GroupObjectType
from PySap2000.com_helper import com_data


@dataclass
class GroupAssignment:
    """
    Group assignment entry
    
    Attributes:
        object_type: Object type (`GroupObjectType`)
        object_name: Object name
    """
    object_type: GroupObjectType
    object_name: str


@dataclass
class Group:
    """
    Group definition data object
    
    Wraps SAP2000 `GroupDef`.
    
    Attributes:
        name: Group name
        color: Display color (`-1` means auto-select)
        for_selection: Used for selection
        for_section_cut: Used for section cut definitions
        for_steel_design: Used for steel design groups
        for_concrete_design: Used for concrete design groups
        for_aluminum_design: Used for aluminum design groups
        for_cold_formed_design: Used for cold-formed design groups
        for_static_nl_stage: Used for static nonlinear stages
        for_bridge_output: Used for bridge response output
        for_auto_seismic_output: Used for auto seismic output
        for_auto_wind_output: Used for auto wind output
        for_mass_and_weight: Used for mass and weight reporting
    """
    
    # Required fields
    name: str = ""
    
    # Display color
    color: int = -1
    
    # Usage flags (defaults match the SAP2000 API)
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
    
    # Class metadata
    _object_type: ClassVar[str] = "GroupDef"
    
    # ==================== Core CRUD methods ====================
    
    def _create(self, model) -> int:
        """
        Create or update the group in SAP2000
        
        Updates the group if it exists; otherwise creates a new one.
        
        Returns:
            `0` on success
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
        Load group data from SAP2000
        
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
            # `result[12]` is the return code.
        
        return self
    
    def _delete(self, model) -> int:
        """
        Delete the group from SAP2000
        
        Note: the `"ALL"` group cannot be deleted.
        
        Returns:
            `0` on success
        """
        return model.GroupDef.Delete(self.name)
    
    # ==================== Static methods ====================
    
    @staticmethod
    def get_count(model) -> int:
        """
        Get the total number of groups
        
        Returns:
            Number of groups
        """
        return model.GroupDef.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """
        Get the list of all group names
        
        Returns:
            List of group names
        """
        result = model.GroupDef.GetNameList(0, [])
        num_names = com_data(result, 0, 0)
        if num_names > 0 and com_data(result, 1):
            return list(com_data(result, 1))
        return []
    
    # ==================== Class methods ====================
    
    @classmethod
    def get_by_name(cls, model, name: str) -> 'Group':
        """
        Get a group by name
        
        Args:
            model: SAP2000 SapModel object
            name: Group name
            
        Returns:
            `Group` instance
            
        Example:
            group = Group.get_by_name(model, "Beams")
            print(f"Used for steel design: {group.for_steel_design}")
        """
        group = cls(name=name)
        group._get(model)
        return group
    
    @classmethod
    def get_all(cls, model, names: List[str] = None) -> List['Group']:
        """
        Get all groups
        
        Args:
            model: SAP2000 SapModel object
            names: List of group names, or `None` for all groups
            
        Returns:
            List of `Group` instances
            
        Example:
            groups = Group.get_all(model)
            for g in groups:
                print(f"{g.name}: color={g.color}")
        """
        if names is None:
            names = cls.get_name_list(model)
        return [cls.get_by_name(model, name) for name in names]
    
    # ==================== Instance methods ====================
    
    def change_name(self, model, new_name: str) -> int:
        """
        Rename the group
        
        Note: the `"ALL"` group cannot be renamed.
        
        Args:
            model: SAP2000 SapModel object
            new_name: New group name
            
        Returns:
            `0` on success
            
        Example:
            group.change_name(model, "NewGroupName")
        """
        ret = model.GroupDef.ChangeName(self.name, new_name)
        if ret == 0:
            self.name = new_name
        return ret
    
    def clear(self, model) -> int:
        """
        Clear all objects from the group
        
        Removes all assignments while keeping the group definition.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` on success
            
        Example:
            group.clear(model)
        """
        return model.GroupDef.Clear(self.name)
    
    def get_assignments(self, model) -> List[GroupAssignment]:
        """
        Get all objects assigned to the group
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            List of `GroupAssignment`
            
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
        Get all objects assigned to the group in raw form
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            List of `(object_type, object_name)` tuples
            
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
        Get the number of objects in the group
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            Number of objects
        """
        result = model.GroupDef.GetAssignments(self.name, 0, [], [])
        return com_data(result, 0, 0)
    
    def get_members_by_type(
        self, 
        model, 
        object_type: GroupObjectType
    ) -> List[str]:
        """
        Get group members of a specific type
        
        Args:
            model: SAP2000 SapModel object
            object_type: Object type
            
        Returns:
            List of object names
            
        Example:
            # Get all frames in the group
            frames = group.get_members_by_type(model, GroupObjectType.FRAME)
        """
        assignments = self.get_assignments_raw(model)
        return [name for obj_type, name in assignments if obj_type == int(object_type)]
    
    # ==================== Convenience methods ====================
    
    def get_points(self, model) -> List[str]:
        """Get all points in the group"""
        return self.get_members_by_type(model, GroupObjectType.POINT)
    
    def get_frames(self, model) -> List[str]:
        """Get all frames in the group"""
        return self.get_members_by_type(model, GroupObjectType.FRAME)
    
    def get_cables(self, model) -> List[str]:
        """Get all cables in the group"""
        return self.get_members_by_type(model, GroupObjectType.CABLE)
    
    def get_tendons(self, model) -> List[str]:
        """Get all tendons in the group"""
        return self.get_members_by_type(model, GroupObjectType.TENDON)
    
    def get_areas(self, model) -> List[str]:
        """Get all areas in the group"""
        return self.get_members_by_type(model, GroupObjectType.AREA)
    
    def get_solids(self, model) -> List[str]:
        """Get all solids in the group"""
        return self.get_members_by_type(model, GroupObjectType.SOLID)
    
    def get_links(self, model) -> List[str]:
        """Get all links in the group"""
        return self.get_members_by_type(model, GroupObjectType.LINK)
