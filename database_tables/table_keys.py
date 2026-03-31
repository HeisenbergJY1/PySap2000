# -*- coding: utf-8 -*-
"""
table_keys.py - SAP2000 table-key constants.

Contains commonly used table keys for easier usage.

Usage:
    from database_tables import TABLE_KEYS, MODEL_DEFINITION_TABLES
    
    # Use constants
    data = DatabaseTables.get_table_for_display(model, TABLE_KEYS.JOINT_COORDINATES)
    
    # Print all model-definition tables
    for key in MODEL_DEFINITION_TABLES:
        print(key)
"""


class TABLE_KEYS:
    """
    Common table-key constants.
    
    Usage:
        TABLE_KEYS.JOINT_COORDINATES
        TABLE_KEYS.FRAME_SECTION_PROPERTIES
    """
    
    # ==================== Joints ====================
    JOINT_COORDINATES = "Joint Coordinates"
    JOINT_RESTRAINTS = "Joint Restraint Assignments"
    JOINT_SPRINGS = "Joint Spring Assignments 1 - Uncoupled"
    JOINT_MASSES = "Joint Added Mass Assignments"
    JOINT_LOADS_FORCE = "Joint Loads - Force"
    JOINT_LOADS_DISPL = "Joint Loads - Ground Displacement"
    
    # ==================== Frames ====================
    FRAME_SECTION_ASSIGNMENTS = "Frame Section Assignments"
    FRAME_SECTION_PROPERTIES = "Frame Section Properties 01 - General"
    FRAME_RELEASES = "Frame Release Assignments 1 - General"
    FRAME_LOADS_DISTRIBUTED = "Frame Loads - Distributed"
    FRAME_LOADS_POINT = "Frame Loads - Point"
    FRAME_LOCAL_AXES = "Frame Local Axes Assignments 1 - Typical"
    FRAME_MODIFIERS = "Frame Property Modifiers"
    FRAME_CONNECTIVITY = "Connectivity - Frame"
    
    # ==================== Areas ====================
    AREA_SECTION_ASSIGNMENTS = "Area Section Assignments"
    AREA_SECTION_PROPERTIES = "Area Section Properties"
    AREA_LOADS_UNIFORM = "Area Loads - Uniform"
    AREA_LOADS_SURFACE_PRESSURE = "Area Loads - Surface Pressure"
    AREA_LOCAL_AXES = "Area Local Axes Assignments 1 - Typical"
    AREA_MODIFIERS = "Area Property Modifiers"
    
    # ==================== Cables ====================
    CABLE_CONNECTIVITY = "Connectivity - Cable"
    CABLE_SECTION_ASSIGNMENTS = "Cable Section Assignments"
    
    # ==================== Materials ====================
    MATERIAL_PROPERTIES_BASIC = "Material Properties - Basic Mechanical Properties"
    MATERIAL_PROPERTIES_STEEL = "Material Properties 02 - Basic Data - Steel"
    MATERIAL_PROPERTIES_CONCRETE = "Material Properties 03a - Basic Data - Concrete"
    MATERIAL_PROPERTIES_REBAR = "Material Properties 03b - Basic Data - Rebar"
    
    # ==================== Loads ====================
    LOAD_PATTERN_DEFINITIONS = "Load Pattern Definitions"
    LOAD_CASE_DEFINITIONS = "Load Case Definitions"
    LOAD_COMBINATION_DEFINITIONS = "Load Combination Definitions"
    
    # ==================== Analysis Results ====================
    JOINT_DISPLACEMENTS = "Joint Displacements"
    JOINT_REACTIONS = "Joint Reactions"
    FRAME_FORCES = "Element Forces - Frames"
    FRAME_STRESSES = "Element Stresses - Frames"
    AREA_FORCES = "Element Forces - Area Shells"
    AREA_STRESSES = "Element Stresses - Area Shells"
    
    # ==================== Design ====================
    STEEL_DESIGN_SUMMARY = "Steel Design 1 - Summary Data - AISC 360-16"
    CONCRETE_DESIGN_SUMMARY = "Concrete Design 1 - Column Summary Data"


# ==================== Grouped table lists ====================

MODEL_DEFINITION_TABLES = [
    # Joints
    "Joint Coordinates",
    "Joint Restraint Assignments",
    "Joint Spring Assignments 1 - Uncoupled",
    "Joint Added Mass Assignments",
    
    # Frames
    "Connectivity - Frame",
    "Frame Section Assignments",
    "Frame Release Assignments 1 - General",
    "Frame Local Axes Assignments 1 - Typical",
    "Frame Property Modifiers",
    
    # Areas
    "Connectivity - Area",
    "Area Section Assignments",
    "Area Local Axes Assignments 1 - Typical",
    "Area Property Modifiers",
    
    # Cables
    "Connectivity - Cable",
    "Cable Section Assignments",
    
    # Materials
    "Material Properties - Basic Mechanical Properties",
    
    # Sections
    "Frame Section Properties 01 - General",
    "Area Section Properties",
    
    # Loads
    "Load Pattern Definitions",
    "Load Case Definitions",
    "Load Combination Definitions",
]

ANALYSIS_RESULTS_TABLES = [
    # Joint results
    "Joint Displacements",
    "Joint Reactions",
    "Joint Velocities",
    "Joint Accelerations",
    
    # Frame results
    "Element Forces - Frames",
    "Element Joint Forces - Frames",
    "Element Stresses - Frames",
    
    # Area results
    "Element Forces - Area Shells",
    "Element Joint Forces - Area Shells",
    "Element Stresses - Area Shells",
    
    # Modal results
    "Modal Participating Mass Ratios",
    "Modal Periods And Frequencies",
    "Modal Load Participation Ratios",
]

DESIGN_TABLES = [
    # Steel design
    "Steel Design 1 - Summary Data - AISC 360-16",
    "Steel Design 2 - PMM Details - AISC 360-16",
    
    # Concrete design
    "Concrete Design 1 - Column Summary Data",
    "Concrete Design 2 - Beam Summary Data",
]
