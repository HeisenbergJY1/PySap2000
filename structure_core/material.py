# -*- coding: utf-8 -*-
"""
material.py - 材料属性
对应 SAP2000 的 PropMaterial

Usage:
    from structure_core import Material, MaterialType
    
    # 获取材料
    mat = Material.get_by_name(model, "4000Psi")
    print(f"弹性模量: {mat.e}, 泊松比: {mat.u}")
    
    # 创建钢材
    steel = Material(
        name="MySteel",
        type=MaterialType.STEEL,
        e=2.0e11,  # 弹性模量 Pa
        u=0.3,     # 泊松比
        a=1.2e-5,  # 热膨胀系数
        w=76.98e3  # 重量密度 N/m³
    )
    steel._create(model)
    
    # 从材料库添加材料
    name = Material.add_from_library(
        model, MaterialType.REBAR, 
        "United States", "ASTM A706", "Grade 60"
    )
"""

import uuid
from dataclasses import dataclass
from typing import Optional, List, Tuple, ClassVar
from enum import IntEnum
from PySap2000.com_helper import com_ret, com_data


class MaterialType(IntEnum):
    """
    材料类型
    对应 SAP2000 的 eMatType 枚举
    """
    STEEL = 1           # eMatType_Steel
    CONCRETE = 2        # eMatType_Concrete
    NO_DESIGN = 3       # eMatType_NoDesign
    ALUMINUM = 4        # eMatType_Aluminum
    COLD_FORMED = 5     # eMatType_ColdFormed
    REBAR = 6           # eMatType_Rebar
    TENDON = 7          # eMatType_Tendon


class MaterialSymmetryType(IntEnum):
    """
    材料对称类型
    对应 SAP2000 的 SymType
    """
    ISOTROPIC = 0      # 各向同性
    ORTHOTROPIC = 1    # 正交各向异性
    ANISOTROPIC = 2    # 各向异性
    UNIAXIAL = 3       # 单轴


class WeightMassOption(IntEnum):
    """
    SetWeightAndMass 的 MyOption 参数
    """
    WEIGHT = 1  # 指定重量密度 [F/L³]
    MASS = 2    # 指定质量密度 [M/L³]


@dataclass
class MaterialDamping:
    """
    材料阻尼数据
    
    Attributes:
        name: 材料名称
        modal_ratio: 模态阻尼比
        viscous_mass_coeff: 粘性比例阻尼的质量系数
        viscous_stiff_coeff: 粘性比例阻尼的刚度系数
        hysteretic_mass_coeff: 滞回比例阻尼的质量系数
        hysteretic_stiff_coeff: 滞回比例阻尼的刚度系数
    """
    name: str = ""
    modal_ratio: float = 0.0
    viscous_mass_coeff: float = 0.0
    viscous_stiff_coeff: float = 0.0
    hysteretic_mass_coeff: float = 0.0
    hysteretic_stiff_coeff: float = 0.0


@dataclass
class Material:
    """
    材料属性 - 对应 SAP2000 PropMaterial
    
    Attributes:
        name: 材料名称
        type: 材料类型 (eMatType)
        symmetry_type: 对称类型
        e: 弹性模量 [F/L²]
        u: 泊松比
        g: 剪切模量 [F/L²] (各向同性材料由程序计算)
        a: 热膨胀系数 [1/T]
        w: 重量密度 [F/L³]
        m: 质量密度 [M/L³]
        color: 显示颜色 (-1 表示自动分配)
        notes: 备注
        guid: 全局唯一标识符
    """
    
    # 标识
    name: str = ""
    
    # 类型
    type: MaterialType = MaterialType.STEEL
    symmetry_type: MaterialSymmetryType = MaterialSymmetryType.ISOTROPIC
    
    # 力学属性
    e: float = 0.0      # 弹性模量
    u: float = 0.0      # 泊松比
    g: float = 0.0      # 剪切模量 (只读，由程序计算)
    a: float = 0.0      # 热膨胀系数
    
    # 物理属性
    w: float = 0.0      # 重量密度
    m: float = 0.0      # 质量密度
    
    # 可选属性
    color: int = -1
    notes: str = ""
    guid: Optional[str] = None
    
    # 类属性
    _object_type: ClassVar[str] = "PropMaterial"

    # ==================== 公开方法 ====================
    
    @classmethod
    def get_by_name(cls, model, name: str) -> 'Material':
        """
        获取指定名称的材料
        
        Args:
            model: SapModel 对象
            name: 材料名称
            
        Returns:
            填充了数据的 Material 对象
            
        Example:
            mat = Material.get_by_name(model, "4000Psi")
            print(f"弹性模量: {mat.e}")
        """
        material = cls(name=name)
        material._get(model)
        return material
    
    @classmethod
    def get_all(cls, model) -> List['Material']:
        """
        获取所有材料
        
        Args:
            model: SapModel 对象
            
        Returns:
            Material 对象列表
            
        Example:
            materials = Material.get_all(model)
            for m in materials:
                print(f"{m.name}: E={m.e}")
        """
        names = cls.get_name_list(model)
        materials = []
        for name in names:
            try:
                material = cls.get_by_name(model, name)
                materials.append(material)
            except Exception:
                pass
        return materials
    
    @staticmethod
    def get_count(model, mat_type: Optional[MaterialType] = None) -> int:
        """
        获取材料总数
        
        Args:
            model: SapModel 对象
            mat_type: 材料类型 (可选，不指定则返回所有类型的数量)
            
        Returns:
            材料数量
            
        Example:
            # 获取所有材料数量
            total = Material.get_count(model)
            
            # 获取钢材数量
            steel_count = Material.get_count(model, MaterialType.STEEL)
        """
        if mat_type is not None:
            return model.PropMaterial.Count(mat_type.value)
        return model.PropMaterial.Count()
    
    @staticmethod
    def get_name_list(model, mat_type: Optional[MaterialType] = None) -> List[str]:
        """
        获取材料名称列表
        
        Args:
            model: SapModel 对象
            mat_type: 材料类型 (可选，不指定则返回所有类型)
            
        Returns:
            材料名称列表
            
        Example:
            # 获取所有材料名称
            names = Material.get_name_list(model)
            
            # 获取混凝土材料名称
            concrete_names = Material.get_name_list(model, MaterialType.CONCRETE)
        """
        if mat_type is not None:
            result = model.PropMaterial.GetNameList(0, [], mat_type.value)
        else:
            result = model.PropMaterial.GetNameList(0, [])
        
        return list(com_data(result, 1, []))
    
    @staticmethod
    def add_from_library(
        model,
        mat_type: MaterialType,
        region: str,
        standard: str,
        grade: str,
        user_name: str = ""
    ) -> str:
        """
        从材料库添加材料
        
        Args:
            model: SapModel 对象
            mat_type: 材料类型
            region: 区域名称 (如 "United States", "China")
            standard: 标准名称 (如 "ASTM A706", "GB 50010")
            grade: 等级名称 (如 "Grade 60", "C30")
            user_name: 用户指定名称 (可选)
            
        Returns:
            程序分配的材料名称
            
        Example:
            name = Material.add_from_library(
                model, MaterialType.REBAR,
                "United States", "ASTM A706", "Grade 60"
            )
        """
        result = model.PropMaterial.AddMaterial(
            "",  # Name - 由程序返回
            mat_type.value,
            region,
            standard,
            grade,
            user_name
        )
        
        return com_data(result, 0, "")

    def set_weight(self, model, weight: float) -> int:
        """
        设置重量密度
        
        Args:
            model: SapModel 对象
            weight: 重量密度 [F/L³]
            
        Returns:
            0 表示成功，非0 表示失败
        """
        self.w = weight
        return model.PropMaterial.SetWeightAndMass(
            self.name, 
            WeightMassOption.WEIGHT,
            weight
        )
    
    def set_mass(self, model, mass: float) -> int:
        """
        设置质量密度
        
        Args:
            model: SapModel 对象
            mass: 质量密度 [M/L³]
            
        Returns:
            0 表示成功，非0 表示失败
        """
        self.m = mass
        return model.PropMaterial.SetWeightAndMass(
            self.name, 
            WeightMassOption.MASS,
            mass
        )
    
    def set_isotropic(self, model, e: float, u: float, a: float = 0.0) -> int:
        """
        设置各向同性力学属性
        
        Args:
            model: SapModel 对象
            e: 弹性模量 [F/L²]
            u: 泊松比
            a: 热膨胀系数 [1/T]
            
        Returns:
            0 表示成功，非0 表示失败
        """
        self.e = e
        self.u = u
        self.a = a
        self.symmetry_type = MaterialSymmetryType.ISOTROPIC
        return model.PropMaterial.SetMPIsotropic(self.name, e, u, a)
    
    def change_name(self, model, new_name: str) -> int:
        """
        修改材料名称
        
        Args:
            model: SapModel 对象
            new_name: 新名称
            
        Returns:
            0 表示成功，非0 表示失败
        """
        ret = model.PropMaterial.ChangeName(self.name, new_name)
        if ret == 0:
            self.name = new_name
        return ret
    
    def get_damping(self, model, temp: float = 0.0) -> 'MaterialDamping':
        """
        获取材料阻尼数据
        
        Args:
            model: SapModel 对象
            temp: 温度 (仅用于温度相关材料)
            
        Returns:
            MaterialDamping 数据对象
        """
        result = model.PropMaterial.GetDamping(self.name, temp)
        
        modal_ratio = com_data(result, 0)
        if modal_ratio is not None:
            return MaterialDamping(
                name=self.name,
                modal_ratio=com_data(result, 0, 0.0),
                viscous_mass_coeff=com_data(result, 1, 0.0),
                viscous_stiff_coeff=com_data(result, 2, 0.0),
                hysteretic_mass_coeff=com_data(result, 3, 0.0),
                hysteretic_stiff_coeff=com_data(result, 4, 0.0)
            )
        
        return MaterialDamping(name=self.name)
    
    def set_damping(
        self,
        model,
        modal_ratio: float = 0.0,
        viscous_mass_coeff: float = 0.0,
        viscous_stiff_coeff: float = 0.0,
        hysteretic_mass_coeff: float = 0.0,
        hysteretic_stiff_coeff: float = 0.0,
        temp: float = 0.0
    ) -> int:
        """
        设置材料阻尼数据
        
        Args:
            model: SapModel 对象
            modal_ratio: 模态阻尼比
            viscous_mass_coeff: 粘性比例阻尼的质量系数
            viscous_stiff_coeff: 粘性比例阻尼的刚度系数
            hysteretic_mass_coeff: 滞回比例阻尼的质量系数
            hysteretic_stiff_coeff: 滞回比例阻尼的刚度系数
            temp: 温度 (仅用于温度相关材料)
            
        Returns:
            0 表示成功，非0 表示失败
        """
        return model.PropMaterial.SetDamping(
            self.name,
            modal_ratio,
            viscous_mass_coeff,
            viscous_stiff_coeff,
            hysteretic_mass_coeff,
            hysteretic_stiff_coeff,
            temp
        )

    # ==================== 内部方法 ====================
    
    def _get(self, model) -> 'Material':
        """从 SAP2000 获取材料数据"""
        # 1. 获取类型
        result = model.PropMaterial.GetTypeOAPI(self.name)
        
        mat_type = com_data(result, 0)
        sym_type = com_data(result, 1)
        ret = com_ret(result)
        
        if mat_type is None:
            from exceptions import MaterialError
            raise MaterialError(f"获取材料 {self.name} 类型失败")
        
        if ret != 0:
            from exceptions import MaterialError
            raise MaterialError(f"材料 {self.name} 不存在")
        
        # 设置类型
        try:
            self.type = MaterialType(mat_type)
        except ValueError:
            self.type = MaterialType.NO_DESIGN
        
        try:
            self.symmetry_type = MaterialSymmetryType(sym_type)
        except ValueError:
            self.symmetry_type = MaterialSymmetryType.ISOTROPIC
        
        # 2. 根据对称类型获取力学属性
        if self.symmetry_type == MaterialSymmetryType.ISOTROPIC:
            result = model.PropMaterial.GetMPIsotropic(self.name)
            self.e = com_data(result, 0, 0.0)
            self.u = com_data(result, 1, 0.0)
            self.a = com_data(result, 2, 0.0)
            self.g = com_data(result, 3, 0.0)
        elif self.symmetry_type == MaterialSymmetryType.UNIAXIAL:
            result = model.PropMaterial.GetMPUniaxial(self.name)
            self.e = com_data(result, 0, 0.0)
            self.a = com_data(result, 1, 0.0)
            self.u = 0
            self.g = 0
        
        # 3. 获取重量和质量密度
        result = model.PropMaterial.GetWeightAndMass(self.name)
        self.w = com_data(result, 0, 0.0)
        self.m = com_data(result, 1, 0.0)
        
        return self
    
    def _create(self, model) -> int:
        """在 SAP2000 中创建材料"""
        # 1. 初始化材料
        ret = model.PropMaterial.SetMaterial(
            self.name, 
            self.type.value,
            self.color,
            self.notes,
            self.guid or ""
        )
        
        if ret != 0:
            return ret
        
        # 2. 设置力学属性
        if self.symmetry_type == MaterialSymmetryType.ISOTROPIC:
            ret = model.PropMaterial.SetMPIsotropic(
                self.name, self.e, self.u, self.a
            )
        elif self.symmetry_type == MaterialSymmetryType.UNIAXIAL:
            ret = model.PropMaterial.SetMPUniaxial(
                self.name, self.e, self.a
            )
        
        if ret != 0:
            return ret
        
        # 3. 设置重量/质量密度
        if self.w > 0:
            ret = model.PropMaterial.SetWeightAndMass(
                self.name, WeightMassOption.WEIGHT, self.w
            )
        elif self.m > 0:
            ret = model.PropMaterial.SetWeightAndMass(
                self.name, WeightMassOption.MASS, self.m
            )
        
        return ret
    
    def _delete(self, model) -> int:
        """删除材料"""
        return model.PropMaterial.Delete(self.name)
    
    def _update(self, model) -> int:
        """更新材料（SAP2000 的 SetMaterial 会覆盖）"""
        return self._create(model)

    # ==================== 便捷属性 ====================
    
    @property
    def elastic_modulus(self) -> float:
        """弹性模量"""
        return self.e
    
    @property
    def poisson_ratio(self) -> float:
        """泊松比"""
        return self.u
    
    @property
    def shear_modulus(self) -> float:
        """剪切模量"""
        return self.g
    
    @property
    def thermal_expansion(self) -> float:
        """热膨胀系数"""
        return self.a
    
    @property
    def weight_density(self) -> float:
        """重量密度"""
        return self.w
    
    @property
    def mass_density(self) -> float:
        """质量密度"""
        return self.m
