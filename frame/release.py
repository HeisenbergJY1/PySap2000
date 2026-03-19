# -*- coding: utf-8 -*-
"""
release.py - 杆件端部释放相关函数

用于设置杆件端部的约束释放（铰接）

SAP2000 API:
- FrameObj.SetReleases(Name, II[], JJ[], StartValue[], EndValue[], ItemType)
- FrameObj.GetReleases(Name, II[], JJ[], StartValue[], EndValue[])
"""

from typing import Tuple, Optional
from .enums import ItemType, FrameReleaseType, RELEASE_PRESETS
from .data_classes import FrameReleaseData
from PySap2000.com_helper import com_ret, com_data


def set_frame_release(
    model,
    frame_name: str,
    release_type: FrameReleaseType,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置杆件端部释放类型（便捷方法）
    
    使用预定义的释放类型快速设置。
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        release_type: 释放类型
            - BOTH_FIXED: 两端固定
            - I_END_HINGED: I端铰接 (释放 R2, R3)
            - J_END_HINGED: J端铰接 (释放 R2, R3)
            - BOTH_HINGED: 两端铰接
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        # 设置杆件两端铰接
        set_frame_release(model, "1", FrameReleaseType.BOTH_HINGED)
        
        # 设置杆件 I 端铰接
        set_frame_release(model, "1", FrameReleaseType.I_END_HINGED)
    """
    release_i, release_j = RELEASE_PRESETS.get(
        release_type, 
        ((False,)*6, (False,)*6)
    )
    
    result = model.FrameObj.SetReleases(
        str(frame_name),
        list(release_i),
        list(release_j),
        [0.0] * 6,
        [0.0] * 6,
        int(item_type)
    )
    return com_ret(result)


def set_frame_release_custom(
    model,
    frame_name: str,
    release_i: Tuple[bool, bool, bool, bool, bool, bool],
    release_j: Tuple[bool, bool, bool, bool, bool, bool],
    start_value: Tuple[float, ...] = None,
    end_value: Tuple[float, ...] = None,
    item_type: ItemType = ItemType.OBJECT
) -> int:
    """
    设置杆件自定义端部释放
    
    可以自由组合 6 个自由度的释放状态。
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
        release_i: I端释放 (U1, U2, U3, R1, R2, R3)
            - True: 释放该自由度
            - False: 固定该自由度
        release_j: J端释放 (U1, U2, U3, R1, R2, R3)
        start_value: I端部分固定刚度值 (可选)
        end_value: J端部分固定刚度值 (可选)
        item_type: 操作范围
    
    Returns:
        0 表示成功
    
    Example:
        # I端释放 R2, R3 (弯矩铰)
        set_frame_release_custom(
            model, "1",
            (False, False, False, False, True, True),
            (False, False, False, False, False, False)
        )
        
        # 两端释放扭转
        set_frame_release_custom(
            model, "1",
            (False, False, False, True, False, False),
            (False, False, False, True, False, False)
        )
    """
    if start_value is None:
        start_value = (0.0,) * 6
    if end_value is None:
        end_value = (0.0,) * 6
    
    return model.FrameObj.SetReleases(
        str(frame_name),
        list(release_i),
        list(release_j),
        list(start_value),
        list(end_value),
        int(item_type)
    )


def get_frame_release(
    model,
    frame_name: str
) -> Optional[FrameReleaseData]:
    """
    获取杆件端部释放状态
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        FrameReleaseData 对象，失败返回 None
    
    Example:
        release = get_frame_release(model, "1")
        if release:
            print(f"I端释放: {release.release_i}")
            print(f"J端释放: {release.release_j}")
    """
    try:
        result = model.FrameObj.GetReleases(str(frame_name))
        ri = com_data(result, 0)
        rj = com_data(result, 1)
        if ri is not None:
            return FrameReleaseData(
                frame_name=str(frame_name),
                release_i=tuple(ri) if ri else (False,) * 6,
                release_j=tuple(rj) if rj else (False,) * 6,
                start_value=tuple(com_data(result, 2, [0.0]*6)),
                end_value=tuple(com_data(result, 3, [0.0]*6))
            )
    except Exception:
        pass
    return None


def get_frame_release_type(
    model,
    frame_name: str
) -> Optional[FrameReleaseType]:
    """
    获取杆件端部释放类型
    
    根据释放状态推断释放类型。
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        释放类型，如果不匹配预定义类型则返回 None
    
    Example:
        release_type = get_frame_release_type(model, "1")
        if release_type == FrameReleaseType.BOTH_HINGED:
            print("这是两端铰接杆件")
    """
    release = get_frame_release(model, frame_name)
    if release:
        for rtype, (expected_i, expected_j) in RELEASE_PRESETS.items():
            if release.release_i == expected_i and release.release_j == expected_j:
                return rtype
    return None


def is_frame_hinged(
    model,
    frame_name: str
) -> Tuple[bool, bool]:
    """
    检查杆件端部是否铰接
    
    Args:
        model: SapModel 对象
        frame_name: 杆件名称
    
    Returns:
        (I端是否铰接, J端是否铰接)
    
    Example:
        i_hinged, j_hinged = is_frame_hinged(model, "1")
        if i_hinged:
            print("I端是铰接")
    """
    release = get_frame_release(model, frame_name)
    if release:
        # 检查 R2 和 R3 是否都释放
        i_hinged = release.release_i[4] and release.release_i[5]
        j_hinged = release.release_j[4] and release.release_j[5]
        return (i_hinged, j_hinged)
    return (False, False)
