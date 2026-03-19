# -*- coding: utf-8 -*-
"""
structure_core - 核心结构对象
对应 SAP2000 的基本几何对象（PointObj, FrameObj, AreaObj 等）和材料

设计原则 (参考 Dlubal API):
- 核心对象 (Point, Frame, Area, Material 等) 是纯数据类
- 扩展功能通过 types_for_xxx/ 模块的函数实现
- 例如: 节点支座使用 types_for_points.set_point_support()

截面定义在 section/ 目录
"""

from .point import Point, PointCoordinateSystemType
from .material import (
    Material, MaterialType, MaterialSymmetryType, 
    WeightMassOption, MaterialDamping
)
# PointSupportType, ItemType 等枚举已移至 types_for_points 模块
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
from link.enums import (
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
    # PointSupportType, ItemType 已移至 types_for_points
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
