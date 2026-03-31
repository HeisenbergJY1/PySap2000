# -*- coding: utf-8 -*-
"""
file.py - File helpers.

Thin wrappers around the SAP2000 File API.

SAP2000 API:
- File.New2DFrame - New 2D frame template
- File.New3DFrame - New 3D frame template
- File.NewBeam - New beam template
- File.NewBlank - New blank model
- File.NewSolidBlock - New solid block template
- File.NewWall - New wall template
- File.OpenFile - Open file
- File.Save - Save file
"""

from PySap2000.global_parameters.units import UnitSystem as Units


# =============================================================================
# Model creation
# =============================================================================

def new_blank(model, units: Units = Units.KN_M_C) -> int:
    """
    Create a blank model.
    
    Args:
        model: SapModel object
        units: Unit system
        
    Returns:
        `0` on success
        
    Example:
        new_blank(model, Units.KN_M_C)
    """
    return model.File.NewBlank(int(units))


def new_2d_frame(
    model,
    template_type: int,
    num_stories: int,
    story_height: float,
    num_bays: int,
    bay_width: float,
    restraint: bool = True,
    beam_section: str = "",
    column_section: str = "",
    brace_section: str = "",
    units: Units = Units.KN_M_C
) -> int:
    """
    Create a new 2D frame template model.

    Args:
        model: SapModel object
        template_type: Template type
            0 = portal frame
            1 = continuous beam
            2 = simply supported beam
            3 = cantilever beam
            4 = truss
        num_stories: Number of stories
        story_height: Story height
        num_bays: Number of bays
        bay_width: Bay width
        restraint: Whether to add supports
        beam_section: Beam section name
        column_section: Column section name
        brace_section: Brace section name
        units: Unit system

    Returns:
        `0` on success
    """
    return model.File.New2DFrame(
        template_type, num_stories, story_height, num_bays, bay_width,
        restraint, beam_section, column_section, brace_section, int(units)
    )


def new_3d_frame(
    model,
    template_type: int,
    num_stories: int,
    story_height: float,
    num_bays_x: int,
    bay_width_x: float,
    num_bays_y: int,
    bay_width_y: float,
    restraint: bool = True,
    beam_section: str = "",
    column_section: str = "",
    brace_section: str = "",
    units: Units = Units.KN_M_C
) -> int:
    """
    Create a new 3D frame template model.

    Args:
        model: SapModel object
        template_type: Template type
            0 = open frame
            1 = perimeter frame
            2 = braced frame
        num_stories: Number of stories
        story_height: Story height
        num_bays_x: Number of bays along X
        bay_width_x: Bay width along X
        num_bays_y: Number of bays along Y
        bay_width_y: Bay width along Y
        restraint: Whether to add supports
        beam_section: Beam section name
        column_section: Column section name
        brace_section: Brace section name
        units: Unit system

    Returns:
        `0` on success
    """
    return model.File.New3DFrame(
        template_type, num_stories, story_height,
        num_bays_x, bay_width_x, num_bays_y, bay_width_y,
        restraint, beam_section, column_section, brace_section, int(units)
    )


def new_beam(
    model,
    num_spans: int,
    span_length: float,
    restraint: bool = True,
    section: str = "",
    units: Units = Units.KN_M_C
) -> int:
    """
    Create a new beam template model.

    Args:
        model: SapModel object
        num_spans: Number of spans
        span_length: Span length
        restraint: Whether to add supports
        section: Section name
        units: Unit system

    Returns:
        `0` on success
    """
    return model.File.NewBeam(num_spans, span_length, restraint, section, int(units))


def new_solid_block(
    model,
    width_x: float,
    width_y: float,
    height: float,
    restraint: bool = True,
    units: Units = Units.KN_M_C
) -> int:
    """
    Create a new solid block template model.

    Args:
        model: SapModel object
        width_x: Width along X
        width_y: Width along Y
        height: Height
        restraint: Whether to add supports
        units: Unit system

    Returns:
        `0` on success
    """
    return model.File.NewSolidBlock(width_x, width_y, height, restraint, int(units))


def new_wall(
    model,
    num_x: int,
    num_z: int,
    width: float,
    height: float,
    restraint: bool = True,
    section: str = "",
    units: Units = Units.KN_M_C
) -> int:
    """
    Create a new wall template model.

    Args:
        model: SapModel object
        num_x: Number of divisions along X
        num_z: Number of divisions along Z
        width: Width
        height: Height
        restraint: Whether to add supports
        section: Section name
        units: Unit system

    Returns:
        `0` on success
    """
    return model.File.NewWall(num_x, num_z, width, height, restraint, section, int(units))


# =============================================================================
# File operations
# =============================================================================

def open_file(model, file_path: str) -> int:
    """
    Open a model file.
    
    Args:
        model: SapModel object
        file_path: File path
        
    Returns:
        `0` on success
        
    Example:
        open_file(model, r"C:\\Models\\example.sdb")
    """
    return model.File.OpenFile(file_path)


def save(model, file_path: str = "") -> int:
    """
    Save the current model.
    
    Args:
        model: SapModel object
        file_path: Target file path. Empty string saves to the current path.
        
    Returns:
        `0` on success
        
    Example:
        save(model)  # Save to the current path
        save(model, r"C:\\Models\\example.sdb")  # Save as
    """
    if file_path:
        return model.File.Save(file_path)
    else:
        return model.File.Save()
