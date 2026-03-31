# -*- coding: utf-8 -*-
"""
enums.py - Area-related enums.

Contains enums used by the SAP2000 `AreaObj` API.

Note: Load-related enums have been moved to `loads/area_load.py`.
"""

from enum import IntEnum


class AreaType(IntEnum):
    """Area object type."""
    SHELL = 1      # Shell element
    PLANE = 2      # Plane element
    ASOLID = 3     # Axisymmetric solid


class AreaMeshType(IntEnum):
    """Automatic meshing type for area objects."""
    NO_MESH = 0                 # No meshing
    MESH_BY_NUMBER = 1          # Divide by count
    MESH_BY_MAX_SIZE = 2        # Divide by maximum size
    MESH_BY_POINTS_ON_EDGE = 3  # Divide by edge points
    COOKIE_CUT_BY_LINES = 4     # Cookie-cut by lines
    COOKIE_CUT_BY_POINTS = 5    # Cookie-cut by points
    GENERAL_DIVIDE = 6          # General divide


class AreaThicknessType(IntEnum):
    """Thickness override type for area objects."""
    NO_OVERWRITE = 0     # No override
    BY_JOINT_PATTERN = 1 # By joint pattern
    BY_POINT = 2         # By point


class AreaOffsetType(IntEnum):
    """Offset type for area objects."""
    NO_OFFSET = 0        # No offset
    BY_JOINT_PATTERN = 1 # By joint pattern
    BY_POINT = 2         # By point


class AreaSpringType(IntEnum):
    """Spring type for area objects."""
    SIMPLE_SPRING = 1   # Simple spring
    LINK_PROPERTY = 2   # Link property


class AreaSimpleSpringType(IntEnum):
    """Simple spring behavior type for area objects."""
    TENSION_COMPRESSION = 1  # Tension and compression
    COMPRESSION_ONLY = 2     # Compression only
    TENSION_ONLY = 3         # Tension only


class AreaSpringLocalOneType(IntEnum):
    """Local-1 axis direction type for area springs."""
    PARALLEL_TO_LOCAL_AXIS = 1  # Parallel to local axis
    NORMAL_TO_FACE = 2          # Normal to face
    USER_VECTOR = 3             # User vector


class AreaFace(IntEnum):
    """Area face identifier."""
    BOTTOM = -1  # Bottom face
    TOP = -2     # Top face


class PlaneRefVectorOption(IntEnum):
    """Plane reference-vector option."""
    COORDINATE_DIRECTION = 1  # Coordinate direction
    TWO_JOINTS = 2            # Two joints
    USER_VECTOR = 3           # User vector


class ItemType(IntEnum):
    """`eItemType` enum."""
    OBJECT = 0            # Single object
    GROUP = 1             # Group
    SELECTED_OBJECTS = 2  # Selected objects
