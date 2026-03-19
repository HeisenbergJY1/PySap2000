# -*- coding: utf-8 -*-
"""
enums.py - 杆件相关枚举类型

包含 SAP2000 FrameObj API 使用的枚举

注意: 荷载相关枚举已移至 loads/frame_load.py
"""

from enum import IntEnum


class FrameType(IntEnum):
    """杆件类型"""
    BEAM = 1      # 梁
    COLUMN = 2    # 柱
    BRACE = 3     # 支撑
    TRUSS = 4     # 桁架
    OTHER = 5     # 其他


class FrameSectionType(IntEnum):
    """
    截面类型
    对应 SAP2000 PropFrame.GetTypeOAPI 返回值
    """
    I_SECTION = 1           # I形截面
    CHANNEL = 2             # 槽钢
    T_SECTION = 3           # T形截面
    ANGLE = 4               # 角钢
    DOUBLE_ANGLE = 5        # 双角钢
    BOX = 6                 # 箱形/方管
    PIPE = 7                # 圆管
    RECTANGULAR = 8         # 矩形
    CIRCLE = 9              # 圆形
    GENERAL = 10            # 通用截面
    DOUBLE_CHANNEL = 11     # 双槽钢
    AUTO = 12               # 自动选择
    SD = 13                 # 截面设计器
    VARIABLE = 14           # 变截面
    JOIST = 15              # 托梁
    BRIDGE = 16             # 桥梁截面
    COLD_C = 17             # 冷弯C型钢
    COLD_2C = 18            # 冷弯双C型钢
    COLD_Z = 19             # 冷弯Z型钢
    COLD_L = 20             # 冷弯角钢
    COLD_2L = 21            # 冷弯双角钢
    COLD_HAT = 22           # 冷弯帽形钢
    BUILTUP_I_COVERPLATE = 23  # 组合I形盖板
    PCC_GIRDER_I = 24       # 预制混凝土I梁
    PCC_GIRDER_U = 25       # 预制混凝土U梁
    BUILTUP_I_HYBRID = 26   # 组合I形混合
    BUILTUP_U_HYBRID = 27   # 组合U形混合
    PCC_GIRDER_SUPER_T = 41 # 预制混凝土超级T梁
    COLD_BOX = 42           # 冷弯箱形
    COLD_I = 43             # 冷弯I形
    COLD_PIPE = 44          # 冷弯圆管
    COLD_T = 45             # 冷弯T形
    TRAPEZOIDAL = 46        # 梯形


class FrameReleaseType(IntEnum):
    """杆件端部释放类型（便捷枚举）"""
    BOTH_FIXED = 0    # 两端固定
    I_END_HINGED = 1  # I端铰接
    J_END_HINGED = 2  # J端铰接
    BOTH_HINGED = 3   # 两端铰接


class ItemType(IntEnum):
    """
    eItemType 枚举
    用于批量操作
    """
    OBJECT = 0           # 单个对象
    GROUP = 1            # 组内所有对象
    SELECTED_OBJECTS = 2 # 所有选中的对象


# 截面类型到中文名称的映射 (便于 AI Agent 理解)
SECTION_TYPE_NAMES = {
    FrameSectionType.I_SECTION: "I形截面",
    FrameSectionType.CHANNEL: "槽钢",
    FrameSectionType.T_SECTION: "T形截面",
    FrameSectionType.ANGLE: "角钢",
    FrameSectionType.DOUBLE_ANGLE: "双角钢",
    FrameSectionType.BOX: "箱形/方管",
    FrameSectionType.PIPE: "圆管",
    FrameSectionType.RECTANGULAR: "矩形",
    FrameSectionType.CIRCLE: "圆形",
    FrameSectionType.GENERAL: "通用截面",
    FrameSectionType.DOUBLE_CHANNEL: "双槽钢",
    FrameSectionType.AUTO: "自动选择",
    FrameSectionType.SD: "截面设计器",
    FrameSectionType.VARIABLE: "变截面",
}


# 端部释放预设 (I端, J端)
RELEASE_PRESETS = {
    FrameReleaseType.BOTH_FIXED: (
        (False, False, False, False, False, False),
        (False, False, False, False, False, False)
    ),
    FrameReleaseType.I_END_HINGED: (
        (False, False, False, False, True, True),
        (False, False, False, False, False, False)
    ),
    FrameReleaseType.J_END_HINGED: (
        (False, False, False, False, False, False),
        (False, False, False, False, True, True)
    ),
    FrameReleaseType.BOTH_HINGED: (
        (False, False, False, False, True, True),
        (False, False, False, False, True, True)
    ),
}
