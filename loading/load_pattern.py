# -*- coding: utf-8 -*-
"""
load_pattern.py - Load pattern definitions.

Wraps the SAP2000 `LoadPatterns` API.

Load patterns are the basis for load assignment, such as `DEAD` and `LIVE`.
Each load pattern can optionally create a corresponding linear static load case.

SAP2000 API:
- `LoadPatterns.Add` - add a load pattern
- `LoadPatterns.ChangeName` - rename a load pattern
- `LoadPatterns.Count` - get the number of load patterns
- `LoadPatterns.Delete` - delete a load pattern
- `LoadPatterns.GetLoadType` - get the load type
- `LoadPatterns.GetNameList` - get all load pattern names
- `LoadPatterns.GetSelfWtMultiplier` - get the self-weight multiplier
- `LoadPatterns.SetLoadType` - set the load type
- `LoadPatterns.SetSelfWtMultiplier` - set the self-weight multiplier

Usage:
    from PySap2000.loading import LoadPattern, LoadPatternType
    
    # Create a load pattern
    dead = LoadPattern(
        name="DEAD",
        load_type=LoadPatternType.DEAD,
        self_weight_multiplier=1.0
    )
    dead._create(model)
    
    # Get a load pattern
    lp = LoadPattern.get_by_name(model, "DEAD")
    print(f"Type: {lp.load_type.name}, SW: {lp.self_weight_multiplier}")
    
    # Get all load patterns
    all_patterns = LoadPattern.get_all(model)
"""

from dataclasses import dataclass
from typing import List, Optional, ClassVar, Union
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class LoadPatternType(IntEnum):
    """
    Load pattern type.

    Matches the SAP2000 `eLoadPatternType` enum.
    """
    DEAD = 1                        # Dead load
    SUPERDEAD = 2                   # Super dead load
    LIVE = 3                        # Live load
    REDUCELIVE = 4                  # Reducible live load
    QUAKE = 5                       # Earthquake
    WIND = 6                        # Wind load
    SNOW = 7                        # Snow load
    OTHER = 8                       # Other
    MOVE = 9                        # Moving load
    TEMPERATURE = 10                # Temperature
    ROOFLIVE = 11                   # Roof live load
    NOTIONAL = 12                   # Notional load
    PATTERNLIVE = 13                # Pattern live load
    WAVE = 14                       # Wave
    BRAKING = 15                    # Braking force
    CENTRIFUGAL = 16                # Centrifugal force
    FRICTION = 17                   # Friction
    ICE = 18                        # Ice load
    WINDONLIVELOAD = 19             # Wind on live load
    HORIZONTALEARTHPRESSURE = 20    # Horizontal earth pressure
    VERTICALEARTHPRESSURE = 21      # Vertical earth pressure
    EARTHSURCHARGE = 22             # Earth surcharge
    DOWNDRAG = 23                   # Downdrag
    VEHICLECOLLISION = 24           # Vehicle collision
    VESSELCOLLISION = 25            # Vessel collision
    TEMPERATUREGRADIENT = 26        # Temperature gradient
    SETTLEMENT = 27                 # Settlement
    SHRINKAGE = 28                  # Shrinkage
    CREEP = 29                      # Creep
    WATERLOADPRESSURE = 30          # Water pressure
    LIVELOADSURCHARGE = 31          # Live load surcharge
    LOCKEDINFORCES = 32             # Locked-in forces
    PEDESTRIANLL = 33               # Pedestrian live load
    PRESTRESS = 34                  # Prestress
    HYPERSTATIC = 35                # Hyperstatic
    BOUYANCY = 36                   # Buoyancy
    STREAMFLOW = 37                 # Stream flow
    IMPACT = 38                     # Impact
    CONSTRUCTION = 39               # Construction


@dataclass
class LoadPattern:
    """
    Load pattern definition.

    Wraps SAP2000 `LoadPatterns`.
    
    Attributes:
        name: Load pattern name
        load_type: Load type (`LoadPatternType`)
        self_weight_multiplier: Self-weight multiplier
        add_load_case: Whether to automatically create a corresponding linear static load case
    """
    name: str = ""
    load_type: LoadPatternType = LoadPatternType.OTHER
    self_weight_multiplier: float = 0.0
    add_load_case: bool = True
    
    _object_type: ClassVar[str] = "LoadPatterns"
    
    def _create(self, model) -> int:
        """
        Create a load pattern.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` if successful, `-1` if it already exists.
        """
        # Check whether the load pattern already exists.
        if self.name:
            try:
                existing = self.get_name_list(model)
                if self.name in existing:
                    return -1
            except Exception:
                pass
        
        result = model.LoadPatterns.Add(
            self.name,
            int(self.load_type),
            self.self_weight_multiplier,
            self.add_load_case
        )
        return com_ret(result)
    
    def _get(self, model) -> int:
        """
        Retrieve load pattern data from the model.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` if successful.
        """
        # Get the load pattern type.
        result = model.LoadPatterns.GetLoadType(self.name, 0)
        try:
            self.load_type = LoadPatternType(com_data(result, 0, 0))
        except ValueError:
            self.load_type = LoadPatternType.OTHER
        ret1 = com_ret(result)
        
        # Get the self-weight multiplier.
        result = model.LoadPatterns.GetSelfWtMultiplier(self.name, 0.0)
        self.self_weight_multiplier = com_data(result, 0, 0.0)
        ret2 = com_ret(result)
        
        return 0 if ret1 == 0 and ret2 == 0 else -1
    
    def _delete(self, model) -> int:
        """
        Delete a load pattern.

        Note: A load pattern cannot be deleted if it is referenced by a load case
        or if it is the only remaining load pattern.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` if successful.
        """
        return model.LoadPatterns.Delete(self.name)
    
    def change_name(self, model, new_name: str) -> int:
        """
        Rename a load pattern.
        
        Args:
            model: SAP2000 SapModel object
            new_name: New name
            
        Returns:
            `0` if successful.
        """
        ret = model.LoadPatterns.ChangeName(self.name, new_name)
        if ret == 0:
            self.name = new_name
        return ret
    
    def set_load_type(self, model, load_type: LoadPatternType) -> int:
        """
        Set the load pattern type.
        
        Args:
            model: SAP2000 SapModel object
            load_type: Load pattern type
            
        Returns:
            `0` if successful.
        """
        ret = model.LoadPatterns.SetLoadType(self.name, int(load_type))
        if ret == 0:
            self.load_type = load_type
        return ret
    
    def set_self_weight_multiplier(self, model, multiplier: float) -> int:
        """
        Set the self-weight multiplier.
        
        Args:
            model: SAP2000 SapModel object
            multiplier: Self-weight multiplier
            
        Returns:
            `0` if successful.
        """
        ret = model.LoadPatterns.SetSelfWtMultiplier(self.name, multiplier)
        if ret == 0:
            self.self_weight_multiplier = multiplier
        return ret
    
    @staticmethod
    def get_count(model) -> int:
        """
        Get the number of load patterns.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            Load pattern count.
        """
        return model.LoadPatterns.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """
        Get the names of all load patterns.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            List of load pattern names.
        """
        result = model.LoadPatterns.GetNameList(0, [])
        names = com_data(result, 1)
        if names:
            return list(names)
        return []
    
    @classmethod
    def get_by_name(cls, model, name: str) -> Optional["LoadPattern"]:
        """
        Get a load pattern by name.
        
        Args:
            model: SAP2000 SapModel object
            name: Load pattern name
            
        Returns:
            `LoadPattern` instance, or `None` if it does not exist.
        """
        lp = cls(name=name)
        ret = lp._get(model)
        if ret == 0:
            return lp
        return None
    
    @classmethod
    def get_all(cls, model) -> List["LoadPattern"]:
        """
        Get all load patterns.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            List of `LoadPattern`.
        """
        names = cls.get_name_list(model)
        result = []
        for name in names:
            lp = cls.get_by_name(model, name)
            if lp:
                result.append(lp)
        return result
