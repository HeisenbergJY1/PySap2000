# -*- coding: utf-8 -*-
"""
enums.py - 分析结果枚举

SAP2000 Analysis Results API 的枚举定义
"""

from enum import IntEnum


class ItemTypeElm(IntEnum):
    """
    结果请求的元素类型
    
    SAP2000 API: eItemTypeElm
    
    用于指定结果请求的范围：
    - OBJECT_ELM: 请求指定对象对应的元素结果
    - ELEMENT: 请求指定元素的结果
    - GROUP_ELM: 请求组内所有元素的结果
    - SELECTION_ELM: 请求所有选中元素的结果
    """
    OBJECT_ELM = 0      # 对象对应的元素
    ELEMENT = 1         # 指定元素
    GROUP_ELM = 2       # 组内元素
    SELECTION_ELM = 3   # 选中元素
