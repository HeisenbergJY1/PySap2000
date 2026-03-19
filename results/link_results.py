# -*- coding: utf-8 -*-
"""
link_results.py - 连接单元结果函数

SAP2000 Results API 的连接单元结果函数封装

SAP2000 API:
- Results.LinkDeformation - 连接单元变形
- Results.LinkForce - 连接单元内力
- Results.LinkJointForce - 连接单元节点力
"""

from typing import List
from .enums import ItemTypeElm
from .data_classes import LinkDeformationResult, LinkForceResult, LinkJointForceResult
from PySap2000.com_helper import com_ret, com_data


def get_link_deformation(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[LinkDeformationResult]:
    """
    获取连接单元变形结果
    
    Args:
        model: SapModel 对象
        name: 连接对象名、连接元素名或组名
        item_type: 元素类型
            
    Returns:
        LinkDeformationResult 列表
    """
    result = model.Results.LinkDeformation(
        name, int(item_type),
        0, [], [], [], [], [],
        [], [], [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        obj = com_data(result, 1)
        elm = com_data(result, 2)
        load_case = com_data(result, 3)
        step_type = com_data(result, 4)
        step_num = com_data(result, 5)
        u1 = com_data(result, 6)
        u2 = com_data(result, 7)
        u3 = com_data(result, 8)
        r1 = com_data(result, 9)
        r2 = com_data(result, 10)
        r3 = com_data(result, 11)
        
        return [
            LinkDeformationResult(
                obj=obj[i] if obj else "",
                elm=elm[i] if elm else "",
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                u1=u1[i] if u1 else 0.0,
                u2=u2[i] if u2 else 0.0,
                u3=u3[i] if u3 else 0.0,
                r1=r1[i] if r1 else 0.0,
                r2=r2[i] if r2 else 0.0,
                r3=r3[i] if r3 else 0.0,
            )
            for i in range(num)
        ]
    return []


def get_link_force(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[LinkForceResult]:
    """
    获取连接单元内力结果
    
    Args:
        model: SapModel 对象
        name: 连接对象名、连接元素名或组名
        item_type: 元素类型
            
    Returns:
        LinkForceResult 列表
    """
    result = model.Results.LinkForce(
        name, int(item_type),
        0, [], [], [], [], [], [],
        [], [], [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        obj = com_data(result, 1)
        elm = com_data(result, 2)
        point_elm = com_data(result, 3)
        load_case = com_data(result, 4)
        step_type = com_data(result, 5)
        step_num = com_data(result, 6)
        p = com_data(result, 7)
        v2 = com_data(result, 8)
        v3 = com_data(result, 9)
        t = com_data(result, 10)
        m2 = com_data(result, 11)
        m3 = com_data(result, 12)
        
        return [
            LinkForceResult(
                obj=obj[i] if obj else "",
                elm=elm[i] if elm else "",
                point_elm=point_elm[i] if point_elm else "",
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                p=p[i] if p else 0.0,
                v2=v2[i] if v2 else 0.0,
                v3=v3[i] if v3 else 0.0,
                t=t[i] if t else 0.0,
                m2=m2[i] if m2 else 0.0,
                m3=m3[i] if m3 else 0.0,
            )
            for i in range(num)
        ]
    return []


def get_link_joint_force(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[LinkJointForceResult]:
    """
    获取连接单元节点力结果
    
    Args:
        model: SapModel 对象
        name: 连接对象名、连接元素名或组名
        item_type: 元素类型
            
    Returns:
        LinkJointForceResult 列表
    """
    result = model.Results.LinkJointForce(
        name, int(item_type),
        0, [], [], [], [], [], [],
        [], [], [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        obj = com_data(result, 1)
        elm = com_data(result, 2)
        point_elm = com_data(result, 3)
        load_case = com_data(result, 4)
        step_type = com_data(result, 5)
        step_num = com_data(result, 6)
        f1 = com_data(result, 7)
        f2 = com_data(result, 8)
        f3 = com_data(result, 9)
        m1 = com_data(result, 10)
        m2 = com_data(result, 11)
        m3 = com_data(result, 12)
        
        return [
            LinkJointForceResult(
                obj=obj[i] if obj else "",
                elm=elm[i] if elm else "",
                point_elm=point_elm[i] if point_elm else "",
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                f1=f1[i] if f1 else 0.0,
                f2=f2[i] if f2 else 0.0,
                f3=f3[i] if f3 else 0.0,
                m1=m1[i] if m1 else 0.0,
                m2=m2[i] if m2 else 0.0,
                m3=m3[i] if m3 else 0.0,
            )
            for i in range(num)
        ]
    return []
