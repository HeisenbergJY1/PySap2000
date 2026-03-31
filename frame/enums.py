# -*- coding: utf-8 -*-
"""
enums.py - Frame-related enums.

Contains enums used by the SAP2000 `FrameObj` API.

Note: Load-related enums have been moved to `loads/frame_load.py`.
"""

from enum import IntEnum


class FrameType(IntEnum):
    """Frame object type."""
    BEAM = 1      # Beam
    COLUMN = 2    # Column
    BRACE = 3     # Brace
    TRUSS = 4     # Truss
    OTHER = 5     # Other


class FrameSectionType(IntEnum):
    """
    Frame section type.

    Matches values returned by `PropFrame.GetTypeOAPI`.
    """
    I_SECTION = 1           # I section
    CHANNEL = 2             # Channel
    T_SECTION = 3           # T section
    ANGLE = 4               # Angle
    DOUBLE_ANGLE = 5        # Double angle
    BOX = 6                 # Box / square tube
    PIPE = 7                # Pipe
    RECTANGULAR = 8         # Rectangle
    CIRCLE = 9              # Circle
    GENERAL = 10            # General section
    DOUBLE_CHANNEL = 11     # Double channel
    AUTO = 12               # Auto-select
    SD = 13                 # Section Designer
    VARIABLE = 14           # Variable section
    JOIST = 15              # Joist
    BRIDGE = 16             # Bridge section
    COLD_C = 17             # Cold-formed C
    COLD_2C = 18            # Double cold-formed C
    COLD_Z = 19             # Cold-formed Z
    COLD_L = 20             # Cold-formed angle
    COLD_2L = 21            # Double cold-formed angle
    COLD_HAT = 22           # Cold-formed hat
    BUILTUP_I_COVERPLATE = 23  # Built-up I with cover plate
    PCC_GIRDER_I = 24       # Precast concrete I girder
    PCC_GIRDER_U = 25       # Precast concrete U girder
    BUILTUP_I_HYBRID = 26   # Hybrid built-up I
    BUILTUP_U_HYBRID = 27   # Hybrid built-up U
    PCC_GIRDER_SUPER_T = 41 # Precast concrete super-T girder
    COLD_BOX = 42           # Cold-formed box
    COLD_I = 43             # Cold-formed I
    COLD_PIPE = 44          # Cold-formed pipe
    COLD_T = 45             # Cold-formed T
    TRAPEZOIDAL = 46        # Trapezoidal


class FrameReleaseType(IntEnum):
    """Convenience enum for frame end-release presets."""
    BOTH_FIXED = 0    # Fixed at both ends
    I_END_HINGED = 1  # Hinged at the I-end
    J_END_HINGED = 2  # Hinged at the J-end
    BOTH_HINGED = 3   # Hinged at both ends


class ItemType(IntEnum):
    """
    `eItemType` enum.

    Used to define the scope of batch operations.
    """
    OBJECT = 0           # Single object
    GROUP = 1            # All objects in a group
    SELECTED_OBJECTS = 2 # All selected objects


# Human-readable names for section types
SECTION_TYPE_NAMES = {
    FrameSectionType.I_SECTION: "I section",
    FrameSectionType.CHANNEL: "Channel",
    FrameSectionType.T_SECTION: "T section",
    FrameSectionType.ANGLE: "Angle",
    FrameSectionType.DOUBLE_ANGLE: "Double angle",
    FrameSectionType.BOX: "Box / square tube",
    FrameSectionType.PIPE: "Pipe",
    FrameSectionType.RECTANGULAR: "Rectangle",
    FrameSectionType.CIRCLE: "Circle",
    FrameSectionType.GENERAL: "General section",
    FrameSectionType.DOUBLE_CHANNEL: "Double channel",
    FrameSectionType.AUTO: "Auto-select",
    FrameSectionType.SD: "Section Designer",
    FrameSectionType.VARIABLE: "Variable section",
}


# End-release presets: (I-end, J-end)
RELEASE_PRESETS = {
    FrameReleaseType.BOTH_FIXED: (
        (False, False, False, False, False, False),
        (False, False, False, False, False, False)
    ),
    FrameReleaseType.I_END_HINGED: (
        (False, False, False, False, True, True),
        (False, False, False, False, False, False)
    ),
    FrameReleaseType.J_END_HINGED: (
        (False, False, False, False, False, False),
        (False, False, False, False, True, True)
    ),
    FrameReleaseType.BOTH_HINGED: (
        (False, False, False, False, True, True),
        (False, False, False, False, True, True)
    ),
}
