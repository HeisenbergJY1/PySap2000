# -*- coding: utf-8 -*-
"""
modal_results.py - Modal analysis result helpers.

Wraps modal-analysis result functions from the SAP2000 Results API.

SAP2000 API:
- `Results.ModalPeriod` - modal periods
- `Results.ModeShape` - mode shapes
- `Results.ModalParticipatingMassRatios` - modal participating mass ratios
- `Results.ModalLoadParticipationRatios` - modal load participation ratios
- `Results.ModalParticipationFactors` - modal participation factors
"""

from typing import List
from .enums import ItemTypeElm
from .data_classes import (
    ModalPeriodResult, ModeShapeResult, ModalMassRatioResult,
    ModalLoadParticipationRatioResult, ModalParticipationFactorResult,
)
from PySap2000.com_helper import com_ret, com_data


def get_modal_period(model) -> List[ModalPeriodResult]:
    """
    Get modal period results.

    Returns period, frequency, and eigenvalue data for all selected modal cases.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        List of `ModalPeriodResult`.
        
    Example:
        from results import deselect_all_cases_and_combos, set_case_selected_for_output
        
        deselect_all_cases_and_combos(model)
        set_case_selected_for_output(model, "MODAL")
        
        results = get_modal_period(model)
        for r in results:
            print(f"Mode {int(r.step_num)}: T={r.period:.3f}s, f={r.frequency:.3f}Hz")
    """
    result = model.Results.ModalPeriod(
        0, [], [], [],
        [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if (ret == 0 or ret == num) and num > 0:
        load_case = com_data(result, 1)
        step_type = com_data(result, 2)
        step_num = com_data(result, 3)
        period = com_data(result, 4)
        frequency = com_data(result, 5)
        circ_freq = com_data(result, 6)
        eigenvalue = com_data(result, 7)
        
        return [
            ModalPeriodResult(
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                period=period[i] if period else 0.0,
                frequency=frequency[i] if frequency else 0.0,
                circ_freq=circ_freq[i] if circ_freq else 0.0,
                eigenvalue=eigenvalue[i] if eigenvalue else 0.0,
            )
            for i in range(num)
        ]
    return []


def get_mode_shape(
    model,
    name: str,
    item_type: ItemTypeElm = ItemTypeElm.GROUP_ELM
) -> List[ModeShapeResult]:
    """
    Get mode shape results.
    
    Args:
        model: SAP2000 SapModel object
        name: Point object name, point element name, or group name
        item_type: Element scope
            
    Returns:
        List of `ModeShapeResult`.
        
    Example:
        from results import deselect_all_cases_and_combos, set_case_selected_for_output
        
        deselect_all_cases_and_combos(model)
        set_case_selected_for_output(model, "MODAL")
        
        # Get mode shapes for all points
        results = get_mode_shape(model, "ALL", ItemTypeElm.GROUP_ELM)
    """
    result = model.Results.ModeShape(
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
            ModeShapeResult(
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


def get_modal_participating_mass_ratios(model) -> List[ModalMassRatioResult]:
    """
    Get modal participating mass ratios.

    Returns participating mass ratios and cumulative ratios for each mode.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        List of `ModalMassRatioResult`.
        
    Example:
        results = get_modal_participating_mass_ratios(model)
        for r in results:
            print(f"Mode {int(r.step_num)}: "
                  f"Ux={r.ux:.2%}, Uy={r.uy:.2%}, Uz={r.uz:.2%}, "
                  f"SumUx={r.sum_ux:.2%}")
    """
    result = model.Results.ModalParticipatingMassRatios(
        0, [], [], [],
        [],
        [], [], [], [], [], [],
        [], [], [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if (ret == 0 or ret == num) and num > 0:
        load_case = com_data(result, 1)
        step_type = com_data(result, 2)
        step_num = com_data(result, 3)
        period = com_data(result, 4)
        ux = com_data(result, 5)
        uy = com_data(result, 6)
        uz = com_data(result, 7)
        sum_ux = com_data(result, 8)
        sum_uy = com_data(result, 9)
        sum_uz = com_data(result, 10)
        rx = com_data(result, 11)
        ry = com_data(result, 12)
        rz = com_data(result, 13)
        sum_rx = com_data(result, 14)
        sum_ry = com_data(result, 15)
        sum_rz = com_data(result, 16)
        
        return [
            ModalMassRatioResult(
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                period=period[i] if period else 0.0,
                ux=ux[i] if ux else 0.0,
                uy=uy[i] if uy else 0.0,
                uz=uz[i] if uz else 0.0,
                sum_ux=sum_ux[i] if sum_ux else 0.0,
                sum_uy=sum_uy[i] if sum_uy else 0.0,
                sum_uz=sum_uz[i] if sum_uz else 0.0,
                rx=rx[i] if rx else 0.0,
                ry=ry[i] if ry else 0.0,
                rz=rz[i] if rz else 0.0,
                sum_rx=sum_rx[i] if sum_rx else 0.0,
                sum_ry=sum_ry[i] if sum_ry else 0.0,
                sum_rz=sum_rz[i] if sum_rz else 0.0,
            )
            for i in range(num)
        ]
    return []


def get_modal_load_participation_ratios(model) -> List[ModalLoadParticipationRatioResult]:
    """
    Get modal load participation ratios.

    Returns static and dynamic participation ratios for each load pattern.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        List of `ModalLoadParticipationRatioResult`.
    """
    result = model.Results.ModalLoadParticipationRatios(
        0, [], [], [], [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if (ret == 0 or ret == num) and num > 0:
        load_case = com_data(result, 1)
        item_type = com_data(result, 2)
        item = com_data(result, 3)
        stat = com_data(result, 4)
        dyn = com_data(result, 5)
        
        return [
            ModalLoadParticipationRatioResult(
                load_case=load_case[i] if load_case else "",
                item_type=item_type[i] if item_type else "",
                item=item[i] if item else "",
                stat=stat[i] if stat else 0.0,
                dyn=dyn[i] if dyn else 0.0,
            )
            for i in range(num)
        ]
    return []


def get_modal_participation_factors(model) -> List[ModalParticipationFactorResult]:
    """
    Get modal participation factors.

    Returns participation factors, modal mass, and modal stiffness for each mode.
    
    Args:
        model: SAP2000 SapModel object
        
    Returns:
        List of `ModalParticipationFactorResult`.
    """
    result = model.Results.ModalParticipationFactors(
        0, [], [], [],
        [],
        [], [], [], [], [], [],
        [], []
    )
    
    num = com_data(result, 0, 0)
    ret = com_ret(result)
    
    if (ret == 0 or ret == num) and num > 0:
        load_case = com_data(result, 1)
        step_type = com_data(result, 2)
        step_num = com_data(result, 3)
        period = com_data(result, 4)
        ux = com_data(result, 5)
        uy = com_data(result, 6)
        uz = com_data(result, 7)
        rx = com_data(result, 8)
        ry = com_data(result, 9)
        rz = com_data(result, 10)
        modal_mass = com_data(result, 11)
        modal_stiff = com_data(result, 12)
        
        return [
            ModalParticipationFactorResult(
                load_case=load_case[i] if load_case else "",
                step_type=step_type[i] if step_type else "",
                step_num=step_num[i] if step_num else 0.0,
                period=period[i] if period else 0.0,
                ux=ux[i] if ux else 0.0,
                uy=uy[i] if uy else 0.0,
                uz=uz[i] if uz else 0.0,
                rx=rx[i] if rx else 0.0,
                ry=ry[i] if ry else 0.0,
                rz=rz[i] if rz else 0.0,
                modal_mass=modal_mass[i] if modal_mass else 0.0,
                modal_stiff=modal_stiff[i] if modal_stiff else 0.0,
            )
            for i in range(num)
        ]
    return []
