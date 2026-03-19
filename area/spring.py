# -*- coding: utf-8 -*-
"""
spring.py - 面单元弹簧函数
对应 SAP2000 的 AreaObj 弹簧相关 API
"""

from typing import Optional, List, Tuple

from .enums import (
    AreaSpringType, AreaSimpleSpringType, AreaSpringLocalOneType, ItemType
)
from .data_classes import AreaSpringData
from PySap2000.com_helper import com_ret, com_data


def set_area_spring(
    model,
    area_name: str,
    spring_type: AreaSpringType,
    stiffness: float,
    simple_spring_type: AreaSimpleSpringType = AreaSimpleSpringType.TENSION_COMPRESSION,
    link_prop: str = "",
    face: int = -1,
    local_one_type: AreaSpringLocalOneType = AreaSpringLocalOneType.PARALLEL_TO_LOCAL_AXIS,
    direction: int = 3,
    outward: bool = True,
    vector: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    angle: float = 0.0,
    replace: bool = True,
    csys: str = "Local",
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置面单元弹簧
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        spring_type: 弹簧类型
            - SIMPLE_SPRING (1): 简单弹簧
            - LINK_PROPERTY (2): 连接属性
        stiffness: 弹簧刚度
        simple_spring_type: 简单弹簧类型
            - TENSION_COMPRESSION (1): 拉压
            - COMPRESSION_ONLY (2): 仅压
            - TENSION_ONLY (3): 仅拉
        link_prop: 连接属性名称 (用于 LINK_PROPERTY 类型)
        face: 面 (-1=底面, -2=顶面)
        local_one_type: 局部1轴方向类型
        direction: 方向
        outward: 是否向外
        vector: 用户向量
        angle: 角度
        replace: 是否替换现有弹簧
        csys: 坐标系
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
        
    Example:
        # 设置面单元 "1" 底面的简单弹簧
        set_area_spring(model, "1", AreaSpringType.SIMPLE_SPRING, 1000.0, face=-1)
    """
    result = model.AreaObj.SetSpring(
        str(area_name), int(spring_type), stiffness, int(simple_spring_type),
        link_prop, face, int(local_one_type), direction, outward,
        list(vector), angle, replace, csys, int(item_type)
    )
    return com_ret(result)


def set_area_spring_data(
    model,
    area_name: str,
    data: AreaSpringData,
    replace: bool = True,
    csys: str = "Local",
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    使用数据对象设置面单元弹簧
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        data: AreaSpringData 对象
        replace: 是否替换现有弹簧
        csys: 坐标系
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    return model.AreaObj.SetSpring(
        str(area_name), int(data.spring_type), data.stiffness, int(data.simple_spring_type),
        data.link_prop, data.face, int(data.local_one_type), data.direction, data.outward,
        list(data.vector), data.angle, replace, csys, int(item_type)
    )


def get_area_spring(
    model,
    area_name: str
) -> Optional[List[AreaSpringData]]:
    """
    获取面单元弹簧
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        AreaSpringData 对象列表，失败返回 None
        
    Example:
        springs = get_area_spring(model, "1")
        if springs:
            for spring in springs:
                print(f"刚度: {spring.stiffness}, 面: {spring.face}")
    """
    try:
        result = model.AreaObj.GetSpring(
            str(area_name), 0, [], [], [], [], [], [], [], [], [], []
        )
        num_springs = com_data(result, 0, 0)
        if num_springs > 0:
            springs = []
            types = com_data(result, 1)
            stiffnesses = com_data(result, 2)
            simple_types = com_data(result, 3)
            link_props = com_data(result, 4)
            faces = com_data(result, 5)
            local_one_types = com_data(result, 6)
            directions = com_data(result, 7)
            outwards = com_data(result, 8)
            vectors = com_data(result, 9)
            angles = com_data(result, 10)
            if True:
                
                for i in range(num_springs):
                    springs.append(AreaSpringData(
                        spring_type=AreaSpringType(types[i]) if types else AreaSpringType.SIMPLE_SPRING,
                        stiffness=stiffnesses[i] if stiffnesses else 0.0,
                        simple_spring_type=AreaSimpleSpringType(simple_types[i]) if simple_types else AreaSimpleSpringType.TENSION_COMPRESSION,
                        link_prop=link_props[i] if link_props else "",
                        face=faces[i] if faces else -1,
                        local_one_type=AreaSpringLocalOneType(local_one_types[i]) if local_one_types else AreaSpringLocalOneType.PARALLEL_TO_LOCAL_AXIS,
                        direction=directions[i] if directions else 3,
                        outward=outwards[i] if outwards else True,
                        vector=tuple(vectors[i]) if vectors and vectors[i] else (0.0, 0.0, 0.0),
                        angle=angles[i] if angles else 0.0
                    ))
                return springs
    except Exception:
        pass
    return None


def delete_area_spring(
    model,
    area_name: str,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    删除面单元弹簧
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        item_type: 项目类型
        
    Returns:
        0 表示成功，非 0 表示失败
    """
    return model.AreaObj.DeleteSpring(str(area_name), int(item_type))


def has_area_spring(
    model,
    area_name: str
) -> bool:
    """
    检查面单元是否有弹簧
    
    Args:
        model: SapModel 对象
        area_name: 面单元名称
        
    Returns:
        True 表示有弹簧，False 表示没有
    """
    springs = get_area_spring(model, area_name)
    return springs is not None and len(springs) > 0
