# -*- coding: utf-8 -*-
"""
table_keys.py - SAP2000 表格键名常量

包含常用的表格键名，方便 AI Agent 和用户使用。

用法:
    from database_tables import TABLE_KEYS, MODEL_DEFINITION_TABLES
    
    # 使用常量
    data = DatabaseTables.get_table_for_display(model, TABLE_KEYS.JOINT_COORDINATES)
    
    # 查看所有模型定义表格
    for key in MODEL_DEFINITION_TABLES:
        print(key)
"""


class TABLE_KEYS:
    """
    常用表格键名常量
    
    使用方式:
        TABLE_KEYS.JOINT_COORDINATES
        TABLE_KEYS.FRAME_SECTION_PROPERTIES
    """
    
    # ==================== 节点 ====================
    JOINT_COORDINATES = "Joint Coordinates"
    JOINT_RESTRAINTS = "Joint Restraint Assignments"
    JOINT_SPRINGS = "Joint Spring Assignments 1 - Uncoupled"
    JOINT_MASSES = "Joint Added Mass Assignments"
    JOINT_LOADS_FORCE = "Joint Loads - Force"
    JOINT_LOADS_DISPL = "Joint Loads - Ground Displacement"
    
    # ==================== 杆件 ====================
    FRAME_SECTION_ASSIGNMENTS = "Frame Section Assignments"
    FRAME_SECTION_PROPERTIES = "Frame Section Properties 01 - General"
    FRAME_RELEASES = "Frame Release Assignments 1 - General"
    FRAME_LOADS_DISTRIBUTED = "Frame Loads - Distributed"
    FRAME_LOADS_POINT = "Frame Loads - Point"
    FRAME_LOCAL_AXES = "Frame Local Axes Assignments 1 - Typical"
    FRAME_MODIFIERS = "Frame Property Modifiers"
    FRAME_CONNECTIVITY = "Connectivity - Frame"
    
    # ==================== 面单元 ====================
    AREA_SECTION_ASSIGNMENTS = "Area Section Assignments"
    AREA_SECTION_PROPERTIES = "Area Section Properties"
    AREA_LOADS_UNIFORM = "Area Loads - Uniform"
    AREA_LOADS_SURFACE_PRESSURE = "Area Loads - Surface Pressure"
    AREA_LOCAL_AXES = "Area Local Axes Assignments 1 - Typical"
    AREA_MODIFIERS = "Area Property Modifiers"
    
    # ==================== 索单元 ====================
    CABLE_CONNECTIVITY = "Connectivity - Cable"
    CABLE_SECTION_ASSIGNMENTS = "Cable Section Assignments"
    
    # ==================== 材料 ====================
    MATERIAL_PROPERTIES_BASIC = "Material Properties - Basic Mechanical Properties"
    MATERIAL_PROPERTIES_STEEL = "Material Properties 02 - Basic Data - Steel"
    MATERIAL_PROPERTIES_CONCRETE = "Material Properties 03a - Basic Data - Concrete"
    MATERIAL_PROPERTIES_REBAR = "Material Properties 03b - Basic Data - Rebar"
    
    # ==================== 荷载 ====================
    LOAD_PATTERN_DEFINITIONS = "Load Pattern Definitions"
    LOAD_CASE_DEFINITIONS = "Load Case Definitions"
    LOAD_COMBINATION_DEFINITIONS = "Load Combination Definitions"
    
    # ==================== 分析结果 ====================
    JOINT_DISPLACEMENTS = "Joint Displacements"
    JOINT_REACTIONS = "Joint Reactions"
    FRAME_FORCES = "Element Forces - Frames"
    FRAME_STRESSES = "Element Stresses - Frames"
    AREA_FORCES = "Element Forces - Area Shells"
    AREA_STRESSES = "Element Stresses - Area Shells"
    
    # ==================== 设计 ====================
    STEEL_DESIGN_SUMMARY = "Steel Design 1 - Summary Data - AISC 360-16"
    CONCRETE_DESIGN_SUMMARY = "Concrete Design 1 - Column Summary Data"


# ==================== 分类表格列表 ====================

MODEL_DEFINITION_TABLES = [
    # 节点
    "Joint Coordinates",
    "Joint Restraint Assignments",
    "Joint Spring Assignments 1 - Uncoupled",
    "Joint Added Mass Assignments",
    
    # 杆件
    "Connectivity - Frame",
    "Frame Section Assignments",
    "Frame Release Assignments 1 - General",
    "Frame Local Axes Assignments 1 - Typical",
    "Frame Property Modifiers",
    
    # 面单元
    "Connectivity - Area",
    "Area Section Assignments",
    "Area Local Axes Assignments 1 - Typical",
    "Area Property Modifiers",
    
    # 索单元
    "Connectivity - Cable",
    "Cable Section Assignments",
    
    # 材料
    "Material Properties - Basic Mechanical Properties",
    
    # 截面
    "Frame Section Properties 01 - General",
    "Area Section Properties",
    
    # 荷载
    "Load Pattern Definitions",
    "Load Case Definitions",
    "Load Combination Definitions",
]

ANALYSIS_RESULTS_TABLES = [
    # 节点结果
    "Joint Displacements",
    "Joint Reactions",
    "Joint Velocities",
    "Joint Accelerations",
    
    # 杆件结果
    "Element Forces - Frames",
    "Element Joint Forces - Frames",
    "Element Stresses - Frames",
    
    # 面单元结果
    "Element Forces - Area Shells",
    "Element Joint Forces - Area Shells",
    "Element Stresses - Area Shells",
    
    # 模态结果
    "Modal Participating Mass Ratios",
    "Modal Periods And Frequencies",
    "Modal Load Participation Ratios",
]

DESIGN_TABLES = [
    # 钢结构设计
    "Steel Design 1 - Summary Data - AISC 360-16",
    "Steel Design 2 - PMM Details - AISC 360-16",
    
    # 混凝土设计
    "Concrete Design 1 - Column Summary Data",
    "Concrete Design 2 - Beam Summary Data",
]
