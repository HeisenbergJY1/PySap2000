# -*- coding: utf-8 -*-
"""
base_react.py - 基底反力结果函数

SAP2000 Results API 的基底反力函数封装

SAP2000 API:
- Results.BaseReact - 基底反力
"""

from typing import List
from .data_classes import BaseReactResult
from PySap2000.com_helper import com_ret, com_data


def get_base_react(model) -> List[BaseReactResult]:
    """
    获取结构基底反力
    
    返回所有选中工况/组合的基底总反力。
    
    Args:
        model: SapModel 对象
        
    Returns:
        BaseReactResult 列表
        
    Example:
        from results import deselect_all_cases_and_combos, set_case_selected_for_output
        
        deselect_all_cases_and_combos(model)
        set_case_selected_for_output(model, "DEAD")
        
        results = get_base_react(model)
        for r in results:
            print(f"{r.load_case}: Fx={r.fx}, Fy={r.fy}, Fz={r.fz}")
    """
    result = model.Results.BaseReact(
        0, [], [], [],
        [], [], [], [], [], [],
        0.0, 0.0, 0.0
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
        
        return [
            BaseReactResult(
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
            )
            for i in range(num)
        ]
    return []
