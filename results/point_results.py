# -*- coding: utf-8 -*-
"""
point_results.py - Point 结果数据对象
对应 SAP2000 的 Results.JointDispl / JointReact

SAP2000 API 参数:

JointDispl(Name, ItemTypeElm, NumberResults, Obj, Elm, LoadCase, StepType, StepNum, U1, U2, U3, R1, R2, R3)
    返回数组索引:
        [0] = NumberResults
        [1] = Obj[]
        [2] = Elm[]
        [3] = LoadCase[]
        [4] = StepType[]
        [5] = StepNum[]
        [6] = U1[] - 局部1轴位移 [L]
        [7] = U2[] - 局部2轴位移 [L]
        [8] = U3[] - 局部3轴位移 [L]
        [9] = R1[] - 绕局部1轴转角 [rad]
        [10] = R2[] - 绕局部2轴转角 [rad]
        [11] = R3[] - 绕局部3轴转角 [rad]
        [-1] = ret (返回值)

JointReact(Name, ItemTypeElm, NumberResults, Obj, Elm, LoadCase, StepType, StepNum, F1, F2, F3, M1, M2, M3)
    返回数组索引:
        [0] = NumberResults
        [1] = Obj[]
        [2] = Elm[]
        [3] = LoadCase[]
        [4] = StepType[]
        [5] = StepNum[]
        [6] = F1[] - 局部1轴反力 [F]
        [7] = F2[] - 局部2轴反力 [F]
        [8] = F3[] - 局部3轴反力 [F]
        [9] = M1[] - 绕局部1轴反力矩 [FL]
        [10] = M2[] - 绕局部2轴反力矩 [FL]
        [11] = M3[] - 绕局部3轴反力矩 [FL]
        [-1] = ret (返回值)

ItemTypeElm:
    0 = ObjectElm (节点对象对应的单元)
    1 = Element (单元)
    2 = GroupElm (组内所有单元)
    3 = SelectionElm (选中的单元)
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import IntEnum


class ItemTypeElm(IntEnum):
    """结果查询对象类型"""
    OBJECT_ELM = 0          # 对象对应的单元
    ELEMENT = 1             # 单元
    GROUP_ELM = 2           # 组内所有单元
    SELECTION_ELM = 3       # 选中的单元


@dataclass
class PointDisplacement:
    """
    Point 位移结果
    
    对应 SAP2000 的 Results.JointDispl 返回值
    
    Attributes:
        point: 节点名称
        element: 单元名称
        load_case: 荷载工况/组合名称
        step_type: 步骤类型
        step_num: 步骤编号
        u1, u2, u3: 位移分量 [L]
        r1, r2, r3: 转角分量 [rad]
    """
    point: str = ""
    element: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    
    # 位移 (局部坐标系)
    u1: float = 0.0     # 局部1轴位移
    u2: float = 0.0     # 局部2轴位移
    u3: float = 0.0     # 局部3轴位移
    
    # 转角 (局部坐标系)
    r1: float = 0.0     # 绕局部1轴转角
    r2: float = 0.0     # 绕局部2轴转角
    r3: float = 0.0     # 绕局部3轴转角
    
    # 向后兼容的属性别名
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
    Point 反力结果
    
    对应 SAP2000 的 Results.JointReact 返回值
    
    Attributes:
        point: 节点名称
        element: 单元名称
        load_case: 荷载工况/组合名称
        step_type: 步骤类型
        step_num: 步骤编号
        f1, f2, f3: 反力分量 [F]
        m1, m2, m3: 反力矩分量 [FL]
    """
    point: str = ""
    element: str = ""
    load_case: str = ""
    step_type: str = ""
    step_num: float = 0.0
    
    # 反力 (局部坐标系)
    f1: float = 0.0     # 局部1轴反力
    f2: float = 0.0     # 局部2轴反力
    f3: float = 0.0     # 局部3轴反力
    
    # 反力矩 (局部坐标系)
    m1: float = 0.0     # 绕局部1轴反力矩
    m2: float = 0.0     # 绕局部2轴反力矩
    m3: float = 0.0     # 绕局部3轴反力矩
    
    # 向后兼容的属性别名
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
    Point 结果查询类
    
    提供节点位移和反力的查询方法
    
    Example:
        results = PointResults(model)
        
        # 获取单个节点位移
        disp = results.get_displacement("1", load_case="DEAD")
        print(f"U3 = {disp.u3}")
        
        # 获取所有节点位移
        all_disp = results.get_all_displacements(load_case="DEAD")
        
        # 获取最大位移
        max_disp = results.get_max_displacement(load_case="DEAD", direction="u3")
    """
    
    def __init__(self, model):
        self._model = model
    
    def _setup_output(self, load_case: str = "", load_combo: str = ""):
        """设置输出工况/组合"""
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
        获取单个 Point 的位移
        
        SAP2000 API: Results.JointDispl(Name, ItemTypeElm, ...)
        
        Args:
            point: 节点名称
            load_case: 荷载工况名称
            load_combo: 荷载组合名称
            item_type: 查询对象类型
            
        Returns:
            PointDisplacement 对象
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
        获取所有 Point 的位移
        
        SAP2000 API: Results.JointDispl(GroupName, GroupElm, ...)
        
        Args:
            load_case: 荷载工况名称
            load_combo: 荷载组合名称
            group: 组名称 ("ALL" 表示所有节点)
            
        Returns:
            PointDisplacement 对象列表
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
        获取最大位移
        
        Args:
            load_case: 荷载工况名称
            load_combo: 荷载组合名称
            direction: 位移方向 ("u1", "u2", "u3", "r1", "r2", "r3")
            
        Returns:
            包含最大/最小值及对应节点的字典
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
        获取单个 Point 的反力
        
        SAP2000 API: Results.JointReact(Name, ItemTypeElm, ...)
        
        Args:
            point: 节点名称
            load_case: 荷载工况名称
            load_combo: 荷载组合名称
            item_type: 查询对象类型
            
        Returns:
            PointReaction 对象
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
        获取所有 Point 的反力
        
        Args:
            load_case: 荷载工况名称
            load_combo: 荷载组合名称
            group: 组名称
            
        Returns:
            PointReaction 对象列表
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
        获取基底总反力
        
        SAP2000 API: Results.BaseReact(...)
        
        Returns:
            包含总反力的字典 {f1, f2, f3, m1, m2, m3}
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
