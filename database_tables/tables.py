# -*- coding: utf-8 -*-
"""
tables.py - Core classes for interactive table editing

Wraps SAP2000 `DatabaseTables` interface.

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
    """Table import type"""
    NOT_IMPORTABLE = 0          # Not importable
    IMPORTABLE = 1              # Importable
    IMPORTABLE_NOT_INTERACTIVE = 2  # Importable but not interactive


class TableExportFormat(IntEnum):
    """Table export format"""
    ARRAY = 1       # Array format
    CSV_FILE = 2    # CSV file
    CSV_STRING = 3  # CSV string
    XML_STRING = 4  # XML string


@dataclass
class TableInfo:
    """
    Table info
    
    Attributes:
        table_key: table key
        table_name: Table display name
        import_type: Import type (`0` not importable, `1` importable, `2` importable but not interactive)
        is_empty: whether the table is empty
    """
    table_key: str
    table_name: str = ""
    import_type: int = 0
    is_empty: bool = True
    
    @property
    def is_importable(self) -> bool:
        """Whether importable."""
        return self.import_type in (1, 2)


@dataclass
class TableField:
    """
    Table field info
    
    Attributes:
        field_key: field key
        field_name: field display name
        description: field description
        units: unit string
        is_importable: Whether importable
    """
    field_key: str
    field_name: str = ""
    description: str = ""
    units: str = ""
    is_importable: bool = True


@dataclass
class TableData:
    """
    Table data
    
    Attributes:
        table_key: table key
        table_version: table version
        field_keys: field key list
        num_records: record count
        data: Data list (row-flattened 1D list)
    """
    table_key: str = ""
    table_version: int = 0
    field_keys: List[str] = field(default_factory=list)
    num_records: int = 0
    data: List[str] = field(default_factory=list)
    
    @property
    def num_fields(self) -> int:
        """Number of fields"""
        return len(self.field_keys)
    
    def get_row(self, row_index: int) -> List[str]:
        """
        Get data for a specific row
        
        Args:
            row_index: row index (0-based)
        
        Returns:
            Data list for that row
        """
        if row_index < 0 or row_index >= self.num_records:
            return []
        start = row_index * self.num_fields
        end = start + self.num_fields
        return self.data[start:end]
    
    def set_row(self, row_index: int, row_data: List[str]) -> bool:
        """
        Set data for a specific row
        
        Args:
            row_index: row index (0-based)
            row_data: Row data list
        
        Returns:
            whether setting succeeds
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
        Add one row
        
        Args:
            row_data: Row data list
        
        Returns:
            whether adding succeeds
        """
        if len(row_data) != self.num_fields:
            return False
        self.data.extend([str(v) for v in row_data])
        self.num_records += 1
        return True
    
    def delete_row(self, row_index: int) -> bool:
        """
        Delete a specific row
        
        Args:
            row_index: row index (0-based)
        
        Returns:
            whether deletion succeeds
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
        Get a specific cell value
        
        Args:
            row_index: row index (0-based)
            field_name: field name
        
        Returns:
            Cell value, or `None` if not found
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
        Set a specific cell value
        
        Args:
            row_index: row index (0-based)
            field_name: field name
            value: new value
        
        Returns:
            whether setting succeeds
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
        Get all values in a specific column
        
        Args:
            field_name: field name
        
        Returns:
            value list for that column
        """
        if field_name not in self.field_keys:
            return []
        col_index = self.field_keys.index(field_name)
        return [self.data[i * self.num_fields + col_index] 
                for i in range(self.num_records)]
    
    def find_rows(self, field_name: str, value: str) -> List[int]:
        """
        Find row indices by field value match
        
        Args:
            field_name: field name
            value: value to match
        
        Returns:
            List of matching row indices
        """
        result = []
        for i in range(self.num_records):
            if self.get_value(i, field_name) == value:
                result.append(i)
        return result
    
    def to_dict_list(self) -> List[Dict[str, str]]:
        """
        Convert to list-of-dicts format
        
        Returns:
            list of dicts (one per row)
        """
        result = []
        for i in range(self.num_records):
            row_data = self.get_row(i)
            row_dict = dict(zip(self.field_keys, row_data))
            result.append(row_dict)
        return result
    
    def from_dict_list(self, dict_list: List[Dict[str, str]]) -> None:
        """
        Import data from list of dicts
        
        Args:
            dict_list: list of dictionaries
        """
        self.data = []
        self.num_records = 0
        for row_dict in dict_list:
            row_data = [row_dict.get(key, "") for key in self.field_keys]
            self.add_row(row_data)
    
    def to_dataframe(self):
        """
        Convert to pandas DataFrame
        
        Returns:
            pandas.DataFrame object
        
        Raises:
            ImportError: if pandas is not installed
        """
        try:
            import pandas as pd
            return pd.DataFrame(self.to_dict_list())
        except ImportError:
            raise ImportError("pandas is required: pip install pandas")
    
    def from_dataframe(self, df) -> None:
        """
        Import from pandas DataFrame
        
        Args:
            df: pandas.DataFrame object
        """
        self.from_dict_list(df.to_dict('records'))
    
    def copy(self) -> 'TableData':
        """Create a copy"""
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
    Apply result
    
    Attributes:
        success: whether successful
        num_fatal_errors: fatal error count
        num_error_msgs: error message count
        num_warn_msgs: warning message count
        num_info_msgs: info message count
        import_log: import log
    """
    success: bool = False
    num_fatal_errors: int = 0
    num_error_msgs: int = 0
    num_warn_msgs: int = 0
    num_info_msgs: int = 0
    import_log: str = ""


class DatabaseTables:
    """
    Database table manager
    
    Provides static methods for interactive table editing.
    
    Typical workflow:
        1. get_available_tables() - Get available tables
        2. get_table_for_editing() - Get table data
        3. Modify the `TableData` object
        4. set_table_for_editing() - Set modified data
        5. apply_edited_tables() - Apply changes to the model
    
    Example:
        # Read and modify joint coordinates
        data = DatabaseTables.get_table_for_editing(model, "Joint Coordinates")
        data.set_value(0, "XorR", "100")  # Modify X coordinate of the first joint
        DatabaseTables.set_table_for_editing(model, data)
        result = DatabaseTables.apply_edited_tables(model)
        if not result.success:
            print(result.import_log)
    """
    
    # ==================== Table query ====================
    
    @staticmethod
    def get_available_tables(model) -> List[TableInfo]:
        """
        Get available table list (tables with data)
        
        Args:
            model: SapModel object
        
        Returns:
            list of `TableInfo` objects
        
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
        Get available table-key list (compact helper)
        
        Args:
            model: SapModel object
        
        Returns:
            List of table keys
        """
        tables = DatabaseTables.get_available_tables(model)
        return [t.table_key for t in tables]
    
    @staticmethod
    def get_all_tables(model) -> List[TableInfo]:
        """
        Get all tables (including empty tables)
        
        Args:
            model: SapModel object
        
        Returns:
            list of `TableInfo` objects
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
                is_empty=True  # `GetAllTables` does not return `IsEmpty`
            ))
        return tables
    
    @staticmethod
    def get_all_table_keys(model) -> List[str]:
        """
        Get all table keys (compact helper)
        
        Args:
            model: SapModel object
        
        Returns:
            List of table keys
        """
        tables = DatabaseTables.get_all_tables(model)
        return [t.table_key for t in tables]
    
    @staticmethod
    def get_fields_in_table(model, table_key: str, table_version: int = 0) -> List[TableField]:
        """
        Get all fields in a table
        
        Args:
            model: SapModel object
            table_key: table key
            table_version: Table version (default `0`)
        
        Returns:
            list of `TableField` objects
        
        Example:
            fields = DatabaseTables.get_fields_in_table(model, "Joint Coordinates")
            for f in fields:
                print(f"{f.field_key}: {f.description} ({f.units})")
        """
        # API: GetAllFieldsInTable(TableKey, TableVersion, NumberFields, 
        #      FieldKey[], FieldName[], Description[], UnitsString[], IsImportable[])
        # Returns: [TableVersion, NumberFields, FieldKey[], FieldName[], Description[], UnitsString[], IsImportable[], ret]
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
        Get all fields in a table (raw format)
        
        Args:
            model: SapModel object
            table_key: table key
            table_version: table version
        
        Returns:
            (field_keys, field_names, descriptions, units, is_importable) tuple
        """
        fields = DatabaseTables.get_fields_in_table(model, table_key, table_version)
        return (
            [f.field_key for f in fields],
            [f.field_name for f in fields],
            [f.description for f in fields],
            [f.units for f in fields],
            [f.is_importable for f in fields]
        )

    
    # ==================== Read tables ====================
    
    @staticmethod
    def get_table_for_display(
        model,
        table_key: str,
        field_keys: List[str] = None,
        group_name: str = ""
    ) -> Optional[TableData]:
        """
        Get display table data (array format).
        
        Args:
            model: SapModel object
            table_key: table key
            field_keys: Field keys to retrieve. `None` or `[""]` means all fields.
            group_name: Group name. Empty string or `"All"` means all objects.
        
        Returns:
            `TableData` object, or `None` on failure
        
        Example:
            data = DatabaseTables.get_table_for_display(
                model, 
                "Frame Section Assignments"
            )
            if data:
                for row in data.to_dict_list():
                    print(row)
        """
        # If no field list is provided, use [""] to request all fields.
        if field_keys is None or len(field_keys) == 0:
            field_keys = [""]
        
        # API: GetTableForDisplayArray(TableKey, FieldKeyList[], GroupName,
        #      TableVersion, FieldKeysIncluded[], NumberRecords, TableData[])
        # Return layout: [input_field_keys, TableVersion, FieldKeysIncluded, NumberRecords, TableData, ret]
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
        Get editable table data (array format).
        
        Similar to `get_table_for_display`, but returns editable data.
        
        Args:
            model: SapModel object
            table_key: table key
            group_name: group name (this parameter is currently inactive)
        
        Returns:
            `TableData` object, or `None` on failure
        
        Example:
            data = DatabaseTables.get_table_for_editing(model, "Joint Coordinates")
            data.set_value(0, "XorR", "100")
            DatabaseTables.set_table_for_editing(model, data)
            DatabaseTables.apply_edited_tables(model)
        """
        # API: GetTableForEditingArray(TableKey, GroupName,
        #      TableVersion, FieldKeysIncluded[], NumberRecords, TableData[])
        # Returns: [TableVersion, FieldKeysIncluded[], NumberRecords, TableData[], ret]
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

    
    # ==================== Edit tables ====================
    
    @staticmethod
    def set_table_for_editing(
        model,
        table_data: TableData
    ) -> int:
        """
        Set editable table data (recommended).
        
        Args:
            model: SapModel object
            table_data: `TableData` object
        
        Returns:
            `0` on success, nonzero on failure
        
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
        Set editable table data (raw-argument form).
        
        Args:
            model: SapModel object
            table_key: table key
            table_version: table version
            field_keys: field key list
            num_records: record count
            data: data list
        
        Returns:
            `0` on success
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
        Apply edited tables
        
        Apply all pending changes set by `set_table_for_editing` to the model.
        
        Args:
            model: SapModel object
            fill_import_log: Whether to populate the import log
        
        Returns:
            `ApplyResult` object
        
        Example:
            DatabaseTables.set_table_for_editing(model, data)
            result = DatabaseTables.apply_edited_tables(model)
            if not result.success:
                print(f"Error: {result.num_fatal_errors} fatal errors")
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
        Cancel table editing
        
        Cancel all unapplied table edits.
        
        Args:
            model: SapModel object
        
        Returns:
            `0` on success
        """
        result = model.DatabaseTables.CancelTableEditing()
        return com_ret(result)
    
    # ==================== Display options ====================
    
    @staticmethod
    def set_load_patterns_selected(
        model,
        load_patterns: List[str],
        selected: bool = True
    ) -> int:
        """
        Set displayed load patterns
        
        Args:
            model: SapModel object
            load_patterns: load-pattern name list
            selected: `True` selects, `False` deselects
        
        Returns:
            `0` on success
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
        Set displayed load cases
        
        Args:
            model: SapModel object
            load_cases: load-case name list
            selected: `True` selects, `False` deselects
        
        Returns:
            `0` on success
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
        Set displayed load combinations
        
        Args:
            model: SapModel object
            load_combos: load-combination name list
            selected: `True` selects, `False` deselects
        
        Returns:
            `0` on success
        """
        result = model.DatabaseTables.SetLoadCombinationsSelectedForDisplay(
            len(load_combos),
            load_combos,
            selected
        )
        return com_ret(result)
    
    # ==================== Export ====================
    
    @staticmethod
    def show_tables_in_excel(
        model,
        table_keys: List[str],
        field_keys_list: List[List[str]] = None,
        group_name: str = ""
    ) -> int:
        """
        Show tables in Excel
        
        Args:
            model: SapModel object
            table_keys: List of table keys
            field_keys_list: Field-key list for each table (optional)
            group_name: group name (optional)
        
        Returns:
            `0` on success
        
        Example:
            DatabaseTables.show_tables_in_excel(
                model,
                ["Frame Section Assignments", "Joint Coordinates"]
            )
        """
        num_tables = len(table_keys)
        
        if field_keys_list is None:
            field_keys_list = [[] for _ in table_keys]
        
        # field count per table
        num_fields_per_table = [len(fields) for fields in field_keys_list]
        
        # flatten field list
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
    
    # ==================== Convenience helpers ====================
    
    @staticmethod
    def read_table(
        model,
        table_key: str,
        as_dataframe: bool = False
    ):
        """
        Read table data (convenience helper)
        
        Args:
            model: SapModel object
            table_key: table key
            as_dataframe: Whether to return a pandas DataFrame
        
        Returns:
            `TableData` object or pandas DataFrame
        
        Example:
            # Returns TableData
            data = DatabaseTables.read_table(model, "Joint Coordinates")
            
            # Returns DataFrame
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
        Edit table data (convenience helper)
        
        Args:
            model: SapModel object
            table_key: table key
            modifications: Modification mapping `{row_index: {field_name: new_value}}`
        
        Returns:
            `ApplyResult` object
        
        Example:
            # Modify the X coordinate in row 0 and Y coordinate in row 1
            result = DatabaseTables.edit_table(model, "Joint Coordinates", {
                0: {"XorR": "100"},
                1: {"Y": "200"}
            })
        """
        data = DatabaseTables.get_table_for_editing(model, table_key)
        if not data:
            return ApplyResult(success=False, import_log="Failed to retrieve table data")
        
        for row_idx, field_values in modifications.items():
            for field_name, value in field_values.items():
                data.set_value(row_idx, field_name, value)
        
        ret = DatabaseTables.set_table_for_editing(model, data)
        if ret != 0:
            return ApplyResult(success=False, import_log="Failed to set table data")
        
        return DatabaseTables.apply_edited_tables(model)
    
    @staticmethod
    def import_from_dataframe(
        model,
        table_key: str,
        df
    ) -> ApplyResult:
        """
        Import from pandas DataFrame
        
        Args:
            model: SapModel object
            table_key: table key
            df: pandas DataFrame
        
        Returns:
            `ApplyResult` object
        
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
            return ApplyResult(success=False, import_log="Failed to retrieve table data")
        
        data.from_dataframe(df)
        
        ret = DatabaseTables.set_table_for_editing(model, data)
        if ret != 0:
            return ApplyResult(success=False, import_log="Failed to set table data")
        
        return DatabaseTables.apply_edited_tables(model)

    # ==================== CSV helpers ====================
    
    @staticmethod
    def get_table_for_display_csv_file(
        model,
        table_key: str,
        file_path: str,
        field_keys: List[str] = None,
        group_name: str = ""
    ) -> int:
        """
        Get display table data and save it as a CSV file
        
        Args:
            model: SapModel object
            table_key: table key
            file_path: CSV file path
            field_keys: Field keys to retrieve. `None` means all fields.
            group_name: Group name. Empty string means all objects.
        
        Returns:
            `0` on success
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
        Get display table data as a CSV string
        
        Args:
            model: SapModel object
            table_key: table key
            field_keys: Field keys to retrieve. `None` means all fields.
            group_name: Group name. Empty string means all objects.
        
        Returns:
            (csv_string, ret) tuple
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
        Get editable table data and save it as a CSV file
        
        Args:
            model: SapModel object
            table_key: table key
            file_path: CSV file path
            field_keys: Field keys to retrieve. `None` means all fields.
        
        Returns:
            `0` on success
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
        Get editable table data as a CSV string
        
        Args:
            model: SapModel object
            table_key: table key
            field_keys: Field keys to retrieve. `None` means all fields.
        
        Returns:
            (csv_string, ret) tuple
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
        Set editable table data from a CSV file
        
        Args:
            model: SapModel object
            table_key: table key
            file_path: CSV file path
        
        Returns:
            `0` on success
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
        Set editable table data from a CSV string
        
        Args:
            model: SapModel object
            table_key: table key
            csv_string: CSV formatted string
        
        Returns:
            `0` on success
        """
        result = model.DatabaseTables.SetTableForEditingCSVString(
            table_key,
            csv_string
        )
        
        return com_ret(result)
    
    # ==================== Get display options ====================
    
    @staticmethod
    def get_load_patterns_selected(model) -> Tuple[List[str], int]:
        """
        Get currently selected load patterns.
        
        Args:
            model: SapModel object
        
        Returns:
            (load_patterns, ret) tuple
        """
        result = model.DatabaseTables.GetLoadPatternsSelectedForDisplay(0, [])
        
        ret = com_ret(result)
        if ret == 0:
            return list(com_data(result, index=1, default=[]) or []), ret
        return [], -1
    
    @staticmethod
    def get_load_cases_selected(model) -> Tuple[List[str], int]:
        """
        Get currently selected load cases.
        
        Args:
            model: SapModel object
        
        Returns:
            (load_cases, ret) tuple
        """
        result = model.DatabaseTables.GetLoadCasesSelectedForDisplay(0, [])
        
        ret = com_ret(result)
        if ret == 0:
            return list(com_data(result, index=1, default=[]) or []), ret
        return [], -1
    
    @staticmethod
    def get_load_combinations_selected(model) -> Tuple[List[str], int]:
        """
        Get currently selected load combinations.
        
        Args:
            model: SapModel object
        
        Returns:
            (load_combos, ret) tuple
        """
        result = model.DatabaseTables.GetLoadCombinationsSelectedForDisplay(0, [])
        
        ret = com_ret(result)
        if ret == 0:
            return list(com_data(result, index=1, default=[]) or []), ret
        return [], -1
    
    # ==================== Named sets ====================
    
    @staticmethod
    def get_section_cuts_selected(model) -> Tuple[List[str], int]:
        """
        Get currently selected section cuts.
        
        Args:
            model: SapModel object
        
        Returns:
            (section_cuts, ret) tuple
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
        Set displayed section cuts.
        
        Args:
            model: SapModel object
            section_cuts: section-cut name list
            selected: `True` selects, `False` deselects
        
        Returns:
            `0` on success
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
        Get currently selected generalized displacements.
        
        Args:
            model: SapModel object
        
        Returns:
            (generalized_displacements, ret) tuple
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
        Set displayed generalized displacements.
        
        Args:
            model: SapModel object
            generalized_displacements: generalized-displacement name list
            selected: `True` selects, `False` deselects
        
        Returns:
            `0` on success
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
        Get currently selected pushover named sets.
        
        Args:
            model: SapModel object
        
        Returns:
            (named_sets, ret) tuple
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
        Set displayed pushover named sets.
        
        Args:
            model: SapModel object
            named_sets: named-set name list
            selected: `True` selects, `False` deselects
        
        Returns:
            `0` on success
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
        Get currently selected joint-response-spectrum named sets.
        
        Args:
            model: SapModel object
        
        Returns:
            (named_sets, ret) tuple
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
        Set displayed joint-response-spectrum named sets.
        
        Args:
            model: SapModel object
            named_sets: named-set name list
            selected: `True` selects, `False` deselects
        
        Returns:
            `0` on success
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
        Get currently selected plot-function-trace named sets.
        
        Args:
            model: SapModel object
        
        Returns:
            (named_sets, ret) tuple
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
        Set displayed plot-function-trace named sets.
        
        Args:
            model: SapModel object
            named_sets: named-set name list
            selected: `True` selects, `False` deselects
        
        Returns:
            `0` on success
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
        Get currently selected element-virtual-work named sets.
        
        Args:
            model: SapModel object
        
        Returns:
            (named_sets, ret) tuple
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
        Set displayedelement virtual-work named sets
        
        Args:
            model: SapModel object
            named_sets: named-set name list
            selected: `True` selects, `False` deselects
        
        Returns:
            `0` on success
        """
        result = model.DatabaseTables.SetElementVirtualWorkNamedSetsSelectedForDisplay(
            len(named_sets),
            named_sets,
            selected
        )
        return com_ret(result)
    
    # ==================== Output options ====================
    
    @staticmethod
    def get_table_output_options(model) -> Tuple[Dict[str, Any], int]:
        """
        Get table output options.
        
        Args:
            model: SapModel object
        
        Returns:
            (options_dict, ret) tuple
            options_dict includes:
                - joints: joint output option (0=All, 1=Selected, 2=None)
                - frames: frame output option
                - cables: cable output option
                - tendons: tendon output option
                - areas: area output option
                - solids: solid output option
                - links: link output option
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
        Set table output options.
        
        Args:
            model: SapModel object
            joints: joint output option (0=All, 1=Selected, 2=None)
            frames: frame output option
            cables: cable output option
            tendons: tendon output option
            areas: area output option
            solids: solid output option
            links: link output option
        
        Returns:
            `0` on success
        """
        result = model.DatabaseTables.SetTableOutputOptionsForDisplay(
            joints, frames, cables, tendons, areas, solids, links
        )
        
        return com_ret(result)
    
    # ==================== Utility helpers ====================
    
    @staticmethod
    def get_obsolete_table_keys(model) -> Tuple[Dict[str, str], int]:
        """
        Get obsolete table-key mapping.
        
        Returns a mapping from obsolete keys to replacement keys.
        
        Args:
            model: SapModel object
        
        Returns:
            (mapping_dict, ret) tuple
            mapping_dict: `{old_key: new_key}`
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
        Find tables (Convenience helpers)
        
        Search table names by keyword.
        
        Args:
            model: SapModel object
            keyword: search keyword (case-insensitive)
            include_empty: whether to include empty tables
        
        Returns:
            List of matching `TableInfo` objects
        
        Example:
            # Search all tables containing "Frame"
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
        Export table to CSV file (convenience helper)
        
        Args:
            model: SapModel object
            table_key: table key
            file_path: CSV file path
            for_editing: `True` exports editing format, `False` exports display format
        
        Returns:
            `0` on success
        
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
        Import table data from a CSV file (convenience helper)
        
        Args:
            model: SapModel object
            table_key: table key
            file_path: CSV file path
            apply_immediately: whether to apply changes immediately
        
        Returns:
            `ApplyResult` object
        
        Example:
            result = DatabaseTables.import_from_csv(model, "Joint Coordinates", "joints.csv")
            if not result.success:
                print(result.import_log)
        """
        ret = DatabaseTables.set_table_for_editing_csv_file(model, table_key, file_path)
        if ret != 0:
            return ApplyResult(success=False, import_log="Failed to set CSV file")
        
        if apply_immediately:
            return DatabaseTables.apply_edited_tables(model)
        else:
            return ApplyResult(success=True, import_log="Data loaded. Call `apply_edited_tables` to apply changes.")
