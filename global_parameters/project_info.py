# -*- coding: utf-8 -*-
"""
project_info.py - Project metadata.

Wraps SAP2000 project information fields.

API Reference:
    - GetProjectInfo(NumberItems, Item[], Data[]) -> Long
    - SetProjectInfo(Item, Data) -> Long
    - GetUserComment(Comment) -> Long
    - SetUserComment(Comment) -> Long

Usage:
    from PySap2000.global_parameters import ProjectInfo

    info = ProjectInfo.get_all(model)

    ProjectInfo.set_item(model, "Company Name", "My Company")
    ProjectInfo.set_item(model, "Project Name", "Bridge Design")
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, List
from PySap2000.com_helper import com_ret, com_data


# Standard SAP2000 project info field names
STANDARD_FIELDS = [
    "Company Name",
    "Client Name", 
    "Project Name",
    "Project Number",
    "Model Name",
    "Model Description",
    "Revision Number",
    "Frame Type",
    "Engineer",
    "Checker",
    "Supervisor",
    "Issue Code",
    "Design Code",
]


@dataclass
class ProjectInfo:
    """
    Project information container.

    Attributes:
        company_name: Company name
        client_name: Client name
        project_name: Project name
        project_number: Project number
        model_name: Model name
        model_description: Model description
        revision_number: Revision number
        frame_type: Frame / structure type
        engineer: Engineer
        checker: Checker
        supervisor: Supervisor
        issue_code: Issue code
        design_code: Design code
        user_comment: User comment
        custom_fields: Additional key-value fields not mapped above
    """
    company_name: str = ""
    client_name: str = ""
    project_name: str = ""
    project_number: str = ""
    model_name: str = ""
    model_description: str = ""
    revision_number: str = ""
    frame_type: str = ""
    engineer: str = ""
    checker: str = ""
    supervisor: str = ""
    issue_code: str = ""
    design_code: str = ""
    user_comment: str = ""
    custom_fields: Dict[str, str] = field(default_factory=dict)
    
    @classmethod
    def get_all(cls, model) -> 'ProjectInfo':
        """
        Load all project information from the model.

        API: GetProjectInfo(NumberItems, Item[], Data[]) -> Long

        Returns:
            Populated `ProjectInfo` instance.
        """
        info = cls()
        result = model.GetProjectInfo(0, [], [])
        num_items = com_data(result, 0, 0)
        items = com_data(result, 1, None)
        data = com_data(result, 2, None)
        
        if num_items > 0 and items and data:
            for i in range(num_items):
                item_name = items[i]
                item_data = data[i]
                
                # Map to attributes
                if item_name == "Company Name":
                    info.company_name = item_data
                elif item_name == "Client Name":
                    info.client_name = item_data
                elif item_name == "Project Name":
                    info.project_name = item_data
                elif item_name == "Project Number":
                    info.project_number = item_data
                elif item_name == "Model Name":
                    info.model_name = item_data
                elif item_name == "Model Description":
                    info.model_description = item_data
                elif item_name == "Revision Number":
                    info.revision_number = item_data
                elif item_name == "Frame Type":
                    info.frame_type = item_data
                elif item_name == "Engineer":
                    info.engineer = item_data
                elif item_name == "Checker":
                    info.checker = item_data
                elif item_name == "Supervisor":
                    info.supervisor = item_data
                elif item_name == "Issue Code":
                    info.issue_code = item_data
                elif item_name == "Design Code":
                    info.design_code = item_data
                else:
                    info.custom_fields[item_name] = item_data
        
        # User comment
        try:
            result = model.GetUserComment("")
            comment = com_data(result, 0, None)
            if comment is not None:
                info.user_comment = comment
        except Exception:
            pass
        
        return info
    
    @staticmethod
    def get_item(model, item_name: str) -> Optional[str]:
        """
        Get a single project info field by name.

        Args:
            model: SAP2000 SapModel object
            item_name: Field name (SAP2000 string)

        Returns:
            Field value, or `None` if not found.
        """
        result = model.GetProjectInfo(0, [], [])
        num_items = com_data(result, 0, 0)
        items = com_data(result, 1, None)
        data = com_data(result, 2, None)
        
        if num_items > 0 and items and data:
            for i in range(num_items):
                if items[i] == item_name:
                    return data[i]
        return None
    
    @staticmethod
    def set_item(model, item_name: str, data: str) -> int:
        """
        Set a single project info field.

        API: SetProjectInfo(Item, Data) -> Long

        Args:
            model: SAP2000 SapModel object
            item_name: Field name
            data: Field value

        Returns:
            `0` if successful.
        """
        return model.SetProjectInfo(item_name, data)
    
    @staticmethod
    def get_user_comment(model) -> str:
        """
        Get the user comment string.

        API: GetUserComment(Comment) -> Long
        """
        result = model.GetUserComment("")
        return com_data(result, 0, "")
    
    @staticmethod
    def set_user_comment(model, comment: str) -> int:
        """
        Set the user comment string.

        API: SetUserComment(Comment) -> Long
        """
        return model.SetUserComment(comment)
    
    def save(self, model) -> int:
        """
        Write all non-empty fields and custom fields to the model.

        Returns:
            Last SAP2000 return code from a `Set*` call (`0` typically means success).
        """
        ret = 0
        
        if self.company_name:
            ret = model.SetProjectInfo("Company Name", self.company_name)
        if self.client_name:
            ret = model.SetProjectInfo("Client Name", self.client_name)
        if self.project_name:
            ret = model.SetProjectInfo("Project Name", self.project_name)
        if self.project_number:
            ret = model.SetProjectInfo("Project Number", self.project_number)
        if self.model_name:
            ret = model.SetProjectInfo("Model Name", self.model_name)
        if self.model_description:
            ret = model.SetProjectInfo("Model Description", self.model_description)
        if self.revision_number:
            ret = model.SetProjectInfo("Revision Number", self.revision_number)
        if self.frame_type:
            ret = model.SetProjectInfo("Frame Type", self.frame_type)
        if self.engineer:
            ret = model.SetProjectInfo("Engineer", self.engineer)
        if self.checker:
            ret = model.SetProjectInfo("Checker", self.checker)
        if self.supervisor:
            ret = model.SetProjectInfo("Supervisor", self.supervisor)
        if self.issue_code:
            ret = model.SetProjectInfo("Issue Code", self.issue_code)
        if self.design_code:
            ret = model.SetProjectInfo("Design Code", self.design_code)
        
        # Custom fields
        for key, value in self.custom_fields.items():
            ret = model.SetProjectInfo(key, value)
        
        # User comment
        if self.user_comment:
            ret = model.SetUserComment(self.user_comment)
        
        return ret
