# -*- coding: utf-8 -*-
"""
structure_core - Core structural objects.

This package contains the base geometric objects and material objects that map
to SAP2000 APIs such as `PointObj`, `FrameObj`, and `AreaObj`.

Design principles:
- core objects such as `Point`, `Frame`, `Area`, and `Material` are pure data classes
- extended behavior is implemented through helper functions in modules such as
  `point/`, `frame/`, and `area/`
- for example, point supports are assigned through `point.set_point_support()`

Section definitions live in the `section/` package.
"""

from .point import Point, PointCoordinateSystemType
from .material import (
    Material, MaterialType, MaterialSymmetryType, 
    WeightMassOption, MaterialDamping
)
# PointSupportType and ItemType live in the `point` package.
from .frame import Frame, FrameType, FrameSectionType, FrameReleaseType
from .area import (
    Area, AreaType, AreaMeshType, AreaThicknessType, AreaOffsetType,
    AreaSpringType, AreaSimpleSpringType, AreaSpringLocalOneType,
    AreaFace, AreaLoadDir, AreaTempLoadType, AreaStrainComponent,
    AreaWindPressureType, AreaDistType, AreaAutoMesh, AreaSpring,
    AreaLoadGravity, AreaLoadUniform, AreaLoadSurfacePressure, AreaLoadTemperature
)
from .cable import Cable, CableType, CableGeometry, CableParameters
from .link import Link, LinkLocalAxesAdvanced
from PySap2000.link.enums import (
    LinkType, LinkDirectionalType, LinkItemType, AxisVectorOption
)

__all__ = [
    # Material (PropMaterial)
    'Material',
    'MaterialType',
    'MaterialSymmetryType',
    'WeightMassOption',
    'MaterialDamping',
    # Point (PointObj)
    'Point',
    'PointCoordinateSystemType',
    # PointSupportType and ItemType live in the `point` package
    # Frame (FrameObj)
    'Frame',
    'FrameType',
    'FrameSectionType',
    'FrameReleaseType',
    # Area (AreaObj)
    'Area',
    'AreaType',
    'AreaMeshType',
    'AreaThicknessType',
    'AreaOffsetType',
    'AreaSpringType',
    'AreaSimpleSpringType',
    'AreaSpringLocalOneType',
    'AreaFace',
    'AreaLoadDir',
    'AreaTempLoadType',
    'AreaStrainComponent',
    'AreaWindPressureType',
    'AreaDistType',
    'AreaAutoMesh',
    'AreaSpring',
    'AreaLoadGravity',
    'AreaLoadUniform',
    'AreaLoadSurfacePressure',
    'AreaLoadTemperature',
    # Cable (CableObj)
    'Cable',
    'CableType',
    'CableGeometry',
    'CableParameters',
    # Link (LinkObj)
    'Link',
    'LinkType',
    'LinkDirectionalType',
    'LinkLocalAxesAdvanced',
    'LinkItemType',
    'AxisVectorOption',
]
