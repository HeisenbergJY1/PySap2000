# -*- coding: utf-8 -*-
"""荷载（节点荷载、杆件荷载）相关测试

依赖 test_loading.py 中创建的 "MyDead" 荷载模式
"""

import pytest
from PySap2000.loads import (
    # 节点荷载
    set_point_load_force,
    get_point_load_force,
    delete_point_load_force,
    set_point_load_displ,
    get_point_load_displ,
    delete_point_load_displ,
    # 杆件荷载
    set_frame_load_distributed,
    get_frame_load_distributed,
    delete_frame_load_distributed,
    set_frame_load_point,
    get_frame_load_point,
    delete_frame_load_point,
    # 枚举
    FrameLoadType,
    FrameLoadDirection,
)
from PySap2000.loading import LoadPattern, LoadPatternType

pytestmark = pytest.mark.loads

# 测试用荷载模式名称（由 ensure_load_pattern fixture 保证存在）
LP_NAME = "TestLP_Loads"


@pytest.fixture(scope="module", autouse=True)
def ensure_load_pattern(app):
    """确保测试用荷载模式存在"""
    lp = LoadPattern(
        name=LP_NAME,
        load_type=LoadPatternType.DEAD,
        self_weight_multiplier=0.0,
    )
    app.create_object(lp)  # 已存在则返回 -1


class TestPointLoadForce:
    """节点力荷载测试"""

    def test_set_point_load_force(self, model):
        ret = set_point_load_force(model, "10", LP_NAME, (0, 0, -100, 0, 0, 0))
        assert ret == 0

    def test_get_point_load_force(self, model):
        loads = get_point_load_force(model, "10")
        assert isinstance(loads, list)
        assert len(loads) > 0

    def test_delete_point_load_force(self, model):
        ret = delete_point_load_force(model, "10", LP_NAME)
        assert ret == 0


class TestPointLoadDispl:
    """节点位移荷载测试"""

    def test_set_point_load_displ(self, model):
        ret = set_point_load_displ(model, "10", LP_NAME, (0, 0, -0.01, 0, 0, 0))
        assert ret == 0

    def test_get_point_load_displ(self, model):
        loads = get_point_load_displ(model, "10")
        assert isinstance(loads, list)
        assert len(loads) > 0

    def test_delete_point_load_displ(self, model):
        ret = delete_point_load_displ(model, "10", LP_NAME)
        assert ret == 0


class TestFrameLoadDistributed:
    """杆件分布荷载测试"""

    def test_set_uniform_load(self, model):
        ret = set_frame_load_distributed(model, "1", LP_NAME, 10)
        assert ret == 0

    def test_get_distributed_load(self, model):
        loads = get_frame_load_distributed(model, "1")
        assert isinstance(loads, list)
        assert len(loads) > 0

    def test_delete_distributed_load(self, model):
        ret = delete_frame_load_distributed(model, "1", LP_NAME)
        assert ret == 0


class TestFrameLoadPoint:
    """杆件集中荷载测试"""

    def test_set_point_load(self, model):
        ret = set_frame_load_point(model, "1", LP_NAME, 100)
        assert ret == 0

    def test_get_point_load(self, model):
        loads = get_frame_load_point(model, "1")
        assert isinstance(loads, list)
        assert len(loads) > 0

    def test_delete_point_load(self, model):
        ret = delete_frame_load_point(model, "1", LP_NAME)
        assert ret == 0
