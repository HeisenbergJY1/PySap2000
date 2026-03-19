# -*- coding: utf-8 -*-
"""
area_results.py - 面单元结果函数

SAP2000 Results API 的面单元结果函数封装

SAP2000 API:
- Results.AreaForceShell - 壳单元内力
- Results.AreaJointForcePlane - 平面单元节点力
- Results.AreaJointForceShell - 壳单元节点力
- Results.AreaStrainShell - 壳单元应变
- Results.AreaStrainShellLayered - 分层壳单元应变
- Results.AreaStressPlane - 平面单元应力
- Results.AreaStressShell - 壳单元应力
- Results.AreaStressShellLayered - 分层壳单元应力
"""

from typing import List
from .enums import ItemTypeElm
from .data_classes import (
    AreaForceShellResult,
    AreaJointForcePlaneResult, AreaJointForceShellResult,
    AreaStrainShellResult, AreaStrainShellLayeredResult,
    AreaStressPlaneResult, AreaStressShellResult, AreaStressShellLayeredResult,
)
from PySap2000.com_helper import com_ret, com_data


def get_area_force_shell(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[AreaForceShellResult]:
    """
    获取壳单元内力结果
    
    仅适用于分配了壳截面属性的面单元（不适用于平面或实体属性）。
    返回的内力是单位长度的内力。
    
    Args:
        model: SapModel 对象
        name: 面对象名、面元素名或组名
        item_type: 元素类型
            - OBJECT_ELM: 指定对象对应的元素
            - ELEMENT: 指定元素
            - GROUP_ELM: 组内所有元素
            - SELECTION_ELM: 所有选中元素 (忽略name)
            
    Returns:
        AreaForceShellResult 列表
        
    Example:
        results = get_area_force_shell(model, "1", ItemTypeElm.OBJECT_ELM)
        for r in results:
            print(f"点 {r.point_elm}: F11={r.f11}, M11={r.m11}")
    """
    result = model.Results.AreaForceShell(
        name, int(item_type),
        0, [], [], [], [], [], [],
        [], [], [], [], [], [], [],
        [], [], [], [], [], [], [],
        [], [], [], []
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
        f11 = com_data(result, 7)
        f22 = com_data(result, 8)
        f12 = com_data(result, 9)
        f_max = com_data(result, 10)
        f_min = com_data(result, 11)
        f_angle = com_data(result, 12)
        f_vm = com_data(result, 13)
        m11 = com_data(result, 14)
        m22 = com_data(result, 15)
        m12 = com_data(result, 16)
        m_max = com_data(result, 17)
        m_min = com_data(result, 18)
        m_angle = com_data(result, 19)
        v13 = com_data(result, 20)
        v23 = com_data(result, 21)
        v_max = com_data(result, 22)
        v_angle = com_data(result, 23)
        
        return [
            AreaForceShellResult(
                obj=obj[i] if obj else "",
                elm=elm[i] if elm else "",
                point_elm=point_elm[i] if point_elm else "",
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                f11=f11[i] if f11 else 0.0,
                f22=f22[i] if f22 else 0.0,
                f12=f12[i] if f12 else 0.0,
                f_max=f_max[i] if f_max else 0.0,
                f_min=f_min[i] if f_min else 0.0,
                f_angle=f_angle[i] if f_angle else 0.0,
                f_vm=f_vm[i] if f_vm else 0.0,
                m11=m11[i] if m11 else 0.0,
                m22=m22[i] if m22 else 0.0,
                m12=m12[i] if m12 else 0.0,
                m_max=m_max[i] if m_max else 0.0,
                m_min=m_min[i] if m_min else 0.0,
                m_angle=m_angle[i] if m_angle else 0.0,
                v13=v13[i] if v13 else 0.0,
                v23=v23[i] if v23 else 0.0,
                v_max=v_max[i] if v_max else 0.0,
                v_angle=v_angle[i] if v_angle else 0.0,
            )
            for i in range(num)
        ]
    return []


def get_area_joint_force_plane(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[AreaJointForcePlaneResult]:
    """
    获取平面单元节点力结果
    
    Args:
        model: SapModel 对象
        name: 面对象名、面元素名或组名
        item_type: 元素类型
            
    Returns:
        AreaJointForcePlaneResult 列表
    """
    result = model.Results.AreaJointForcePlane(
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
            AreaJointForcePlaneResult(
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


def get_area_joint_force_shell(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[AreaJointForceShellResult]:
    """
    获取壳单元节点力结果
    
    Args:
        model: SapModel 对象
        name: 面对象名、面元素名或组名
        item_type: 元素类型
            
    Returns:
        AreaJointForceShellResult 列表
    """
    result = model.Results.AreaJointForceShell(
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
            AreaJointForceShellResult(
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


def get_area_strain_shell(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[AreaStrainShellResult]:
    """
    获取壳单元应变结果
    
    Args:
        model: SapModel 对象
        name: 面对象名、面元素名或组名
        item_type: 元素类型
            
    Returns:
        AreaStrainShellResult 列表
    """
    result = model.Results.AreaStrainShell(
        name, int(item_type),
        0, [], [], [], [], [], [],
        [], [], [], [], [], [], [],
        [], [], [], []
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
        e11 = com_data(result, 7)
        e22 = com_data(result, 8)
        g12 = com_data(result, 9)
        e_max = com_data(result, 10)
        e_min = com_data(result, 11)
        e_angle = com_data(result, 12)
        e_vm = com_data(result, 13)
        g13 = com_data(result, 14)
        g23 = com_data(result, 15)
        g_max = com_data(result, 16)
        g_angle = com_data(result, 17)
        
        return [
            AreaStrainShellResult(
                obj=obj[i] if obj else "",
                elm=elm[i] if elm else "",
                point_elm=point_elm[i] if point_elm else "",
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                e11=e11[i] if e11 else 0.0,
                e22=e22[i] if e22 else 0.0,
                g12=g12[i] if g12 else 0.0,
                e_max=e_max[i] if e_max else 0.0,
                e_min=e_min[i] if e_min else 0.0,
                e_angle=e_angle[i] if e_angle else 0.0,
                e_vm=e_vm[i] if e_vm else 0.0,
                g13=g13[i] if g13 else 0.0,
                g23=g23[i] if g23 else 0.0,
                g_max=g_max[i] if g_max else 0.0,
                g_angle=g_angle[i] if g_angle else 0.0,
            )
            for i in range(num)
        ]
    return []


def get_area_strain_shell_layered(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[AreaStrainShellLayeredResult]:
    """
    获取分层壳单元应变结果
    
    Args:
        model: SapModel 对象
        name: 面对象名、面元素名或组名
        item_type: 元素类型
            
    Returns:
        AreaStrainShellLayeredResult 列表
    """
    result = model.Results.AreaStrainShellLayered(
        name, int(item_type),
        0, [], [], [], [], [], [], [], [], [],
        [], [], [], [], [], [], [],
        [], [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        obj = com_data(result, 1)
        elm = com_data(result, 2)
        layer = com_data(result, 3)
        int_pt_num = com_data(result, 4)
        int_pt_loc = com_data(result, 5)
        point_elm = com_data(result, 6)
        load_case = com_data(result, 7)
        step_type = com_data(result, 8)
        step_num = com_data(result, 9)
        e11 = com_data(result, 10)
        e22 = com_data(result, 11)
        g12 = com_data(result, 12)
        e_max = com_data(result, 13)
        e_min = com_data(result, 14)
        e_angle = com_data(result, 15)
        e_vm = com_data(result, 16)
        g13 = com_data(result, 17)
        g23 = com_data(result, 18)
        g_max = com_data(result, 19)
        g_angle = com_data(result, 20)
        
        return [
            AreaStrainShellLayeredResult(
                obj=obj[i] if obj else "",
                elm=elm[i] if elm else "",
                layer=layer[i] if layer else "",
                int_pt_num=int_pt_num[i] if int_pt_num else 0,
                int_pt_loc=int_pt_loc[i] if int_pt_loc else 0.0,
                point_elm=point_elm[i] if point_elm else "",
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                e11=e11[i] if e11 else 0.0,
                e22=e22[i] if e22 else 0.0,
                g12=g12[i] if g12 else 0.0,
                e_max=e_max[i] if e_max else 0.0,
                e_min=e_min[i] if e_min else 0.0,
                e_angle=e_angle[i] if e_angle else 0.0,
                e_vm=e_vm[i] if e_vm else 0.0,
                g13=g13[i] if g13 else 0.0,
                g23=g23[i] if g23 else 0.0,
                g_max=g_max[i] if g_max else 0.0,
                g_angle=g_angle[i] if g_angle else 0.0,
            )
            for i in range(num)
        ]
    return []


def get_area_stress_plane(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[AreaStressPlaneResult]:
    """
    获取平面单元应力结果
    
    Args:
        model: SapModel 对象
        name: 面对象名、面元素名或组名
        item_type: 元素类型
            
    Returns:
        AreaStressPlaneResult 列表
    """
    result = model.Results.AreaStressPlane(
        name, int(item_type),
        0, [], [], [], [], [], [],
        [], [], [], [], [], [], [], []
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
        s11 = com_data(result, 7)
        s22 = com_data(result, 8)
        s33 = com_data(result, 9)
        s12 = com_data(result, 10)
        s_max = com_data(result, 11)
        s_min = com_data(result, 12)
        s_angle = com_data(result, 13)
        s_vm = com_data(result, 14)
        
        return [
            AreaStressPlaneResult(
                obj=obj[i] if obj else "",
                elm=elm[i] if elm else "",
                point_elm=point_elm[i] if point_elm else "",
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                s11=s11[i] if s11 else 0.0,
                s22=s22[i] if s22 else 0.0,
                s33=s33[i] if s33 else 0.0,
                s12=s12[i] if s12 else 0.0,
                s_max=s_max[i] if s_max else 0.0,
                s_min=s_min[i] if s_min else 0.0,
                s_angle=s_angle[i] if s_angle else 0.0,
                s_vm=s_vm[i] if s_vm else 0.0,
            )
            for i in range(num)
        ]
    return []


def get_area_stress_shell(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[AreaStressShellResult]:
    """
    获取壳单元应力结果
    
    Args:
        model: SapModel 对象
        name: 面对象名、面元素名或组名
        item_type: 元素类型
            
    Returns:
        AreaStressShellResult 列表
    """
    result = model.Results.AreaStressShell(
        name, int(item_type),
        0, [], [], [], [], [], [],
        [], [], [], [], [], [], [],
        [], [], [], [], [], [], [],
        [], [], [], []
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
        s11_top = com_data(result, 7)
        s22_top = com_data(result, 8)
        s12_top = com_data(result, 9)
        s_max_top = com_data(result, 10)
        s_min_top = com_data(result, 11)
        s_angle_top = com_data(result, 12)
        s_vm_top = com_data(result, 13)
        s11_bot = com_data(result, 14)
        s22_bot = com_data(result, 15)
        s12_bot = com_data(result, 16)
        s_max_bot = com_data(result, 17)
        s_min_bot = com_data(result, 18)
        s_angle_bot = com_data(result, 19)
        s_vm_bot = com_data(result, 20)
        s13_avg = com_data(result, 21)
        s23_avg = com_data(result, 22)
        s_max_avg = com_data(result, 23)
        s_angle_avg = com_data(result, 24)
        
        return [
            AreaStressShellResult(
                obj=obj[i] if obj else "",
                elm=elm[i] if elm else "",
                point_elm=point_elm[i] if point_elm else "",
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                s11_top=s11_top[i] if s11_top else 0.0,
                s22_top=s22_top[i] if s22_top else 0.0,
                s12_top=s12_top[i] if s12_top else 0.0,
                s_max_top=s_max_top[i] if s_max_top else 0.0,
                s_min_top=s_min_top[i] if s_min_top else 0.0,
                s_angle_top=s_angle_top[i] if s_angle_top else 0.0,
                s_vm_top=s_vm_top[i] if s_vm_top else 0.0,
                s11_bot=s11_bot[i] if s11_bot else 0.0,
                s22_bot=s22_bot[i] if s22_bot else 0.0,
                s12_bot=s12_bot[i] if s12_bot else 0.0,
                s_max_bot=s_max_bot[i] if s_max_bot else 0.0,
                s_min_bot=s_min_bot[i] if s_min_bot else 0.0,
                s_angle_bot=s_angle_bot[i] if s_angle_bot else 0.0,
                s_vm_bot=s_vm_bot[i] if s_vm_bot else 0.0,
                s13_avg=s13_avg[i] if s13_avg else 0.0,
                s23_avg=s23_avg[i] if s23_avg else 0.0,
                s_max_avg=s_max_avg[i] if s_max_avg else 0.0,
                s_angle_avg=s_angle_avg[i] if s_angle_avg else 0.0,
            )
            for i in range(num)
        ]
    return []


def get_area_stress_shell_layered(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[AreaStressShellLayeredResult]:
    """
    获取分层壳单元应力结果
    
    Args:
        model: SapModel 对象
        name: 面对象名、面元素名或组名
        item_type: 元素类型
            
    Returns:
        AreaStressShellLayeredResult 列表
    """
    result = model.Results.AreaStressShellLayered(
        name, int(item_type),
        0, [], [], [], [], [], [], [], [], [],
        [], [], [], [], [], [], [],
        [], [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        obj = com_data(result, 1)
        elm = com_data(result, 2)
        layer = com_data(result, 3)
        int_pt_num = com_data(result, 4)
        int_pt_loc = com_data(result, 5)
        point_elm = com_data(result, 6)
        load_case = com_data(result, 7)
        step_type = com_data(result, 8)
        step_num = com_data(result, 9)
        s11 = com_data(result, 10)
        s22 = com_data(result, 11)
        s12 = com_data(result, 12)
        s_max = com_data(result, 13)
        s_min = com_data(result, 14)
        s_angle = com_data(result, 15)
        s_vm = com_data(result, 16)
        s13 = com_data(result, 17)
        s23 = com_data(result, 18)
        s_max_shear = com_data(result, 19)
        s_angle_shear = com_data(result, 20)
        
        return [
            AreaStressShellLayeredResult(
                obj=obj[i] if obj else "",
                elm=elm[i] if elm else "",
                layer=layer[i] if layer else "",
                int_pt_num=int_pt_num[i] if int_pt_num else 0,
                int_pt_loc=int_pt_loc[i] if int_pt_loc else 0.0,
                point_elm=point_elm[i] if point_elm else "",
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                s11=s11[i] if s11 else 0.0,
                s22=s22[i] if s22 else 0.0,
                s12=s12[i] if s12 else 0.0,
                s_max=s_max[i] if s_max else 0.0,
                s_min=s_min[i] if s_min else 0.0,
                s_angle=s_angle[i] if s_angle else 0.0,
                s_vm=s_vm[i] if s_vm else 0.0,
                s13=s13[i] if s13 else 0.0,
                s23=s23[i] if s23 else 0.0,
                s_max_shear=s_max_shear[i] if s_max_shear else 0.0,
                s_angle_shear=s_angle_shear[i] if s_angle_shear else 0.0,
            )
            for i in range(num)
        ]
    return []
