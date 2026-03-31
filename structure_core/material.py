# -*- coding: utf-8 -*-
"""
material.py - Material properties.

Maps to SAP2000 `PropMaterial`.

Usage:
    from structure_core import Material, MaterialType
    
    # Fetch a material
    mat = Material.get_by_name(model, "4000Psi")
    print(f"Elastic modulus: {mat.e}, Poisson ratio: {mat.u}")
    
    # Create a steel material
    steel = Material(
        name="MySteel",
        type=MaterialType.STEEL,
        e=2.0e11,  # Elastic modulus [Pa]
        u=0.3,     # Poisson ratio
        a=1.2e-5,  # Thermal expansion coefficient
        w=76.98e3  # Weight density [N/m^3]
    )
    steel._create(model)
    
    # Add a material from the material library
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
    Material type.

    Matches the SAP2000 `eMatType` enum.
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
    Material symmetry type.

    Matches SAP2000 `SymType`.
    """
    ISOTROPIC = 0      # Isotropic
    ORTHOTROPIC = 1    # Orthotropic
    ANISOTROPIC = 2    # Anisotropic
    UNIAXIAL = 3       # Uniaxial


class WeightMassOption(IntEnum):
    """
    `MyOption` values for `SetWeightAndMass`.
    """
    WEIGHT = 1  # Weight density [F/L^3]
    MASS = 2    # Mass density [M/L^3]


@dataclass
class MaterialDamping:
    """
    Material damping data.
    
    Attributes:
        name: Material name
        modal_ratio: Modal damping ratio
        viscous_mass_coeff: Viscous mass-proportional damping coefficient
        viscous_stiff_coeff: Viscous stiffness-proportional damping coefficient
        hysteretic_mass_coeff: Hysteretic mass-proportional damping coefficient
        hysteretic_stiff_coeff: Hysteretic stiffness-proportional damping coefficient
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
    Material property object mapping to SAP2000 `PropMaterial`.
    
    Attributes:
        name: Material name
        type: Material type (`eMatType`)
        symmetry_type: Symmetry type
        e: Elastic modulus [F/L^2]
        u: Poisson ratio
        g: Shear modulus [F/L^2] (computed for isotropic materials)
        a: Thermal expansion coefficient [1/T]
        w: Weight density [F/L^3]
        m: Mass density [M/L^3]
        color: Display color (`-1` means auto-assign)
        notes: Notes
        guid: Globally unique identifier
    """
    
    # Identity
    name: str = ""
    
    # Type
    type: MaterialType = MaterialType.STEEL
    symmetry_type: MaterialSymmetryType = MaterialSymmetryType.ISOTROPIC
    
    # Mechanical properties
    e: float = 0.0      # Elastic modulus
    u: float = 0.0      # Poisson ratio
    g: float = 0.0      # Shear modulus (read-only, computed by SAP2000)
    a: float = 0.0      # Thermal expansion coefficient
    
    # Physical properties
    w: float = 0.0      # Weight density
    m: float = 0.0      # Mass density
    
    # Optional attributes
    color: int = -1
    notes: str = ""
    guid: Optional[str] = None
    
    # Class metadata
    _object_type: ClassVar[str] = "PropMaterial"

    # ==================== Public Methods ====================
    
    @classmethod
    def get_by_name(cls, model, name: str) -> 'Material':
        """
        Fetch a material by name.
        
        Args:
            model: `SapModel` object
            name: Material name
            
        Returns:
            A populated `Material` object
            
        Example:
            mat = Material.get_by_name(model, "4000Psi")
            print(f"Elastic modulus: {mat.e}")
        """
        material = cls(name=name)
        material._get(model)
        return material
    
    @classmethod
    def get_all(cls, model) -> List['Material']:
        """
        Fetch all materials.
        
        Args:
            model: `SapModel` object
            
        Returns:
            List of `Material` objects
            
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
        Return the total number of materials.
        
        Args:
            model: `SapModel` object
            mat_type: Optional material type filter
            
        Returns:
            Number of materials
            
        Example:
            # Get the total number of materials
            total = Material.get_count(model)
            
            # Get the number of steel materials
            steel_count = Material.get_count(model, MaterialType.STEEL)
        """
        if mat_type is not None:
            return model.PropMaterial.Count(mat_type.value)
        return model.PropMaterial.Count()
    
    @staticmethod
    def get_name_list(model, mat_type: Optional[MaterialType] = None) -> List[str]:
        """
        Return the list of material names.
        
        Args:
            model: `SapModel` object
            mat_type: Optional material type filter
            
        Returns:
            List of material names
            
        Example:
            # Get all material names
            names = Material.get_name_list(model)
            
            # Get concrete material names
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
        Add a material from the built-in library.
        
        Args:
            model: `SapModel` object
            mat_type: Material type
            region: Region name such as `"United States"` or `"China"`
            standard: Standard name such as `"ASTM A706"`
            grade: Grade name such as `"Grade 60"` or `"C30"`
            user_name: Optional user-specified material name
            
        Returns:
            Material name assigned by SAP2000
            
        Example:
            name = Material.add_from_library(
                model, MaterialType.REBAR,
                "United States", "ASTM A706", "Grade 60"
            )
        """
        result = model.PropMaterial.AddMaterial(
            "",  # Name - returned by SAP2000
            mat_type.value,
            region,
            standard,
            grade,
            user_name
        )
        
        return com_data(result, 0, "")

    def set_weight(self, model, weight: float) -> int:
        """
        Set weight density
        
        Args:
            model: SapModel object
            weight: Weight density [F/L³]
            
        Returns:
            `0` on success, nonzero on failure
        """
        self.w = weight
        return model.PropMaterial.SetWeightAndMass(
            self.name, 
            WeightMassOption.WEIGHT,
            weight
        )
    
    def set_mass(self, model, mass: float) -> int:
        """
        Set mass density
        
        Args:
            model: SapModel object
            mass: Mass density [M/L³]
            
        Returns:
            `0` on success, nonzero on failure
        """
        self.m = mass
        return model.PropMaterial.SetWeightAndMass(
            self.name, 
            WeightMassOption.MASS,
            mass
        )
    
    def set_isotropic(self, model, e: float, u: float, a: float = 0.0) -> int:
        """
        Set isotropic mechanical properties
        
        Args:
            model: SapModel object
            e: Elastic modulus [F/L²]
            u: Poisson's ratio
            a: Thermal expansion coefficient [1/T]
            
        Returns:
            `0` on success, nonzero on failure
        """
        self.e = e
        self.u = u
        self.a = a
        self.symmetry_type = MaterialSymmetryType.ISOTROPIC
        return model.PropMaterial.SetMPIsotropic(self.name, e, u, a)
    
    def change_name(self, model, new_name: str) -> int:
        """
        Change material name
        
        Args:
            model: SapModel object
            new_name: New name
            
        Returns:
            `0` on success, nonzero on failure
        """
        ret = model.PropMaterial.ChangeName(self.name, new_name)
        if ret == 0:
            self.name = new_name
        return ret
    
    def get_damping(self, model, temp: float = 0.0) -> 'MaterialDamping':
        """
        Get material damping data
        
        Args:
            model: SapModel object
            temp: Temperature (for temperature-dependent materials only)
            
        Returns:
            `MaterialDamping` data object
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
        Set material damping data
        
        Args:
            model: SapModel object
            modal_ratio: Modal damping ratio
            viscous_mass_coeff: Mass coefficient for viscous proportional damping
            viscous_stiff_coeff: Stiffness coefficient for viscous proportional damping
            hysteretic_mass_coeff: Mass coefficient for hysteretic proportional damping
            hysteretic_stiff_coeff: Stiffness coefficient for hysteretic proportional damping
            temp: Temperature (for temperature-dependent materials only)
            
        Returns:
            `0` on success, nonzero on failure
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

    # ==================== Internal methods ====================
    
    def _get(self, model) -> 'Material':
        """Fetch material data from SAP2000"""
        # 1. Get type
        result = model.PropMaterial.GetTypeOAPI(self.name)
        
        mat_type = com_data(result, 0)
        sym_type = com_data(result, 1)
        ret = com_ret(result)
        
        if mat_type is None:
            from PySap2000.exceptions import MaterialError
            raise MaterialError(f"Failed to get material {self.name} type")
        
        if ret != 0:
            from PySap2000.exceptions import MaterialError
            raise MaterialError(f"Material {self.name} does not exist")
        
        # Set type
        try:
            self.type = MaterialType(mat_type)
        except ValueError:
            self.type = MaterialType.NO_DESIGN
        
        try:
            self.symmetry_type = MaterialSymmetryType(sym_type)
        except ValueError:
            self.symmetry_type = MaterialSymmetryType.ISOTROPIC
        
        # 2. Get mechanical properties by symmetry type
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
        
        # 3. Get weight and mass density
        result = model.PropMaterial.GetWeightAndMass(self.name)
        self.w = com_data(result, 0, 0.0)
        self.m = com_data(result, 1, 0.0)
        
        return self
    
    def _create(self, model) -> int:
        """Create material in SAP2000."""
        # 1. Initialize material
        ret = model.PropMaterial.SetMaterial(
            self.name, 
            self.type.value,
            self.color,
            self.notes,
            self.guid or ""
        )
        
        if ret != 0:
            return ret
        
        # 2. Set mechanical properties
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
        
        # 3. Set weight/mass density
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
        """Delete material."""
        return model.PropMaterial.Delete(self.name)
    
    def _update(self, model) -> int:
        """
        Update properties of an existing material.

        Updates only mechanical and physical properties; it does not create a
        new material. Raises `MaterialError` if the material does not exist.
        """
        existing = self.get_name_list(model)
        if self.name not in existing:
            from PySap2000.exceptions import MaterialError
            raise MaterialError(
                f"Material '{self.name}' does not exist and cannot be updated. Use `_create` to create it first."
            )
        
        ret = 0
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
        
        if self.w > 0:
            ret = model.PropMaterial.SetWeightAndMass(
                self.name, WeightMassOption.WEIGHT, self.w
            )
        elif self.m > 0:
            ret = model.PropMaterial.SetWeightAndMass(
                self.name, WeightMassOption.MASS, self.m
            )
        
        return ret

    # ==================== Convenience properties ====================
    
    @property
    def elastic_modulus(self) -> float:
        """Elastic modulus"""
        return self.e
    
    @property
    def poisson_ratio(self) -> float:
        """Poisson's ratio"""
        return self.u
    
    @property
    def shear_modulus(self) -> float:
        """Shear modulus"""
        return self.g
    
    @property
    def thermal_expansion(self) -> float:
        """Thermal expansion coefficient"""
        return self.a
    
    @property
    def weight_density(self) -> float:
        """Weight density"""
        return self.w
    
    @property
    def mass_density(self) -> float:
        """Mass density"""
        return self.m
