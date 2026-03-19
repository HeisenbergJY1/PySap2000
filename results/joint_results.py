# -*- coding: utf-8 -*-
"""
joint_results.py - 节点结果函数

SAP2000 Results API 的节点结果函数封装

SAP2000 API:
- Results.JointDispl - 节点位移
- Results.JointDisplAbs - 节点绝对位移
- Results.JointReact - 节点反力
- Results.JointAcc - 节点加速度
- Results.JointAccAbs - 节点绝对加速度
- Results.JointVel - 节点速度
- Results.JointVelAbs - 节点绝对速度
- Results.JointRespSpec - 节点反应谱
"""

from typing import List
from .enums import ItemTypeElm
from .data_classes import (
    JointDisplResult, JointReactResult,
    JointDisplAbsResult, JointAccResult, JointAccAbsResult,
    JointVelResult, JointVelAbsResult, JointRespSpecResult,
)
from PySap2000.com_helper import com_ret, com_data


def get_joint_displ(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[JointDisplResult]:
    """
    获取节点位移结果
    
    Args:
        model: SapModel 对象
        name: 点对象名、点元素名或组名
        item_type: 元素类型
            - OBJECT_ELM: 指定对象对应的元素
            - ELEMENT: 指定元素
            - GROUP_ELM: 组内所有元素
            - SELECTION_ELM: 所有选中元素 (忽略name)
            
    Returns:
        JointDisplResult 列表
        
    Example:
        # 获取单个点的位移
        results = get_joint_displ(model, "1", ItemTypeElm.OBJECT_ELM)
        
        # 获取所有点的位移
        results = get_joint_displ(model, "ALL", ItemTypeElm.GROUP_ELM)
        
        # 获取选中点的位移
        results = get_joint_displ(model, "", ItemTypeElm.SELECTION_ELM)
    """
    result = model.Results.JointDispl(
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
            JointDisplResult(
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


def get_joint_react(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[JointReactResult]:
    """
    获取节点反力结果
    
    反力来自约束、弹簧和接地连接单元。
    
    Args:
        model: SapModel 对象
        name: 点对象名、点元素名或组名
        item_type: 元素类型
            
    Returns:
        JointReactResult 列表
        
    Example:
        # 获取单个支座的反力
        results = get_joint_react(model, "1", ItemTypeElm.OBJECT_ELM)
        
        # 获取所有支座的反力
        results = get_joint_react(model, "ALL", ItemTypeElm.GROUP_ELM)
    """
    result = model.Results.JointReact(
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
        f1 = com_data(result, 6)
        f2 = com_data(result, 7)
        f3 = com_data(result, 8)
        m1 = com_data(result, 9)
        m2 = com_data(result, 10)
        m3 = com_data(result, 11)
        
        return [
            JointReactResult(
                obj=obj[i] if obj else "",
                elm=elm[i] if elm else "",
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


def get_joint_displ_abs(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[JointDisplAbsResult]:
    """
    获取节点绝对位移结果（用于多支座激励分析）
    
    Args:
        model: SapModel 对象
        name: 点对象名、点元素名或组名
        item_type: 元素类型
            
    Returns:
        JointDisplAbsResult 列表
    """
    result = model.Results.JointDisplAbs(
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
            JointDisplAbsResult(
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


def get_joint_acc(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[JointAccResult]:
    """
    获取节点加速度结果
    
    Args:
        model: SapModel 对象
        name: 点对象名、点元素名或组名
        item_type: 元素类型
            
    Returns:
        JointAccResult 列表
    """
    result = model.Results.JointAcc(
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
            JointAccResult(
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


def get_joint_acc_abs(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[JointAccAbsResult]:
    """
    获取节点绝对加速度结果（用于多支座激励分析）
    
    Args:
        model: SapModel 对象
        name: 点对象名、点元素名或组名
        item_type: 元素类型
            
    Returns:
        JointAccAbsResult 列表
    """
    result = model.Results.JointAccAbs(
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
            JointAccAbsResult(
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


def get_joint_vel(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[JointVelResult]:
    """
    获取节点速度结果
    
    Args:
        model: SapModel 对象
        name: 点对象名、点元素名或组名
        item_type: 元素类型
            
    Returns:
        JointVelResult 列表
    """
    result = model.Results.JointVel(
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
            JointVelResult(
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


def get_joint_vel_abs(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[JointVelAbsResult]:
    """
    获取节点绝对速度结果（用于多支座激励分析）
    
    Args:
        model: SapModel 对象
        name: 点对象名、点元素名或组名
        item_type: 元素类型
            
    Returns:
        JointVelAbsResult 列表
    """
    result = model.Results.JointVelAbs(
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
            JointVelAbsResult(
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


def get_joint_resp_spec(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[JointRespSpecResult]:
    """
    获取节点反应谱结果
    
    Args:
        model: SapModel 对象
        name: 点对象名、点元素名或组名
        item_type: 元素类型
            
    Returns:
        JointRespSpecResult 列表
    """
    result = model.Results.JointRespSpec(
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
            JointRespSpecResult(
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
