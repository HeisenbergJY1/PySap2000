# -*- coding: utf-8 -*-
"""
测试维度1~3修改的函数（需要连接运行中的 SAP2000 实例）

测试项:
  1. com_ret 性能 (sys._getframe vs inspect.stack)
  2. Application._ensure_connected / disconnect
  3. Application 各方法走 com_ret
  4. Point.get_all (Database Tables)
  5. Frame.get_all (Database Tables)
  6. Frame._calculate_length (point_cache)
  7. get_points_with_support (Database Tables)
"""

import sys, os
# 确保 PySap2000 包可被导入（无论从哪个目录运行）
_this_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_this_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)

from PySap2000 import Application
from PySap2000.structure_core import Point, Frame
from PySap2000.point.support import get_points_with_support, get_point_restraint
from PySap2000.com_helper import com_ret
from PySap2000.exceptions import ConnectionError
import time


def test_com_ret_basic():
    """测试 com_ret 基本功能"""
    print("\n=== 1. com_ret 基本功能 ===")
    
    # 成功返回
    assert com_ret(0) == 0, "单值 0 应返回 0"
    assert com_ret([1.0, 2.0, 0]) == 0, "列表最后元素 0 应返回 0"
    assert com_ret((1.0, 2.0, 0)) == 0, "元组最后元素 0 应返回 0"
    
    # 失败返回（不抛异常，因为 strict_mode 默认 False）
    assert com_ret(1) == 1, "单值 1 应返回 1"
    assert com_ret([1.0, 2.0, 1]) == 1, "列表最后元素 1 应返回 1"
    
    # context 参数
    assert com_ret(1, context="test_func") == 1, "context 参数应正常工作"
    
    print("  com_ret 基本功能 OK")


def test_com_ret_performance():
    """测试 com_ret 性能（sys._getframe 应比 inspect.stack 快很多）"""
    print("\n=== 2. com_ret 性能 ===")
    
    n = 10000
    start = time.perf_counter()
    for _ in range(n):
        com_ret(0)  # 成功路径，不触发帧内省
    elapsed_success = time.perf_counter() - start
    
    start = time.perf_counter()
    for _ in range(n):
        com_ret(1)  # 失败路径，触发 sys._getframe
    elapsed_fail = time.perf_counter() - start
    
    print(f"  {n} 次成功调用: {elapsed_success*1000:.1f}ms")
    print(f"  {n} 次失败调用: {elapsed_fail*1000:.1f}ms")
    print(f"  失败路径应 < 500ms (旧 inspect.stack 版本约 3000ms+)")
    assert elapsed_fail < 2.0, f"com_ret 失败路径太慢: {elapsed_fail:.2f}s"
    print("  com_ret 性能 OK")


def test_ensure_connected(app):
    """测试 _ensure_connected 守卫"""
    print("\n=== 3. _ensure_connected ===")
    
    # 正常连接时不应抛异常
    app._ensure_connected()
    print("  连接状态下 _ensure_connected OK")
    
    # model 属性应正常工作
    m = app.model
    assert m is not None, "model 不应为 None"
    print("  app.model 属性 OK")


def test_disconnect():
    """测试 disconnect 和重复调用安全性"""
    print("\n=== 4. disconnect 幂等性 ===")
    
    app = Application(attach_to_instance=True)
    assert app._model is not None
    
    # disconnect 后 _model 应为 None
    app.disconnect()
    assert app._model is None, "disconnect 后 _model 应为 None"
    assert app._sap_object is None, "disconnect 后 _sap_object 应为 None (attach 模式)"
    
    # 重复 disconnect 不应报错
    app.disconnect()
    print("  disconnect 幂等性 OK")
    
    # disconnect 后调用方法应抛 ConnectionError
    try:
        app.get_units()
        assert False, "应抛出 ConnectionError"
    except ConnectionError:
        print("  断开后调用方法正确抛出 ConnectionError")


def test_context_manager():
    """测试 Context Manager"""
    print("\n=== 5. Context Manager ===")
    
    with Application(attach_to_instance=True) as app:
        units = app.get_units()
        assert isinstance(units, int), f"get_units 应返回 int, 得到 {type(units)}"
        print(f"  with 块内 get_units = {units} OK")
    
    # 退出 with 后 _model 应为 None
    assert app._model is None, "退出 with 后 _model 应为 None"
    print("  Context Manager 退出清理 OK")


def test_application_methods(app):
    """测试 Application 各方法走 com_ret"""
    print("\n=== 6. Application 方法 (com_ret) ===")
    
    # get/set units
    original_units = app.get_units()
    ret = app.set_units(6)  # kN_m_C
    assert ret == 0, f"set_units 返回 {ret}"
    app.set_units(original_units)
    print(f"  set_units/get_units OK (当前={original_units})")
    
    # get_units_name
    name = app.get_units_name()
    assert isinstance(name, str) and name != "Unknown", f"get_units_name={name}"
    print(f"  get_units_name = {name}")
    
    # get_version
    ver = app.get_version()
    assert len(ver) == 2, f"get_version 应返回 2 元素元组, 得到 {ver}"
    print(f"  get_version = {ver}")
    
    # get_model_filename
    fn = app.get_model_filename(include_path=False)
    print(f"  get_model_filename = {fn}")
    
    # get/set merge_tol
    tol = app.get_merge_tol()
    assert isinstance(tol, float), f"get_merge_tol 应返回 float, 得到 {type(tol)}"
    print(f"  get_merge_tol = {tol}")
    
    # get_present_coord_system
    csys = app.get_present_coord_system()
    assert isinstance(csys, str), f"应返回 str, 得到 {type(csys)}"
    print(f"  get_present_coord_system = {csys}")
    
    # get_project_info
    info = app.get_project_info()
    assert isinstance(info, dict), f"应返回 dict, 得到 {type(info)}"
    print(f"  get_project_info = {len(info)} 项")
    
    # get/set user_comment
    comment = app.get_user_comment()
    print(f"  get_user_comment = '{comment[:30]}...' " if len(comment) > 30 else f"  get_user_comment = '{comment}'")
    
    # refresh_view
    app.refresh_view()
    print("  refresh_view OK")
    
    print("  所有 Application 方法 OK")


def test_point_get_all(app):
    """测试 Point.get_all (Database Tables)"""
    print("\n=== 7. Point.get_all (DB Tables) ===")
    
    points = Point.get_all(app.model)
    print(f"  获取到 {len(points)} 个节点")
    
    assert len(points) > 0, "模型中应至少有 1 个节点"
    
    # 检查数据完整性
    p = points[0]
    assert p.no is not None, "节点名称不应为 None"
    assert isinstance(p.x, float), f"x 应为 float, 得到 {type(p.x)}"
    assert isinstance(p.y, float), f"y 应为 float, 得到 {type(p.y)}"
    assert isinstance(p.z, float), f"z 应为 float, 得到 {type(p.z)}"
    print(f"  第一个节点: {p.no} ({p.x}, {p.y}, {p.z})")
    
    # 对比: 用旧方法逐个获取验证数据一致性
    p_old = Point.get_by_name(app.model, str(points[0].no))
    assert abs(p.x - p_old.x) < 1e-6, f"x 不一致: {p.x} vs {p_old.x}"
    assert abs(p.y - p_old.y) < 1e-6, f"y 不一致: {p.y} vs {p_old.y}"
    assert abs(p.z - p_old.z) < 1e-6, f"z 不一致: {p.z} vs {p_old.z}"
    print("  与 get_by_name 对比数据一致 OK")
    
    # 测试 names 过滤
    if len(points) >= 2:
        subset = Point.get_all(app.model, names=[points[0].no, points[1].no])
        assert len(subset) == 2, f"过滤后应有 2 个, 得到 {len(subset)}"
        print("  names 过滤 OK")
    
    # 性能对比
    start = time.perf_counter()
    pts_new = Point.get_all(app.model)
    t_new = time.perf_counter() - start
    
    start = time.perf_counter()
    names = Point.get_name_list(app.model)
    pts_old = []
    for name in names:
        p = Point(no=name)
        p._get(app.model)
        pts_old.append(p)
    t_old = time.perf_counter() - start
    
    print(f"  DB Tables: {t_new*1000:.1f}ms vs 逐个COM: {t_old*1000:.1f}ms ({len(pts_new)} 节点)")
    print(f"  加速比: {t_old/t_new:.1f}x")


def test_frame_get_all(app):
    """测试 Frame.get_all (Database Tables)"""
    print("\n=== 8. Frame.get_all (DB Tables) ===")
    
    frames = Frame.get_all(app.model)
    print(f"  获取到 {len(frames)} 个杆件")
    
    if len(frames) == 0:
        print("  模型中没有杆件，跳过")
        return
    
    # 检查数据完整性
    f = frames[0]
    assert f.no is not None, "杆件名称不应为 None"
    assert f.start_point is not None, "start_point 不应为 None"
    assert f.end_point is not None, "end_point 不应为 None"
    print(f"  第一个杆件: {f.no}, {f.start_point}->{f.end_point}, sec={f.section}, L={f.length}")
    
    # 对比: 用旧方法逐个获取验证
    f_old = Frame.get_by_name(app.model, str(frames[0].no))
    assert str(f.start_point) == str(f_old.start_point), \
        f"start_point 不一致: {f.start_point} vs {f_old.start_point}"
    assert str(f.end_point) == str(f_old.end_point), \
        f"end_point 不一致: {f.end_point} vs {f_old.end_point}"
    if f.length is not None and f_old.length is not None:
        assert abs(f.length - f_old.length) < 0.01, \
            f"length 不一致: {f.length} vs {f_old.length}"
    print("  与 get_by_name 对比数据一致 OK")
    
    # 性能对比
    start = time.perf_counter()
    fs_new = Frame.get_all(app.model)
    t_new = time.perf_counter() - start
    
    start = time.perf_counter()
    names = Frame.get_name_list(app.model)
    fs_old = [Frame.get_by_name(app.model, n) for n in names]
    t_old = time.perf_counter() - start
    
    print(f"  DB Tables: {t_new*1000:.1f}ms vs 逐个COM: {t_old*1000:.1f}ms ({len(fs_new)} 杆件)")
    print(f"  加速比: {t_old/t_new:.1f}x")


def test_get_points_with_support(app):
    """测试 get_points_with_support (Database Tables)"""
    print("\n=== 9. get_points_with_support (DB Tables) ===")
    
    supported = get_points_with_support(app.model)
    print(f"  有支座的节点: {len(supported)} 个")
    
    if len(supported) > 0:
        print(f"  前几个: {supported[:5]}")
        
        # 验证: 用旧方法逐个检查前几个节点确实有约束
        for name in supported[:3]:
            r = get_point_restraint(app.model, name)
            assert r is not None and any(r), \
                f"节点 {name} 应有约束, 得到 {r}"
        print("  与 get_point_restraint 逐个验证一致 OK")
    
    # 性能对比
    from PySap2000.com_helper import com_data
    
    start = time.perf_counter()
    s_new = get_points_with_support(app.model)
    t_new = time.perf_counter() - start
    
    start = time.perf_counter()
    result = app.model.PointObj.GetNameList(0, [])
    all_names = list(com_data(result, 1) or [])
    s_old = []
    for name in all_names:
        r = get_point_restraint(app.model, name)
        if r and any(r):
            s_old.append(name)
    t_old = time.perf_counter() - start
    
    assert len(s_new) == len(s_old), \
        f"结果数量不一致: DB Tables={len(s_new)} vs 逐个={len(s_old)}"
    print(f"  DB Tables: {t_new*1000:.1f}ms vs 逐个COM: {t_old*1000:.1f}ms")
    print(f"  加速比: {t_old/t_new:.1f}x")


# ==================== 运行所有测试 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("PySap2000 维度1~3 修改验证测试")
    print("需要: SAP2000 正在运行且已打开模型")
    print("=" * 60)
    
    # 不依赖 SAP2000 的测试
    test_com_ret_basic()
    test_com_ret_performance()
    
    # 依赖 SAP2000 的测试
    with Application(attach_to_instance=True) as app:
        test_ensure_connected(app)
        test_application_methods(app)
        test_point_get_all(app)
        test_frame_get_all(app)
        test_get_points_with_support(app)
    
    # disconnect 相关测试（会断开连接，放最后）
    test_disconnect()
    test_context_manager()
    
    print("\n" + "=" * 60)
    print("全部测试通过!")
    print("=" * 60)
