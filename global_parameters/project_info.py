# -*- coding: utf-8 -*-
"""
project_info.py - 项目信息
对应 SAP2000 的项目信息设置

API Reference:
    - GetProjectInfo(NumberItems, Item[], Data[]) -> Long
    - SetProjectInfo(Item, Data) -> Long
    - GetUserComment(Comment) -> Long
    - SetUserComment(Comment) -> Long

Usage:
    from PySap2000.global_parameters import ProjectInfo
    
    # 获取所有项目信息
    info = ProjectInfo.get_all(model)
    
    # 设置项目信息
    ProjectInfo.set_item(model, "Company Name", "My Company")
    ProjectInfo.set_item(model, "Project Name", "Bridge Design")
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, List
from PySap2000.com_helper import com_ret, com_data


# 标准项目信息字段
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
    项目信息数据类
    
    Attributes:
        company_name: 公司名称
        client_name: 客户名称
        project_name: 项目名称
        project_number: 项目编号
        model_name: 模型名称
        model_description: 模型描述
        revision_number: 版本号
        frame_type: 结构类型
        engineer: 工程师
        checker: 校核人
        supervisor: 审核人
        issue_code: 出图编号
        design_code: 设计规范
        user_comment: 用户备注
        custom_fields: 自定义字段
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
        获取所有项目信息
        
        API: GetProjectInfo(NumberItems, Item[], Data[]) -> Long
        
        Returns:
            ProjectInfo 对象
        """
        info = cls()
        
        # 获取项目信息
        result = model.GetProjectInfo(0, [], [])
        num_items = com_data(result, 0, 0)
        items = com_data(result, 1, None)
        data = com_data(result, 2, None)
        
        if num_items > 0 and items and data:
            for i in range(num_items):
                item_name = items[i]
                item_data = data[i]
                
                # 映射到属性
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
        
        # 获取用户备注
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
        获取指定项目信息
        
        Args:
            model: SapModel 对象
            item_name: 项目信息名称
            
        Returns:
            项目信息值，不存在返回 None
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
        设置项目信息
        
        API: SetProjectInfo(Item, Data) -> Long
        
        Args:
            model: SapModel 对象
            item_name: 项目信息名称
            data: 项目信息值
            
        Returns:
            0 表示成功
        """
        return model.SetProjectInfo(item_name, data)
    
    @staticmethod
    def get_user_comment(model) -> str:
        """
        获取用户备注
        
        API: GetUserComment(Comment) -> Long
        """
        result = model.GetUserComment("")
        return com_data(result, 0, "")
    
    @staticmethod
    def set_user_comment(model, comment: str) -> int:
        """
        设置用户备注
        
        API: SetUserComment(Comment) -> Long
        """
        return model.SetUserComment(comment)
    
    def save(self, model) -> int:
        """
        保存项目信息到模型
        
        Returns:
            0 表示成功
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
        
        # 保存自定义字段
        for key, value in self.custom_fields.items():
            ret = model.SetProjectInfo(key, value)
        
        # 保存用户备注
        if self.user_comment:
            ret = model.SetUserComment(self.user_comment)
        
        return ret
