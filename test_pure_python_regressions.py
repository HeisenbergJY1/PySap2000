# -*- coding: utf-8 -*-
"""Pure Python regression tests that do not require a SAP2000 instance."""

import os
import sys
import tomllib
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from setuptools.discovery import find_package_path


_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_THIS_DIR)
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)

from PySap2000 import Application
from PySap2000.database_tables.tables import TableData
from PySap2000.exceptions import ObjectError
from PySap2000.global_parameters.units import UnitSystem
import PySap2000.report.data_collector as data_collector_module
import PySap2000.report.generator as generator_module
import PySap2000.section.frame_section as frame_section_module
import PySap2000.statistics.cable_usage as cable_usage_module
import PySap2000.statistics.steel_usage as steel_usage_module
import PySap2000.structure_core.cable as cable_module


def _make_table(table_key, field_keys, rows):
    """Build a `TableData` instance from row dictionaries."""
    data = []
    for row in rows:
        for field in field_keys:
            value = row.get(field, "")
            data.append("" if value is None else str(value))
    return TableData(
        table_key=table_key,
        field_keys=list(field_keys),
        num_records=len(rows),
        data=data,
    )


class _UnitsTrackingModel:
    """Minimal fake model that tracks unit switches."""

    def __init__(self, initial_units=UnitSystem.KN_MM_C):
        self.current_units = initial_units
        self.set_units_calls = []

    def GetPresentUnits(self):
        return self.current_units

    def SetPresentUnits(self, units):
        self.set_units_calls.append(units)
        self.current_units = units
        return 0


class TestApplicationBulkDispatch(unittest.TestCase):
    """Pure Python coverage for `Application.get_object_list`."""

    @staticmethod
    def _make_app():
        app = Application.__new__(Application)
        app._model = object()
        return app

    def test_get_object_list_uses_name_filtered_get_all(self):
        class NameFiltered:
            calls = []

            @classmethod
            def get_all(cls, model, names=None):
                cls.calls.append((model, names))
                return ["ok"]

        app = self._make_app()
        result = app.get_object_list(NameFiltered, ["1", "2"])

        self.assertEqual(["ok"], result)
        self.assertEqual([(app._model, ["1", "2"])], NameFiltered.calls)

    def test_get_object_list_uses_legacy_name_filtered__get_all(self):
        class LegacyNameFiltered:
            calls = []

            @classmethod
            def _get_all(cls, model, nos=None):
                cls.calls.append((model, nos))
                return ["legacy"]

        app = self._make_app()
        result = app.get_object_list(LegacyNameFiltered, ["3"])

        self.assertEqual(["legacy"], result)
        self.assertEqual([(app._model, ["3"])], LegacyNameFiltered.calls)

    def test_get_object_list_rejects_non_name_filtered_get_all(self):
        class EnumFiltered:
            calls = []

            @classmethod
            def get_all(cls, model, prop_type=None):
                cls.calls.append((model, prop_type))
                return ["unexpected"]

        app = self._make_app()

        with self.assertRaisesRegex(ObjectError, "does not support filtered bulk retrieval"):
            app.get_object_list(EnumFiltered, ["DECK"])

        self.assertEqual([], EnumFiltered.calls)


class TestPackagingConfig(unittest.TestCase):
    """Regression coverage for the package layout declared in `pyproject.toml`."""

    def test_package_dir_maps_the_current_repo_layout(self):
        config = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
        package_dir = config["tool"]["setuptools"]["package-dir"]

        root_path = os.path.normpath(find_package_path("PySap2000", package_dir, "."))
        report_path = os.path.normpath(
            find_package_path("PySap2000.report", package_dir, ".")
        )
        statistics_path = os.path.normpath(
            find_package_path("PySap2000.statistics", package_dir, ".")
        )

        self.assertEqual(".", root_path)
        self.assertEqual("report", report_path)
        self.assertEqual("statistics", statistics_path)


class TestReportRegressions(unittest.TestCase):
    """Pure Python tests for report collection and generation helpers."""

    def test_collect_frame_element_info_reads_imported_helpers_and_overwrites(self):
        fake_frame = SimpleNamespace(section="SEC1", length=12.34)
        fake_release = SimpleNamespace(
            release_i=(True, False, False, False, False, True),
            release_j=(False, False, False, False, True, True),
        )

        pmm_table = _make_table(
            "Steel Design 2 - PMM Details - Chinese 2018",
            ["Frame", "LRatioMajor", "LRatioMinor", "MueMajor", "MueMinor"],
            [
                {
                    "Frame": "F1",
                    "LRatioMajor": 1.2,
                    "LRatioMinor": 1.3,
                    "MueMajor": 0.9,
                    "MueMinor": 0.8,
                }
            ],
        )
        overwrite_table = _make_table(
            "Steel Design Overwrites - Chinese 2018",
            ["Frame", "XLMajor", "MuMinor"],
            [{"Frame": "F1", "XLMajor": 1.5, "MuMinor": 1.1}],
        )

        def fake_get_table(_model, table_key):
            tables = {
                "Steel Design 2 - PMM Details - Chinese 2018": pmm_table,
                "Steel Design Overwrites - Chinese 2018": overwrite_table,
            }
            return tables.get(table_key)

        with patch.object(
            data_collector_module.DatabaseTables,
            "get_table_for_display",
            side_effect=fake_get_table,
        ), patch(
            "PySap2000.structure_core.frame.Frame.get_by_name",
            return_value=fake_frame,
        ), patch(
            "PySap2000.frame.release.get_frame_release",
            return_value=fake_release,
        ):
            results = data_collector_module.collect_frame_element_info(object(), ["F1"])

        self.assertEqual(1, len(results))
        info = results[0]
        self.assertEqual("SEC1", info.section_name)
        self.assertAlmostEqual(12.34, info.length)
        self.assertAlmostEqual(1.5, info.unbraced_ratio_major)
        self.assertAlmostEqual(1.3, info.unbraced_ratio_minor)
        self.assertAlmostEqual(0.9, info.mue_major)
        self.assertAlmostEqual(1.1, info.mue_minor)
        self.assertEqual("U1 R3", info.release_i)
        self.assertEqual("R2 R3", info.release_j)

    def test_report_generator_uses_frame_name_list_without_sap(self):
        class _FakeRFonts:
            def set(self, *_args):
                return None

        class _FakeStyle:
            def __init__(self):
                self.font = SimpleNamespace(name=None, size=None)
                self._element = SimpleNamespace(
                    rPr=SimpleNamespace(rFonts=_FakeRFonts())
                )

        class _FakeDocument:
            def __init__(self):
                self.styles = {"Normal": _FakeStyle()}
                self.saved_path = None

            def save(self, path):
                self.saved_path = path

        fake_doc = _FakeDocument()
        output_path = os.path.join(_THIS_DIR, "pure_python_report.docx")

        with patch.object(generator_module, "Document", return_value=fake_doc), patch(
            "PySap2000.structure_core.frame.Frame.get_name_list",
            return_value=["F1", "F2"],
        ) as get_names:
            generator = generator_module.ReportGenerator(object())
            result = generator.generate(
                output_path,
                frame_names=None,
                include_element_info=False,
                include_design_results=False,
                include_charts=False,
            )

        self.assertEqual(os.path.abspath(output_path), result)
        self.assertEqual(output_path, fake_doc.saved_path)
        get_names.assert_called_once()


class TestSectionAndStatisticsRegressions(unittest.TestCase):
    """Pure Python coverage for section/statistics helpers."""

    def test_frame_section_calculates_weight_and_restores_units(self):
        model = _UnitsTrackingModel(initial_units=UnitSystem.KN_MM_C)
        model.PropFrame = SimpleNamespace(GetSectProps=lambda *args: [0.02])
        model.PropMaterial = SimpleNamespace(GetWeightAndMass=lambda name: [0.0, 8000.0])

        section = frame_section_module.FrameSection(name="SEC1", material="STEEL")
        weight = section._calculate_weight_per_meter(model)

        self.assertAlmostEqual(160.0, weight)
        self.assertEqual(
            [UnitSystem.N_M_C, UnitSystem.KN_MM_C],
            model.set_units_calls,
        )

    def test_steel_usage_calculates_totals_from_fake_tables(self):
        model = _UnitsTrackingModel(initial_units=UnitSystem.KN_MM_C)

        def get_table_for_display_array(table_key, *_args):
            if table_key == "Connectivity - Frame":
                return (None, None, ["Frame", "Length"], 1, ["F1", "2.0"], 0)
            if table_key == "Frame Section Assignments":
                return (
                    None,
                    None,
                    ["Frame", "AnalSect", "MatProp"],
                    1,
                    ["F1", "SEC1", "Default"],
                    0,
                )
            return (None, None, [], 0, [], 1)

        model.DatabaseTables = SimpleNamespace(
            GetTableForDisplayArray=get_table_for_display_array
        )
        model.PropFrame = SimpleNamespace(
            GetSectProps=lambda *args: [0.01],
            GetTypeOAPI=lambda name: [8],
            GetRectangle=lambda name: ["", "STEEL"],
        )
        model.PropMaterial = SimpleNamespace(
            GetWeightAndMass=lambda name: [0.0, 7850.0]
        )

        usage = steel_usage_module.SteelUsage.calculate(model, group_by="material")

        self.assertAlmostEqual(157.0, usage.total)
        self.assertEqual({"STEEL": 157.0}, usage.by_material)
        self.assertEqual(
            [UnitSystem.N_M_C, UnitSystem.KN_MM_C],
            model.set_units_calls,
        )

    def test_cable_usage_calculates_totals_from_fake_tables(self):
        model = _UnitsTrackingModel(initial_units=UnitSystem.KN_MM_C)

        def get_table_for_display_array(table_key, *_args):
            if table_key == "Connectivity - Cable":
                return (None, None, ["Cable", "Length"], 1, ["C1", "10.0"], 0)
            if table_key == "Cable Section Assignments":
                return (
                    None,
                    None,
                    ["Cable", "CableSect"],
                    1,
                    ["C1", "CAB1"],
                    0,
                )
            return (None, None, [], 0, [], 1)

        model.CableObj = SimpleNamespace(GetNameList=lambda *_args: (1, ["C1"]))
        model.DatabaseTables = SimpleNamespace(
            GetTableForDisplayArray=get_table_for_display_array
        )
        model.PropCable = SimpleNamespace(GetProp=lambda *args: ["WIRE", 0.005, 0, "", "", 0])
        model.PropMaterial = SimpleNamespace(GetWeightAndMass=lambda name: [0.0, 7.85])

        usage = cable_usage_module.CableUsage.calculate(model, group_by="material")

        self.assertAlmostEqual(392.5, usage.total)
        self.assertEqual({"WIRE": 392.5}, usage.by_material)
        self.assertEqual(
            [UnitSystem.N_M_C, UnitSystem.KN_MM_C],
            model.set_units_calls,
        )


class TestCableBulkGetterAlias(unittest.TestCase):
    """Regression coverage for the new `Cable.get_all` alias."""

    def test_get_all_delegates_to_legacy_bulk_getter(self):
        calls = []
        model = object()

        def fake_get_all(cls, sap_model, nos=None):
            calls.append((sap_model, nos))
            return ["C1"]

        with patch.object(
            cable_module.Cable,
            "_get_all",
            new=classmethod(fake_get_all),
        ):
            result = cable_module.Cable.get_all(model, ["C1"])

        self.assertEqual(["C1"], result)
        self.assertEqual([(model, ["C1"])], calls)


if __name__ == "__main__":
    unittest.main(verbosity=2)
