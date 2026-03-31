# -*- coding: utf-8 -*-
"""
database_tables - SAP2000 interactive table editing.

Wraps the SAP2000 `DatabaseTables` interface for reading and editing model
data tables.

Main features:
- Get available table lists
- Read table data (Array / CSV / XML)
- Edit table data
- Export tables to Excel

Usage:
    from database_tables import DatabaseTables
    
    # Get all available tables
    tables = DatabaseTables.get_available_tables(model)
    
    # Read table data
    data = DatabaseTables.get_table_for_display(model, "Frame Section Assignments")
    
    # Edit table (method 1: standard workflow)
    data = DatabaseTables.get_table_for_editing(model, "Joint Coordinates")
    data.set_value(0, "XorR", "100")
    DatabaseTables.set_table_for_editing(model, data)
    result = DatabaseTables.apply_edited_tables(model)
    
    # Edit table (method 2: convenience helper)
    result = DatabaseTables.edit_table(model, "Joint Coordinates", {
        0: {"XorR": "100"}
    })

API categories:
    `DATABASE_TABLES_API_CATEGORIES` - for capability discovery
"""

from .tables import (
    # Main class
    DatabaseTables,
    
    # Dataclasses
    TableData,
    TableField,
    TableInfo,
    ApplyResult,
    
    # Enums
    TableExportFormat,
    TableImportType,
)

from .table_keys import (
    # Common table-key constants
    TABLE_KEYS,
    
    # Grouped table-key lists
    MODEL_DEFINITION_TABLES,
    ANALYSIS_RESULTS_TABLES,
    DESIGN_TABLES,
)


# ==================== API category index (for discoverability) ====================

DATABASE_TABLES_API_CATEGORIES = {
    "table_query": {
        "description": "Get available tables and field metadata",
        "functions": [
            "get_available_tables",      # Get available table list (with data)
            "get_available_table_keys",  # Get available table-key list
            "get_all_tables",            # Get all table list
            "get_all_table_keys",        # Get all table-key list
            "get_fields_in_table",       # Get all fields in a table
            "get_all_fields_in_table",   # Get all fields in raw form
            "find_tables",               # Find tables (convenience helper)
            "get_obsolete_table_keys",   # Get obsolete table-key mapping
        ]
    },
    "read_tables_array": {
        "description": "Read table data (Array format)",
        "functions": [
            "get_table_for_display",     # Get display-table data
            "get_table_for_editing",     # Get editable table data
            "read_table",                # Read table (convenience helper)
        ]
    },
    "read_tables_csv": {
        "description": "Read table data (CSV format)",
        "functions": [
            "get_table_for_display_csv_file",    # Get display table and save as CSV file
            "get_table_for_display_csv_string",  # Get display table as CSV string
            "get_table_for_editing_csv_file",    # Get editing table and save as CSV file
            "get_table_for_editing_csv_string",  # Get editing table as CSV string
            "export_to_csv",                     # Export table to CSV (convenience helper)
        ]
    },
    "edit_tables": {
        "description": "Edit and apply table data",
        "functions": [
            "set_table_for_editing",         # Set editable table data (TableData)
            "set_table_for_editing_array",   # Set editable table data (raw args)
            "set_table_for_editing_csv_file",    # Set editing data from CSV file
            "set_table_for_editing_csv_string",  # Set editing data from CSV string
            "apply_edited_tables",           # Apply edited tables
            "cancel_table_editing",          # Cancel table editing
            "edit_table",                    # Edit table (convenience helper)
            "import_from_dataframe",         # Import from DataFrame
            "import_from_csv",               # Import from CSV file (convenience helper)
        ]
    },
    "display_options_loads": {
        "description": "Set load display options",
        "functions": [
            "get_load_patterns_selected",    # Get selected load patterns
            "set_load_patterns_selected",    # Set displayed load patterns
            "get_load_cases_selected",       # Get selected load cases
            "set_load_cases_selected",       # Set displayed load cases
            "get_load_combinations_selected", # Get selected load combinations
            "set_load_combinations_selected", # Set displayed load combinations
        ]
    },
    "display_options_named_sets": {
        "description": "Set named-set display options",
        "functions": [
            "get_section_cuts_selected",                 # Get selected section cuts
            "set_section_cuts_selected",                 # Set displayed section cuts
            "get_generalized_displacements_selected",    # Get selected generalized displacements
            "set_generalized_displacements_selected",    # Set displayed generalized displacements
            "get_pushover_named_sets_selected",          # Get selected pushover named sets
            "set_pushover_named_sets_selected",          # Set displayed pushover named sets
            "get_joint_response_spectra_named_sets_selected",   # Get selected joint response spectra named sets
            "set_joint_response_spectra_named_sets_selected",   # Set displayed joint response spectra named sets
            "get_plot_function_traces_named_sets_selected",     # Get selected plot-function trace named sets
            "set_plot_function_traces_named_sets_selected",     # Set displayed plot-function trace named sets
            "get_element_virtual_work_named_sets_selected",     # Get selected element virtual-work named sets
            "set_element_virtual_work_named_sets_selected",     # Set displayed element virtual-work named sets
        ]
    },
    "output_options": {
        "description": "Set table output options",
        "functions": [
            "get_table_output_options",      # Get table output options
            "set_table_output_options",      # Set table output options
        ]
    },
    "export": {
        "description": "Export tables to external formats",
        "functions": [
            "show_tables_in_excel",          # Show tables in Excel
        ]
    },
}


__all__ = [
    # Main class
    'DatabaseTables',
    
    # Dataclasses
    'TableData',
    'TableField',
    'TableInfo',
    'ApplyResult',
    
    # Enums
    'TableExportFormat',
    'TableImportType',
    
    # Table keys
    'TABLE_KEYS',
    'MODEL_DEFINITION_TABLES',
    'ANALYSIS_RESULTS_TABLES',
    'DESIGN_TABLES',
    
    # API category index
    'DATABASE_TABLES_API_CATEGORIES',
]
