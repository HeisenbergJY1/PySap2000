# -*- coding: utf-8 -*-
"""
frame_results.py - Frame result helpers.

Wraps frame-result functions from the SAP2000 Results API.

SAP2000 API:
- `Results.FrameForce` - frame internal forces
- `Results.FrameJointForce` - frame joint forces
"""

from typing import List
from .enums import ItemTypeElm
from .data_classes import FrameForceResult, FrameJointForceResult
from PySap2000.com_helper import com_ret, com_data


def get_frame_force(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[FrameForceResult]:
    """
    Get internal force results for frame elements.
    
    Args:
        model: SAP2000 SapModel object
        name: Line object name, line element name, or group name
        item_type: Element scope
            - `OBJECT_ELM`: elements associated with the specified object
            - `ELEMENT`: the specified element
            - `GROUP_ELM`: all elements in the group
            - `SELECTION_ELM`: all selected elements, ignoring `name`
            
    Returns:
        List of `FrameForceResult`.
        
    Example:
        # Get internal forces for a single frame object
        results = get_frame_force(model, "1", ItemTypeElm.OBJECT_ELM)
        for r in results:
            print(f"Station: {r.obj_sta}, P={r.p}, V2={r.v2}, M3={r.m3}")
        
        # Get internal forces for all frame objects
        results = get_frame_force(model, "ALL", ItemTypeElm.GROUP_ELM)
    """
    result = model.Results.FrameForce(
        name, int(item_type),
        0, [], [], [], [], [], [], [],
        [], [], [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        obj = com_data(result, 1)
        obj_sta = com_data(result, 2)
        elm = com_data(result, 3)
        elm_sta = com_data(result, 4)
        load_case = com_data(result, 5)
        step_type = com_data(result, 6)
        step_num = com_data(result, 7)
        p = com_data(result, 8)
        v2 = com_data(result, 9)
        v3 = com_data(result, 10)
        t = com_data(result, 11)
        m2 = com_data(result, 12)
        m3 = com_data(result, 13)
        
        return [
            FrameForceResult(
                obj=obj[i] if obj else "",
                obj_sta=obj_sta[i] if obj_sta else 0.0,
                elm=elm[i] if elm else "",
                elm_sta=elm_sta[i] if elm_sta else 0.0,
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


def get_frame_joint_force(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[FrameJointForceResult]:
    """
    Get joint force results for frame elements.
    
    Args:
        model: SAP2000 SapModel object
        name: Line object name, line element name, or group name
        item_type: Element scope
            
    Returns:
        List of `FrameJointForceResult`.
    """
    result = model.Results.FrameJointForce(
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
            FrameJointForceResult(
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
