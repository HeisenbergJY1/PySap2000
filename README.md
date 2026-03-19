# PySap2000

SAP2000 的 Python 封装库，通过 comtypes 调用 COM 接口，提供 Pythonic 的 API 操作 SAP2000 模型。

## 环境要求

- Windows（SAP2000 仅支持 Windows COM 接口）
- Python 3.7+
- SAP2000 v20 及以上版本（推荐 v24+）

## 安装

```bash
pip install pysap2000
```

可选依赖：

```bash
# AI Agent 支持
pip install pysap2000[agent]

# 可视化支持
pip install pysap2000[vis]

# 开发依赖
pip install pysap2000[dev]

# 全部安装
pip install pysap2000[all]
```

## 快速上手

使用前请先启动 SAP2000 并打开一个模型文件。

```python
from PySap2000 import Application
from PySap2000.structure_core import Point, Frame
from PySap2000.global_parameters import Units, UnitSystem

# 连接正在运行的 SAP2000
with Application() as app:
    # 设置单位
    Units.set_present_units(app.model, UnitSystem.KN_M_C)

    # 创建节点
    app.create_object(Point(no=1, x=0, y=0, z=0))
    app.create_object(Point(no=2, x=10, y=0, z=0))

    # 创建杆件
    app.create_object(Frame(no=1, start_point=1, end_point=2, section="W14X30"))

    # 运行分析
    app.calculate()
```

## 核心模块

| 模块 | 说明 |
|------|------|
| `structure_core` | 核心对象：Point、Frame、Area、Cable、Link、Material |
| `point` | 节点属性：支座、约束、弹簧、质量、局部坐标 |
| `frame` | 杆件属性：截面、释放、修正系数、局部坐标 |
| `area` | 面单元属性：厚度、网格划分、偏移、弹簧 |
| `cable` | 索单元属性：截面、修正系数、输出站 |
| `link` | 连接单元属性：截面、局部坐标 |
| `section` | 截面定义：框架截面、面截面、索截面、连接截面 |
| `loading` | 荷载模式、荷载工况、荷载组合、质量源 |
| `loads` | 荷载施加：节点荷载、杆件荷载、面荷载、索荷载 |
| `results` | 分析结果：位移、内力、反力、应力 |
| `analyze` | 分析控制：运行分析、设置分析选项 |
| `design` | 设计：钢结构设计、设计规范 |
| `constraints` | 约束：刚性连接、等位移约束 |
| `database_tables` | 交互式表格：读取、编辑、导入导出 |
| `global_parameters` | 全局参数：单位、模型设置、项目信息 |
| `group` | 分组管理 |
| `selection` | 选择集操作 |
| `statistics` | 用钢量统计 |

## 更多示例

### 添加支座和荷载

```python
from PySap2000.point import set_point_restraint
from PySap2000.loads import PointLoad

# 固定支座
set_point_restraint(app.model, "1", [True]*6)

# 施加节点荷载
app.create_object(PointLoad(
    load_pattern="DEAD",
    points=["2"],
    fz=-10.0
))
```

### 获取分析结果

```python
from PySap2000.results import PointResults, FrameResults

# 节点位移
point_results = PointResults(app.model)
disp = point_results.get_displacement("2", load_case="DEAD")
print(f"竖向位移: {disp.uz}")

# 杆件内力
frame_results = FrameResults(app.model)
forces = frame_results.get_forces("1", load_case="DEAD")
```

### 钢结构设计

```python
from PySap2000.design import set_steel_code, start_steel_design, get_steel_summary_results, SteelDesignCode

set_steel_code(app.model, SteelDesignCode.CHINESE_2010)
start_steel_design(app.model)
results = get_steel_summary_results(app.model, "ALL", ItemType.GROUP)
```

### 交互式表格

```python
from PySap2000.database_tables import DatabaseTables

# 读取表格
data = DatabaseTables.get_table_for_display(app.model, "Joint Coordinates")
for row in data.to_dict_list():
    print(row)

# 编辑表格
result = DatabaseTables.edit_table(app.model, "Joint Coordinates", {
    0: {"XorR": "100"}
})
```

## 配置

```python
from PySap2000.config import config

# 严格模式：COM 调用失败时抛出异常
config.strict_mode = True

# 日志配置
from PySap2000.logger import setup_logger
setup_logger(level="DEBUG", log_file="pysap2000.log")
```

也支持环境变量：

```bash
set PYSAP_STRICT_MODE=true
set PYSAP_LOG_LEVEL=DEBUG
```

## 许可证

MIT License
