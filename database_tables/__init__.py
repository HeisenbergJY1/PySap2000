# -*- coding: utf-8 -*-
"""
database_tables - SAP2000 交互式表格编辑模块

对应 SAP2000 的 DatabaseTables 接口，用于读取和编辑模型数据表格。

主要功能:
- 获取可用表格列表
- 读取表格数据 (Array/CSV/XML)
- 编辑表格数据
- 导出到 Excel

用法:
    from database_tables import DatabaseTables
    
    # 获取所有可用表格
    tables = DatabaseTables.get_available_tables(model)
    
    # 读取表格数据
    data = DatabaseTables.get_table_for_display(model, "Frame Section Assignments")
    
    # 编辑表格 (方式1: 标准流程)
    data = DatabaseTables.get_table_for_editing(model, "Joint Coordinates")
    data.set_value(0, "XorR", "100")
    DatabaseTables.set_table_for_editing(model, data)
    result = DatabaseTables.apply_edited_tables(model)
    
    # 编辑表格 (方式2: 便捷方法)
    result = DatabaseTables.edit_table(model, "Joint Coordinates", {
        0: {"XorR": "100"}
    })

API 分类:
    DATABASE_TABLES_API_CATEGORIES - 供 AI Agent 发现功能
"""

from .tables import (
    # 主类
    DatabaseTables,
    
    # 数据类
    TableData,
    TableField,
    TableInfo,
    ApplyResult,
    
    # 枚举
    TableExportFormat,
    TableImportType,
)

from .table_keys import (
    # 常用表格键名常量
    TABLE_KEYS,
    
    # 分类表格键名
    MODEL_DEFINITION_TABLES,
    ANALYSIS_RESULTS_TABLES,
    DESIGN_TABLES,
)


# ==================== API 分类索引 (供 AI Agent 发现功能) ====================

DATABASE_TABLES_API_CATEGORIES = {
    "表格查询": {
        "description": "获取可用表格和字段信息",
        "functions": [
            "get_available_tables",      # 获取可用表格列表 (有数据的)
            "get_available_table_keys",  # 获取可用表格键名列表
            "get_all_tables",            # 获取所有表格列表
            "get_all_table_keys",        # 获取所有表格键名列表
            "get_fields_in_table",       # 获取表格中的所有字段
            "get_all_fields_in_table",   # 获取表格中的所有字段 (原始格式)
            "find_tables",               # 搜索表格 (便捷方法)
            "get_obsolete_table_keys",   # 获取废弃表格键名映射
        ]
    },
    "读取表格 (Array)": {
        "description": "读取表格数据 (Array 格式)",
        "functions": [
            "get_table_for_display",     # 获取显示用表格数据
            "get_table_for_editing",     # 获取编辑用表格数据
            "read_table",                # 读取表格 (便捷方法)
        ]
    },
    "读取表格 (CSV)": {
        "description": "读取表格数据 (CSV 格式)",
        "functions": [
            "get_table_for_display_csv_file",    # 获取显示用表格并保存为 CSV 文件
            "get_table_for_display_csv_string",  # 获取显示用表格为 CSV 字符串
            "get_table_for_editing_csv_file",    # 获取编辑用表格并保存为 CSV 文件
            "get_table_for_editing_csv_string",  # 获取编辑用表格为 CSV 字符串
            "export_to_csv",                     # 导出表格到 CSV (便捷方法)
        ]
    },
    "编辑表格": {
        "description": "编辑和应用表格数据",
        "functions": [
            "set_table_for_editing",         # 设置编辑表格数据 (TableData)
            "set_table_for_editing_array",   # 设置编辑表格数据 (原始参数)
            "set_table_for_editing_csv_file",    # 从 CSV 文件设置编辑数据
            "set_table_for_editing_csv_string",  # 从 CSV 字符串设置编辑数据
            "apply_edited_tables",           # 应用已编辑的表格
            "cancel_table_editing",          # 取消表格编辑
            "edit_table",                    # 编辑表格 (便捷方法)
            "import_from_dataframe",         # 从 DataFrame 导入
            "import_from_csv",               # 从 CSV 文件导入 (便捷方法)
        ]
    },
    "显示选项 - 荷载": {
        "description": "设置荷载显示选项",
        "functions": [
            "get_load_patterns_selected",    # 获取选中的荷载模式
            "set_load_patterns_selected",    # 设置显示的荷载模式
            "get_load_cases_selected",       # 获取选中的荷载工况
            "set_load_cases_selected",       # 设置显示的荷载工况
            "get_load_combinations_selected", # 获取选中的荷载组合
            "set_load_combinations_selected", # 设置显示的荷载组合
        ]
    },
    "显示选项 - Named Sets": {
        "description": "设置命名集显示选项",
        "functions": [
            "get_section_cuts_selected",                 # 获取选中的截面切割
            "set_section_cuts_selected",                 # 设置显示的截面切割
            "get_generalized_displacements_selected",    # 获取选中的广义位移
            "set_generalized_displacements_selected",    # 设置显示的广义位移
            "get_pushover_named_sets_selected",          # 获取选中的 Pushover 命名集
            "set_pushover_named_sets_selected",          # 设置显示的 Pushover 命名集
            "get_joint_response_spectra_named_sets_selected",   # 获取选中的节点反应谱命名集
            "set_joint_response_spectra_named_sets_selected",   # 设置显示的节点反应谱命名集
            "get_plot_function_traces_named_sets_selected",     # 获取选中的绘图函数轨迹命名集
            "set_plot_function_traces_named_sets_selected",     # 设置显示的绘图函数轨迹命名集
            "get_element_virtual_work_named_sets_selected",     # 获取选中的单元虚功命名集
            "set_element_virtual_work_named_sets_selected",     # 设置显示的单元虚功命名集
        ]
    },
    "输出选项": {
        "description": "设置表格输出选项",
        "functions": [
            "get_table_output_options",      # 获取表格输出选项
            "set_table_output_options",      # 设置表格输出选项
        ]
    },
    "导出": {
        "description": "导出表格到外部格式",
        "functions": [
            "show_tables_in_excel",          # 在 Excel 中显示表格
        ]
    },
}


__all__ = [
    # 主类
    'DatabaseTables',
    
    # 数据类
    'TableData',
    'TableField',
    'TableInfo',
    'ApplyResult',
    
    # 枚举
    'TableExportFormat',
    'TableImportType',
    
    # 表格键名
    'TABLE_KEYS',
    'MODEL_DEFINITION_TABLES',
    'ANALYSIS_RESULTS_TABLES',
    'DESIGN_TABLES',
    
    # API 分类索引
    'DATABASE_TABLES_API_CATEGORIES',
]
