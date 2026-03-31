# -*- coding: utf-8 -*-
"""
loads - Load module.

Contains all load-related dataclasses and helper functions.

Structure:
- `point_load`: Point loads (force and displacement)
- `frame_load`: Frame loads (distributed and point)
- `area_load`: Area loads
- `cable_load`: Cable loads
- `link_load`: Link loads
"""

from .point_load import (
    # Enums
    PointLoadItemType,
    # Dataclasses
    PointLoadForceData,
    PointLoadDisplData,
    # Functions
    set_point_load_force,
    get_point_load_force,
    delete_point_load_force,
    set_point_load_displ,
    get_point_load_displ,
    delete_point_load_displ,
)
from .frame_load import (
    # Enums
    FrameLoadType,
    FrameLoadDirection,
    FrameLoadItemType,
    # Dataclasses
    FrameLoadDistributedData,
    FrameLoadPointData,
    # Functions
    set_frame_load_distributed,
    get_frame_load_distributed,
    delete_frame_load_distributed,
    set_frame_load_point,
    get_frame_load_point,
    delete_frame_load_point,
)
from .area_load import (
    # Enums
    AreaLoadDir,
    AreaTempLoadType,
    AreaStrainComponent,
    AreaWindPressureType,
    AreaDistType,
    AreaLoadItemType,
    # Dataclasses
    AreaLoadGravity,
    AreaLoadUniform,
    AreaLoadSurfacePressure,
    AreaLoadTemperature,
    AreaLoadPorePressure,
    AreaLoadStrain,
    AreaLoadRotate,
    AreaLoadUniformToFrame,
    AreaLoadWindPressure,
    # Functions
    set_area_load_gravity,
    get_area_load_gravity,
    delete_area_load_gravity,
    set_area_load_uniform,
    get_area_load_uniform,
    delete_area_load_uniform,
    set_area_load_surface_pressure,
    get_area_load_surface_pressure,
    delete_area_load_surface_pressure,
    set_area_load_temperature,
    get_area_load_temperature,
    delete_area_load_temperature,
    set_area_load_pore_pressure,
    get_area_load_pore_pressure,
    delete_area_load_pore_pressure,
    set_area_load_strain,
    get_area_load_strain,
    delete_area_load_strain,
    set_area_load_rotate,
    get_area_load_rotate,
    delete_area_load_rotate,
    set_area_load_uniform_to_frame,
    get_area_load_uniform_to_frame,
    delete_area_load_uniform_to_frame,
    set_area_load_wind_pressure,
    get_area_load_wind_pressure,
    delete_area_load_wind_pressure,
)
from .cable_load import (
    # Enums
    CableLoadDirection,
    CableLoadItemType,
    # Dataclasses
    CableLoadDistributedData,
    CableLoadTemperatureData,
    CableLoadStrainData,
    CableLoadDeformationData,
    CableLoadGravityData,
    CableLoadTargetForceData,
    # Functions
    set_cable_load_distributed,
    get_cable_load_distributed,
    delete_cable_load_distributed,
    set_cable_load_temperature,
    get_cable_load_temperature,
    delete_cable_load_temperature,
    set_cable_load_strain,
    get_cable_load_strain,
    delete_cable_load_strain,
    set_cable_load_deformation,
    get_cable_load_deformation,
    delete_cable_load_deformation,
    set_cable_load_gravity,
    get_cable_load_gravity,
    delete_cable_load_gravity,
    set_cable_load_target_force,
    get_cable_load_target_force,
    delete_cable_load_target_force,
)
from .link_load import (
    # Enums
    LinkLoadItemType,
    # Dataclasses
    LinkLoadDeformationData,
    LinkLoadGravityData,
    LinkLoadTargetForceData,
    # Functions
    set_link_load_deformation,
    get_link_load_deformation,
    delete_link_load_deformation,
    set_link_load_gravity,
    get_link_load_gravity,
    delete_link_load_gravity,
    set_link_load_target_force,
    get_link_load_target_force,
    delete_link_load_target_force,
)

__all__ = [
    # Point loads - Enums
    'PointLoadItemType',
    # Point loads - Dataclasses
    'PointLoadForceData',
    'PointLoadDisplData',
    # Point loads - Functions
    'set_point_load_force',
    'get_point_load_force',
    'delete_point_load_force',
    'set_point_load_displ',
    'get_point_load_displ',
    'delete_point_load_displ',
    # Frame loads - Enums
    'FrameLoadType',
    'FrameLoadDirection',
    'FrameLoadItemType',
    # Frame loads - Dataclasses
    'FrameLoadDistributedData',
    'FrameLoadPointData',
    # Frame loads - Functions
    'set_frame_load_distributed',
    'get_frame_load_distributed',
    'delete_frame_load_distributed',
    'set_frame_load_point',
    'get_frame_load_point',
    'delete_frame_load_point',
    # Area loads - Enums
    'AreaLoadDir',
    'AreaTempLoadType',
    'AreaStrainComponent',
    'AreaWindPressureType',
    'AreaDistType',
    'AreaLoadItemType',
    # Area loads - Dataclasses
    'AreaLoadGravity',
    'AreaLoadUniform',
    'AreaLoadSurfacePressure',
    'AreaLoadTemperature',
    'AreaLoadPorePressure',
    'AreaLoadStrain',
    'AreaLoadRotate',
    'AreaLoadUniformToFrame',
    'AreaLoadWindPressure',
    # Area loads - Functions
    'set_area_load_gravity',
    'get_area_load_gravity',
    'delete_area_load_gravity',
    'set_area_load_uniform',
    'get_area_load_uniform',
    'delete_area_load_uniform',
    'set_area_load_surface_pressure',
    'get_area_load_surface_pressure',
    'delete_area_load_surface_pressure',
    'set_area_load_temperature',
    'get_area_load_temperature',
    'delete_area_load_temperature',
    'set_area_load_pore_pressure',
    'get_area_load_pore_pressure',
    'delete_area_load_pore_pressure',
    'set_area_load_strain',
    'get_area_load_strain',
    'delete_area_load_strain',
    'set_area_load_rotate',
    'get_area_load_rotate',
    'delete_area_load_rotate',
    'set_area_load_uniform_to_frame',
    'get_area_load_uniform_to_frame',
    'delete_area_load_uniform_to_frame',
    'set_area_load_wind_pressure',
    'get_area_load_wind_pressure',
    'delete_area_load_wind_pressure',
    # Cable loads - Enums
    'CableLoadDirection',
    'CableLoadItemType',
    # Cable loads - Dataclasses
    'CableLoadDistributedData',
    'CableLoadTemperatureData',
    'CableLoadStrainData',
    'CableLoadDeformationData',
    'CableLoadGravityData',
    'CableLoadTargetForceData',
    # Cable loads - Functions
    'set_cable_load_distributed',
    'get_cable_load_distributed',
    'delete_cable_load_distributed',
    'set_cable_load_temperature',
    'get_cable_load_temperature',
    'delete_cable_load_temperature',
    'set_cable_load_strain',
    'get_cable_load_strain',
    'delete_cable_load_strain',
    'set_cable_load_deformation',
    'get_cable_load_deformation',
    'delete_cable_load_deformation',
    'set_cable_load_gravity',
    'get_cable_load_gravity',
    'delete_cable_load_gravity',
    'set_cable_load_target_force',
    'get_cable_load_target_force',
    'delete_cable_load_target_force',
    # Link loads - Enums
    'LinkLoadItemType',
    # Link loads - Dataclasses
    'LinkLoadDeformationData',
    'LinkLoadGravityData',
    'LinkLoadTargetForceData',
    # Link loads - Functions
    'set_link_load_deformation',
    'get_link_load_deformation',
    'delete_link_load_deformation',
    'set_link_load_gravity',
    'get_link_load_gravity',
    'delete_link_load_gravity',
    'set_link_load_target_force',
    'get_link_load_target_force',
    'delete_link_load_target_force',
]
