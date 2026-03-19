# -*- coding: utf-8 -*-
"""
data_collector.py - 从 SAP2000 模型中采集计算书所需数据

通过 DatabaseTables.GetTableForDisplayArray 提取所有数据，自动适配设计规范版本。
不依赖 GetAvailableTables (该 API 在某些 comtypes 版本下参数不兼容)。

采集两类数据:
1. 单元信息 (表 2.5): 截面、长度、无支撑长度系数、计算长度系数、端部释放
2. 钢结构设计结果 (表 5.1): 应力比、内力、稳定系数、长细比、超限信息
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple

from database_tables.tables import DatabaseTables, TableData


@dataclass
class FrameElementInfo:
    """单元信息 (表 2.5)"""
    no: str = ""
    section_name: str = ""
    length: float = 0.0
    unbraced_ratio_major: float = 1.0
    unbraced_ratio_minor: float = 1.0
    mue_major: float = 1.0
    mue_minor: float = 1.0
    release_i: str = "---"
    release_j: str = "---"


@dataclass
class SteelDesignResultRow:
    """钢结构设计结果 (表 5.1)"""
    index: int = 0
    frame_name: str = ""
    ratio: float = 0.0
    n: float = 0.0
    m3: float = 0.0
    m2: float = 0.0
    phi3: float = 0.0
    phi2: float = 0.0
    phi_b3: float = 0.0
    phi_b2: float = 0.0
    slenderness_major: float = 0.0
    slenderness_minor: float = 0.0
    exceeded: str = "无"


def _safe_float(value: Optional[str], default: float = 0.0) -> float:
    """安全转换字符串为浮点数"""
    if value is None or value == "" or value == "None":
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def _format_release(release_tuple: Tuple[bool, ...]) -> str:
    """将释放元组转为可读字符串"""
    labels = ["U1", "U2", "U3", "R1", "R2", "R3"]
    released = [labels[i] for i in range(min(6, len(release_tuple))) if release_tuple[i]]
    return " ".join(released) if released else "---"


def _try_get_table(model, table_key: str) -> Optional[TableData]:
    """尝试获取表格，失败返回 None (不抛异常)"""
    try:
        return DatabaseTables.get_table_for_display(model, table_key)
    except Exception:
        return None


def _build_table_index(table: TableData, key_field: str) -> Dict[str, List[int]]:
    """为表格数据建立索引，加速按名称查找"""
    index: Dict[str, List[int]] = {}
    for i in range(table.num_records):
        val = table.get_value(i, key_field)
        if val:
            index.setdefault(val, []).append(i)
    return index


def _first_match(table: TableData, row: int, field_candidates: List[str]) -> Optional[str]:
    """在一行中尝试多个字段名，返回第一个有效值的结果"""
    for fld in field_candidates:
        val = table.get_value(row, fld)
        if val is not None and val != "" and val != "None":
            return val
    return None


# 已知的中国规范版本后缀，按优先级排列
_CHINESE_SUFFIXES = ["Chinese 2018", "Chinese 2010"]


def _find_steel_design_tables(model) -> Dict[str, Optional[str]]:
    """
    通过直接尝试已知表名来发现钢结构设计表格。
    不依赖 GetAvailableTables。
    """
    result: Dict[str, Optional[str]] = {
        "summary": None, "pmm": None, "overwrite": None
    }

    for suffix in _CHINESE_SUFFIXES:
        # Summary
        if result["summary"] is None:
            key = f"Steel Design 1 - Summary Data - {suffix}"
            t = _try_get_table(model, key)
            if t and t.num_records > 0:
                result["summary"] = key

        # PMM Details
        if result["pmm"] is None:
            key = f"Steel Design 2 - PMM Details - {suffix}"
            t = _try_get_table(model, key)
            if t and t.num_records > 0:
                result["pmm"] = key

        # Overwrite
        if result["overwrite"] is None:
            key = f"Steel Design Overwrites - {suffix}"
            t = _try_get_table(model, key)
            if t and t.num_records > 0:
                result["overwrite"] = key

    return result


def collect_frame_element_info(
    model,
    frame_names: List[str],
) -> List[FrameElementInfo]:
    """
    采集单元信息 (表 2.5)
    """
    from structure_core.frame import Frame
    from frame.release import get_frame_release

    # 1. 基本信息 (截面、长度、释放)
    results = []
    for name in frame_names:
        info = FrameElementInfo(no=name)
        try:
            frame = Frame.get_by_name(model, name)
            info.section_name = frame.section or ""
            info.length = frame.length or 0.0
        except Exception:
            pass
        try:
            release = get_frame_release(model, name)
            if release:
                info.release_i = _format_release(release.release_i)
                info.release_j = _format_release(release.release_j)
        except Exception:
            pass
        results.append(info)

    # 2. 从 DatabaseTables 获取无支撑长度系数和计算长度系数
    design_tables = _find_steel_design_tables(model)

    # 从 PMM Details 表
    pmm_key = design_tables.get("pmm")
    if pmm_key:
        pmm_table = _try_get_table(model, pmm_key)
        if pmm_table and pmm_table.num_records > 0:
            idx = _build_table_index(pmm_table, "Frame")
            for info in results:
                rows = idx.get(info.no, [])
                if not rows:
                    continue
                row = rows[0]
                # 无支撑长度系数
                v = _first_match(pmm_table, row, ["LRatioMajor", "XLMajor", "UnbracedMajor"])
                if v:
                    info.unbraced_ratio_major = _safe_float(v, 1.0)
                v = _first_match(pmm_table, row, ["LRatioMinor", "XLMinor", "UnbracedMinor"])
                if v:
                    info.unbraced_ratio_minor = _safe_float(v, 1.0)
                # 计算长度系数 μ
                v = _first_match(pmm_table, row, ["MueMajor", "MuMajor", "KMajor"])
                if v:
                    info.mue_major = _safe_float(v, 1.0)
                v = _first_match(pmm_table, row, ["MueMinor", "MuMinor", "KMinor"])
                if v:
                    info.mue_minor = _safe_float(v, 1.0)

    # 从 Overwrite 表补充
    ow_key = design_tables.get("overwrite")
    if ow_key:
        ow_table = _try_get_table(model, ow_key)
        if ow_table and ow_table.num_records > 0:
            idx = _build_table_index(ow_table, "Frame")
            for info in results:
                rows = idx.get(info.no, [])
                if not rows:
                    continue
                row = rows[0]
                v = _first_match(ow_table, row, ["XLMajor"])
                if v and _safe_float(v) > 0:
                    info.unbraced_ratio_major = _safe_float(v, 1.0)
                v = _first_match(ow_table, row, ["XLMinor"])
                if v and _safe_float(v) > 0:
                    info.unbraced_ratio_minor = _safe_float(v, 1.0)
                v = _first_match(ow_table, row, ["MuMajor"])
                if v and _safe_float(v) > 0:
                    info.mue_major = _safe_float(v, 1.0)
                v = _first_match(ow_table, row, ["MuMinor"])
                if v and _safe_float(v) > 0:
                    info.mue_minor = _safe_float(v, 1.0)

    return results


def collect_steel_design_results(
    model,
    frame_names: List[str],
) -> List[SteelDesignResultRow]:
    """
    采集钢结构设计结果 (表 5.1)
    全部通过 DatabaseTables API 获取。
    """
    design_tables = _find_steel_design_tables(model)

    frame_data: Dict[str, SteelDesignResultRow] = {}
    for idx, name in enumerate(frame_names, start=1):
        frame_data[name] = SteelDesignResultRow(index=idx, frame_name=name)

    # ---- Summary 表: 应力比 ----
    summary_key = design_tables.get("summary")
    if summary_key:
        st = _try_get_table(model, summary_key)
        if st and st.num_records > 0:
            idx_map = _build_table_index(st, "Frame")
            for name, row_obj in frame_data.items():
                rows = idx_map.get(name, [])
                if not rows:
                    continue
                best_row = rows[0]
                best_ratio = _safe_float(st.get_value(rows[0], "Ratio"))
                for r in rows[1:]:
                    ratio = _safe_float(st.get_value(r, "Ratio"))
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_row = r
                row_obj.ratio = best_ratio
                row_obj.exceeded = "无" if best_ratio <= 1.0 else "有"

    # ---- PMM Details 表: 内力、稳定系数、长细比 ----
    pmm_key = design_tables.get("pmm")
    if pmm_key:
        pt = _try_get_table(model, pmm_key)
        if pt and pt.num_records > 0:
            idx_map = _build_table_index(pt, "Frame")
            for name, row_obj in frame_data.items():
                rows = idx_map.get(name, [])
                if not rows:
                    continue
                # 找最大应力比行 (Chinese 2018 用 TotalRatio)
                best_row = rows[0]
                best_ratio = _safe_float(
                    _first_match(pt, rows[0], ["TotalRatio", "Ratio"]))
                for r in rows[1:]:
                    ratio = _safe_float(
                        _first_match(pt, r, ["TotalRatio", "Ratio"]))
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_row = r

                # 轴力 N
                v = _first_match(pt, best_row, ["N", "PUorPD", "P"])
                if v:
                    row_obj.n = _safe_float(v)
                # M3 (Major)
                v = _first_match(pt, best_row, ["MMajor", "MU3orMD3", "M3"])
                if v:
                    row_obj.m3 = _safe_float(v)
                # M2 (Minor)
                v = _first_match(pt, best_row, ["MMinor", "MU2orMD2", "M2"])
                if v:
                    row_obj.m2 = _safe_float(v)
                # φ3 轴心稳定 (Major)
                v = _first_match(pt, best_row, ["PhiMajor", "Phi3"])
                if v:
                    row_obj.phi3 = _safe_float(v)
                # φ2 轴心稳定 (Minor)
                v = _first_match(pt, best_row, ["PhiMinor", "Phi2"])
                if v:
                    row_obj.phi2 = _safe_float(v)
                # φb3 弯曲稳定 (Major)
                v = _first_match(pt, best_row, ["PhibMajor", "PhiB3", "Phib3"])
                if v:
                    row_obj.phi_b3 = _safe_float(v)
                # φb2 弯曲稳定 (Minor)
                v = _first_match(pt, best_row, ["PhibMinor", "PhiB2", "Phib2"])
                if v:
                    row_obj.phi_b2 = _safe_float(v)
                # 长细比 主轴
                v = _first_match(pt, best_row, ["LambdaMajor", "LamMajor"])
                if v:
                    row_obj.slenderness_major = _safe_float(v)
                # 长细比 次轴
                v = _first_match(pt, best_row, ["LambdaMinor", "LamMinor"])
                if v:
                    row_obj.slenderness_minor = _safe_float(v)

    return [frame_data[name] for name in frame_names if name in frame_data]


def discover_tables(model, keyword: str = "Steel Design") -> List[str]:
    """
    调试工具：通过直接尝试常见表名来发现可用表格。
    绕开 GetAvailableTables 的 comtypes 兼容性问题。
    """
    # 已知的钢结构设计表名模式
    candidates = []
    for suffix in _CHINESE_SUFFIXES:
        candidates.extend([
            f"Steel Design 1 - Summary Data - {suffix}",
            f"Steel Design 2 - PMM Details - {suffix}",
            f"Steel Design 3 - Detailed Data - {suffix}",
            f"Steel Design Overwrites - {suffix}",
        ])

    found = []
    for key in candidates:
        if keyword.lower() not in key.lower():
            continue
        t = _try_get_table(model, key)
        if t is not None:
            found.append(f"{key}  (records={t.num_records}, fields={t.field_keys})")

    return found


def discover_table_fields(model, table_key: str) -> List[str]:
    """
    调试工具：列出指定表格的所有字段键名。
    """
    t = _try_get_table(model, table_key)
    if t:
        return t.field_keys
    return []
