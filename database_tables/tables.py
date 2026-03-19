# -*- coding: utf-8 -*-
"""
tables.py - 交互式表格编辑核心类

对应 SAP2000 的 DatabaseTables 接口

API Reference:
    - DatabaseTables.GetAvailableTables
    - DatabaseTables.GetAllTables
    - DatabaseTables.GetAllFieldsInTable
    - DatabaseTables.GetTableForDisplayArray
    - DatabaseTables.GetTableForEditingArray
    - DatabaseTables.SetTableForEditingArray
    - DatabaseTables.ApplyEditedTables
    - DatabaseTables.CancelTableEditing
    - DatabaseTables.ShowTablesInExcel
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any, Union
from PySap2000.com_helper import com_ret, com_data
from enum import IntEnum


class TableImportType(IntEnum):
    """表格导入类型"""
    NOT_IMPORTABLE = 0          # 不可导入
    IMPORTABLE = 1              # 可导入
    IMPORTABLE_NOT_INTERACTIVE = 2  # 可导入但不可交互


class TableExportFormat(IntEnum):
    """表格导出格式"""
    ARRAY = 1       # 数组格式
    CSV_FILE = 2    # CSV 文件
    CSV_STRING = 3  # CSV 字符串
    XML_STRING = 4  # XML 字符串


@dataclass
class TableInfo:
    """
    表格信息
    
    Attributes:
        table_key: 表格键名
        table_name: 表格显示名称
        import_type: 导入类型 (0=不可导入, 1=可导入, 2=可导入但不可交互)
        is_empty: 是否为空表格
    """
    table_key: str
    table_name: str = ""
    import_type: int = 0
    is_empty: bool = True
    
    @property
    def is_importable(self) -> bool:
        """是否可导入"""
        return self.import_type in (1, 2)


@dataclass
class TableField:
    """
    表格字段信息
    
    Attributes:
        field_key: 字段键名
        field_name: 字段显示名称
        description: 字段描述
        units: 单位字符串
        is_importable: 是否可导入
    """
    field_key: str
    field_name: str = ""
    description: str = ""
    units: str = ""
    is_importable: bool = True


@dataclass
class TableData:
    """
    表格数据
    
    Attributes:
        table_key: 表格键名
        table_version: 表格版本
        field_keys: 字段键名列表
        num_records: 记录数
        data: 数据列表 (按行展开的一维列表)
    """
    table_key: str = ""
    table_version: int = 0
    field_keys: List[str] = field(default_factory=list)
    num_records: int = 0
    data: List[str] = field(default_factory=list)
    
    @property
    def num_fields(self) -> int:
        """字段数量"""
        return len(self.field_keys)
    
    def get_row(self, row_index: int) -> List[str]:
        """
        获取指定行的数据
        
        Args:
            row_index: 行索引 (0-based)
        
        Returns:
            该行的数据列表
        """
        if row_index < 0 or row_index >= self.num_records:
            return []
        start = row_index * self.num_fields
        end = start + self.num_fields
        return self.data[start:end]
    
    def set_row(self, row_index: int, row_data: List[str]) -> bool:
        """
        设置指定行的数据
        
        Args:
            row_index: 行索引 (0-based)
            row_data: 行数据列表
        
        Returns:
            是否设置成功
        """
        if row_index < 0 or row_index >= self.num_records:
            return False
        if len(row_data) != self.num_fields:
            return False
        start = row_index * self.num_fields
        for i, value in enumerate(row_data):
            self.data[start + i] = str(value)
        return True
    
    def add_row(self, row_data: List[str]) -> bool:
        """
        添加一行数据
        
        Args:
            row_data: 行数据列表
        
        Returns:
            是否添加成功
        """
        if len(row_data) != self.num_fields:
            return False
        self.data.extend([str(v) for v in row_data])
        self.num_records += 1
        return True
    
    def delete_row(self, row_index: int) -> bool:
        """
        删除指定行
        
        Args:
            row_index: 行索引 (0-based)
        
        Returns:
            是否删除成功
        """
        if row_index < 0 or row_index >= self.num_records:
            return False
        start = row_index * self.num_fields
        end = start + self.num_fields
        del self.data[start:end]
        self.num_records -= 1
        return True
    
    def get_value(self, row_index: int, field_name: str) -> Optional[str]:
        """
        获取指定单元格的值
        
        Args:
            row_index: 行索引 (0-based)
            field_name: 字段名称
        
        Returns:
            单元格值，未找到返回 None
        """
        if field_name not in self.field_keys:
            return None
        col_index = self.field_keys.index(field_name)
        data_index = row_index * self.num_fields + col_index
        if 0 <= data_index < len(self.data):
            return self.data[data_index]
        return None
    
    def set_value(self, row_index: int, field_name: str, value: str) -> bool:
        """
        设置指定单元格的值
        
        Args:
            row_index: 行索引 (0-based)
            field_name: 字段名称
            value: 新值
        
        Returns:
            是否设置成功
        """
        if field_name not in self.field_keys:
            return False
        col_index = self.field_keys.index(field_name)
        data_index = row_index * self.num_fields + col_index
        if 0 <= data_index < len(self.data):
            self.data[data_index] = str(value)
            return True
        return False
    
    def get_column(self, field_name: str) -> List[str]:
        """
        获取指定列的所有值
        
        Args:
            field_name: 字段名称
        
        Returns:
            该列的值列表
        """
        if field_name not in self.field_keys:
            return []
        col_index = self.field_keys.index(field_name)
        return [self.data[i * self.num_fields + col_index] 
                for i in range(self.num_records)]
    
    def find_rows(self, field_name: str, value: str) -> List[int]:
        """
        查找字段值匹配的行索引
        
        Args:
            field_name: 字段名称
            value: 要匹配的值
        
        Returns:
            匹配的行索引列表
        """
        result = []
        for i in range(self.num_records):
            if self.get_value(i, field_name) == value:
                result.append(i)
        return result
    
    def to_dict_list(self) -> List[Dict[str, str]]:
        """
        转换为字典列表格式
        
        Returns:
            每行一个字典的列表
        """
        result = []
        for i in range(self.num_records):
            row_data = self.get_row(i)
            row_dict = dict(zip(self.field_keys, row_data))
            result.append(row_dict)
        return result
    
    def from_dict_list(self, dict_list: List[Dict[str, str]]) -> None:
        """
        从字典列表导入数据
        
        Args:
            dict_list: 字典列表
        """
        self.data = []
        self.num_records = 0
        for row_dict in dict_list:
            row_data = [row_dict.get(key, "") for key in self.field_keys]
            self.add_row(row_data)
    
    def to_dataframe(self):
        """
        转换为 pandas DataFrame
        
        Returns:
            pandas.DataFrame 对象
        
        Raises:
            ImportError: 如果未安装 pandas
        """
        try:
            import pandas as pd
            return pd.DataFrame(self.to_dict_list())
        except ImportError:
            raise ImportError("需要安装 pandas: pip install pandas")
    
    def from_dataframe(self, df) -> None:
        """
        从 pandas DataFrame 导入数据
        
        Args:
            df: pandas.DataFrame 对象
        """
        self.from_dict_list(df.to_dict('records'))
    
    def copy(self) -> 'TableData':
        """创建副本"""
        return TableData(
            table_key=self.table_key,
            table_version=self.table_version,
            field_keys=self.field_keys.copy(),
            num_records=self.num_records,
            data=self.data.copy()
        )


@dataclass
class ApplyResult:
    """
    应用编辑结果
    
    Attributes:
        success: 是否成功
        num_fatal_errors: 致命错误数
        num_error_msgs: 错误消息数
        num_warn_msgs: 警告消息数
        num_info_msgs: 信息消息数
        import_log: 导入日志
    """
    success: bool = False
    num_fatal_errors: int = 0
    num_error_msgs: int = 0
    num_warn_msgs: int = 0
    num_info_msgs: int = 0
    import_log: str = ""


class DatabaseTables:
    """
    数据库表格管理类
    
    提供交互式表格编辑的静态方法
    
    典型工作流程:
        1. get_available_tables() - 获取可用表格
        2. get_table_for_editing() - 获取表格数据
        3. 修改 TableData 对象
        4. set_table_for_editing() - 设置修改后的数据
        5. apply_edited_tables() - 应用更改到模型
    
    Example:
        # 读取并修改节点坐标
        data = DatabaseTables.get_table_for_editing(model, "Joint Coordinates")
        data.set_value(0, "XorR", "100")  # 修改第一个节点的 X 坐标
        DatabaseTables.set_table_for_editing(model, data)
        result = DatabaseTables.apply_edited_tables(model)
        if not result.success:
            print(result.import_log)
    """
    
    # ==================== 表格查询 ====================
    
    @staticmethod
    def get_available_tables(model) -> List[TableInfo]:
        """
        获取可用表格列表 (有数据的表格)
        
        Args:
            model: SapModel 对象
        
        Returns:
            TableInfo 对象列表
        
        Example:
            tables = DatabaseTables.get_available_tables(model)
            for t in tables:
                print(f"{t.table_key}: empty={t.is_empty}, importable={t.is_importable}")
        """
        # API: GetAvailableTables(NumberTables, TableKey[], TableName[], ImportType[])
        result = model.DatabaseTables.GetAvailableTables(0, [], [], [])
        
        ret = com_ret(result)
        if ret != 0:
            return []
        
        num_tables = com_data(result, index=0, default=0)
        table_keys = list(com_data(result, index=1, default=[]) or [])
        table_names = list(com_data(result, index=2, default=[]) or [])
        import_types = list(com_data(result, index=3, default=[]) or [])
        
        tables = []
        for i in range(num_tables):
            tables.append(TableInfo(
                table_key=table_keys[i] if i < len(table_keys) else "",
                table_name=table_names[i] if i < len(table_names) else "",
                import_type=import_types[i] if i < len(import_types) else 0,
                is_empty=False
            ))
        return tables
    
    @staticmethod
    def get_available_table_keys(model) -> List[str]:
        """
        获取可用表格键名列表 (简化版)
        
        Args:
            model: SapModel 对象
        
        Returns:
            表格键名列表
        """
        tables = DatabaseTables.get_available_tables(model)
        return [t.table_key for t in tables]
    
    @staticmethod
    def get_all_tables(model) -> List[TableInfo]:
        """
        获取所有表格列表 (包括空表格)
        
        Args:
            model: SapModel 对象
        
        Returns:
            TableInfo 对象列表
        """
        # API: GetAllTables(NumberTables, TableKey[], TableName[], ImportType[])
        result = model.DatabaseTables.GetAllTables(0, [], [], [])
        
        ret = com_ret(result)
        if ret != 0:
            return []
        
        num_tables = com_data(result, index=0, default=0)
        table_keys = list(com_data(result, index=1, default=[]) or [])
        table_names = list(com_data(result, index=2, default=[]) or [])
        import_types = list(com_data(result, index=3, default=[]) or [])
        
        tables = []
        for i in range(num_tables):
            tables.append(TableInfo(
                table_key=table_keys[i] if i < len(table_keys) else "",
                table_name=table_names[i] if i < len(table_names) else "",
                import_type=import_types[i] if i < len(import_types) else 0,
                is_empty=True  # GetAllTables 不返回 IsEmpty
            ))
        return tables
    
    @staticmethod
    def get_all_table_keys(model) -> List[str]:
        """
        获取所有表格键名列表 (简化版)
        
        Args:
            model: SapModel 对象
        
        Returns:
            表格键名列表
        """
        tables = DatabaseTables.get_all_tables(model)
        return [t.table_key for t in tables]
    
    @staticmethod
    def get_fields_in_table(model, table_key: str, table_version: int = 0) -> List[TableField]:
        """
        获取表格中的所有字段
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            table_version: 表格版本 (默认 0)
        
        Returns:
            TableField 对象列表
        
        Example:
            fields = DatabaseTables.get_fields_in_table(model, "Joint Coordinates")
            for f in fields:
                print(f"{f.field_key}: {f.description} ({f.units})")
        """
        # API: GetAllFieldsInTable(TableKey, TableVersion, NumberFields, 
        #      FieldKey[], FieldName[], Description[], UnitsString[], IsImportable[])
        # 返回: [TableVersion, NumberFields, FieldKey[], FieldName[], Description[], UnitsString[], IsImportable[], ret]
        result = model.DatabaseTables.GetAllFieldsInTable(
            table_key, table_version, 0, [], [], [], [], []
        )
        
        ret = com_ret(result)
        if ret != 0:
            return []
        
        num_fields = com_data(result, index=1, default=0)
        field_keys = list(com_data(result, index=2, default=[]) or [])
        field_names = list(com_data(result, index=3, default=[]) or [])
        descriptions = list(com_data(result, index=4, default=[]) or [])
        units = list(com_data(result, index=5, default=[]) or [])
        is_importable = list(com_data(result, index=6, default=[]) or [])
        
        fields = []
        for i in range(num_fields):
            fields.append(TableField(
                field_key=field_keys[i] if i < len(field_keys) else "",
                field_name=field_names[i] if i < len(field_names) else "",
                description=descriptions[i] if i < len(descriptions) else "",
                units=units[i] if i < len(units) else "",
                is_importable=is_importable[i] if i < len(is_importable) else True
            ))
        return fields
    
    @staticmethod
    def get_all_fields_in_table(
        model,
        table_key: str,
        table_version: int = 0
    ) -> Tuple[List[str], List[str], List[str], List[str], List[bool]]:
        """
        获取表格中的所有字段 (原始格式)
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            table_version: 表格版本
        
        Returns:
            (field_keys, field_names, descriptions, units, is_importable) 元组
        """
        fields = DatabaseTables.get_fields_in_table(model, table_key, table_version)
        return (
            [f.field_key for f in fields],
            [f.field_name for f in fields],
            [f.description for f in fields],
            [f.units for f in fields],
            [f.is_importable for f in fields]
        )

    
    # ==================== 读取表格 ====================
    
    @staticmethod
    def get_table_for_display(
        model,
        table_key: str,
        field_keys: List[str] = None,
        group_name: str = ""
    ) -> Optional[TableData]:
        """
        获取显示用表格数据 (Array 格式)
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            field_keys: 要获取的字段列表，None 或 [""] 表示所有字段
            group_name: 组名称，空字符串或 "All" 表示所有对象
        
        Returns:
            TableData 对象，失败返回 None
        
        Example:
            data = DatabaseTables.get_table_for_display(
                model, 
                "Frame Section Assignments"
            )
            if data:
                for row in data.to_dict_list():
                    print(row)
        """
        # 如果 field_keys 为 None 或空，使用 [""] 表示所有字段
        if field_keys is None or len(field_keys) == 0:
            field_keys = [""]
        
        # API: GetTableForDisplayArray(TableKey, FieldKeyList[], GroupName,
        #      TableVersion, FieldKeysIncluded[], NumberRecords, TableData[])
        # 返回格式: [输入的field_keys, TableVersion, FieldKeysIncluded, NumberRecords, TableData, ret]
        result = model.DatabaseTables.GetTableForDisplayArray(
            table_key,
            field_keys,
            group_name,
            0,      # TableVersion (output)
            [],     # FieldKeysIncluded (output)
            0,      # NumberRecords (output)
            []      # TableData (output)
        )
        
        ret = com_ret(result)
        if ret != 0:
            return None
        
        return TableData(
            table_key=table_key,
            table_version=com_data(result, index=1, default=0),
            field_keys=list(com_data(result, index=2, default=[]) or []),
            num_records=com_data(result, index=3, default=0),
            data=list(com_data(result, index=4, default=[]) or [])
        )
    
    @staticmethod
    def get_table_for_editing(
        model,
        table_key: str,
        group_name: str = ""
    ) -> Optional[TableData]:
        """
        获取编辑用表格数据 (Array 格式)
        
        与 get_table_for_display 类似，但返回可编辑的数据。
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            group_name: 组名称 (当前版本未激活此参数)
        
        Returns:
            TableData 对象，失败返回 None
        
        Example:
            data = DatabaseTables.get_table_for_editing(model, "Joint Coordinates")
            data.set_value(0, "XorR", "100")
            DatabaseTables.set_table_for_editing(model, data)
            DatabaseTables.apply_edited_tables(model)
        """
        # API: GetTableForEditingArray(TableKey, GroupName,
        #      TableVersion, FieldKeysIncluded[], NumberRecords, TableData[])
        # 返回: [TableVersion, FieldKeysIncluded[], NumberRecords, TableData[], ret]
        result = model.DatabaseTables.GetTableForEditingArray(
            table_key,
            group_name,
            0,      # TableVersion (output)
            [],     # FieldKeysIncluded (output)
            0,      # NumberRecords (output)
            []      # TableData (output)
        )
        
        ret = com_ret(result)
        if ret != 0:
            return None
        
        return TableData(
            table_key=table_key,
            table_version=com_data(result, index=0, default=0),
            field_keys=list(com_data(result, index=1, default=[]) or []),
            num_records=com_data(result, index=2, default=0),
            data=list(com_data(result, index=3, default=[]) or [])
        )

    
    # ==================== 编辑表格 ====================
    
    @staticmethod
    def set_table_for_editing(
        model,
        table_data: TableData
    ) -> int:
        """
        设置编辑表格数据 (推荐方式)
        
        Args:
            model: SapModel 对象
            table_data: TableData 对象
        
        Returns:
            0 表示成功，非零表示失败
        
        Example:
            data = DatabaseTables.get_table_for_editing(model, "Joint Coordinates")
            data.set_value(0, "XorR", "100")
            ret = DatabaseTables.set_table_for_editing(model, data)
            if ret == 0:
                DatabaseTables.apply_edited_tables(model)
        """
        # API: SetTableForEditingArray(TableKey, TableVersion, 
        #      FieldKeysIncluded[], NumberRecords, TableData[])
        result = model.DatabaseTables.SetTableForEditingArray(
            table_data.table_key,
            table_data.table_version,
            table_data.field_keys,
            table_data.num_records,
            table_data.data
        )
        
        return com_ret(result)
    
    @staticmethod
    def set_table_for_editing_array(
        model,
        table_key: str,
        table_version: int,
        field_keys: List[str],
        num_records: int,
        data: List[str]
    ) -> int:
        """
        设置编辑表格数据 (原始参数方式)
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            table_version: 表格版本
            field_keys: 字段键名列表
            num_records: 记录数
            data: 数据列表
        
        Returns:
            0 表示成功
        """
        result = model.DatabaseTables.SetTableForEditingArray(
            table_key,
            table_version,
            field_keys,
            num_records,
            data
        )
        
        return com_ret(result)
    
    @staticmethod
    def apply_edited_tables(
        model,
        fill_import_log: bool = True
    ) -> ApplyResult:
        """
        应用已编辑的表格
        
        将所有通过 set_table_for_editing 设置的更改应用到模型。
        
        Args:
            model: SapModel 对象
            fill_import_log: 是否填充导入日志
        
        Returns:
            ApplyResult 对象
        
        Example:
            DatabaseTables.set_table_for_editing(model, data)
            result = DatabaseTables.apply_edited_tables(model)
            if not result.success:
                print(f"错误: {result.num_fatal_errors} 个致命错误")
                print(result.import_log)
        """
        # API: ApplyEditedTables(FillImportLog, NumFatalErrors, NumErrorMsgs, 
        #      NumWarnMsgs, NumInfoMsgs, ImportLog)
        result = model.DatabaseTables.ApplyEditedTables(
            fill_import_log, 0, 0, 0, 0, ""
        )
        
        apply_result = ApplyResult()
        apply_result.success = (com_ret(result) == 0)
        apply_result.num_fatal_errors = com_data(result, index=1, default=0)
        apply_result.num_error_msgs = com_data(result, index=2, default=0)
        apply_result.num_warn_msgs = com_data(result, index=3, default=0)
        apply_result.num_info_msgs = com_data(result, index=4, default=0)
        apply_result.import_log = com_data(result, index=5, default="")
        
        return apply_result
    
    @staticmethod
    def cancel_table_editing(model) -> int:
        """
        取消表格编辑
        
        取消所有未应用的表格编辑。
        
        Args:
            model: SapModel 对象
        
        Returns:
            0 表示成功
        """
        result = model.DatabaseTables.CancelTableEditing()
        return com_ret(result)
    
    # ==================== 显示选项 ====================
    
    @staticmethod
    def set_load_patterns_selected(
        model,
        load_patterns: List[str],
        selected: bool = True
    ) -> int:
        """
        设置显示的荷载模式
        
        Args:
            model: SapModel 对象
            load_patterns: 荷载模式名称列表
            selected: True=选中, False=取消选中
        
        Returns:
            0 表示成功
        """
        result = model.DatabaseTables.SetLoadPatternsSelectedForDisplay(
            len(load_patterns),
            load_patterns,
            selected
        )
        return com_ret(result)
    
    @staticmethod
    def set_load_cases_selected(
        model,
        load_cases: List[str],
        selected: bool = True
    ) -> int:
        """
        设置显示的荷载工况
        
        Args:
            model: SapModel 对象
            load_cases: 荷载工况名称列表
            selected: True=选中, False=取消选中
        
        Returns:
            0 表示成功
        """
        result = model.DatabaseTables.SetLoadCasesSelectedForDisplay(
            len(load_cases),
            load_cases,
            selected
        )
        return com_ret(result)
    
    @staticmethod
    def set_load_combinations_selected(
        model,
        load_combos: List[str],
        selected: bool = True
    ) -> int:
        """
        设置显示的荷载组合
        
        Args:
            model: SapModel 对象
            load_combos: 荷载组合名称列表
            selected: True=选中, False=取消选中
        
        Returns:
            0 表示成功
        """
        result = model.DatabaseTables.SetLoadCombinationsSelectedForDisplay(
            len(load_combos),
            load_combos,
            selected
        )
        return com_ret(result)
    
    # ==================== 导出 ====================
    
    @staticmethod
    def show_tables_in_excel(
        model,
        table_keys: List[str],
        field_keys_list: List[List[str]] = None,
        group_name: str = ""
    ) -> int:
        """
        在 Excel 中显示表格
        
        Args:
            model: SapModel 对象
            table_keys: 表格键名列表
            field_keys_list: 每个表格的字段键名列表 (可选)
            group_name: 组名称 (可选)
        
        Returns:
            0 表示成功
        
        Example:
            DatabaseTables.show_tables_in_excel(
                model,
                ["Frame Section Assignments", "Joint Coordinates"]
            )
        """
        num_tables = len(table_keys)
        
        if field_keys_list is None:
            field_keys_list = [[] for _ in table_keys]
        
        # 每个表格的字段数
        num_fields_per_table = [len(fields) for fields in field_keys_list]
        
        # 展平字段列表
        all_field_keys = []
        for fields in field_keys_list:
            all_field_keys.extend(fields)
        
        result = model.DatabaseTables.ShowTablesInExcel(
            num_tables,
            table_keys,
            num_fields_per_table,
            all_field_keys,
            group_name
        )
        
        return com_ret(result)
    
    # ==================== 便捷方法 ====================
    
    @staticmethod
    def read_table(
        model,
        table_key: str,
        as_dataframe: bool = False
    ):
        """
        读取表格数据 (便捷方法)
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            as_dataframe: 是否返回 pandas DataFrame
        
        Returns:
            TableData 对象或 pandas DataFrame
        
        Example:
            # 返回 TableData
            data = DatabaseTables.read_table(model, "Joint Coordinates")
            
            # 返回 DataFrame
            df = DatabaseTables.read_table(model, "Joint Coordinates", as_dataframe=True)
        """
        data = DatabaseTables.get_table_for_display(model, table_key)
        if data and as_dataframe:
            return data.to_dataframe()
        return data
    
    @staticmethod
    def edit_table(
        model,
        table_key: str,
        modifications: Dict[int, Dict[str, str]]
    ) -> ApplyResult:
        """
        编辑表格数据 (便捷方法)
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            modifications: 修改字典 {行索引: {字段名: 新值}}
        
        Returns:
            ApplyResult 对象
        
        Example:
            # 修改第0行的 X 坐标和第1行的 Y 坐标
            result = DatabaseTables.edit_table(model, "Joint Coordinates", {
                0: {"XorR": "100"},
                1: {"Y": "200"}
            })
        """
        data = DatabaseTables.get_table_for_editing(model, table_key)
        if not data:
            return ApplyResult(success=False, import_log="无法获取表格数据")
        
        for row_idx, field_values in modifications.items():
            for field_name, value in field_values.items():
                data.set_value(row_idx, field_name, value)
        
        ret = DatabaseTables.set_table_for_editing(model, data)
        if ret != 0:
            return ApplyResult(success=False, import_log="设置表格数据失败")
        
        return DatabaseTables.apply_edited_tables(model)
    
    @staticmethod
    def import_from_dataframe(
        model,
        table_key: str,
        df
    ) -> ApplyResult:
        """
        从 pandas DataFrame 导入数据
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            df: pandas DataFrame
        
        Returns:
            ApplyResult 对象
        
        Example:
            import pandas as pd
            df = pd.DataFrame({
                'Joint': ['1', '2'],
                'XorR': ['0', '100'],
                'Y': ['0', '0'],
                'Z': ['0', '0']
            })
            result = DatabaseTables.import_from_dataframe(model, "Joint Coordinates", df)
        """
        data = DatabaseTables.get_table_for_editing(model, table_key)
        if not data:
            return ApplyResult(success=False, import_log="无法获取表格数据")
        
        data.from_dataframe(df)
        
        ret = DatabaseTables.set_table_for_editing(model, data)
        if ret != 0:
            return ApplyResult(success=False, import_log="设置表格数据失败")
        
        return DatabaseTables.apply_edited_tables(model)

    # ==================== CSV 格式方法 ====================
    
    @staticmethod
    def get_table_for_display_csv_file(
        model,
        table_key: str,
        file_path: str,
        field_keys: List[str] = None,
        group_name: str = ""
    ) -> int:
        """
        获取显示用表格数据并保存为 CSV 文件
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            file_path: CSV 文件路径
            field_keys: 要获取的字段列表，None 表示所有字段
            group_name: 组名称，空字符串表示所有对象
        
        Returns:
            0 表示成功
        """
        if field_keys is None:
            field_keys = []
        
        result = model.DatabaseTables.GetTableForDisplayCSVFile(
            table_key,
            field_keys,
            group_name,
            file_path
        )
        
        return com_ret(result)
    
    @staticmethod
    def get_table_for_display_csv_string(
        model,
        table_key: str,
        field_keys: List[str] = None,
        group_name: str = ""
    ) -> Tuple[str, int]:
        """
        获取显示用表格数据为 CSV 字符串
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            field_keys: 要获取的字段列表，None 表示所有字段
            group_name: 组名称，空字符串表示所有对象
        
        Returns:
            (csv_string, ret) 元组
        """
        if field_keys is None:
            field_keys = []
        
        result = model.DatabaseTables.GetTableForDisplayCSVString(
            table_key,
            field_keys,
            group_name,
            ""  # CSVString (output)
        )
        
        return com_data(result, index=-2, default=""), com_ret(result)
    
    @staticmethod
    def get_table_for_editing_csv_file(
        model,
        table_key: str,
        file_path: str,
        field_keys: List[str] = None
    ) -> int:
        """
        获取编辑用表格数据并保存为 CSV 文件
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            file_path: CSV 文件路径
            field_keys: 要获取的字段列表，None 表示所有字段
        
        Returns:
            0 表示成功
        """
        if field_keys is None:
            field_keys = []
        
        result = model.DatabaseTables.GetTableForEditingCSVFile(
            table_key,
            field_keys,
            file_path
        )
        
        return com_ret(result)
    
    @staticmethod
    def get_table_for_editing_csv_string(
        model,
        table_key: str,
        field_keys: List[str] = None
    ) -> Tuple[str, int]:
        """
        获取编辑用表格数据为 CSV 字符串
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            field_keys: 要获取的字段列表，None 表示所有字段
        
        Returns:
            (csv_string, ret) 元组
        """
        if field_keys is None:
            field_keys = []
        
        result = model.DatabaseTables.GetTableForEditingCSVString(
            table_key,
            field_keys,
            ""  # CSVString (output)
        )
        
        return com_data(result, index=-2, default=""), com_ret(result)
    
    @staticmethod
    def set_table_for_editing_csv_file(
        model,
        table_key: str,
        file_path: str
    ) -> int:
        """
        从 CSV 文件设置编辑表格数据
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            file_path: CSV 文件路径
        
        Returns:
            0 表示成功
        """
        result = model.DatabaseTables.SetTableForEditingCSVFile(
            table_key,
            file_path
        )
        
        return com_ret(result)
    
    @staticmethod
    def set_table_for_editing_csv_string(
        model,
        table_key: str,
        csv_string: str
    ) -> int:
        """
        从 CSV 字符串设置编辑表格数据
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            csv_string: CSV 格式字符串
        
        Returns:
            0 表示成功
        """
        result = model.DatabaseTables.SetTableForEditingCSVString(
            table_key,
            csv_string
        )
        
        return com_ret(result)
    
    # ==================== 获取显示选项 ====================
    
    @staticmethod
    def get_load_patterns_selected(model) -> Tuple[List[str], int]:
        """
        获取当前选中显示的荷载模式
        
        Args:
            model: SapModel 对象
        
        Returns:
            (load_patterns, ret) 元组
        """
        result = model.DatabaseTables.GetLoadPatternsSelectedForDisplay(0, [])
        
        ret = com_ret(result)
        if ret == 0:
            return list(com_data(result, index=1, default=[]) or []), ret
        return [], -1
    
    @staticmethod
    def get_load_cases_selected(model) -> Tuple[List[str], int]:
        """
        获取当前选中显示的荷载工况
        
        Args:
            model: SapModel 对象
        
        Returns:
            (load_cases, ret) 元组
        """
        result = model.DatabaseTables.GetLoadCasesSelectedForDisplay(0, [])
        
        ret = com_ret(result)
        if ret == 0:
            return list(com_data(result, index=1, default=[]) or []), ret
        return [], -1
    
    @staticmethod
    def get_load_combinations_selected(model) -> Tuple[List[str], int]:
        """
        获取当前选中显示的荷载组合
        
        Args:
            model: SapModel 对象
        
        Returns:
            (load_combos, ret) 元组
        """
        result = model.DatabaseTables.GetLoadCombinationsSelectedForDisplay(0, [])
        
        ret = com_ret(result)
        if ret == 0:
            return list(com_data(result, index=1, default=[]) or []), ret
        return [], -1
    
    # ==================== Named Sets 方法 ====================
    
    @staticmethod
    def get_section_cuts_selected(model) -> Tuple[List[str], int]:
        """
        获取当前选中显示的截面切割
        
        Args:
            model: SapModel 对象
        
        Returns:
            (section_cuts, ret) 元组
        """
        result = model.DatabaseTables.GetSectionCutsSelectedForDisplay(0, [])
        
        ret = com_ret(result)
        if ret == 0:
            return list(com_data(result, index=1, default=[]) or []), ret
        return [], -1
    
    @staticmethod
    def set_section_cuts_selected(
        model,
        section_cuts: List[str],
        selected: bool = True
    ) -> int:
        """
        设置显示的截面切割
        
        Args:
            model: SapModel 对象
            section_cuts: 截面切割名称列表
            selected: True=选中, False=取消选中
        
        Returns:
            0 表示成功
        """
        result = model.DatabaseTables.SetSectionCutsSelectedForDisplay(
            len(section_cuts),
            section_cuts,
            selected
        )
        return com_ret(result)
    
    @staticmethod
    def get_generalized_displacements_selected(model) -> Tuple[List[str], int]:
        """
        获取当前选中显示的广义位移
        
        Args:
            model: SapModel 对象
        
        Returns:
            (generalized_displacements, ret) 元组
        """
        result = model.DatabaseTables.GetGeneralizedDisplacementsSelectedForDisplay(0, [])
        
        ret = com_ret(result)
        if ret == 0:
            return list(com_data(result, index=1, default=[]) or []), ret
        return [], -1
    
    @staticmethod
    def set_generalized_displacements_selected(
        model,
        generalized_displacements: List[str],
        selected: bool = True
    ) -> int:
        """
        设置显示的广义位移
        
        Args:
            model: SapModel 对象
            generalized_displacements: 广义位移名称列表
            selected: True=选中, False=取消选中
        
        Returns:
            0 表示成功
        """
        result = model.DatabaseTables.SetGeneralizedDisplacementsSelectedForDisplay(
            len(generalized_displacements),
            generalized_displacements,
            selected
        )
        return com_ret(result)

    
    @staticmethod
    def get_pushover_named_sets_selected(model) -> Tuple[List[str], int]:
        """
        获取当前选中显示的 Pushover 命名集
        
        Args:
            model: SapModel 对象
        
        Returns:
            (named_sets, ret) 元组
        """
        result = model.DatabaseTables.GetPushoverNamedSetsSelectedForDisplay(0, [])
        
        ret = com_ret(result)
        if ret == 0:
            return list(com_data(result, index=1, default=[]) or []), ret
        return [], -1
    
    @staticmethod
    def set_pushover_named_sets_selected(
        model,
        named_sets: List[str],
        selected: bool = True
    ) -> int:
        """
        设置显示的 Pushover 命名集
        
        Args:
            model: SapModel 对象
            named_sets: 命名集名称列表
            selected: True=选中, False=取消选中
        
        Returns:
            0 表示成功
        """
        result = model.DatabaseTables.SetPushoverNamedSetsSelectedForDisplay(
            len(named_sets),
            named_sets,
            selected
        )
        return com_ret(result)
    
    @staticmethod
    def get_joint_response_spectra_named_sets_selected(model) -> Tuple[List[str], int]:
        """
        获取当前选中显示的节点反应谱命名集
        
        Args:
            model: SapModel 对象
        
        Returns:
            (named_sets, ret) 元组
        """
        result = model.DatabaseTables.GetJointResponseSpectraNamedSetsSelectedForDisplay(0, [])
        
        ret = com_ret(result)
        if ret == 0:
            return list(com_data(result, index=1, default=[]) or []), ret
        return [], -1
    
    @staticmethod
    def set_joint_response_spectra_named_sets_selected(
        model,
        named_sets: List[str],
        selected: bool = True
    ) -> int:
        """
        设置显示的节点反应谱命名集
        
        Args:
            model: SapModel 对象
            named_sets: 命名集名称列表
            selected: True=选中, False=取消选中
        
        Returns:
            0 表示成功
        """
        result = model.DatabaseTables.SetJointResponseSpectraNamedSetsSelectedForDisplay(
            len(named_sets),
            named_sets,
            selected
        )
        return com_ret(result)
    
    @staticmethod
    def get_plot_function_traces_named_sets_selected(model) -> Tuple[List[str], int]:
        """
        获取当前选中显示的绘图函数轨迹命名集
        
        Args:
            model: SapModel 对象
        
        Returns:
            (named_sets, ret) 元组
        """
        result = model.DatabaseTables.GetPlotFunctionTracesNamedSetsSelectedForDisplay(0, [])
        
        ret = com_ret(result)
        if ret == 0:
            return list(com_data(result, index=1, default=[]) or []), ret
        return [], -1
    
    @staticmethod
    def set_plot_function_traces_named_sets_selected(
        model,
        named_sets: List[str],
        selected: bool = True
    ) -> int:
        """
        设置显示的绘图函数轨迹命名集
        
        Args:
            model: SapModel 对象
            named_sets: 命名集名称列表
            selected: True=选中, False=取消选中
        
        Returns:
            0 表示成功
        """
        result = model.DatabaseTables.SetPlotFunctionTracesNamedSetsSelectedForDisplay(
            len(named_sets),
            named_sets,
            selected
        )
        return com_ret(result)
    
    @staticmethod
    def get_element_virtual_work_named_sets_selected(model) -> Tuple[List[str], int]:
        """
        获取当前选中显示的单元虚功命名集
        
        Args:
            model: SapModel 对象
        
        Returns:
            (named_sets, ret) 元组
        """
        result = model.DatabaseTables.GetElementVirtualWorkNamedSetsSelectedForDisplay(0, [])
        
        ret = com_ret(result)
        if ret == 0:
            return list(com_data(result, index=1, default=[]) or []), ret
        return [], -1
    
    @staticmethod
    def set_element_virtual_work_named_sets_selected(
        model,
        named_sets: List[str],
        selected: bool = True
    ) -> int:
        """
        设置显示的单元虚功命名集
        
        Args:
            model: SapModel 对象
            named_sets: 命名集名称列表
            selected: True=选中, False=取消选中
        
        Returns:
            0 表示成功
        """
        result = model.DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay(
            len(named_sets),
            named_sets,
            selected
        )
        return com_ret(result)
    
    # ==================== 输出选项 ====================
    
    @staticmethod
    def get_table_output_options(model) -> Tuple[Dict[str, Any], int]:
        """
        获取表格输出选项
        
        Args:
            model: SapModel 对象
        
        Returns:
            (options_dict, ret) 元组
            options_dict 包含:
                - joints: 节点输出选项 (0=All, 1=Selected, 2=None)
                - frames: 杆件输出选项
                - cables: 索输出选项
                - tendons: 预应力筋输出选项
                - areas: 面单元输出选项
                - solids: 实体单元输出选项
                - links: 连接单元输出选项
        """
        # API: GetTableOutputOptionsForDisplay(Joints, Frames, Cables, Tendons, Areas, Solids, Links)
        result = model.DatabaseTables.GetTableOutputOptionsForDisplay(
            0, 0, 0, 0, 0, 0, 0
        )
        
        ret = com_ret(result)
        if ret == 0:
            return {
                "joints": com_data(result, index=0),
                "frames": com_data(result, index=1),
                "cables": com_data(result, index=2),
                "tendons": com_data(result, index=3),
                "areas": com_data(result, index=4),
                "solids": com_data(result, index=5),
                "links": com_data(result, index=6)
            }, ret
        return {}, -1
    
    @staticmethod
    def set_table_output_options(
        model,
        joints: int = 0,
        frames: int = 0,
        cables: int = 0,
        tendons: int = 0,
        areas: int = 0,
        solids: int = 0,
        links: int = 0
    ) -> int:
        """
        设置表格输出选项
        
        Args:
            model: SapModel 对象
            joints: 节点输出选项 (0=All, 1=Selected, 2=None)
            frames: 杆件输出选项
            cables: 索输出选项
            tendons: 预应力筋输出选项
            areas: 面单元输出选项
            solids: 实体单元输出选项
            links: 连接单元输出选项
        
        Returns:
            0 表示成功
        """
        result = model.DatabaseTables.SetTableOutputOptionsForDisplay(
            joints, frames, cables, tendons, areas, solids, links
        )
        
        return com_ret(result)
    
    # ==================== 工具方法 ====================
    
    @staticmethod
    def get_obsolete_table_keys(model) -> Tuple[Dict[str, str], int]:
        """
        获取废弃表格键名映射
        
        返回旧表格键名到新表格键名的映射。
        
        Args:
            model: SapModel 对象
        
        Returns:
            (mapping_dict, ret) 元组
            mapping_dict: {旧键名: 新键名}
        """
        # API: GetObsoleteTableKeyList(NumberItems, OldKey[], NewKey[])
        result = model.DatabaseTables.GetObsoleteTableKeyList(0, [], [])
        
        ret = com_ret(result)
        if ret != 0:
            return {}, -1
        
        num_items = com_data(result, index=0, default=0)
        old_keys = list(com_data(result, index=1, default=[]) or [])
        new_keys = list(com_data(result, index=2, default=[]) or [])
        
        mapping = {}
        for i in range(num_items):
            if i < len(old_keys) and i < len(new_keys):
                mapping[old_keys[i]] = new_keys[i]
        return mapping, ret
    
    @staticmethod
    def find_tables(model, keyword: str, include_empty: bool = False) -> List[TableInfo]:
        """
        搜索表格 (便捷方法)
        
        根据关键字搜索表格名称。
        
        Args:
            model: SapModel 对象
            keyword: 搜索关键字 (不区分大小写)
            include_empty: 是否包含空表格
        
        Returns:
            匹配的 TableInfo 列表
        
        Example:
            # 搜索所有包含 "Frame" 的表格
            tables = DatabaseTables.find_tables(model, "Frame")
            for t in tables:
                print(t.table_key)
        """
        if include_empty:
            all_tables = DatabaseTables.get_all_tables(model)
        else:
            all_tables = DatabaseTables.get_available_tables(model)
        
        keyword_lower = keyword.lower()
        return [t for t in all_tables 
                if keyword_lower in t.table_key.lower() or keyword_lower in t.table_name.lower()]
    
    @staticmethod
    def export_to_csv(
        model,
        table_key: str,
        file_path: str,
        for_editing: bool = False
    ) -> int:
        """
        导出表格到 CSV 文件 (便捷方法)
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            file_path: CSV 文件路径
            for_editing: True=导出可编辑格式, False=导出显示格式
        
        Returns:
            0 表示成功
        
        Example:
            DatabaseTables.export_to_csv(model, "Joint Coordinates", "joints.csv")
        """
        if for_editing:
            return DatabaseTables.get_table_for_editing_csv_file(model, table_key, file_path)
        else:
            return DatabaseTables.get_table_for_display_csv_file(model, table_key, file_path)
    
    @staticmethod
    def import_from_csv(
        model,
        table_key: str,
        file_path: str,
        apply_immediately: bool = True
    ) -> ApplyResult:
        """
        从 CSV 文件导入表格数据 (便捷方法)
        
        Args:
            model: SapModel 对象
            table_key: 表格键名
            file_path: CSV 文件路径
            apply_immediately: 是否立即应用更改
        
        Returns:
            ApplyResult 对象
        
        Example:
            result = DatabaseTables.import_from_csv(model, "Joint Coordinates", "joints.csv")
            if not result.success:
                print(result.import_log)
        """
        ret = DatabaseTables.set_table_for_editing_csv_file(model, table_key, file_path)
        if ret != 0:
            return ApplyResult(success=False, import_log="设置 CSV 文件失败")
        
        if apply_immediately:
            return DatabaseTables.apply_edited_tables(model)
        else:
            return ApplyResult(success=True, import_log="数据已加载，请调用 apply_edited_tables 应用更改")
