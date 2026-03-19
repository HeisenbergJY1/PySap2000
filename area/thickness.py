# -*- coding: utf-8 -*-
"""
thickness.py - 面单元厚度函数
对应 SAP2000 的 AreaObj 厚度相关 API
"""

from typing import Optional, List

from .enums import AreaThicknessType, ItemType
from .data_classes import AreaThicknessData
from PySap2000.com_helper import com_ret, com_data


def set_area_thickness(
    model,
    area_name: str,
    thickness_type: AreaThicknessType,
    thickness_pattern: str,
    thickness_pattern_sf: float,
    thickness: List[float],
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置面单元厚度覆盖
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        thickness_type: 厚度类型
            - NO_OVERWRITE: 不覆盖 (使用截面属性定义的厚度)
            - BY_JOINT_PATTERN: 按节点模式
            - BY_POINT: 按节点
        thickness_pattern: 厚度模式名称 (用于 BY_JOINT_PATTERN)
        thickness_pattern_sf: 厚度模式比例因子
        thickness: 厚度值列表 (每个节点一个值，用于 BY_POINT)
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
        
    Example:
        # 按节点设置厚度
        set_area_thickness(model, "1", AreaThicknessType.BY_POINT, "", 1.0, [0.2, 0.2, 0.25, 0.25])
    """
    result = model.AreaObj.SetThickness(
        str(area_name), int(thickness_type), thickness_pattern,
        thickness_pattern_sf, thickness, int(item_type)
    )
    return com_ret(result)


def set_area_thickness_data(
    model,
    area_name: str,
    data: AreaThicknessData,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    使用数据对象设置面单元厚度覆盖
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        data: AreaThicknessData 对象
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
        
    Example:
        data = AreaThicknessData(
            thickness_type=AreaThicknessType.BY_POINT,
            thickness=[0.2, 0.2, 0.25, 0.25]
        )
        set_area_thickness_data(model, "1", data)
    """
    return model.AreaObj.SetThickness(
        str(area_name), int(data.thickness_type), data.thickness_pattern,
        data.thickness_pattern_sf, data.thickness or [], int(item_type)
    )


def get_area_thickness(
    model,
    area_name: str
) -> Optional[AreaThicknessData]:
    """
    获取面单元厚度覆盖
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        AreaThicknessData 对象，失败返回 None
        
    Example:
        data = get_area_thickness(model, "1")
        if data:
            print(f"厚度类型: {data.thickness_type}")
            print(f"厚度值: {data.thickness}")
    """
    try:
        result = model.AreaObj.GetThickness(str(area_name), 0, "", 0.0, [])
        ret = com_ret(result)
        if ret == 0:
            tt_val = com_data(result, 0)
            thickness_type = AreaThicknessType(tt_val) if tt_val is not None else AreaThicknessType.NO_OVERWRITE
            thickness_pattern = com_data(result, 1, "") or ""
            thickness_pattern_sf = com_data(result, 2, 1.0) or 1.0
            thickness_raw = com_data(result, 3)
            thickness = list(thickness_raw) if thickness_raw else None
            if True:
                return AreaThicknessData(
                    thickness_type=thickness_type,
                    thickness_pattern=thickness_pattern,
                    thickness_pattern_sf=thickness_pattern_sf,
                    thickness=thickness
                )
    except Exception:
        pass
    return None


def has_area_thickness(
    model,
    area_name: str
) -> bool:
    """
    检查面单元是否有厚度覆盖
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        True 表示有厚度覆盖，False 表示无
    """
    data = get_area_thickness(model, area_name)
    if data:
        return data.thickness_type != AreaThicknessType.NO_OVERWRITE
    return False
