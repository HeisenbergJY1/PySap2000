# -*- coding: utf-8 -*-
"""
model_settings.py - Model-wide settings.

Includes active degrees of freedom, merge tolerance, coordinate system, and related options.

API Reference:
    - Analyze.GetActiveDOF(DOF[]) -> Long
    - Analyze.SetActiveDOF(DOF[]) -> Long
    - GetMergeTol(MergeTol) -> Long
    - SetMergeTol(MergeTol) -> Long
    - GetPresentCoordSystem() -> String
    - SetPresentCoordSystem(CSys) -> Long

Usage:
    from PySap2000.global_parameters import ModelSettings, ActiveDOF

    dof = ModelSettings.get_active_dof(model)

    # 2D XZ plane (UX, UZ, RY)
    ModelSettings.set_active_dof(model, ActiveDOF.XZ_PLANE)

    ModelSettings.set_merge_tolerance(model, 0.01)
"""

from dataclasses import dataclass
from typing import Tuple, List
from enum import IntEnum
from PySap2000.com_helper import com_ret, com_data


class ActiveDOF(IntEnum):
    """
    Preset active-DOF configurations.
    """
    FULL_3D = 0          # Full 3D (UX, UY, UZ, RX, RY, RZ)
    XZ_PLANE = 1         # XZ plane (UX, UZ, RY)
    XY_PLANE = 2         # XY plane (UX, UY, RZ)
    SPACE_TRUSS = 3      # Space truss (UX, UY, UZ)
    PLANE_TRUSS_XZ = 4   # Plane truss XZ (UX, UZ)
    PLANE_TRUSS_XY = 5   # Plane truss XY (UX, UY)
    GRID = 6             # Grid (UZ, RX, RY)


# Preset -> six booleans (UX, UY, UZ, RX, RY, RZ)
DOF_PRESETS = {
    ActiveDOF.FULL_3D: (True, True, True, True, True, True),
    ActiveDOF.XZ_PLANE: (True, False, True, False, True, False),
    ActiveDOF.XY_PLANE: (True, True, False, False, False, True),
    ActiveDOF.SPACE_TRUSS: (True, True, True, False, False, False),
    ActiveDOF.PLANE_TRUSS_XZ: (True, False, True, False, False, False),
    ActiveDOF.PLANE_TRUSS_XY: (True, True, False, False, False, False),
    ActiveDOF.GRID: (False, False, True, True, True, False),
}


@dataclass
class DOFState:
    """
    Active degree-of-freedom flags in global axes.

    Attributes:
        ux: Translation along X
        uy: Translation along Y
        uz: Translation along Z
        rx: Rotation about X
        ry: Rotation about Y
        rz: Rotation about Z
    """
    ux: bool = True
    uy: bool = True
    uz: bool = True
    rx: bool = True
    ry: bool = True
    rz: bool = True
    
    def to_tuple(self) -> Tuple[bool, ...]:
        """Return a 6-tuple of booleans."""
        return (self.ux, self.uy, self.uz, self.rx, self.ry, self.rz)
    
    def to_list(self) -> List[bool]:
        """Return a 6-element list of booleans."""
        return [self.ux, self.uy, self.uz, self.rx, self.ry, self.rz]
    
    @classmethod
    def from_tuple(cls, dof: Tuple[bool, ...]) -> 'DOFState':
        """Build from a 6-tuple (or shorter tuple, padded with defaults)."""
        return cls(
            ux=dof[0] if len(dof) > 0 else True,
            uy=dof[1] if len(dof) > 1 else True,
            uz=dof[2] if len(dof) > 2 else True,
            rx=dof[3] if len(dof) > 3 else True,
            ry=dof[4] if len(dof) > 4 else True,
            rz=dof[5] if len(dof) > 5 else True,
        )
    
    @classmethod
    def from_preset(cls, preset: ActiveDOF) -> 'DOFState':
        """Build from an `ActiveDOF` preset."""
        dof = DOF_PRESETS.get(preset, (True,) * 6)
        return cls.from_tuple(dof)


class ModelSettings:
    """
    Static helpers for model-level SAP2000 settings.
    """
    
    # --- Active degrees of freedom ---
    
    @staticmethod
    def get_active_dof(model) -> DOFState:
        """
        Get the active degrees of freedom.

        API: Analyze.GetActiveDOF(DOF[]) -> Long

        Returns:
            `DOFState` instance.
        """
        result = model.Analyze.GetActiveDOF([False]*6)
        dof = com_data(result, 0, None)
        if dof and len(dof) >= 6:
            return DOFState.from_tuple(tuple(dof))
        return DOFState()
    
    @staticmethod
    def set_active_dof(
        model, 
        dof: ActiveDOF = None,
        custom_dof: Tuple[bool, ...] = None
    ) -> int:
        """
        Set the active degrees of freedom.

        API: Analyze.SetActiveDOF(DOF[]) -> Long

        Args:
            model: SAP2000 SapModel object
            dof: Preset (`ActiveDOF`), ignored if `custom_dof` is given
            custom_dof: Explicit six booleans `(UX, UY, UZ, RX, RY, RZ)`

        Returns:
            SAP2000 return code (`0` typically means success).
        """
        if custom_dof is not None:
            dof_list = list(custom_dof)
            if len(dof_list) < 6:
                dof_list.extend([False] * (6 - len(dof_list)))
        elif dof is not None:
            dof_list = list(DOF_PRESETS.get(dof, (True,) * 6))
        else:
            dof_list = [True] * 6
        
        result = model.Analyze.SetActiveDOF(dof_list)
        return com_ret(result)
    
    @staticmethod
    def set_2d_xz_plane(model) -> int:
        """Use the XZ plane 2D DOF preset."""
        return ModelSettings.set_active_dof(model, ActiveDOF.XZ_PLANE)
    
    @staticmethod
    def set_2d_xy_plane(model) -> int:
        """Use the XY plane 2D DOF preset."""
        return ModelSettings.set_active_dof(model, ActiveDOF.XY_PLANE)
    
    @staticmethod
    def set_3d_full(model) -> int:
        """Use the full 3D DOF preset."""
        return ModelSettings.set_active_dof(model, ActiveDOF.FULL_3D)
    
    # --- Merge tolerance ---
    
    @staticmethod
    def get_merge_tolerance(model) -> float:
        """
        Get automatic merge tolerance (length units).

        API: GetMergeTol(MergeTol) -> Long

        Returns:
            Merge tolerance [L].
        """
        result = model.GetMergeTol(0.0)
        val = com_data(result, 0, None)
        if val is not None:
            return val
        return result if isinstance(result, float) else 0.0
    
    @staticmethod
    def set_merge_tolerance(model, tolerance: float) -> int:
        """
        Set automatic merge tolerance.

        API: SetMergeTol(MergeTol) -> Long

        Args:
            model: SAP2000 SapModel object
            tolerance: Merge tolerance [L]

        Returns:
            `0` if successful.
        """
        return model.SetMergeTol(tolerance)
    
    # --- Coordinate system ---
    
    @staticmethod
    def get_present_coord_system(model) -> str:
        """
        Get the present coordinate system name.

        API: GetPresentCoordSystem() -> String

        Returns:
            Coordinate system name.
        """
        return model.GetPresentCoordSystem()
    
    @staticmethod
    def set_present_coord_system(model, csys: str) -> int:
        """
        Set the present coordinate system.

        API: SetPresentCoordSystem(CSys) -> Long

        Args:
            model: SAP2000 SapModel object
            csys: Coordinate system name

        Returns:
            `0` if successful.
        """
        return model.SetPresentCoordSystem(csys)
    
    # --- Model lock ---
    
    @staticmethod
    def is_model_locked(model) -> bool:
        """
        Return whether the model is locked.

        API: GetModelIsLocked() -> Boolean
        """
        return model.GetModelIsLocked()
    
    @staticmethod
    def set_model_locked(model, locked: bool) -> int:
        """
        Set the model lock state.

        API: SetModelIsLocked(Locked) -> Long
        """
        return model.SetModelIsLocked(locked)
    
    @staticmethod
    def unlock_model(model) -> int:
        """Unlock the model."""
        return ModelSettings.set_model_locked(model, False)
    
    @staticmethod
    def lock_model(model) -> int:
        """Lock the model."""
        return ModelSettings.set_model_locked(model, True)
    
    # --- Model file paths ---
    
    @staticmethod
    def get_model_filename(model) -> str:
        """
        Get the model file name (no path).

        API: GetModelFilename() -> String
        """
        return model.GetModelFilename()
    
    @staticmethod
    def get_model_filepath(model) -> str:
        """
        Get the full model file path.

        API: GetModelFilepath() -> String
        """
        return model.GetModelFilepath()
