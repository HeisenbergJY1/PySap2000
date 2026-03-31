# -*- coding: utf-8 -*-
"""
point_results.py - Point result data objects.
Wraps SAP2000 `Results.JointDispl` and `Results.JointReact`.

SAP2000 API signatures:

JointDispl(Name, ItemTypeElm, NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3)
    Returned tuple indexes:
        [0] = NumberResults
        [1] = Obj[]
        [2] = Elm[]
        [3] = LoadCase[]
        [4] = StepType[]
        [5] = StepNum[]
        [6] = U1[] - local-1 displacement [L]
        [7] = U2[] - local-2 displacement [L]
        [8] = U3[] - local-3 displacement [L]
        [9] = R1[] - rotation about local axis 1 [rad]
        [10] = R2[] - rotation about local axis 2 [rad]
        [11] = R3[] - rotation about local axis 3 [rad]
        [-1] = ret (return code)

JointReact(Name, ItemTypeElm, NumberResults, Obj, Elm, LoadCase, StepType, StepNum, F1, F2, F3, M1, M2, M3)
    Returned tuple indexes:
        [0] = NumberResults
        [1] = Obj[]
        [2] = Elm[]
        [3] = LoadCase[]
        [4] = StepType[]
        [5] = StepNum[]
        [6] = F1[] - local-1 reaction [F]
        [7] = F2[] - local-2 reaction [F]
        [8] = F3[] - local-3 reaction [F]
        [9] = M1[] - reaction moment about local axis 1 [FL]
        [10] = M2[] - reaction moment about local axis 2 [FL]
        [11] = M3[] - reaction moment about local axis 3 [FL]
        [-1] = ret (return code)

ItemTypeElm:
    0 = ObjectElm (elements associated with the joint object)
    1 = Element (element)
    2 = GroupElm (all elements in the group)
    3 = SelectionElm (selected elements)
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import IntEnum


class ItemTypeElm(IntEnum):
    """Object scope for result queries."""
    OBJECT_ELM = 0          # Elements associated with the object
    ELEMENT = 1             # Element
    GROUP_ELM = 2           # All elements in the group
    SELECTION_ELM = 3       # Selected elements


@dataclass
class PointDisplacement:
    """
    Point displacement result.

    Matches the return values of SAP2000 `Results.JointDispl`.
    
    Attributes:
        point: Point name
        element: Element name
        load_case: Load case or combo name
        step_type: Step type
        step_num: Step number
        u1, u2, u3: Displacement components [L]
        r1, r2, r3: Rotation components [rad]
    """
    point: str = ""
    element: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    
    # Displacements in the local coordinate system
    u1: float = 0.0     # Local-1 displacement
    u2: float = 0.0     # Local-2 displacement
    u3: float = 0.0     # Local-3 displacement
    
    # Rotations in the local coordinate system
    r1: float = 0.0     # Rotation about local axis 1
    r2: float = 0.0     # Rotation about local axis 2
    r3: float = 0.0     # Rotation about local axis 3
    
    # Backward-compatible property aliases
    @property
    def ux(self) -> float:
        return self.u1
    
    @property
    def uy(self) -> float:
        return self.u2
    
    @property
    def uz(self) -> float:
        return self.u3
    
    @property
    def rx(self) -> float:
        return self.r1
    
    @property
    def ry(self) -> float:
        return self.r2
    
    @property
    def rz(self) -> float:
        return self.r3


@dataclass
class PointReaction:
    """
    Point reaction result.

    Matches the return values of SAP2000 `Results.JointReact`.
    
    Attributes:
        point: Point name
        element: Element name
        load_case: Load case or combo name
        step_type: Step type
        step_num: Step number
        f1, f2, f3: Reaction force components [F]
        m1, m2, m3: Reaction moment components [FL]
    """
    point: str = ""
    element: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    
    # Reactions in the local coordinate system
    f1: float = 0.0     # Local-1 reaction
    f2: float = 0.0     # Local-2 reaction
    f3: float = 0.0     # Local-3 reaction
    
    # Reaction moments in the local coordinate system
    m1: float = 0.0     # Reaction moment about local axis 1
    m2: float = 0.0     # Reaction moment about local axis 2
    m3: float = 0.0     # Reaction moment about local axis 3
    
    # Backward-compatible property aliases
    @property
    def fx(self) -> float:
        return self.f1
    
    @property
    def fy(self) -> float:
        return self.f2
    
    @property
    def fz(self) -> float:
        return self.f3
    
    @property
    def mx(self) -> float:
        return self.m1
    
    @property
    def my(self) -> float:
        return self.m2
    
    @property
    def mz(self) -> float:
        return self.m3


class PointResults:
    """
    Point result query helper.

    Provides methods to query joint displacements and reactions.
    
    Example:
        results = PointResults(model)
        
        # Get the displacement of one point
        disp = results.get_displacement("1", load_case="DEAD")
        print(f"U3 = {disp.u3}")
        
        # Get all point displacements
        all_disp = results.get_all_displacements(load_case="DEAD")
        
        # Get the maximum displacement
        max_disp = results.get_max_displacement(load_case="DEAD", direction="u3")
    """
    
    def __init__(self, model):
        self._model = model
    
    def _setup_output(self, load_case: str = "", load_combo: str = ""):
        """Set the active output case and combo selection."""
        self._model.Results.Setup.DeselectAllCasesAndCombosForOutput()
        if load_case:
            self._model.Results.Setup.SetCaseSelectedForOutput(load_case)
        if load_combo:
            self._model.Results.Setup.SetComboSelectedForOutput(load_combo)
    
    def get_displacement(
        self, 
        point: str, 
        load_case: str = "", 
        load_combo: str = "",
        item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
    ) -> PointDisplacement:
        """
        Get the displacement of a single point.

        SAP2000 API: `Results.JointDispl(Name, ItemTypeElm, ...)`
        
        Args:
            point: Point name
            load_case: Load case name
            load_combo: Load combination name
            item_type: Query scope
            
        Returns:
            `PointDisplacement` instance.
        """
        self._setup_output(load_case, load_combo)
        result = self._model.Results.JointDispl(point, item_type.value)
        
        if result[-1] == 0 and result[0] > 0:
            return PointDisplacement(
                point=result[1][0] if result[1] else point,
                element=result[2][0] if result[2] else "",
                load_case=result[3][0] if result[3] else (load_case or load_combo),
                step_type=result[4][0] if result[4] else "",
                step_num=result[5][0] if result[5] else 0.0,
                u1=result[6][0],
                u2=result[7][0],
                u3=result[8][0],
                r1=result[9][0],
                r2=result[10][0],
                r3=result[11][0]
            )
        return PointDisplacement(point=point, load_case=load_case or load_combo)
    
    def get_all_displacements(
        self, 
        load_case: str = "", 
        load_combo: str = "",
        group: str = "ALL"
    ) -> List[PointDisplacement]:
        """
        Get displacements for all requested points.

        SAP2000 API: `Results.JointDispl(GroupName, GroupElm, ...)`
        
        Args:
            load_case: Load case name
            load_combo: Load combination name
            group: Group name. `"ALL"` means all points.
            
        Returns:
            List of `PointDisplacement`.
        """
        self._setup_output(load_case, load_combo)
        result = self._model.Results.JointDispl(group, ItemTypeElm.GROUP_ELM.value)
        
        displacements = []
        if result[-1] == 0 and result[0] > 0:
            for i in range(result[0]):
                disp = PointDisplacement(
                    point=result[1][i] if result[1] else "",
                    element=result[2][i] if result[2] else "",
                    load_case=result[3][i] if result[3] else (load_case or load_combo),
                    step_type=result[4][i] if result[4] else "",
                    step_num=result[5][i] if result[5] else 0.0,
                    u1=result[6][i],
                    u2=result[7][i],
                    u3=result[8][i],
                    r1=result[9][i],
                    r2=result[10][i],
                    r3=result[11][i]
                )
                displacements.append(disp)
        
        return displacements
    
    def get_max_displacement(
        self, 
        load_case: str = "", 
        load_combo: str = "", 
        direction: str = "u3"
    ) -> Dict[str, Any]:
        """
        Get the maximum and minimum displacement in a given direction.
        
        Args:
            load_case: Load case name
            load_combo: Load combination name
            direction: Displacement direction (`"u1"`, `"u2"`, `"u3"`, `"r1"`, `"r2"`, `"r3"`)
            
        Returns:
            Dictionary containing max/min values and corresponding points.
        """
        displacements = self.get_all_displacements(load_case, load_combo)
        
        max_val, min_val = float('-inf'), float('inf')
        max_point, min_point = None, None
        
        for disp in displacements:
            val = getattr(disp, direction, 0)
            if val > max_val:
                max_val, max_point = val, disp.point
            if val < min_val:
                min_val, min_point = val, disp.point
        
        return {
            'max_value': max_val, 
            'max_point': max_point,
            'min_value': min_val, 
            'min_point': min_point, 
            'direction': direction
        }
    
    def get_reaction(
        self, 
        point: str, 
        load_case: str = "", 
        load_combo: str = "",
        item_type: ItemTypeElm = ItemTypeElm.OBJECT_ELM
    ) -> PointReaction:
        """
        Get the reaction of a single point.

        SAP2000 API: `Results.JointReact(Name, ItemTypeElm, ...)`
        
        Args:
            point: Point name
            load_case: Load case name
            load_combo: Load combination name
            item_type: Query scope
            
        Returns:
            `PointReaction` instance.
        """
        self._setup_output(load_case, load_combo)
        result = self._model.Results.JointReact(point, item_type.value)
        
        if result[-1] == 0 and result[0] > 0:
            return PointReaction(
                point=result[1][0] if result[1] else point,
                element=result[2][0] if result[2] else "",
                load_case=result[3][0] if result[3] else (load_case or load_combo),
                step_type=result[4][0] if result[4] else "",
                step_num=result[5][0] if result[5] else 0.0,
                f1=result[6][0],
                f2=result[7][0],
                f3=result[8][0],
                m1=result[9][0],
                m2=result[10][0],
                m3=result[11][0]
            )
        return PointReaction(point=point, load_case=load_case or load_combo)
    
    def get_all_reactions(
        self, 
        load_case: str = "", 
        load_combo: str = "",
        group: str = "ALL"
    ) -> List[PointReaction]:
        """
        Get reactions for all requested points.
        
        Args:
            load_case: Load case name
            load_combo: Load combination name
            group: Group name
            
        Returns:
            List of `PointReaction`.
        """
        self._setup_output(load_case, load_combo)
        result = self._model.Results.JointReact(group, ItemTypeElm.GROUP_ELM.value)
        
        reactions = []
        if result[-1] == 0 and result[0] > 0:
            for i in range(result[0]):
                react = PointReaction(
                    point=result[1][i] if result[1] else "",
                    element=result[2][i] if result[2] else "",
                    load_case=result[3][i] if result[3] else (load_case or load_combo),
                    step_type=result[4][i] if result[4] else "",
                    step_num=result[5][i] if result[5] else 0.0,
                    f1=result[6][i],
                    f2=result[7][i],
                    f3=result[8][i],
                    m1=result[9][i],
                    m2=result[10][i],
                    m3=result[11][i]
                )
                reactions.append(react)
        
        return reactions
    
    def get_base_reaction(
        self, 
        load_case: str = "", 
        load_combo: str = ""
    ) -> Dict[str, float]:
        """
        Get total base reactions.

        SAP2000 API: `Results.BaseReact(...)`
        
        Returns:
            Dictionary containing total reactions: `{f1, f2, f3, m1, m2, m3}`.
        """
        self._setup_output(load_case, load_combo)
        result = self._model.Results.BaseReact()
        
        if result[-1] == 0 and result[0] > 0:
            return {
                'f1': sum(result[4]),   # FX
                'f2': sum(result[5]),   # FY
                'f3': sum(result[6]),   # FZ
                'm1': sum(result[7]),   # MX
                'm2': sum(result[8]),   # MY
                'm3': sum(result[9]),   # MZ
            }
        return {'f1': 0, 'f2': 0, 'f3': 0, 'm1': 0, 'm2': 0, 'm3': 0}
