# -*- coding: utf-8 -*-
"""
edit_solid.py - 实体编辑

SAP2000 EditSolid API 封装

SAP2000 API:
- EditSolid.Divide - 分割实体
"""

from typing import List
from PySap2000.com_helper import com_ret, com_data


def divide_solid(
    model,
    name: str,
    num_1: int = 2,
    num_2: int = 2,
    num_3: int = 2
) -> List[str]:
    """
    分割实体单元
    
    Args:
        model: SapModel 对象
        name: 实体名称
        num_1: 局部1方向分割数
        num_2: 局部2方向分割数
        num_3: 局部3方向分割数
        
    Returns:
        新创建的实体名称列表
    """
    result = model.EditSolid.Divide(name, num_1, num_2, num_3, 0, [])
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []
