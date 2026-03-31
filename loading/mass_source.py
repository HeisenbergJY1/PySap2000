# -*- coding: utf-8 -*-
"""
mass_source.py - Mass source definitions.

Wraps the SAP2000 `SourceMass` API.

Mass sources define where mass comes from in dynamic analysis, including:
- element self-mass (`MassFromElements`)
- explicitly assigned masses (`MassFromMasses`)
- load patterns (`MassFromLoads`)

SAP2000 API:
- `SourceMass.SetMassSource` - create or update a mass source
- `SourceMass.GetMassSource` - get mass source data
- `SourceMass.GetNameList` - get all mass source names
- `SourceMass.Count` - get the number of mass sources
- `SourceMass.ChangeName` - rename a mass source
- `SourceMass.Delete` - delete a mass source
- `SourceMass.GetDefault` - get the default mass source
- `SourceMass.SetDefault` - set the default mass source

Usage:
    from PySap2000.loading import MassSource, MassSourceLoad
    
    # Create a mass source
    ms = MassSource(
        name="MyMassSource",
        mass_from_elements=True,
        mass_from_masses=True,
        mass_from_loads=True,
        is_default=True,
        loads=[MassSourceLoad("DEAD", 1.0), MassSourceLoad("SDL", 0.5)]
    )
    ms._create(model)
    
    # Get a mass source
    ms = MassSource.get_by_name(model, "MSSSRC1")
    
    # Get the default mass source
    default_name = MassSource.get_default_name(model)
"""

from dataclasses import dataclass, field
from typing import List, Optional, ClassVar, Union

from PySap2000.com_helper import com_ret, com_data


@dataclass
class MassSourceLoad:
    """
    Load pattern definition within a mass source.
    
    Attributes:
        load_pattern: Load pattern name
        scale_factor: Scale factor
    """
    load_pattern: str
    scale_factor: float = 1.0


@dataclass
class MassSource:
    """
    Mass source definition.

    Used to define mass sources for dynamic analysis.
    
    Attributes:
        name: Mass source name
        mass_from_elements: Whether element self-mass is included
        mass_from_masses: Whether explicitly assigned masses are included
        mass_from_loads: Whether load patterns are included
        is_default: Whether this is the default mass source
        loads: List of load patterns, used when `mass_from_loads=True`
    """
    name: str = ""
    mass_from_elements: bool = True
    mass_from_masses: bool = True
    mass_from_loads: bool = False
    is_default: bool = False
    loads: List[MassSourceLoad] = field(default_factory=list)
    
    _object_type: ClassVar[str] = "SourceMass"
    
    def _create(self, model) -> int:
        """
        Create or update a mass source.

        If a mass source with the same name already exists, it is overwritten.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` if successful.
        """
        num_loads = len(self.loads)
        load_patterns = [ld.load_pattern for ld in self.loads] if self.loads else []
        scale_factors = [ld.scale_factor for ld in self.loads] if self.loads else []
        
        return model.SourceMass.SetMassSource(
            self.name,
            self.mass_from_elements,
            self.mass_from_masses,
            self.mass_from_loads,
            self.is_default,
            num_loads,
            load_patterns,
            scale_factors
        )
    
    def _get(self, model) -> int:
        """
        Retrieve mass source data from the model.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` if successful.
        """
        result = model.SourceMass.GetMassSource(
            self.name, False, False, False, False, 0, [], []
        )
        
        self.mass_from_elements = com_data(result, 0, False)
        self.mass_from_masses = com_data(result, 1, False)
        self.mass_from_loads = com_data(result, 2, False)
        self.is_default = com_data(result, 3, False)
        num_loads = com_data(result, 4, 0)
        load_patterns = com_data(result, 5) or []
        scale_factors = com_data(result, 6) or []
        ret = com_ret(result)
        
        self.loads = []
        if num_loads > 0 and load_patterns and scale_factors:
            for i in range(num_loads):
                self.loads.append(MassSourceLoad(
                    load_pattern=load_patterns[i],
                    scale_factor=scale_factors[i]
                ))
        
        return ret if ret is not None else -1
    
    def _delete(self, model) -> int:
        """
        Delete a mass source.

        Note: The default mass source cannot be deleted.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` if successful.
        """
        return model.SourceMass.Delete(self.name)
    
    def change_name(self, model, new_name: str) -> int:
        """
        Rename a mass source.
        
        Args:
            model: SAP2000 SapModel object
            new_name: New name
            
        Returns:
            `0` if successful.
        """
        ret = model.SourceMass.ChangeName(self.name, new_name)
        if ret == 0:
            self.name = new_name
        return ret
    
    def set_as_default(self, model) -> int:
        """
        Set this mass source as the default.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` if successful.
        """
        ret = model.SourceMass.SetDefault(self.name)
        if ret == 0:
            self.is_default = True
        return ret
    
    @staticmethod
    def get_count(model) -> int:
        """
        Get the number of mass sources.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            Mass source count.
        """
        return model.SourceMass.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """
        Get the names of all mass sources.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            List of mass source names.
        """
        result = model.SourceMass.GetNameList(0, [])
        names = com_data(result, 1)
        if names:
            return list(names)
        return []
    
    @staticmethod
    def get_default_name(model) -> str:
        """
        Get the name of the default mass source.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            Default mass source name.
        """
        result = model.SourceMass.GetDefault("")
        name = com_data(result, 0)
        return name if name else ""
    
    @classmethod
    def get_by_name(cls, model, name: str) -> Optional["MassSource"]:
        """
        Get a mass source by name.
        
        Args:
            model: SAP2000 SapModel object
            name: Mass source name
            
        Returns:
            `MassSource` instance, or `None` if it does not exist.
        """
        ms = cls(name=name)
        ret = ms._get(model)
        if ret == 0:
            return ms
        return None
    
    @classmethod
    def get_all(cls, model) -> List["MassSource"]:
        """
        Get all mass sources.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            List of `MassSource`.
        """
        names = cls.get_name_list(model)
        result = []
        for name in names:
            ms = cls.get_by_name(model, name)
            if ms:
                result.append(ms)
        return result
    
    @classmethod
    def get_default(cls, model) -> Optional["MassSource"]:
        """
        Get the default mass source.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            Default `MassSource` instance.
        """
        name = cls.get_default_name(model)
        if name:
            return cls.get_by_name(model, name)
        return None
    
    def add_load(self, load_pattern: str, scale_factor: float = 1.0) -> None:
        """
        Add a load pattern to the mass source.
        
        Args:
            load_pattern: Load pattern name
            scale_factor: Scale factor
        """
        self.loads.append(MassSourceLoad(load_pattern, scale_factor))
        self.mass_from_loads = True
    
    def clear_loads(self) -> None:
        """Clear all load patterns."""
        self.loads = []
