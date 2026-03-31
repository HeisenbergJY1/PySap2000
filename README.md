# PySap2000

Python wrapper for SAP2000. It uses `comtypes` to call the COM API and exposes a Pythonic interface for working with SAP2000 models.

## Requirements

- Windows (SAP2000 COM is Windows-only)
- Python 3.7+
- SAP2000 v20 or later (v24+ recommended)

## Installation

```bash
pip install pysap2000
```

Optional extras:

```bash
# Agent-oriented extras
pip install pysap2000[agent]

# Visualization extras
pip install pysap2000[vis]

# Development extras
pip install pysap2000[dev]

# Everything
pip install pysap2000[all]
```

## Quick start

Start SAP2000 and open a model file before running the example.

```python
from PySap2000 import Application
from PySap2000.structure_core import Point, Frame
from PySap2000.global_parameters import Units, UnitSystem

# Attach to a running SAP2000 instance
with Application() as app:
    # Set units
    Units.set_present_units(app.model, UnitSystem.KN_M_C)

    # Create joints
    app.create_object(Point(no=1, x=0, y=0, z=0))
    app.create_object(Point(no=2, x=10, y=0, z=0))

    # Create frame
    app.create_object(Frame(no=1, start_point=1, end_point=2, section="W14X30"))

    # Run analysis
    app.calculate()
```

## Core packages

| Package | Purpose |
|---------|---------|
| `structure_core` | Core objects: Point, Frame, Area, Cable, Link, Material |
| `point` | Joint properties: restraints, constraints, springs, mass, local axes |
| `frame` | Frame properties: section, releases, modifiers, local axes |
| `area` | Area properties: thickness, meshing, offsets, springs |
| `cable` | Cable properties: section, modifiers, output stations |
| `link` | Link properties: section, local axes |
| `section` | Section definitions: frame, area, cable, link |
| `loading` | Load patterns, load cases, combinations, mass source |
| `loads` | Applied loads: joint, frame, area, cable |
| `results` | Results: displacements, forces, reactions, stresses |
| `analyze` | Analysis control: run analysis, solver options |
| `design` | Design: steel design, design codes |
| `constraints` | Constraints: rigid links, equal DOF |
| `database_tables` | Interactive tables: read, edit, import/export |
| `global_parameters` | Globals: units, model settings, project info |
| `group` | Groups |
| `selection` | Selection |
| `statistics` | Steel usage statistics |

## More examples

### Restraints and loads

```python
from PySap2000.point import set_point_restraint
from PySap2000.loads import PointLoad

# Fixed support
set_point_restraint(app.model, "1", [True]*6)

# Joint load
app.create_object(PointLoad(
    load_pattern="DEAD",
    points=["2"],
    fz=-10.0
))
```

### Retrieve results

```python
from PySap2000.results import PointResults, FrameResults

# Joint displacement
point_results = PointResults(app.model)
disp = point_results.get_displacement("2", load_case="DEAD")
print(f"Vertical displacement: {disp.uz}")

# Frame forces
frame_results = FrameResults(app.model)
forces = frame_results.get_forces("1", load_case="DEAD")
```

### Steel design

```python
from PySap2000.design import set_steel_code, start_steel_design, get_steel_summary_results, SteelDesignCode

set_steel_code(app.model, SteelDesignCode.CHINESE_2010)
start_steel_design(app.model)
results = get_steel_summary_results(app.model, "ALL", ItemType.GROUP)
```

### Interactive tables

```python
from PySap2000.database_tables import DatabaseTables

# Read a table
data = DatabaseTables.get_table_for_display(app.model, "Joint Coordinates")
for row in data.to_dict_list():
    print(row)

# Edit a table
result = DatabaseTables.edit_table(app.model, "Joint Coordinates", {
    0: {"XorR": "100"}
})
```

## Configuration

```python
from PySap2000.config import config

# Strict mode: raise on COM failures
config.strict_mode = True

# Logging
from PySap2000.logger import setup_logger
setup_logger(level="DEBUG", log_file="pysap2000.log")
```

Environment variables:

```bash
set PYSAP_STRICT_MODE=true
set PYSAP_LOG_LEVEL=DEBUG
```

## License

MIT License
