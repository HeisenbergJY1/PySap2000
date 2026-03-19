# -*- coding: utf-8 -*-
"""
cable_results.py - Cable 结果数据对象
对应 SAP2000 的 Results.CableForce
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CableForce:
    """Cable 内力结果"""
    cable: str = ""
    station: float = 0.0
    load_case: str = ""
    tension: float = 0.0        # 索力
    sag: float = 0.0            # 垂度
    length: float = 0.0         # 长度


@dataclass 
class CableDeformation:
    """Cable 变形结果"""
    cable: str = ""
    load_case: str = ""
    axial_deform: float = 0.0   # 轴向变形
    sag: float = 0.0            # 垂度


class CableResults:
    """Cable 结果查询类"""
    
    def __init__(self, model):
        self._model = model
    
    def _setup_output(self, load_case: str = "", load_combo: str = ""):
        self._model.Results.Setup.DeselectAllCasesAndCombosForOutput()
        if load_case:
            self._model.Results.Setup.SetCaseSelectedForOutput(load_case)
        if load_combo:
            self._model.Results.Setup.SetComboSelectedForOutput(load_combo)
    
    def get_forces(self, cable: str, load_case: str = "", load_combo: str = "") -> List[CableForce]:
        """获取 Cable 内力"""
        self._setup_output(load_case, load_combo)
        result = self._model.Results.CableForce(cable, ItemTypeElm=0)
        
        forces = []
        if result[-1] == 0 and result[0] > 0:
            for i in range(result[0]):
                forces.append(CableForce(
                    cable=result[1][i],
                    station=result[2][i] if len(result) > 2 else 0.0,
                    load_case=load_case or load_combo,
                    tension=result[6][i] if len(result) > 6 else 0.0
                ))
        return forces
    
    def get_max_tension(self, load_case: str = "", load_combo: str = "") -> Dict[str, Any]:
        """获取最大索力"""
        self._setup_output(load_case, load_combo)
        cables = self.get_name_list(self._model)
        
        max_val = float('-inf')
        max_cable = None
        
        for cable in cables:
            forces = self.get_forces(cable, load_case, load_combo)
            for force in forces:
                if force.tension > max_val:
                    max_val = force.tension
                    max_cable = cable
        
        return {
            'max_tension': max_val,
            'cable': max_cable,
            'load_case': load_case or load_combo
        }
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """获取所有 Cable 名称列表"""
        result = model.CableObj.GetNameList()
        return list(result[1]) if result[0] > 0 else []
