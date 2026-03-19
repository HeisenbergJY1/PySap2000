# -*- coding: utf-8 -*-
"""
loads - 荷载模块

包含所有荷载相关的数据类和函数

结构:
- point_load: 节点荷载 (力荷载、位移荷载)
- frame_load: 框架荷载 (分布荷载、集中荷载)
- area_load: 面荷载
- cable_load: 索荷载
- link_load: 连接荷载
"""

from .point_load import (
    # 枚举
    PointLoadItemType,
    # 数据类
    PointLoadForceData,
    PointLoadDisplData,
    # 函数
    set_point_load_force,
    get_point_load_force,
    delete_point_load_force,
    set_point_load_displ,
    get_point_load_displ,
    delete_point_load_displ,
)
from .frame_load import (
    # 枚举
    FrameLoadType,
    FrameLoadDirection,
    FrameLoadItemType,
    # 数据类
    FrameLoadDistributedData,
    FrameLoadPointData,
    # 函数
    set_frame_load_distributed,
    get_frame_load_distributed,
    delete_frame_load_distributed,
    set_frame_load_point,
    get_frame_load_point,
    delete_frame_load_point,
)
from .area_load import (
    # 枚举
    AreaLoadDir,
    AreaTempLoadType,
    AreaStrainComponent,
    AreaWindPressureType,
    AreaDistType,
    AreaLoadItemType,
    # 数据类
    AreaLoadGravity,
    AreaLoadUniform,
    AreaLoadSurfacePressure,
    AreaLoadTemperature,
    AreaLoadPorePressure,
    AreaLoadStrain,
    AreaLoadRotate,
    AreaLoadUniformToFrame,
    AreaLoadWindPressure,
    # 函数
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
    # 枚举
    CableLoadDirection,
    CableLoadItemType,
    # 数据类
    CableLoadDistributedData,
    CableLoadTemperatureData,
    CableLoadStrainData,
    CableLoadDeformationData,
    CableLoadGravityData,
    CableLoadTargetForceData,
    # 函数
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
    # 枚举
    LinkLoadItemType,
    # 数据类
    LinkLoadDeformationData,
    LinkLoadGravityData,
    LinkLoadTargetForceData,
    # 函数
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
    # Point 荷载 - 枚举
    'PointLoadItemType',
    # Point 荷载 - 数据类
    'PointLoadForceData',
    'PointLoadDisplData',
    # Point 荷载 - 函数
    'set_point_load_force',
    'get_point_load_force',
    'delete_point_load_force',
    'set_point_load_displ',
    'get_point_load_displ',
    'delete_point_load_displ',
    # Frame 荷载 - 枚举
    'FrameLoadType',
    'FrameLoadDirection',
    'FrameLoadItemType',
    # Frame 荷载 - 数据类
    'FrameLoadDistributedData',
    'FrameLoadPointData',
    # Frame 荷载 - 函数
    'set_frame_load_distributed',
    'get_frame_load_distributed',
    'delete_frame_load_distributed',
    'set_frame_load_point',
    'get_frame_load_point',
    'delete_frame_load_point',
    # Area 荷载 - 枚举
    'AreaLoadDir',
    'AreaTempLoadType',
    'AreaStrainComponent',
    'AreaWindPressureType',
    'AreaDistType',
    'AreaLoadItemType',
    # Area 荷载 - 数据类
    'AreaLoadGravity',
    'AreaLoadUniform',
    'AreaLoadSurfacePressure',
    'AreaLoadTemperature',
    'AreaLoadPorePressure',
    'AreaLoadStrain',
    'AreaLoadRotate',
    'AreaLoadUniformToFrame',
    'AreaLoadWindPressure',
    # Area 荷载 - 函数
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
    # Cable 荷载 - 枚举
    'CableLoadDirection',
    'CableLoadItemType',
    # Cable 荷载 - 数据类
    'CableLoadDistributedData',
    'CableLoadTemperatureData',
    'CableLoadStrainData',
    'CableLoadDeformationData',
    'CableLoadGravityData',
    'CableLoadTargetForceData',
    # Cable 荷载 - 函数
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
    # Link 荷载 - 枚举
    'LinkLoadItemType',
    # Link 荷载 - 数据类
    'LinkLoadDeformationData',
    'LinkLoadGravityData',
    'LinkLoadTargetForceData',
    # Link 荷载 - 函数
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
