# -*- coding: utf-8 -*-
"""
area_load.py - 面单元荷载

包含:
- 枚举: AreaLoadDir, AreaTempLoadType, AreaStrainComponent, AreaWindPressureType, AreaDistType, AreaLoadItemType
- 数据类: AreaLoadGravity, AreaLoadUniform, AreaLoadSurfacePressure, AreaLoadTemperature, 
          AreaLoadPorePressure, AreaLoadStrain, AreaLoadRotate, AreaLoadUniformToFrame, AreaLoadWindPressure
- 函数: set_area_load_xxx, get_area_load_xxx, delete_area_load_xxx

SAP2000 API:
- AreaObj.SetLoadGravity / GetLoadGravity / DeleteLoadGravity
- AreaObj.SetLoadUniform / GetLoadUniform / DeleteLoadUniform
- AreaObj.SetLoadSurfacePressure / GetLoadSurfacePressure / DeleteLoadSurfacePressure
- AreaObj.SetLoadTemperature / GetLoadTemperature / DeleteLoadTemperature
- AreaObj.SetLoadPorePressure / GetLoadPorePressure / DeleteLoadPorePressure
- AreaObj.SetLoadStrain / GetLoadStrain / DeleteLoadStrain
- AreaObj.SetLoadRotate / GetLoadRotate / DeleteLoadRotate
- AreaObj.SetLoadUniformToFrame / GetLoadUniformToFrame / DeleteLoadUniformToFrame
- AreaObj.SetLoadWindPressure_1 / GetLoadWindPressure_1 / DeleteLoadWindPressure
"""

from dataclasses import dataclass
from typing import List
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


# ==================== 枚举 ====================

class AreaLoadDir(IntEnum):
    """面单元荷载方向"""
    LOCAL_1 = 1
    LOCAL_2 = 2
    LOCAL_3 = 3
    GLOBAL_X = 4
    GLOBAL_Y = 5
    GLOBAL_Z = 6
    PROJECTED_X = 7
    PROJECTED_Y = 8
    PROJECTED_Z = 9
    GRAVITY = 10
    PROJECTED_GRAVITY = 11


class AreaTempLoadType(IntEnum):
    """面单元温度荷载类型"""
    TEMPERATURE = 1
    TEMPERATURE_GRADIENT = 3


class AreaStrainComponent(IntEnum):
    """面单元应变分量"""
    STRAIN_11 = 1
    STRAIN_22 = 2
    STRAIN_12 = 3
    CURVATURE_11 = 4
    CURVATURE_22 = 5
    CURVATURE_12 = 6


class AreaWindPressureType(IntEnum):
    """面单元风压类型"""
    FROM_CP = 1
    FROM_CODE = 2


class AreaDistType(IntEnum):
    """面单元荷载分布类型"""
    ONE_WAY = 1
    TWO_WAY = 2


class AreaLoadItemType(IntEnum):
    """荷载应用对象类型"""
    OBJECT = 0
    GROUP = 1
    SELECTED_OBJECTS = 2


# ==================== 数据类 ====================

@dataclass
class AreaLoadGravity:
    """面单元重力荷载数据"""
    area_name: str = ""
    load_pattern: str = ""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    csys: str = "Global"


@dataclass
class AreaLoadUniform:
    """面单元均布荷载数据"""
    area_name: str = ""
    load_pattern: str = ""
    value: float = 0.0
    direction: AreaLoadDir = AreaLoadDir.GRAVITY
    csys: str = "Global"


@dataclass
class AreaLoadSurfacePressure:
    """面单元表面压力荷载数据"""
    area_name: str = ""
    load_pattern: str = ""
    face: int = -1
    value: float = 0.0
    pattern_name: str = ""


@dataclass
class AreaLoadTemperature:
    """面单元温度荷载数据"""
    area_name: str = ""
    load_pattern: str = ""
    load_type: AreaTempLoadType = AreaTempLoadType.TEMPERATURE
    value: float = 0.0
    pattern_name: str = ""


@dataclass
class AreaLoadPorePressure:
    """面单元孔隙压力荷载数据"""
    area_name: str = ""
    load_pattern: str = ""
    value: float = 0.0
    pattern_name: str = ""


@dataclass
class AreaLoadStrain:
    """面单元应变荷载数据"""
    area_name: str = ""
    load_pattern: str = ""
    component: AreaStrainComponent = AreaStrainComponent.STRAIN_11
    value: float = 0.0
    pattern_name: str = ""


@dataclass
class AreaLoadRotate:
    """面单元旋转荷载数据"""
    area_name: str = ""
    load_pattern: str = ""
    value: float = 0.0


@dataclass
class AreaLoadUniformToFrame:
    """面单元均布荷载传递到框架数据"""
    area_name: str = ""
    load_pattern: str = ""
    value: float = 0.0
    direction: AreaLoadDir = AreaLoadDir.GRAVITY
    dist_type: AreaDistType = AreaDistType.TWO_WAY
    csys: str = "Global"


@dataclass
class AreaLoadWindPressure:
    """面单元风压荷载数据"""
    area_name: str = ""
    load_pattern: str = ""
    wind_pressure_type: AreaWindPressureType = AreaWindPressureType.FROM_CP
    cp: float = 0.0


# ==================== 重力荷载函数 ====================

def set_area_load_gravity(
    model,
    area_name: str,
    load_pattern: str,
    x: float = 0.0,
    y: float = 0.0,
    z: float = -1.0,
    replace: bool = True,
    csys: str = "Global",
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """设置面单元重力荷载"""
    return model.AreaObj.SetLoadGravity(
        str(area_name), load_pattern, x, y, z, replace, csys, int(item_type)
    )


def get_area_load_gravity(
    model,
    area_name: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> List[AreaLoadGravity]:
    """获取面单元重力荷载"""
    loads = []
    try:
        result = model.AreaObj.GetLoadGravity(
            str(area_name), 0, [], [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            area_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            csys_list = com_data(result, 3)
            x_list = com_data(result, 4)
            y_list = com_data(result, 5)
            z_list = com_data(result, 6)
            for i in range(num_items):
                loads.append(AreaLoadGravity(
                    area_name=area_names[i] if area_names else str(area_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    x=x_list[i] if x_list else 0.0,
                    y=y_list[i] if y_list else 0.0,
                    z=z_list[i] if z_list else 0.0,
                    csys=csys_list[i] if csys_list else "Global"
                ))
    except Exception:
        pass
    return loads


def delete_area_load_gravity(
    model,
    area_name: str,
    load_pattern: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """删除面单元重力荷载"""
    return model.AreaObj.DeleteLoadGravity(str(area_name), load_pattern, int(item_type))


# ==================== 均布荷载函数 ====================

def set_area_load_uniform(
    model,
    area_name: str,
    load_pattern: str,
    value: float,
    direction: AreaLoadDir = AreaLoadDir.GRAVITY,
    replace: bool = True,
    csys: str = "Global",
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """设置面单元均布荷载"""
    return model.AreaObj.SetLoadUniform(
        str(area_name), load_pattern, value, int(direction), replace, csys, int(item_type)
    )


def get_area_load_uniform(
    model,
    area_name: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> List[AreaLoadUniform]:
    """获取面单元均布荷载"""
    loads = []
    try:
        result = model.AreaObj.GetLoadUniform(
            str(area_name), 0, [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            area_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            csys_list = com_data(result, 3)
            dir_list = com_data(result, 4)
            value_list = com_data(result, 5)
            for i in range(num_items):
                loads.append(AreaLoadUniform(
                    area_name=area_names[i] if area_names else str(area_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    value=value_list[i] if value_list else 0.0,
                    direction=AreaLoadDir(dir_list[i]) if dir_list else AreaLoadDir.GRAVITY,
                    csys=csys_list[i] if csys_list else "Global"
                ))
    except Exception:
        pass
    return loads


def delete_area_load_uniform(
    model,
    area_name: str,
    load_pattern: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """删除面单元均布荷载"""
    return model.AreaObj.DeleteLoadUniform(str(area_name), load_pattern, int(item_type))


# ==================== 表面压力荷载函数 ====================

def set_area_load_surface_pressure(
    model,
    area_name: str,
    load_pattern: str,
    face: int,
    value: float,
    pattern_name: str = "",
    replace: bool = True,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """设置面单元表面压力荷载 (face: -1=底面, -2=顶面)"""
    return model.AreaObj.SetLoadSurfacePressure(
        str(area_name), load_pattern, face, value, pattern_name, replace, int(item_type)
    )


def get_area_load_surface_pressure(
    model,
    area_name: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> List[AreaLoadSurfacePressure]:
    """获取面单元表面压力荷载"""
    loads = []
    try:
        result = model.AreaObj.GetLoadSurfacePressure(
            str(area_name), 0, [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            area_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            faces = com_data(result, 3)
            values = com_data(result, 4)
            patterns = com_data(result, 5)
            for i in range(num_items):
                loads.append(AreaLoadSurfacePressure(
                    area_name=area_names[i] if area_names else str(area_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    face=faces[i] if faces else -1,
                    value=values[i] if values else 0.0,
                    pattern_name=patterns[i] if patterns else ""
                ))
    except Exception:
        pass
    return loads


def delete_area_load_surface_pressure(
    model,
    area_name: str,
    load_pattern: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """删除面单元表面压力荷载"""
    return model.AreaObj.DeleteLoadSurfacePressure(str(area_name), load_pattern, int(item_type))


# ==================== 温度荷载函数 ====================

def set_area_load_temperature(
    model,
    area_name: str,
    load_pattern: str,
    load_type: AreaTempLoadType,
    value: float,
    pattern_name: str = "",
    replace: bool = True,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """设置面单元温度荷载"""
    return model.AreaObj.SetLoadTemperature(
        str(area_name), load_pattern, int(load_type), value, pattern_name, replace, int(item_type)
    )


def get_area_load_temperature(
    model,
    area_name: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> List[AreaLoadTemperature]:
    """获取面单元温度荷载"""
    loads = []
    try:
        result = model.AreaObj.GetLoadTemperature(
            str(area_name), 0, [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            area_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            load_types = com_data(result, 3)
            values = com_data(result, 4)
            patterns = com_data(result, 5)
            for i in range(num_items):
                loads.append(AreaLoadTemperature(
                    area_name=area_names[i] if area_names else str(area_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    load_type=AreaTempLoadType(load_types[i]) if load_types else AreaTempLoadType.TEMPERATURE,
                    value=values[i] if values else 0.0,
                    pattern_name=patterns[i] if patterns else ""
                ))
    except Exception:
        pass
    return loads


def delete_area_load_temperature(
    model,
    area_name: str,
    load_pattern: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """删除面单元温度荷载"""
    return model.AreaObj.DeleteLoadTemperature(str(area_name), load_pattern, int(item_type))


# ==================== 孔隙压力荷载函数 ====================

def set_area_load_pore_pressure(
    model,
    area_name: str,
    load_pattern: str,
    value: float,
    pattern_name: str = "",
    replace: bool = True,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """设置面单元孔隙压力荷载"""
    return model.AreaObj.SetLoadPorePressure(
        str(area_name), load_pattern, value, pattern_name, replace, int(item_type)
    )


def get_area_load_pore_pressure(
    model,
    area_name: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> List[AreaLoadPorePressure]:
    """获取面单元孔隙压力荷载"""
    loads = []
    try:
        result = model.AreaObj.GetLoadPorePressure(
            str(area_name), 0, [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            area_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            values = com_data(result, 3)
            patterns = com_data(result, 4)
            for i in range(num_items):
                loads.append(AreaLoadPorePressure(
                    area_name=area_names[i] if area_names else str(area_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    value=values[i] if values else 0.0,
                    pattern_name=patterns[i] if patterns else ""
                ))
    except Exception:
        pass
    return loads


def delete_area_load_pore_pressure(
    model,
    area_name: str,
    load_pattern: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """删除面单元孔隙压力荷载"""
    return model.AreaObj.DeleteLoadPorePressure(str(area_name), load_pattern, int(item_type))


# ==================== 应变荷载函数 ====================

def set_area_load_strain(
    model,
    area_name: str,
    load_pattern: str,
    component: AreaStrainComponent,
    value: float,
    replace: bool = True,
    pattern_name: str = "",
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """设置面单元应变荷载"""
    return model.AreaObj.SetLoadStrain(
        str(area_name), load_pattern, int(component), value, replace, pattern_name, int(item_type)
    )


def get_area_load_strain(
    model,
    area_name: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> List[AreaLoadStrain]:
    """获取面单元应变荷载"""
    loads = []
    try:
        result = model.AreaObj.GetLoadStrain(
            str(area_name), 0, [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            area_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            components = com_data(result, 3)
            values = com_data(result, 4)
            patterns = com_data(result, 5)
            for i in range(num_items):
                loads.append(AreaLoadStrain(
                    area_name=area_names[i] if area_names else str(area_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    component=AreaStrainComponent(components[i]) if components else AreaStrainComponent.STRAIN_11,
                    value=values[i] if values else 0.0,
                    pattern_name=patterns[i] if patterns else ""
                ))
    except Exception:
        pass
    return loads


def delete_area_load_strain(
    model,
    area_name: str,
    load_pattern: str,
    component: AreaStrainComponent,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """删除面单元应变荷载"""
    return model.AreaObj.DeleteLoadStrain(str(area_name), load_pattern, int(component), int(item_type))


# ==================== 旋转荷载函数 ====================

def set_area_load_rotate(
    model,
    area_name: str,
    load_pattern: str,
    value: float,
    replace: bool = True,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """设置面单元旋转荷载 (value: 旋转速度 rad/s)"""
    return model.AreaObj.SetLoadRotate(
        str(area_name), load_pattern, value, replace, int(item_type)
    )


def get_area_load_rotate(
    model,
    area_name: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> List[AreaLoadRotate]:
    """获取面单元旋转荷载"""
    loads = []
    try:
        result = model.AreaObj.GetLoadRotate(
            str(area_name), 0, [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            area_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            values = com_data(result, 3)
            for i in range(num_items):
                loads.append(AreaLoadRotate(
                    area_name=area_names[i] if area_names else str(area_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    value=values[i] if values else 0.0
                ))
    except Exception:
        pass
    return loads


def delete_area_load_rotate(
    model,
    area_name: str,
    load_pattern: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """删除面单元旋转荷载"""
    return model.AreaObj.DeleteLoadRotate(str(area_name), load_pattern, int(item_type))


# ==================== 均布荷载传递到框架函数 ====================

def set_area_load_uniform_to_frame(
    model,
    area_name: str,
    load_pattern: str,
    value: float,
    direction: AreaLoadDir = AreaLoadDir.GRAVITY,
    dist_type: AreaDistType = AreaDistType.TWO_WAY,
    replace: bool = True,
    csys: str = "Global",
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """设置面单元均布荷载传递到框架"""
    return model.AreaObj.SetLoadUniformToFrame(
        str(area_name), load_pattern, value, int(direction), int(dist_type),
        replace, csys, int(item_type)
    )


def get_area_load_uniform_to_frame(
    model,
    area_name: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> List[AreaLoadUniformToFrame]:
    """获取面单元均布荷载传递到框架"""
    loads = []
    try:
        result = model.AreaObj.GetLoadUniformToFrame(
            str(area_name), 0, [], [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            area_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            csys_list = com_data(result, 3)
            dir_list = com_data(result, 4)
            value_list = com_data(result, 5)
            dist_types = com_data(result, 6)
            for i in range(num_items):
                loads.append(AreaLoadUniformToFrame(
                    area_name=area_names[i] if area_names else str(area_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    value=value_list[i] if value_list else 0.0,
                    direction=AreaLoadDir(dir_list[i]) if dir_list else AreaLoadDir.GRAVITY,
                    dist_type=AreaDistType(dist_types[i]) if dist_types else AreaDistType.TWO_WAY,
                    csys=csys_list[i] if csys_list else "Global"
                ))
    except Exception:
        pass
    return loads


def delete_area_load_uniform_to_frame(
    model,
    area_name: str,
    load_pattern: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """删除面单元均布荷载传递到框架"""
    return model.AreaObj.DeleteLoadUniformToFrame(str(area_name), load_pattern, int(item_type))


# ==================== 风压荷载函数 ====================

def set_area_load_wind_pressure(
    model,
    area_name: str,
    load_pattern: str,
    wind_pressure_type: AreaWindPressureType = AreaWindPressureType.FROM_CP,
    cp: float = 0.0,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """设置面单元风压荷载"""
    return model.AreaObj.SetLoadWindPressure_1(
        str(area_name), load_pattern, int(wind_pressure_type), cp, int(item_type)
    )


def get_area_load_wind_pressure(
    model,
    area_name: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> List[AreaLoadWindPressure]:
    """获取面单元风压荷载"""
    loads = []
    try:
        result = model.AreaObj.GetLoadWindPressure_1(
            str(area_name), 0, [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            area_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            wind_types = com_data(result, 3)
            cps = com_data(result, 4)
            for i in range(num_items):
                loads.append(AreaLoadWindPressure(
                    area_name=area_names[i] if area_names else str(area_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    wind_pressure_type=AreaWindPressureType(wind_types[i]) if wind_types else AreaWindPressureType.FROM_CP,
                    cp=cps[i] if cps else 0.0
                ))
    except Exception:
        pass
    return loads


def delete_area_load_wind_pressure(
    model,
    area_name: str,
    load_pattern: str,
    item_type: AreaLoadItemType = AreaLoadItemType.OBJECT
) -> int:
    """删除面单元风压荷载"""
    return model.AreaObj.DeleteLoadWindPressure(str(area_name), load_pattern, int(item_type))
