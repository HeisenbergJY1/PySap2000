# -*- coding: utf-8 -*-
"""
load_case.py - Load case definitions.

Wraps the SAP2000 `LoadCases` API.

Load cases define how the structure is analyzed. Each case type has its own
subtypes and parameter sets.

SAP2000 API structure:
- `LoadCases` (base API)
  - `ChangeName`, `Count`, `Delete`, `GetNameList_1`, `GetTypeOAPI_2`, `SetDesignType`
- `LoadCases.StaticLinear`
- `LoadCases.StaticNonlinear`
- `LoadCases.ModalEigen`
- `LoadCases.ModalRitz`
- `LoadCases.ResponseSpectrum`
- `LoadCases.DirHistLinear`
- `LoadCases.DirHistNonlinear`
- `LoadCases.ModHistLinear`
- `LoadCases.ModHistNonlinear`
- `LoadCases.Buckling`
- `LoadCases.SteadyState`
- `LoadCases.PSD`
- `LoadCases.MovingLoad`
- `LoadCases.Hyperstatic`
- `LoadCases.StaticLinearMultistep`
- `LoadCases.StaticNonlinearMultistep`
- `LoadCases.StaticNonlinearStaged`

Usage:
    from PySap2000.loading import LoadCase, LoadCaseType
    
    # Get all load cases
    all_cases = LoadCase.get_all(model)
    
    # Filter by type
    static_cases = LoadCase.get_name_list(model, LoadCaseType.LINEAR_STATIC)
    
    # Get load case information
    case = LoadCase.get_by_name(model, "DEAD")
    print(f"Type: {case.case_type.name}")
"""

from dataclasses import dataclass, field
from typing import List, Optional, ClassVar, Union, Tuple
from enum import IntEnum

from .load_pattern import LoadPatternType
from PySap2000.com_helper import com_ret, com_data


class LoadCaseType(IntEnum):
    """
    Load case type.

    Matches the SAP2000 `eLoadCaseType` enum.
    """
    LINEAR_STATIC = 1               # Linear static
    NONLINEAR_STATIC = 2            # Nonlinear static
    MODAL = 3                       # Modal
    RESPONSE_SPECTRUM = 4           # Response spectrum
    LINEAR_HISTORY = 5              # Modal linear time history
    NONLINEAR_HISTORY = 6           # Modal nonlinear time history
    LINEAR_DYNAMIC = 7              # Direct-integration linear time history
    NONLINEAR_DYNAMIC = 8           # Direct-integration nonlinear time history
    MOVING_LOAD = 9                 # Moving load
    BUCKLING = 10                   # Buckling
    STEADY_STATE = 11               # Steady state
    POWER_SPECTRAL_DENSITY = 12     # Power spectral density
    LINEAR_STATIC_MULTISTEP = 13    # Multi-step linear static
    HYPERSTATIC = 14                # Hyperstatic
    EXTERNAL_RESULTS = 15           # External results
    STAGED_CONSTRUCTION = 16        # Staged construction
    NONLINEAR_STATIC_MULTISTEP = 17 # Multi-step nonlinear static


class ModalSubType(IntEnum):
    """
    Modal load case subtype.

    Only applies to `LoadCaseType.MODAL`.
    """
    EIGEN = 1   # Eigen modal
    RITZ = 2    # Ritz modal


class TimeHistorySubType(IntEnum):
    """
    Time-history load case subtype.

    Only applies to `LoadCaseType.LINEAR_HISTORY`.
    """
    TRANSIENT = 1   # Transient
    PERIODIC = 2    # Periodic


class DesignTypeOption(IntEnum):
    """
    Design type option.
    """
    PROGRAM_DETERMINED = 0  # Program determined
    USER_SPECIFIED = 1      # User specified


@dataclass
class LoadCaseLoad:
    """
    Single load definition inside a load case.

    Used for load settings in `StaticLinear` and similar case types.
    
    Attributes:
        load_type: `"Load"` (load pattern) or `"Accel"` (acceleration)
        load_name: Load pattern name or direction (`UX`, `UY`, `UZ`, `RX`, `RY`, `RZ`)
        scale_factor: Scale factor
    """
    load_type: str = "Load"     # "Load" or "Accel"
    load_name: str = ""         # Pattern name or direction
    scale_factor: float = 1.0


@dataclass
class LoadCase:
    """
    Load case definition.

    Wraps SAP2000 `LoadCases`.

    This is a base class that provides common operations across all load case
    types. Detailed setup for specific case types must still be done through
    the corresponding sub-APIs.
    
    Attributes:
        name: Case name
        case_type: Case type (`LoadCaseType`)
        sub_type: Subtype, only meaningful for modal and linear-history cases
        design_type: Design type (`LoadPatternType`)
        design_type_option: Design type option
        is_auto: Whether the case is auto-created
    """
    name: str = ""
    case_type: LoadCaseType = LoadCaseType.LINEAR_STATIC
    sub_type: int = 0
    design_type: LoadPatternType = LoadPatternType.DEAD
    design_type_option: DesignTypeOption = DesignTypeOption.PROGRAM_DETERMINED
    is_auto: bool = False
    
    _object_type: ClassVar[str] = "LoadCases"

    
    def _get(self, model) -> int:
        """
        Retrieve load case data from the model.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` if successful.
        """
        result = model.LoadCases.GetTypeOAPI_2(
            self.name, 0, 0, 0, 0, 0
        )
        
        try:
            self.case_type = LoadCaseType(com_data(result, 0, 1))
        except ValueError:
            self.case_type = LoadCaseType.LINEAR_STATIC
        
        self.sub_type = com_data(result, 1, 0)
        
        try:
            self.design_type = LoadPatternType(com_data(result, 2, 8))
        except ValueError:
            self.design_type = LoadPatternType.OTHER
        
        try:
            self.design_type_option = DesignTypeOption(com_data(result, 3, 0))
        except ValueError:
            self.design_type_option = DesignTypeOption.PROGRAM_DETERMINED
        
        self.is_auto = bool(com_data(result, 4, False))
        ret = com_ret(result)
        
        return ret
    
    def _delete(self, model) -> int:
        """
        Delete the load case.
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` if successful.
        """
        return model.LoadCases.Delete(self.name)
    
    def change_name(self, model, new_name: str) -> int:
        """
        Rename the load case.
        
        Args:
            model: SAP2000 SapModel object
            new_name: New name
            
        Returns:
            `0` if successful.
        """
        ret = model.LoadCases.ChangeName(self.name, new_name)
        if ret == 0:
            self.name = new_name
        return ret
    
    def set_design_type(
        self, 
        model, 
        design_type_option: DesignTypeOption,
        design_type: LoadPatternType = LoadPatternType.DEAD
    ) -> int:
        """
        Set the design type.
        
        Args:
            model: SAP2000 SapModel object
            design_type_option: Design type option (`program determined` or `user specified`)
            design_type: Design type, only used when `design_type_option=USER_SPECIFIED`
            
        Returns:
            `0` if successful.
        """
        ret = model.LoadCases.SetDesignType(
            self.name,
            int(design_type_option),
            int(design_type)
        )
        if ret == 0:
            self.design_type_option = design_type_option
            if design_type_option == DesignTypeOption.USER_SPECIFIED:
                self.design_type = design_type
        return ret
    
    @staticmethod
    def get_count(model, case_type: Optional[LoadCaseType] = None) -> int:
        """
        Get the number of load cases.
        
        Args:
            model: SAP2000 SapModel object
            case_type: Optional case type filter
            
        Returns:
            Load case count.
        """
        if case_type is None:
            return model.LoadCases.Count()
        else:
            return model.LoadCases.Count(int(case_type))
    
    @staticmethod
    def get_name_list(
        model, 
        case_type: Optional[LoadCaseType] = None
    ) -> List[str]:
        """
        Get the list of load case names.
        
        Args:
            model: SAP2000 SapModel object
            case_type: Optional case type filter
            
        Returns:
            List of load case names.
        """
        if case_type is None:
            result = model.LoadCases.GetNameList_1(0, [])
        else:
            result = model.LoadCases.GetNameList_1(0, [], int(case_type))
        
        names = com_data(result, 1)
        if names:
            return list(names)
        return []
    
    @classmethod
    def get_by_name(cls, model, name: str) -> Optional["LoadCase"]:
        """
        Get a load case by name.
        
        Args:
            model: SAP2000 SapModel object
            name: Case name
            
        Returns:
            `LoadCase` instance, or `None` if it does not exist.
        """
        case = cls(name=name)
        ret = case._get(model)
        if ret == 0:
            return case
        return None
    
    @classmethod
    def get_all(
        cls, 
        model, 
        case_type: Optional[LoadCaseType] = None
    ) -> List["LoadCase"]:
        """
        Get all load cases.
        
        Args:
            model: SAP2000 SapModel object
            case_type: Optional case type filter
            
        Returns:
            List of `LoadCase`.
        """
        names = cls.get_name_list(model, case_type)
        result = []
        for name in names:
            case = cls.get_by_name(model, name)
            if case:
                result.append(case)
        return result
    
    def get_modal_sub_type(self) -> Optional[ModalSubType]:
        """
        Get the modal subtype.

        Only valid when `case_type == MODAL`.
        
        Returns:
            `ModalSubType` or `None`.
        """
        if self.case_type == LoadCaseType.MODAL and self.sub_type in (1, 2):
            return ModalSubType(self.sub_type)
        return None
    
    def get_time_history_sub_type(self) -> Optional[TimeHistorySubType]:
        """
        Get the time-history subtype.

        Only valid when `case_type == LINEAR_HISTORY`.
        
        Returns:
            `TimeHistorySubType` or `None`.
        """
        if self.case_type == LoadCaseType.LINEAR_HISTORY and self.sub_type in (1, 2):
            return TimeHistorySubType(self.sub_type)
        return None


# =============================================================================
# Static case creation helpers
# =============================================================================

def create_static_linear_case(model, name: str) -> int:
    """
    Create a linear static load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.StaticLinear.SetCase(name)


def create_static_nonlinear_case(model, name: str) -> int:
    """
    Create a nonlinear static load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.StaticNonlinear.SetCase(name)


# =============================================================================
# Modal case creation helpers
# =============================================================================

def create_modal_eigen_case(model, name: str) -> int:
    """
    Create an eigen modal load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.ModalEigen.SetCase(name)


def create_modal_ritz_case(model, name: str) -> int:
    """
    Create a Ritz modal load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.ModalRitz.SetCase(name)


# =============================================================================
# Dynamic case creation helpers
# =============================================================================

def create_response_spectrum_case(model, name: str) -> int:
    """
    Create a response-spectrum load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.ResponseSpectrum.SetCase(name)


def create_buckling_case(model, name: str) -> int:
    """
    Create a buckling load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.Buckling.SetCase(name)


# =============================================================================
# Time-history case creation helpers
# =============================================================================

def create_direct_history_linear_case(model, name: str) -> int:
    """
    Create a direct-integration linear time-history load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.DirHistLinear.SetCase(name)


def create_direct_history_nonlinear_case(model, name: str) -> int:
    """
    Create a direct-integration nonlinear time-history load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.DirHistNonlinear.SetCase(name)


def create_modal_history_linear_case(model, name: str) -> int:
    """
    Create a modal linear time-history load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.ModHistLinear.SetCase(name)


def create_modal_history_nonlinear_case(model, name: str) -> int:
    """
    Create a modal nonlinear time-history load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.ModHistNonlinear.SetCase(name)


# =============================================================================
# Other case creation helpers
# =============================================================================

def create_steady_state_case(model, name: str) -> int:
    """
    Create a steady-state load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.SteadyState.SetCase(name)


def create_psd_case(model, name: str) -> int:
    """
    Create a power spectral density load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.PSD.SetCase(name)


def create_moving_load_case(model, name: str) -> int:
    """
    Create a moving load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.MovingLoad.SetCase(name)


def create_hyperstatic_case(model, name: str) -> int:
    """
    Create a hyperstatic load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.Hyperstatic.SetCase(name)


# =============================================================================
# Multi-step case creation helpers
# =============================================================================

def create_static_linear_multistep_case(model, name: str) -> int:
    """
    Create a multi-step linear static load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.StaticLinearMultistep.SetCase(name)


def create_static_nonlinear_multistep_case(model, name: str) -> int:
    """
    Create a multi-step nonlinear static load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.StaticNonlinearMultistep.SetCase(name)


def create_staged_construction_case(model, name: str) -> int:
    """
    Create a staged-construction load case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        `0` if successful.
    """
    return model.LoadCases.StaticNonlinearStaged.SetCase(name)


# =============================================================================
# Static-case load-setting helpers
# =============================================================================

def get_static_linear_loads(
    model, 
    name: str
) -> Tuple[List[LoadCaseLoad], int]:
    """
    Get load definitions for a linear static case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        
    Returns:
        Tuple `(loads, return_code)`.
    """
    result = model.LoadCases.StaticLinear.GetLoads(name, 0, [], [], [])
    
    loads = []
    num_loads = com_data(result, 0, 0)
    load_types = com_data(result, 1) or []
    load_names = com_data(result, 2) or []
    scale_factors = com_data(result, 3) or []
    ret = com_ret(result)
    
    if ret == 0 and num_loads > 0:
        for i in range(num_loads):
            load = LoadCaseLoad(
                load_type=load_types[i] if i < len(load_types) else "Load",
                load_name=load_names[i] if i < len(load_names) else "",
                scale_factor=scale_factors[i] if i < len(scale_factors) else 1.0
            )
            loads.append(load)
        return loads, ret
    
    return [], -1


def set_static_linear_loads(
    model, 
    name: str, 
    loads: List[LoadCaseLoad]
) -> int:
    """
    Set load definitions for a linear static case.
    
    Args:
        model: SAP2000 SapModel object
        name: Case name
        loads: List of load definitions
        
    Returns:
        `0` if successful.
    """
    if not loads:
        return -1
    
    num_loads = len(loads)
    load_types = [load.load_type for load in loads]
    load_names = [load.load_name for load in loads]
    scale_factors = [load.scale_factor for load in loads]
    
    return model.LoadCases.StaticLinear.SetLoads(
        name, num_loads, load_types, load_names, scale_factors
    )
