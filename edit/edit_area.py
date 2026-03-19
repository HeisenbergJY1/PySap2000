# -*- coding: utf-8 -*-
"""
edit_area.py - 面单元编辑

SAP2000 EditArea API 封装

SAP2000 API:
- EditArea.Divide - 分割面单元
- EditArea.ExpandShrink - 扩展/收缩
- EditArea.Merge - 合并
- EditArea.PointAdd - 添加点
- EditArea.PointRemove - 移除点
- EditArea.ChangeConnectivity - 修改连接
"""

from typing import List
from PySap2000.com_helper import com_ret, com_data


def divide_area(
    model,
    name: str,
    mesh_type: int,
    num_1: int = 2,
    num_2: int = 2,
    max_size_1: float = 0.0,
    max_size_2: float = 0.0,
    constrain_points: bool = True,
    delete_original: bool = True
) -> List[str]:
    """
    分割面单元
    
    Args:
        model: SapModel 对象
        name: 面单元名称
        mesh_type: 网格类型
            0 = 按数量分割
            1 = 按最大尺寸分割
            2 = 按点分割
        num_1: 局部1方向分割数
        num_2: 局部2方向分割数
        max_size_1: 局部1方向最大尺寸
        max_size_2: 局部2方向最大尺寸
        constrain_points: 是否约束到现有点
        delete_original: 是否删除原单元
        
    Returns:
        新创建的面单元名称列表
    """
    result = model.EditArea.Divide(
        name, mesh_type, num_1, num_2, max_size_1, max_size_2,
        constrain_points, delete_original, 0, []
    )
    num = com_data(result, 0, 0)
    names = com_data(result, 1, None)
    if num > 0 and names:
        return list(names)
    return []


def expand_shrink_area(model, name: str, offset: float) -> int:
    """
    扩展或收缩面单元
    
    Args:
        model: SapModel 对象
        name: 面单元名称
        offset: 偏移量（正值扩展，负值收缩）
        
    Returns:
        0 表示成功
    """
    return model.EditArea.ExpandShrink(name, offset)


def merge_area(model, names: List[str], delete_original: bool = True) -> str:
    """
    合并面单元
    
    Args:
        model: SapModel 对象
        names: 要合并的面单元名称列表
        delete_original: 是否删除原单元
        
    Returns:
        新创建的面单元名称
    """
    # COM 签名: Merge(NumberAreas, Names) — 只接受数量和名称数组
    # delete_original 和 NewAreaName 是 comtypes 自动处理的输出参数
    result = model.EditArea.Merge(len(names), names)
    # 返回值中查找新面单元名称（字符串类型的元素）
    if isinstance(result, str) and result:
        return result
    # comtypes 返回 list/tuple 时，遍历查找字符串类型的新名称
    i = 0
    while True:
        item = com_data(result, i, None)
        if item is None:
            break
        if isinstance(item, str) and item:
            return item
        i += 1
    return ""


def add_point_to_area(model, name: str, point_name: str) -> int:
    """
    向面单元添加点
    
    Args:
        model: SapModel 对象
        name: 面单元名称
        point_name: 要添加的点名称
        
    Returns:
        0 表示成功
    """
    return model.EditArea.PointAdd(name, point_name)


def remove_point_from_area(model, name: str, point_name: str) -> int:
    """
    从面单元移除点
    
    Args:
        model: SapModel 对象
        name: 面单元名称
        point_name: 要移除的点名称
        
    Returns:
        0 表示成功
    """
    return model.EditArea.PointRemove(name, point_name)


def change_area_connectivity(
    model,
    name: str,
    point_names: List[str]
) -> int:
    """
    修改面单元连接
    
    Args:
        model: SapModel 对象
        name: 面单元名称
        point_names: 新的点名称列表
        
    Returns:
        0 表示成功
    """
    return model.EditArea.ChangeConnectivity(name, len(point_names), point_names)
