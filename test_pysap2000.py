# -*- coding: utf-8 -*-
"""
Manual checks for dimension-1~3 changes (requires a running SAP2000 instance).

Covers:
  1. com_ret performance (sys._getframe vs inspect.stack)
  2. Application._ensure_connected / disconnect
  3. Application methods routed through com_ret
  4. Point.get_all (database tables)
  5. Frame.get_all (database tables)
  6. Frame._calculate_length (point_cache)
  7. get_points_with_support (database tables)
"""

import sys
import os

# Ensure PySap2000 is importable regardless of cwd
_this_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_this_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from PySap2000 import Application
from PySap2000.structure_core import Point, Frame
from PySap2000.point.support import get_points_with_support, get_point_restraint
from PySap2000.com_helper import com_ret
from PySap2000.exceptions import ConnectionError
import time


def test_com_ret_basic():
    """Basic com_ret behavior."""
    print("\n=== 1. com_ret basics ===")

    # Success paths
    assert com_ret(0) == 0, "scalar 0 should return 0"
    assert com_ret([1.0, 2.0, 0]) == 0, "last list element 0 should return 0"
    assert com_ret((1.0, 2.0, 0)) == 0, "last tuple element 0 should return 0"

    # Failure paths (no raise when strict_mode is False by default)
    assert com_ret(1) == 1, "scalar 1 should return 1"
    assert com_ret([1.0, 2.0, 1]) == 1, "last list element 1 should return 1"

    # context kwarg
    assert com_ret(1, context="test_func") == 1, "context kwarg should work"

    print("  com_ret basics OK")


def test_com_ret_performance():
    """com_ret performance (success path should avoid heavy introspection)."""
    print("\n=== 2. com_ret performance ===")

    n = 10000
    start = time.perf_counter()
    for _ in range(n):
        com_ret(0)  # success path
    elapsed_success = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(n):
        com_ret(1)  # failure path uses sys._getframe
    elapsed_fail = time.perf_counter() - start

    print(f"  {n} success calls: {elapsed_success * 1000:.1f}ms")
    print(f"  {n} failure calls: {elapsed_fail * 1000:.1f}ms")
    print("  failure path should be fast (old inspect.stack was ~3000ms+)")
    assert elapsed_fail < 2.0, f"com_ret failure path too slow: {elapsed_fail:.2f}s"
    print("  com_ret performance OK")


def test_ensure_connected(app):
    """_ensure_connected guard."""
    print("\n=== 3. _ensure_connected ===")

    app._ensure_connected()
    print("  _ensure_connected OK while connected")

    m = app.model
    assert m is not None, "model should not be None"
    print("  app.model OK")


def test_disconnect():
    """disconnect and repeated calls."""
    print("\n=== 4. disconnect idempotency ===")

    app = Application(attach_to_instance=True)
    assert app._model is not None

    app.disconnect()
    assert app._model is None, "_model should be None after disconnect"
    assert app._sap_object is None, "_sap_object should be None after disconnect (attach mode)"

    app.disconnect()
    print("  disconnect idempotent OK")

    try:
        app.get_units()
        assert False, "expected ConnectionError"
    except ConnectionError:
        print("  calls after disconnect raise ConnectionError as expected")


def test_context_manager():
    """Context manager cleanup."""
    print("\n=== 5. Context manager ===")

    with Application(attach_to_instance=True) as app:
        units = app.get_units()
        assert isinstance(units, int), f"get_units should return int, got {type(units)}"
        print(f"  inside with: get_units = {units} OK")

    assert app._model is None, "_model should be None after with block"
    print("  context manager cleanup OK")


def test_application_methods(app):
    """Application helpers use com_ret."""
    print("\n=== 6. Application methods (com_ret) ===")

    original_units = app.get_units()
    ret = app.set_units(6)  # kN_m_C
    assert ret == 0, f"set_units returned {ret}"
    app.set_units(original_units)
    print(f"  set_units/get_units OK (original={original_units})")

    name = app.get_units_name()
    assert isinstance(name, str) and name != "Unknown", f"get_units_name={name}"
    print(f"  get_units_name = {name}")

    ver = app.get_version()
    assert len(ver) == 2, f"get_version should return 2-tuple, got {ver}"
    print(f"  get_version = {ver}")

    fn = app.get_model_filename(include_path=False)
    print(f"  get_model_filename = {fn}")

    tol = app.get_merge_tol()
    assert isinstance(tol, float), f"get_merge_tol should return float, got {type(tol)}"
    print(f"  get_merge_tol = {tol}")

    csys = app.get_present_coord_system()
    assert isinstance(csys, str), f"should return str, got {type(csys)}"
    print(f"  get_present_coord_system = {csys}")

    info = app.get_project_info()
    assert isinstance(info, dict), f"should return dict, got {type(info)}"
    print(f"  get_project_info: {len(info)} keys")

    comment = app.get_user_comment()
    if len(comment) > 30:
        print(f"  get_user_comment = '{comment[:30]}...' ")
    else:
        print(f"  get_user_comment = '{comment}'")

    app.refresh_view()
    print("  refresh_view OK")

    print("  all Application checks OK")


def test_point_get_all(app):
    """Point.get_all via database tables."""
    print("\n=== 7. Point.get_all (DB tables) ===")

    points = Point.get_all(app.model)
    print(f"  joints: {len(points)}")

    assert len(points) > 0, "model should have at least one joint"

    p = points[0]
    assert p.no is not None, "joint name should not be None"
    assert isinstance(p.x, float), f"x should be float, got {type(p.x)}"
    assert isinstance(p.y, float), f"y should be float, got {type(p.y)}"
    assert isinstance(p.z, float), f"z should be float, got {type(p.z)}"
    print(f"  first joint: {p.no} ({p.x}, {p.y}, {p.z})")

    p_old = Point.get_by_name(app.model, str(points[0].no))
    assert abs(p.x - p_old.x) < 1e-6, f"x mismatch: {p.x} vs {p_old.x}"
    assert abs(p.y - p_old.y) < 1e-6, f"y mismatch: {p.y} vs {p_old.y}"
    assert abs(p.z - p_old.z) < 1e-6, f"z mismatch: {p.z} vs {p_old.z}"
    print("  matches get_by_name OK")

    if len(points) >= 2:
        subset = Point.get_all(app.model, names=[points[0].no, points[1].no])
        assert len(subset) == 2, f"filtered count should be 2, got {len(subset)}"
        print("  names filter OK")

    start = time.perf_counter()
    pts_new = Point.get_all(app.model)
    t_new = time.perf_counter() - start

    start = time.perf_counter()
    names = Point.get_name_list(app.model)
    pts_old = []
    for name in names:
        pj = Point(no=name)
        pj._get(app.model)
        pts_old.append(pj)
    t_old = time.perf_counter() - start

    print(
        f"  DB tables: {t_new * 1000:.1f}ms vs per-COM: {t_old * 1000:.1f}ms "
        f"({len(pts_new)} joints)"
    )
    print(f"  speedup: {t_old / t_new:.1f}x")


def test_frame_get_all(app):
    """Frame.get_all via database tables."""
    print("\n=== 8. Frame.get_all (DB tables) ===")

    frames = Frame.get_all(app.model)
    print(f"  frames: {len(frames)}")

    if len(frames) == 0:
        print("  no frames in model, skip")
        return

    f = frames[0]
    assert f.no is not None, "frame name should not be None"
    assert f.start_point is not None, "start_point should not be None"
    assert f.end_point is not None, "end_point should not be None"
    print(f"  first frame: {f.no}, {f.start_point}->{f.end_point}, sec={f.section}, L={f.length}")

    f_old = Frame.get_by_name(app.model, str(frames[0].no))
    assert str(f.start_point) == str(f_old.start_point), (
        f"start_point mismatch: {f.start_point} vs {f_old.start_point}"
    )
    assert str(f.end_point) == str(f_old.end_point), (
        f"end_point mismatch: {f.end_point} vs {f_old.end_point}"
    )
    if f.length is not None and f_old.length is not None:
        assert abs(f.length - f_old.length) < 0.01, (
            f"length mismatch: {f.length} vs {f_old.length}"
        )
    print("  matches get_by_name OK")

    start = time.perf_counter()
    fs_new = Frame.get_all(app.model)
    t_new = time.perf_counter() - start

    start = time.perf_counter()
    names = Frame.get_name_list(app.model)
    fs_old = [Frame.get_by_name(app.model, n) for n in names]
    t_old = time.perf_counter() - start

    print(
        f"  DB tables: {t_new * 1000:.1f}ms vs per-COM: {t_old * 1000:.1f}ms "
        f"({len(fs_new)} frames)"
    )
    print(f"  speedup: {t_old / t_new:.1f}x")


def test_get_points_with_support(app):
    """get_points_with_support via database tables."""
    print("\n=== 9. get_points_with_support (DB tables) ===")

    supported = get_points_with_support(app.model)
    print(f"  joints with support: {len(supported)}")

    if len(supported) > 0:
        print(f"  first few: {supported[:5]}")

        for name in supported[:3]:
            r = get_point_restraint(app.model, name)
            assert r is not None and any(r), f"joint {name} should have restraint, got {r}"
        print("  matches per-joint get_point_restraint OK")

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

    assert len(s_new) == len(s_old), (
        f"count mismatch: DB tables={len(s_new)} vs per-joint={len(s_old)}"
    )
    print(f"  DB tables: {t_new * 1000:.1f}ms vs per-COM: {t_old * 1000:.1f}ms")
    print(f"  speedup: {t_old / t_new:.1f}x")


# --- Run all (uncomment as needed) ---

if __name__ == "__main__":
    # print("=" * 60)
    # print("PySap2000 dimension-1~3 verification")
    # print("Requires: SAP2000 running with a model open")
    # print("=" * 60)

    # # No SAP2000
    # test_com_ret_basic()
    # test_com_ret_performance()

    # # With SAP2000
    # with Application(attach_to_instance=True) as app:
    #     test_ensure_connected(app)
    #     test_application_methods(app)
    #     test_point_get_all(app)
    #     test_frame_get_all(app)
    #     test_get_points_with_support(app)

    # # disconnect tests last
    # test_disconnect()
    # test_context_manager()

    # print("\n" + "=" * 60)
    # print("All checks passed.")
    # print("=" * 60)

    # # Option: open model file
    # with Application(model_file="bridge.sdb") as app:
    #     app.calculate()
    #     # process results
    pass
