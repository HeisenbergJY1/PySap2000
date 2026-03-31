# -*- coding: utf-8 -*-
"""
cable_results.py - Cable result data objects.

Wraps SAP2000 `Results.CableForce`.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CableForce:
    """Cable internal force result."""
    cable: str = ""
    station: float = 0.0
    load_case: str = ""
    tension: float = 0.0        # Cable force
    sag: float = 0.0            # Sag
    length: float = 0.0         # Length


@dataclass 
class CableDeformation:
    """Cable deformation result."""
    cable: str = ""
    load_case: str = ""
    axial_deform: float = 0.0   # Axial deformation
    sag: float = 0.0            # Sag


class CableResults:
    """Cable result query helper."""
    
    def __init__(self, model):
        self._model = model
    
    def _setup_output(self, load_case: str = "", load_combo: str = ""):
        self._model.Results.Setup.DeselectAllCasesAndCombosForOutput()
        if load_case:
            self._model.Results.Setup.SetCaseSelectedForOutput(load_case)
        if load_combo:
            self._model.Results.Setup.SetComboSelectedForOutput(load_combo)
    
    def get_forces(self, cable: str, load_case: str = "", load_combo: str = "") -> List[CableForce]:
        """Get internal forces for a cable."""
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
        """Get the maximum cable force."""
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
        """Get the names of all cable objects."""
        result = model.CableObj.GetNameList()
        return list(result[1]) if result[0] > 0 else []
