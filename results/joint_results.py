# -*- coding: utf-8 -*-
"""
joint_results.py - Joint result helpers.

Wraps joint-result functions from the SAP2000 Results API.

SAP2000 API:
- `Results.JointDispl` - joint displacements
- `Results.JointDisplAbs` - absolute joint displacements
- `Results.JointReact` - joint reactions
- `Results.JointAcc` - joint accelerations
- `Results.JointAccAbs` - absolute joint accelerations
- `Results.JointVel` - joint velocities
- `Results.JointVelAbs` - absolute joint velocities
- `Results.JointRespSpec` - joint response spectrum results
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
    Get joint displacement results.
    
    Args:
        model: SAP2000 SapModel object
        name: Point object name, point element name, or group name
        item_type: Element scope
            - `OBJECT_ELM`: elements associated with the specified object
            - `ELEMENT`: the specified element
            - `GROUP_ELM`: all elements in the group
            - `SELECTION_ELM`: all selected elements, ignoring `name`
            
    Returns:
        List of `JointDisplResult`.
        
    Example:
        # Get displacement for a single point
        results = get_joint_displ(model, "1", ItemTypeElm.OBJECT_ELM)
        
        # Get displacements for all points
        results = get_joint_displ(model, "ALL", ItemTypeElm.GROUP_ELM)
        
        # Get displacements for selected points
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
    Get joint reaction results.

    Reactions come from restraints, springs, and grounded link elements.
    
    Args:
        model: SAP2000 SapModel object
        name: Point object name, point element name, or group name
        item_type: Element scope
            
    Returns:
        List of `JointReactResult`.
        
    Example:
        # Get reactions for a single support point
        results = get_joint_react(model, "1", ItemTypeElm.OBJECT_ELM)
        
        # Get reactions for all support points
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
    Get absolute joint displacement results, typically for multi-support excitation.
    
    Args:
        model: SAP2000 SapModel object
        name: Point object name, point element name, or group name
        item_type: Element scope
            
    Returns:
        List of `JointDisplAbsResult`.
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
    Get joint acceleration results.
    
    Args:
        model: SAP2000 SapModel object
        name: Point object name, point element name, or group name
        item_type: Element scope
            
    Returns:
        List of `JointAccResult`.
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
    Get absolute joint acceleration results, typically for multi-support excitation.
    
    Args:
        model: SAP2000 SapModel object
        name: Point object name, point element name, or group name
        item_type: Element scope
            
    Returns:
        List of `JointAccAbsResult`.
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
    Get joint velocity results.
    
    Args:
        model: SAP2000 SapModel object
        name: Point object name, point element name, or group name
        item_type: Element scope
            
    Returns:
        List of `JointVelResult`.
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
    Get absolute joint velocity results, typically for multi-support excitation.
    
    Args:
        model: SAP2000 SapModel object
        name: Point object name, point element name, or group name
        item_type: Element scope
            
    Returns:
        List of `JointVelAbsResult`.
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
    Get joint response spectrum results.
    
    Args:
        model: SAP2000 SapModel object
        name: Point object name, point element name, or group name
        item_type: Element scope
            
    Returns:
        List of `JointRespSpecResult`.
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
