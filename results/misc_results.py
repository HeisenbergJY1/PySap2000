# -*- coding: utf-8 -*-
"""
misc_results.py - 杂项结果函数

SAP2000 Results API 的杂项结果函数封装

SAP2000 API:
- Results.AssembledJointMass_1 - 组装节点质量
- Results.BaseReactWithCentroid - 带质心的基底反力
- Results.BucklingFactor - 屈曲因子
- Results.GeneralizedDispl - 广义位移
- Results.PanelZoneDeformation - 节点域变形
- Results.PanelZoneForce - 节点域内力
- Results.SectionCutAnalysis - 截面切割分析结果
- Results.SectionCutDesign - 截面切割设计结果
- Results.StepLabel - 步骤标签
"""

from typing import List
from .enums import ItemTypeElm
from .data_classes import (
    AssembledJointMassResult, BaseReactWithCentroidResult, BucklingFactorResult,
    GeneralizedDisplResult, PanelZoneDeformationResult, PanelZoneForceResult,
    SectionCutAnalysisResult, SectionCutDesignResult, StepLabelResult,
)
from PySap2000.com_helper import com_ret, com_data


def get_assembled_joint_mass(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[AssembledJointMassResult]:
    """
    获取组装节点质量
    
    Args:
        model: SapModel 对象
        name: 点对象名、点元素名或组名
        item_type: 元素类型
            
    Returns:
        AssembledJointMassResult 列表
    """
    result = model.Results.AssembledJointMass_1(
        name, int(item_type),
        0, [], [],
        [], [], [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    if isinstance(num, (list, tuple)):
        num = num[0] if num else 0
    num = int(num) if num else 0
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        obj = com_data(result, 1)
        elm = com_data(result, 2)
        u1 = com_data(result, 3)
        u2 = com_data(result, 4)
        u3 = com_data(result, 5)
        r1 = com_data(result, 6)
        r2 = com_data(result, 7)
        r3 = com_data(result, 8)
        
        return [
            AssembledJointMassResult(
                obj=obj[i] if obj else "",
                elm=elm[i] if elm else "",
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


def get_base_react_with_centroid(model) -> List[BaseReactWithCentroidResult]:
    """
    获取带质心的基底反力
    
    Args:
        model: SapModel 对象
        
    Returns:
        BaseReactWithCentroidResult 列表
    """
    result = model.Results.BaseReactWithCentroid(
        0, [], [], [],
        [], [], [], [], [], [],
        0.0, 0.0, 0.0,
        [], [], [],
        [], [], [],
        [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if (ret == 0 or ret == num) and num > 0:
        load_case = com_data(result, 1)
        step_type = com_data(result, 2)
        step_num = com_data(result, 3)
        fx = com_data(result, 4)
        fy = com_data(result, 5)
        fz = com_data(result, 6)
        mx = com_data(result, 7)
        my = com_data(result, 8)
        mz = com_data(result, 9)
        gx = com_data(result, 10, 0.0)
        gy = com_data(result, 11, 0.0)
        gz = com_data(result, 12, 0.0)
        xcentroid_fx = com_data(result, 13)
        ycentroid_fx = com_data(result, 14)
        zcentroid_fx = com_data(result, 15)
        xcentroid_fy = com_data(result, 16)
        ycentroid_fy = com_data(result, 17)
        zcentroid_fy = com_data(result, 18)
        xcentroid_fz = com_data(result, 19)
        ycentroid_fz = com_data(result, 20)
        zcentroid_fz = com_data(result, 21)
        
        return [
            BaseReactWithCentroidResult(
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                fx=fx[i] if fx else 0.0,
                fy=fy[i] if fy else 0.0,
                fz=fz[i] if fz else 0.0,
                mx=mx[i] if mx else 0.0,
                my=my[i] if my else 0.0,
                mz=mz[i] if mz else 0.0,
                gx=gx if isinstance(gx, (int, float)) else 0.0,
                gy=gy if isinstance(gy, (int, float)) else 0.0,
                gz=gz if isinstance(gz, (int, float)) else 0.0,
                xcentroid_fx=xcentroid_fx[i] if xcentroid_fx else 0.0,
                ycentroid_fx=ycentroid_fx[i] if ycentroid_fx else 0.0,
                zcentroid_fx=zcentroid_fx[i] if zcentroid_fx else 0.0,
                xcentroid_fy=xcentroid_fy[i] if xcentroid_fy else 0.0,
                ycentroid_fy=ycentroid_fy[i] if ycentroid_fy else 0.0,
                zcentroid_fy=zcentroid_fy[i] if zcentroid_fy else 0.0,
                xcentroid_fz=xcentroid_fz[i] if xcentroid_fz else 0.0,
                ycentroid_fz=ycentroid_fz[i] if ycentroid_fz else 0.0,
                zcentroid_fz=zcentroid_fz[i] if zcentroid_fz else 0.0,
            )
            for i in range(num)
        ]
    return []


def get_buckling_factor(model) -> List[BucklingFactorResult]:
    """
    获取屈曲因子
    
    Args:
        model: SapModel 对象
        
    Returns:
        BucklingFactorResult 列表
    """
    result = model.Results.BucklingFactor(
        0, [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if (ret == 0 or ret == num) and num > 0:
        load_case = com_data(result, 1)
        step_type = com_data(result, 2)
        step_num = com_data(result, 3)
        factor = com_data(result, 4)
        
        return [
            BucklingFactorResult(
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                factor=factor[i] if factor else 0.0,
            )
            for i in range(num)
        ]
    return []


def get_generalized_displ(model, name: str) -> List[GeneralizedDisplResult]:
    """
    获取广义位移结果
    
    Args:
        model: SapModel 对象
        name: 广义位移名称
        
    Returns:
        GeneralizedDisplResult 列表
    """
    result = model.Results.GeneralizedDispl(
        name,
        0, [], [], [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        gd_name = com_data(result, 1)
        load_case = com_data(result, 2)
        step_type = com_data(result, 3)
        step_num = com_data(result, 4)
        dof_type = com_data(result, 5)
        value = com_data(result, 6)
        
        return [
            GeneralizedDisplResult(
                name=gd_name[i] if gd_name else "",
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                dof_type=dof_type[i] if dof_type else "",
                value=value[i] if value else 0.0,
            )
            for i in range(num)
        ]
    return []


def get_panel_zone_deformation(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[PanelZoneDeformationResult]:
    """
    获取节点域变形结果
    
    Args:
        model: SapModel 对象
        name: 元素名或组名
        item_type: 元素类型
            
    Returns:
        PanelZoneDeformationResult 列表
    """
    result = model.Results.PanelZoneDeformation(
        name, int(item_type),
        0, [], [], [], [],
        [], [], [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        elm = com_data(result, 1)
        load_case = com_data(result, 2)
        step_type = com_data(result, 3)
        step_num = com_data(result, 4)
        u1 = com_data(result, 5)
        u2 = com_data(result, 6)
        u3 = com_data(result, 7)
        r1 = com_data(result, 8)
        r2 = com_data(result, 9)
        r3 = com_data(result, 10)
        
        return [
            PanelZoneDeformationResult(
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


def get_panel_zone_force(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
) -> List[PanelZoneForceResult]:
    """
    获取节点域内力结果
    
    Args:
        model: SapModel 对象
        name: 元素名或组名
        item_type: 元素类型
            
    Returns:
        PanelZoneForceResult 列表
    """
    result = model.Results.PanelZoneForce(
        name, int(item_type),
        0, [], [], [], [],
        [], [], [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        elm = com_data(result, 1)
        load_case = com_data(result, 2)
        step_type = com_data(result, 3)
        step_num = com_data(result, 4)
        p = com_data(result, 5)
        v2 = com_data(result, 6)
        v3 = com_data(result, 7)
        t = com_data(result, 8)
        m2 = com_data(result, 9)
        m3 = com_data(result, 10)
        
        return [
            PanelZoneForceResult(
                elm=elm[i] if elm else "",
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


def get_section_cut_analysis(model, name: str) -> List[SectionCutAnalysisResult]:
    """
    获取截面切割分析结果
    
    Args:
        model: SapModel 对象
        name: 截面切割名称
        
    Returns:
        SectionCutAnalysisResult 列表
    """
    result = model.Results.SectionCutAnalysis(
        name,
        0, [], [], [], [],
        [], [], [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        sc_name = com_data(result, 1)
        load_case = com_data(result, 2)
        step_type = com_data(result, 3)
        step_num = com_data(result, 4)
        f1 = com_data(result, 5)
        f2 = com_data(result, 6)
        f3 = com_data(result, 7)
        m1 = com_data(result, 8)
        m2 = com_data(result, 9)
        m3 = com_data(result, 10)
        
        return [
            SectionCutAnalysisResult(
                name=sc_name[i] if sc_name else "",
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


def get_section_cut_design(model, name: str) -> List[SectionCutDesignResult]:
    """
    获取截面切割设计结果
    
    Args:
        model: SapModel 对象
        name: 截面切割名称
        
    Returns:
        SectionCutDesignResult 列表
    """
    result = model.Results.SectionCutDesign(
        name,
        0, [], [], [], [],
        [], [], [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        sc_name = com_data(result, 1)
        load_case = com_data(result, 2)
        step_type = com_data(result, 3)
        step_num = com_data(result, 4)
        p = com_data(result, 5)
        v2 = com_data(result, 6)
        v3 = com_data(result, 7)
        t = com_data(result, 8)
        m2 = com_data(result, 9)
        m3 = com_data(result, 10)
        
        return [
            SectionCutDesignResult(
                name=sc_name[i] if sc_name else "",
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


def get_step_label(model, load_case: str) -> List[StepLabelResult]:
    """
    获取步骤标签
    
    Args:
        model: SapModel 对象
        load_case: 工况名称
        
    Returns:
        StepLabelResult 列表
    """
    result = model.Results.StepLabel(
        load_case,
        0, [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if ret == 0 and num > 0:
        step_num = com_data(result, 1)
        label = com_data(result, 2)
        
        return [
            StepLabelResult(
                load_case=load_case,
                step_num=step_num[i] if step_num else 0,
                label=label[i] if label else "",
            )
            for i in range(num)
        ]
    return []
