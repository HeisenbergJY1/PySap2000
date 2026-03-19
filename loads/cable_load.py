# -*- coding: utf-8 -*-
"""
cable_load.py - 索单元荷载

包含:
- 枚举: CableLoadDirection, CableLoadItemType
- 数据类: CableLoadDistributedData, CableLoadTemperatureData, CableLoadStrainData,
          CableLoadDeformationData, CableLoadGravityData, CableLoadTargetForceData
- 函数: set_cable_load_xxx, get_cable_load_xxx, delete_cable_load_xxx

SAP2000 API:
- CableObj.SetLoadDistributed / GetLoadDistributed / DeleteLoadDistributed
- CableObj.SetLoadTemperature / GetLoadTemperature / DeleteLoadTemperature
- CableObj.SetLoadStrain / GetLoadStrain / DeleteLoadStrain
- CableObj.SetLoadDeformation / GetLoadDeformation / DeleteLoadDeformation
- CableObj.SetLoadGravity / GetLoadGravity / DeleteLoadGravity
- CableObj.SetLoadTargetForce / GetLoadTargetForce / DeleteLoadTargetForce
"""

from dataclasses import dataclass
from typing import List
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


# ==================== 枚举 ====================

class CableLoadDirection(IntEnum):
    """索单元荷载方向"""
    LOCAL_1 = 1                 # 局部1轴 (仅 CSys=Local)
    LOCAL_2 = 2                 # 局部2轴 (仅 CSys=Local)
    LOCAL_3 = 3                 # 局部3轴 (仅 CSys=Local)
    GLOBAL_X = 4                # 全局X方向
    GLOBAL_Y = 5                # 全局Y方向
    GLOBAL_Z = 6                # 全局Z方向
    PROJECTED_GLOBAL_X = 7      # 投影全局X方向
    PROJECTED_GLOBAL_Y = 8      # 投影全局Y方向
    PROJECTED_GLOBAL_Z = 9      # 投影全局Z方向
    GRAVITY = 10                # 重力方向 (负全局Z)
    PROJECTED_GRAVITY = 11      # 投影重力方向


class CableLoadItemType(IntEnum):
    """荷载应用对象类型"""
    OBJECT = 0              # 单个对象
    GROUP = 1               # 组
    SELECTED_OBJECTS = 2    # 选中对象


# ==================== 数据类 ====================

@dataclass
class CableLoadDistributedData:
    """索单元分布荷载数据"""
    cable_name: str = ""
    load_pattern: str = ""
    load_type: int = 1      # 1=Force, 2=Moment
    direction: int = 10     # 默认重力方向
    value: float = 0.0
    csys: str = "Global"


@dataclass
class CableLoadTemperatureData:
    """索单元温度荷载数据"""
    cable_name: str = ""
    load_pattern: str = ""
    load_type: int = 1      # 1=Temperature, 2=Temperature Gradient
    value: float = 0.0
    pattern_name: str = ""


@dataclass
class CableLoadStrainData:
    """索单元应变荷载数据"""
    cable_name: str = ""
    load_pattern: str = ""
    strain_type: int = 1    # 1=Axial
    value: float = 0.0
    pattern_name: str = ""


@dataclass
class CableLoadDeformationData:
    """索单元变形荷载数据"""
    cable_name: str = ""
    load_pattern: str = ""
    value: float = 0.0      # 轴向变形 [L]


@dataclass
class CableLoadGravityData:
    """索单元重力荷载数据"""
    cable_name: str = ""
    load_pattern: str = ""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    csys: str = "Global"


@dataclass
class CableLoadTargetForceData:
    """索单元目标力荷载数据"""
    cable_name: str = ""
    load_pattern: str = ""
    p: float = 0.0          # 目标轴力 [F]
    rd: float = 0.5         # 相对距离 (0-1)


# ==================== 分布荷载函数 ====================

def set_cable_load_distributed(
    model,
    cable_name: str,
    load_pattern: str,
    value: float,
    load_type: int = 1,
    direction: CableLoadDirection = CableLoadDirection.GRAVITY,
    csys: str = "Global",
    replace: bool = True,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    设置索单元分布荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        load_pattern: 荷载模式名称
        value: 荷载值 [F/L]
        load_type: 荷载类型 (1=Force, 2=Moment)
        direction: 荷载方向
        csys: 坐标系名称
        replace: True=替换现有荷载, False=叠加
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        set_cable_load_distributed(model, "1", "DEAD", 10)
    """
    return model.CableObj.SetLoadDistributed(
        str(cable_name), load_pattern, load_type, int(direction),
        value, csys, replace, int(item_type)
    )


def get_cable_load_distributed(
    model,
    cable_name: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> List[CableLoadDistributedData]:
    """
    获取索单元分布荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        item_type: 操作范围
    
    Returns:
        CableLoadDistributedData 对象列表
    """
    loads = []
    try:
        result = model.CableObj.GetLoadDistributed(
            str(cable_name), 0, [], [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            cable_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            my_types = com_data(result, 3)
            csys_list = com_data(result, 4)
            dirs = com_data(result, 5)
            vals = com_data(result, 6)
            for i in range(num_items):
                loads.append(CableLoadDistributedData(
                    cable_name=cable_names[i] if cable_names else str(cable_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    load_type=my_types[i] if my_types else 1,
                    direction=dirs[i] if dirs else 10,
                    value=vals[i] if vals else 0.0,
                    csys=csys_list[i] if csys_list else "Global"
                ))
    except Exception:
        pass
    return loads


def delete_cable_load_distributed(
    model,
    cable_name: str,
    load_pattern: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    删除索单元分布荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        load_pattern: 荷载模式名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.CableObj.DeleteLoadDistributed(str(cable_name), load_pattern, int(item_type))


# ==================== 温度荷载函数 ====================

def set_cable_load_temperature(
    model,
    cable_name: str,
    load_pattern: str,
    value: float,
    load_type: int = 1,
    pattern_name: str = "",
    replace: bool = True,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    设置索单元温度荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        load_pattern: 荷载模式名称
        value: 温度值
        load_type: 荷载类型 (1=Temperature, 2=Temperature Gradient)
        pattern_name: 模式名称
        replace: True=替换现有荷载, False=叠加
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.CableObj.SetLoadTemperature(
        str(cable_name), load_pattern, load_type, value, pattern_name, replace, int(item_type)
    )


def get_cable_load_temperature(
    model,
    cable_name: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> List[CableLoadTemperatureData]:
    """
    获取索单元温度荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        item_type: 操作范围
    
    Returns:
        CableLoadTemperatureData 对象列表
    """
    loads = []
    try:
        result = model.CableObj.GetLoadTemperature(
            str(cable_name), 0, [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            cable_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            load_types = com_data(result, 3)
            values = com_data(result, 4)
            patterns = com_data(result, 5)
            for i in range(num_items):
                loads.append(CableLoadTemperatureData(
                    cable_name=cable_names[i] if cable_names else str(cable_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    load_type=load_types[i] if load_types else 1,
                    value=values[i] if values else 0.0,
                    pattern_name=patterns[i] if patterns else ""
                ))
    except Exception:
        pass
    return loads


def delete_cable_load_temperature(
    model,
    cable_name: str,
    load_pattern: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    删除索单元温度荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        load_pattern: 荷载模式名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.CableObj.DeleteLoadTemperature(str(cable_name), load_pattern, int(item_type))


# ==================== 应变荷载函数 ====================

def set_cable_load_strain(
    model,
    cable_name: str,
    load_pattern: str,
    value: float,
    strain_type: int = 1,
    pattern_name: str = "",
    replace: bool = True,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    设置索单元应变荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        load_pattern: 荷载模式名称
        value: 应变值
        strain_type: 应变类型 (1=Axial)
        pattern_name: 模式名称
        replace: True=替换现有荷载, False=叠加
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.CableObj.SetLoadStrain(
        str(cable_name), load_pattern, strain_type, value, pattern_name, replace, int(item_type)
    )


def get_cable_load_strain(
    model,
    cable_name: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> List[CableLoadStrainData]:
    """
    获取索单元应变荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        item_type: 操作范围
    
    Returns:
        CableLoadStrainData 对象列表
    """
    loads = []
    try:
        result = model.CableObj.GetLoadStrain(
            str(cable_name), 0, [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            cable_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            strain_types = com_data(result, 3)
            values = com_data(result, 4)
            patterns = com_data(result, 5)
            for i in range(num_items):
                loads.append(CableLoadStrainData(
                    cable_name=cable_names[i] if cable_names else str(cable_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    strain_type=strain_types[i] if strain_types else 1,
                    value=values[i] if values else 0.0,
                    pattern_name=patterns[i] if patterns else ""
                ))
    except Exception:
        pass
    return loads


def delete_cable_load_strain(
    model,
    cable_name: str,
    load_pattern: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    删除索单元应变荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        load_pattern: 荷载模式名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.CableObj.DeleteLoadStrain(str(cable_name), load_pattern, int(item_type))



# ==================== 变形荷载函数 ====================

def set_cable_load_deformation(
    model,
    cable_name: str,
    load_pattern: str,
    value: float,
    replace: bool = True,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    设置索单元变形荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        load_pattern: 荷载模式名称
        value: 轴向变形值 [L]
        replace: True=替换现有荷载, False=叠加
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.CableObj.SetLoadDeformation(
        str(cable_name), load_pattern, value, replace, int(item_type)
    )


def get_cable_load_deformation(
    model,
    cable_name: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> List[CableLoadDeformationData]:
    """
    获取索单元变形荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        item_type: 操作范围
    
    Returns:
        CableLoadDeformationData 对象列表
    """
    loads = []
    try:
        result = model.CableObj.GetLoadDeformation(
            str(cable_name), 0, [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            cable_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            values = com_data(result, 3)
            for i in range(num_items):
                loads.append(CableLoadDeformationData(
                    cable_name=cable_names[i] if cable_names else str(cable_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    value=values[i] if values else 0.0
                ))
    except Exception:
        pass
    return loads


def delete_cable_load_deformation(
    model,
    cable_name: str,
    load_pattern: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    删除索单元变形荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        load_pattern: 荷载模式名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.CableObj.DeleteLoadDeformation(str(cable_name), load_pattern, int(item_type))


# ==================== 重力荷载函数 ====================

def set_cable_load_gravity(
    model,
    cable_name: str,
    load_pattern: str,
    x: float = 0.0,
    y: float = 0.0,
    z: float = -1.0,
    replace: bool = True,
    csys: str = "Global",
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    设置索单元重力荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        load_pattern: 荷载模式名称
        x: X方向重力系数
        y: Y方向重力系数
        z: Z方向重力系数 (默认-1)
        replace: True=替换现有荷载, False=叠加
        csys: 坐标系名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.CableObj.SetLoadGravity(
        str(cable_name), load_pattern, x, y, z, replace, csys, int(item_type)
    )


def get_cable_load_gravity(
    model,
    cable_name: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> List[CableLoadGravityData]:
    """
    获取索单元重力荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        item_type: 操作范围
    
    Returns:
        CableLoadGravityData 对象列表
    """
    loads = []
    try:
        result = model.CableObj.GetLoadGravity(
            str(cable_name), 0, [], [], [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            cable_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            csys_list = com_data(result, 3)
            x_list = com_data(result, 4)
            y_list = com_data(result, 5)
            z_list = com_data(result, 6)
            for i in range(num_items):
                loads.append(CableLoadGravityData(
                    cable_name=cable_names[i] if cable_names else str(cable_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    x=x_list[i] if x_list else 0.0,
                    y=y_list[i] if y_list else 0.0,
                    z=z_list[i] if z_list else 0.0,
                    csys=csys_list[i] if csys_list else "Global"
                ))
    except Exception:
        pass
    return loads


def delete_cable_load_gravity(
    model,
    cable_name: str,
    load_pattern: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    删除索单元重力荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        load_pattern: 荷载模式名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.CableObj.DeleteLoadGravity(str(cable_name), load_pattern, int(item_type))


# ==================== 目标力荷载函数 ====================

def set_cable_load_target_force(
    model,
    cable_name: str,
    load_pattern: str,
    p: float,
    rd: float = 0.5,
    replace: bool = True,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    设置索单元目标力荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        load_pattern: 荷载模式名称
        p: 目标轴力 [F]
        rd: 相对距离 (0-1)
        replace: True=替换现有荷载, False=叠加
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.CableObj.SetLoadTargetForce(
        str(cable_name), load_pattern, p, rd, replace, int(item_type)
    )


def get_cable_load_target_force(
    model,
    cable_name: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> List[CableLoadTargetForceData]:
    """
    获取索单元目标力荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        item_type: 操作范围
    
    Returns:
        CableLoadTargetForceData 对象列表
    """
    loads = []
    try:
        result = model.CableObj.GetLoadTargetForce(
            str(cable_name), 0, [], [], [], [], int(item_type)
        )
        num_items = com_data(result, 0, 0)
        if num_items > 0:
            cable_names = com_data(result, 1)
            load_pats = com_data(result, 2)
            p_list = com_data(result, 3)
            rd_list = com_data(result, 4)
            for i in range(num_items):
                loads.append(CableLoadTargetForceData(
                    cable_name=cable_names[i] if cable_names else str(cable_name),
                    load_pattern=load_pats[i] if load_pats else "",
                    p=p_list[i] if p_list else 0.0,
                    rd=rd_list[i] if rd_list else 0.5
                ))
    except Exception:
        pass
    return loads


def delete_cable_load_target_force(
    model,
    cable_name: str,
    load_pattern: str,
    item_type: CableLoadItemType = CableLoadItemType.OBJECT
) -> int:
    """
    删除索单元目标力荷载
    
    Args:
        model: SapModel 对象
        cable_name: 索单元名称
        load_pattern: 荷载模式名称
        item_type: 操作范围
    
    Returns:
        0 表示成功
    """
    return model.CableObj.DeleteLoadTargetForce(str(cable_name), load_pattern, int(item_type))