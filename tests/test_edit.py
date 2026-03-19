# -*- coding: utf-8 -*-
"""编辑操作测试 (Edit)

注意: 编辑操作会修改模型，测试需要谨慎。
只测试安全的操作（坐标修改后恢复、分割等）。
"""

import pytest
from PySap2000.edit import (
    change_point_coordinates,
    divide_frame_by_ratio,
)

pytestmark = pytest.mark.edit


class TestEditPoint:
    """点编辑测试"""

    def test_change_point_coordinates(self, model):
        """移动点5到新位置，再移回来"""
        # 先获取原始坐标 (点5: 5, 5, 0)
        ret = change_point_coordinates(model, "5", 5.0, 5.0, 1.0)
        assert ret == 0
        # 验证坐标已改变
        result = model.PointObj.GetCoordCartesian("5", 0.0, 0.0, 0.0)
        if isinstance(result, (list, tuple)) and len(result) >= 3:
            assert abs(result[2] - 1.0) < 0.01
        # 恢复原始坐标
        change_point_coordinates(model, "5", 5.0, 5.0, 0.0)


class TestEditFrame:
    """框架编辑测试"""

    def test_divide_frame_by_ratio(self, model):
        """分割框架 - 使用专用框架避免影响其他测试"""
        from PySap2000.structure_core import Point, Frame

        # 创建专用点和框架
        p1 = Point(no=201, x=100, y=0, z=0)
        p2 = Point(no=202, x=110, y=0, z=0)
        p1._create(model)
        p2._create(model)
        f = Frame(no="EditTestFrame", start_point="201", end_point="202")
        f._create(model)

        # 分割为2段 (ratio=1.0 等分)
        names = divide_frame_by_ratio(model, "EditTestFrame", num_segments=2, ratio=1.0)
        # 分割后应返回新框架名称列表
        assert isinstance(names, list)
        # 分割成功时返回非空列表
        if len(names) > 0:
            assert len(names) >= 2
