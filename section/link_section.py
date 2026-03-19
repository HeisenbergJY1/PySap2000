# -*- coding: utf-8 -*-
"""
link_section.py - 连接单元属性
对应 SAP2000 的 PropLink

Usage:
    from section import LinkSection, LinkSectionType
    
    # 获取连接属性
    link = LinkSection.get_by_name(model, "L1")
    print(f"类型: {link.type_name}")
    
    # 创建线性连接
    link = LinkSection(
        name="L1",
        section_type=LinkSectionType.LINEAR
    )
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, ClassVar
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class LinkSectionType(IntEnum):
    """连接属性类型 - 对应 SAP2000 eLinkPropType"""
    LINEAR = 1                    # 线性
    DAMPER = 2                    # 阻尼器
    GAP = 3                       # 间隙
    HOOK = 4                      # 钩
    PLASTIC_WEN = 5               # 塑性(Wen)
    RUBBER_ISOLATOR = 6           # 橡胶隔震器
    FRICTION_ISOLATOR = 7         # 摩擦隔震器
    MULTILINEAR_ELASTIC = 8       # 多线性弹性
    MULTILINEAR_PLASTIC = 9       # 多线性塑性
    TC_FRICTION_ISOLATOR = 10     # T/C 摩擦隔震器





# 连接类型中文名称
LINK_TYPE_NAMES: Dict[LinkSectionType, str] = {
    LinkSectionType.LINEAR: "线性",
    LinkSectionType.DAMPER: "阻尼器",
    LinkSectionType.GAP: "间隙",
    LinkSectionType.HOOK: "钩",
    LinkSectionType.PLASTIC_WEN: "塑性(Wen)",
    LinkSectionType.RUBBER_ISOLATOR: "橡胶隔震器",
    LinkSectionType.FRICTION_ISOLATOR: "摩擦隔震器",
    LinkSectionType.MULTILINEAR_ELASTIC: "多线性弹性",
    LinkSectionType.MULTILINEAR_PLASTIC: "多线性塑性",
    LinkSectionType.TC_FRICTION_ISOLATOR: "T/C摩擦隔震器",
}


@dataclass
class LinkSection:
    """
    连接单元属性 - 对应 SAP2000 PropLink
    
    Attributes:
        name: 属性名称
        section_type: 属性类型
        type_name: 属性类型中文名称
        dof: 自由度激活状态 [U1, U2, U3, R1, R2, R3]
        fixed: 自由度固定状态
        stiffness: 有效刚度 Ke
        damping: 有效阻尼 Ce
        dj2: U2 剪切弹簧到 J 端距离
        dj3: U3 剪切弹簧到 J 端距离
    """
    
    # 标识
    name: str = ""
    
    # 类型
    section_type: Optional[LinkSectionType] = None
    type_name: str = ""
    
    # 通用属性
    dof: List[bool] = field(default_factory=lambda: [False] * 6)
    fixed: List[bool] = field(default_factory=lambda: [False] * 6)
    stiffness: List[float] = field(default_factory=lambda: [0.0] * 6)
    damping: List[float] = field(default_factory=lambda: [0.0] * 6)
    dj2: float = 0.0
    dj3: float = 0.0
    
    # 非线性属性
    nonlinear: List[bool] = field(default_factory=lambda: [False] * 6)
    k_initial: List[float] = field(default_factory=lambda: [0.0] * 6)
    
    # 阻尼器属性
    c_nonlinear: List[float] = field(default_factory=lambda: [0.0] * 6)
    c_exponent: List[float] = field(default_factory=lambda: [1.0] * 6)
    
    # 间隙/钩属性
    opening: List[float] = field(default_factory=lambda: [0.0] * 6)
    
    # 质量属性
    weight: float = 0.0
    mass: float = 0.0
    r1: float = 0.0
    r2: float = 0.0
    r3: float = 0.0
    
    # 耦合标志
    stiffness_coupled: bool = False
    damping_coupled: bool = False
    
    notes: str = ""
    guid: Optional[str] = None
    
    _object_type: ClassVar[str] = "PropLink"

    @classmethod
    def get_by_name(cls, model, name: str) -> 'LinkSection':
        """获取指定名称的连接属性"""
        prop = cls(name=name)
        prop._get(model)
        return prop
    
    @classmethod
    def get_all(cls, model) -> List['LinkSection']:
        """获取所有连接属性"""
        names = cls.get_name_list(model)
        return [cls.get_by_name(model, n) for n in names]
    
    @staticmethod
    def get_count(model) -> int:
        """获取连接属性总数"""
        return model.PropLink.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """获取连接属性名称列表"""
        result = model.PropLink.GetNameList(0, [])
        names = com_data(result, 1)
        return list(names) if names else []

    def _get(self, model) -> 'LinkSection':
        """从 SAP2000 获取连接属性数据"""
        result = model.PropLink.GetTypeOAPI(self.name)
        
        type_val = com_data(result, 0)
        ret = com_ret(result)
        if type_val is not None:
            if ret != 0:
                from exceptions import SectionError
                raise SectionError(f"连接属性 {self.name} 不存在")
            
            try:
                self.section_type = LinkSectionType(type_val)
                self.type_name = LINK_TYPE_NAMES.get(self.section_type, f"未知({type_val})")
            except ValueError:
                self.section_type = None
                self.type_name = f"未知({type_val})"
        
        # 根据类型获取详细属性
        if self.section_type == LinkSectionType.LINEAR:
            self._get_linear(model)
        elif self.section_type == LinkSectionType.DAMPER:
            self._get_damper(model)
        elif self.section_type == LinkSectionType.GAP:
            self._get_gap(model)
        elif self.section_type == LinkSectionType.HOOK:
            self._get_hook(model)
        
        self._get_weight_and_mass(model)
        return self
    
    def _get_linear(self, model):
        result = model.PropLink.GetLinear(self.name)
        if com_data(result, 0) is not None:
            self.dof = list(com_data(result, 0, default=[])) or [False] * 6
            self.fixed = list(com_data(result, 1, default=[])) or [False] * 6
            self.stiffness = list(com_data(result, 2, default=[])) or [0.0] * 6
            self.damping = list(com_data(result, 3, default=[])) or [0.0] * 6
            self.dj2 = com_data(result, 4, default=0.0)
            self.dj3 = com_data(result, 5, default=0.0)
            self.stiffness_coupled = com_data(result, 6, default=False)
            self.damping_coupled = com_data(result, 7, default=False)
            self.notes = com_data(result, 8, default="") or ""
            self.guid = com_data(result, 9) or None
    
    def _get_damper(self, model):
        result = model.PropLink.GetDamper(self.name)
        if com_data(result, 0) is not None:
            self.dof = list(com_data(result, 0, default=[])) or [False] * 6
            self.fixed = list(com_data(result, 1, default=[])) or [False] * 6
            self.nonlinear = list(com_data(result, 2, default=[])) or [False] * 6
            self.stiffness = list(com_data(result, 3, default=[])) or [0.0] * 6
            self.damping = list(com_data(result, 4, default=[])) or [0.0] * 6
            self.k_initial = list(com_data(result, 5, default=[])) or [0.0] * 6
            self.c_nonlinear = list(com_data(result, 6, default=[])) or [0.0] * 6
            self.c_exponent = list(com_data(result, 7, default=[])) or [1.0] * 6
            self.dj2 = com_data(result, 8, default=0.0)
            self.dj3 = com_data(result, 9, default=0.0)
            self.notes = com_data(result, 10, default="") or ""
            self.guid = com_data(result, 11) or None
    
    def _get_gap(self, model):
        result = model.PropLink.GetGap(self.name)
        if com_data(result, 0) is not None:
            self.dof = list(com_data(result, 0, default=[])) or [False] * 6
            self.fixed = list(com_data(result, 1, default=[])) or [False] * 6
            self.nonlinear = list(com_data(result, 2, default=[])) or [False] * 6
            self.stiffness = list(com_data(result, 3, default=[])) or [0.0] * 6
            self.damping = list(com_data(result, 4, default=[])) or [0.0] * 6
            self.k_initial = list(com_data(result, 5, default=[])) or [0.0] * 6
            self.opening = list(com_data(result, 6, default=[])) or [0.0] * 6
            self.dj2 = com_data(result, 7, default=0.0)
            self.dj3 = com_data(result, 8, default=0.0)
            self.notes = com_data(result, 9, default="") or ""
            self.guid = com_data(result, 10) or None
    
    def _get_hook(self, model):
        result = model.PropLink.GetHook(self.name)
        if com_data(result, 0) is not None:
            self.dof = list(com_data(result, 0, default=[])) or [False] * 6
            self.fixed = list(com_data(result, 1, default=[])) or [False] * 6
            self.nonlinear = list(com_data(result, 2, default=[])) or [False] * 6
            self.stiffness = list(com_data(result, 3, default=[])) or [0.0] * 6
            self.damping = list(com_data(result, 4, default=[])) or [0.0] * 6
            self.k_initial = list(com_data(result, 5, default=[])) or [0.0] * 6
            self.opening = list(com_data(result, 6, default=[])) or [0.0] * 6
            self.dj2 = com_data(result, 7, default=0.0)
            self.dj3 = com_data(result, 8, default=0.0)
            self.notes = com_data(result, 9, default="") or ""
            self.guid = com_data(result, 10) or None
    
    def _get_weight_and_mass(self, model):
        result = model.PropLink.GetWeightAndMass(self.name)
        if com_data(result, 0) is not None:
            self.weight = com_data(result, 0, default=0.0)
            self.mass = com_data(result, 1, default=0.0)
            self.r1 = com_data(result, 2, default=0.0)
            self.r2 = com_data(result, 3, default=0.0)
            self.r3 = com_data(result, 4, default=0.0)

    def _create(self, model) -> int:
        """在 SAP2000 中创建连接属性"""
        from PySap2000.logger import get_logger
        _log = get_logger("link_section")
        if self.name:
            try:
                existing = self.get_name_list(model)
                if self.name in existing:
                    _log.warning(f"LinkSection '{self.name}' already exists, skipped")
                    return -1
            except Exception:
                pass
        if self.section_type == LinkSectionType.LINEAR:
            result = model.PropLink.SetLinear(
                self.name, self.dof, self.fixed, self.stiffness, self.damping,
                self.dj2, self.dj3, self.stiffness_coupled, self.damping_coupled,
                self.notes, self.guid or ""
            )
        elif self.section_type == LinkSectionType.DAMPER:
            result = model.PropLink.SetDamper(
                self.name, self.dof, self.fixed, self.nonlinear,
                self.stiffness, self.damping, self.k_initial,
                self.c_nonlinear, self.c_exponent, self.dj2, self.dj3,
                self.notes, self.guid or ""
            )
        elif self.section_type == LinkSectionType.GAP:
            result = model.PropLink.SetGap(
                self.name, self.dof, self.fixed, self.nonlinear,
                self.stiffness, self.damping, self.k_initial, self.opening,
                self.dj2, self.dj3, self.notes, self.guid or ""
            )
        elif self.section_type == LinkSectionType.HOOK:
            result = model.PropLink.SetHook(
                self.name, self.dof, self.fixed, self.nonlinear,
                self.stiffness, self.damping, self.k_initial, self.opening,
                self.dj2, self.dj3, self.notes, self.guid or ""
            )
        else:
            return -1
        return com_ret(result)
    
    def _delete(self, model) -> int:
        return model.PropLink.Delete(self.name)

