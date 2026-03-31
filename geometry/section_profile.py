# -*- coding: utf-8 -*-
"""
section_profile.py - Section profile generator

Generates 2D section profile points from section type and parameters.
Used for downstream 3D solid generation (extrusion, sweep, etc.).

Supported section types:
- Circle: Circular section
- Rect: Rectangular section
- I: I-section
- Pipe: Pipe section
- Box: Box section
- Channel: Channel section
- Tee: Tee section
- Angle: Angle section
"""

from dataclasses import dataclass
from typing import List, Tuple
import math


@dataclass
class SectionProfile:
    """Base section profile class"""
    
    def get_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """
        Get section profile points (2D local coordinates).
        
        Args:
            num_segments: Number of arc segments
            
        Returns:
            [(y, z), ...] List of coordinate points (`x` is along the element axis)
        """
        raise NotImplementedError


@dataclass
class CircleProfile(SectionProfile):
    """Circular section"""
    diameter: float  # Diameter (m)
    
    def get_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """Generate circular profile points"""
        radius = self.diameter / 2
        points = []
        for i in range(num_segments):
            angle = 2 * math.pi * i / num_segments
            y = radius * math.cos(angle)
            z = radius * math.sin(angle)
            points.append((y, z))
        return points


@dataclass
class RectProfile(SectionProfile):
    """Rectangular section"""
    width: float   # Width (y direction, m)
    height: float  # Height (z direction, m)
    
    def get_profile_points(self, num_segments: int = 4) -> List[Tuple[float, float]]:
        """Generate rectangular profile points"""
        w2 = self.width / 2
        h2 = self.height / 2
        return [
            (-w2, -h2),
            (w2, -h2),
            (w2, h2),
            (-w2, h2),
        ]


@dataclass
class IProfile(SectionProfile):
    """I-section"""
    height: float       # Total height (m)
    top_width: float    # Top flange width (m)
    bottom_width: float # Bottom flange width (m)
    web_thickness: float    # Web thickness (m)
    flange_thickness: float # Top flange thickness (m)
    bottom_flange_thickness: float = None  # Bottom flange thickness (m); if `None`, uses `flange_thickness`
    
    def get_profile_points(self, num_segments: int = 12) -> List[Tuple[float, float]]:
        """Generate I-section profile points"""
        h = self.height
        tw = self.top_width
        bw = self.bottom_width
        wt = self.web_thickness
        tft = self.flange_thickness  # Top flange thickness
        bft = self.bottom_flange_thickness if self.bottom_flange_thickness else self.flange_thickness  # Bottom flange thickness
        
        # Start from lower-left corner, counterclockwise
        points = [
            # Bottom flange
            (-bw/2, -h/2),
            (bw/2, -h/2),
            (bw/2, -h/2 + bft),
            # Right side of web
            (wt/2, -h/2 + bft),
            (wt/2, h/2 - tft),
            # Top flange
            (tw/2, h/2 - tft),
            (tw/2, h/2),
            (-tw/2, h/2),
            (-tw/2, h/2 - tft),
            # Left side of web
            (-wt/2, h/2 - tft),
            (-wt/2, -h/2 + bft),
            (-bw/2, -h/2 + bft),
        ]
        return points


@dataclass
class PipeProfile(SectionProfile):
    """Pipe section (hollow circle)."""
    outer_diameter: float  # Outer diameter (m)
    wall_thickness: float  # Wall thickness (m)
    
    def get_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """
        Generate outer profile points for a pipe
        
        Note: Hollow sections in Rhino require creating outer and inner curves separately, then applying boolean operations.
        This returns the outer profile only; handle the inner profile separately.
        """
        outer_radius = self.outer_diameter / 2
        
        points = []
        
        # Return only the outer contour (counterclockwise)
        for i in range(num_segments):
            angle = 2 * math.pi * i / num_segments
            y = outer_radius * math.cos(angle)
            z = outer_radius * math.sin(angle)
            points.append((y, z))
        
        return points
    
    def get_inner_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """Get inner contour points (for boolean operations)"""
        inner_radius = self.outer_diameter / 2 - self.wall_thickness
        
        points = []
        
        # Inner contour (counterclockwise)
        for i in range(num_segments):
            angle = 2 * math.pi * i / num_segments
            y = inner_radius * math.cos(angle)
            z = inner_radius * math.sin(angle)
            points.append((y, z))
        
        return points


@dataclass
class BoxProfile(SectionProfile):
    """Box section (hollow rectangle)."""
    height: float          # Height (m)
    width: float           # Width (m)
    flange_thickness: float  # Top/bottom plate thickness (m)
    web_thickness: float     # Left/right plate thickness (m)
    
    def get_profile_points(self, num_segments: int = 4) -> List[Tuple[float, float]]:
        """
        Generate outer contour points for a box
        
        Note: Hollow sections in Rhino require creating outer and inner rectangles separately, then applying boolean operations.
        This returns the outer rectangle only; handle the inner rectangle separately.
        """
        h = self.height
        w = self.width
        
        # Outer rectangle (counterclockwise)
        points = [
            (-w/2, -h/2),
            (w/2, -h/2),
            (w/2, h/2),
            (-w/2, h/2),
        ]
        
        return points
    
    def get_inner_profile_points(self, num_segments: int = 4) -> List[Tuple[float, float]]:
        """Get inner rectangle contour points (for boolean operations)"""
        h = self.height
        w = self.width
        ft = self.flange_thickness
        wt = self.web_thickness
        
        # Inner rectangle (counterclockwise)
        points = [
            (-w/2 + wt, -h/2 + ft),
            (w/2 - wt, -h/2 + ft),
            (w/2 - wt, h/2 - ft),
            (-w/2 + wt, h/2 - ft),
        ]
        
        return points


@dataclass
class ChannelProfile(SectionProfile):
    """Channel section (C-shape)."""
    height: float          # Height (m)
    width: float           # Flange width (m)
    flange_thickness: float  # Flange thickness (m)
    web_thickness: float     # Web thickness (m)
    mirror: bool = False     # Whether mirrored
    
    def get_profile_points(self, num_segments: int = 8) -> List[Tuple[float, float]]:
        """Generate channel profile points"""
        h = self.height
        w = self.width
        ft = self.flange_thickness
        wt = self.web_thickness
        
        if not self.mirror:
            # Standard orientation (opening to the right)
            points = [
                # Start from lower-left corner, counterclockwise
                (-wt/2, -h/2),
                (w - wt/2, -h/2),
                (w - wt/2, -h/2 + ft),
                (wt/2, -h/2 + ft),
                (wt/2, h/2 - ft),
                (w - wt/2, h/2 - ft),
                (w - wt/2, h/2),
                (-wt/2, h/2),
            ]
        else:
            # Mirrored orientation (opening to the left)
            points = [
                (-w + wt/2, -h/2),
                (wt/2, -h/2),
                (wt/2, -h/2 + ft),
                (-w + wt/2, -h/2 + ft),
                (-w + wt/2, h/2 - ft),
                (wt/2, h/2 - ft),
                (wt/2, h/2),
                (-w + wt/2, h/2),
            ]
        
        return points


@dataclass
class TeeProfile(SectionProfile):
    """Tee section"""
    height: float          # Total height (m)
    width: float           # Flange width (m)
    flange_thickness: float  # Flange thickness (m)
    web_thickness: float     # Web thickness (m)
    mirror: bool = False     # Whether mirrored (vertical flip)
    
    def get_profile_points(self, num_segments: int = 6) -> List[Tuple[float, float]]:
        """Generate tee profile points"""
        h = self.height
        w = self.width
        ft = self.flange_thickness
        wt = self.web_thickness
        
        if not self.mirror:
            # Standard orientation (upright T)
            points = [
                # Start from lower-left corner, counterclockwise
                (-wt/2, -h/2),
                (wt/2, -h/2),
                (wt/2, h/2 - ft),
                (w/2, h/2 - ft),
                (w/2, h/2),
                (-w/2, h/2),
                (-w/2, h/2 - ft),
                (-wt/2, h/2 - ft),
            ]
        else:
            # Mirrored orientation (inverted T)
            points = [
                (-w/2, -h/2),
                (w/2, -h/2),
                (w/2, -h/2 + ft),
                (wt/2, -h/2 + ft),
                (wt/2, h/2),
                (-wt/2, h/2),
                (-wt/2, -h/2 + ft),
                (-w/2, -h/2 + ft),
            ]
        
        return points


@dataclass
class AngleProfile(SectionProfile):
    """Angle section (L-shape)."""
    height: float          # Vertical leg height (m)
    width: float           # Horizontal leg width (m)
    flange_thickness: float  # Horizontal leg thickness (m)
    web_thickness: float     # Vertical leg thickness (m)
    
    def get_profile_points(self, num_segments: int = 6) -> List[Tuple[float, float]]:
        """Generate angle profile points"""
        h = self.height
        w = self.width
        ft = self.flange_thickness
        wt = self.web_thickness
        
        # L-shape, start from lower-left corner, counterclockwise
        points = [
            (0, 0),
            (w, 0),
            (w, ft),
            (wt, ft),
            (wt, h),
            (0, h),
        ]
        
        # Move to approximate centroid
        center_y = (w + wt) / 4
        center_z = (h + ft) / 4
        points = [(y - center_y, z - center_z) for y, z in points]
        
        return points


def rotate_profile_points(
    points: List[Tuple[float, float]], angle_deg: float
) -> List[Tuple[float, float]]:
    """
    Rotate section profile points about the origin by a specified angle

    Used to apply SAP2000 local-axis rotation (`local_axis_angle`),
    rotating the section profile in the y-z plane about the element axis.

    Args:
        points: Section profile points `[(y, z), ...]`
        angle_deg: Rotation angle in degrees; positive is counterclockwise

    Returns:
        List of rotated profile points
    """
    if abs(angle_deg) < 1e-10:
        return points

    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    rotated = []
    for y, z in points:
        new_y = y * cos_a - z * sin_a
        new_z = y * sin_a + z * cos_a
        rotated.append((new_y, new_z))
    return rotated


def _transform_points(
    points: List[Tuple[float, float]],
    x_center: float,
    y_center: float,
    rotation: float
) -> List[Tuple[float, float]]:
    """
    Apply rotation and translation to profile points (for SD sub-shapes).
    
    Args:
        points: Source profile points (relative to shape center)
        x_center: Shape center X coordinate (SD coordinate system)
        y_center: Shape center Y coordinate (SD coordinate system)
        rotation: Counterclockwise rotation angle [deg]
    
    Returns:
        Transformed profile points
    """
    # Rotate first
    if abs(rotation) > 1e-10:
        points = rotate_profile_points(points, rotation)
    # Then translate
    return [(y + x_center, z + y_center) for y, z in points]


@dataclass
class DblAngleProfile(SectionProfile):
    """Double-angle section."""
    height: float           # Vertical leg height (m)
    width: float            # Horizontal leg width (m)
    flange_thickness: float # Horizontal leg thickness (m)
    web_thickness: float    # Vertical leg thickness (m)
    separation: float = 0.0 # Separation between angles (m)
    
    def get_profile_points(self, num_segments: int = 12) -> List[Tuple[float, float]]:
        """Generate double-angle profile points (two L-shapes)"""
        h = self.height
        w = self.width
        ft = self.flange_thickness
        wt = self.web_thickness
        gap = self.separation / 2
        
        # Right angle (standard L-shape)
        right = [
            (gap, -h/2),
            (gap + wt, -h/2),
            (gap + wt, -h/2 + ft),
            (gap + w, -h/2 + ft),
            (gap + w, -h/2),
            # Simplified as outer contour
        ]
        
        # Simplified: return two separate angle contours
        right_points = [
            (gap, -h/2),
            (gap + w, -h/2),
            (gap + w, -h/2 + ft),
            (gap + wt, -h/2 + ft),
            (gap + wt, h/2),
            (gap, h/2),
        ]
        
        # Left angle (mirrored)
        left_points = [
            (-gap, -h/2),
            (-gap, h/2),
            (-gap - wt, h/2),
            (-gap - wt, -h/2 + ft),
            (-gap - w, -h/2 + ft),
            (-gap - w, -h/2),
        ]
        
        return right_points + left_points


@dataclass
class SDShapeData:
    """Data for a single SD-section sub-shape"""
    shape_type: int                              # Shape type ID
    shape_name: str                              # Shape name
    points: List[Tuple[float, float]]            # Profile points
    inner_points: List[Tuple[float, float]] = None  # Inner profile points (hollow section)


@dataclass
class SDProfile(SectionProfile):
    """
    Section Designer custom section
    
    Composed of multiple sub-shapes, each with its own profile points.
    Supports both solid and hollow sub-shapes.
    """
    shapes: List[SDShapeData] = None
    
    def __post_init__(self):
        if self.shapes is None:
            self.shapes = []
    
    def add_shape(self, shape: SDShapeData):
        """Add a sub-shape"""
        self.shapes.append(shape)
    
    def get_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """
        Get outer profile points from all sub-shapes.
        
        Note: An SD section may contain multiple disconnected sub-shapes.
        This returns the first sub-shape profile points for simple extrusion,
        for full rendering use `get_all_shapes()`.
        """
        if not self.shapes:
            return []
        # Return profile points of the first shape.
        return self.shapes[0].points
    
    def get_all_shapes(self) -> List[SDShapeData]:
        """Get all sub-shape data (for full rendering)"""
        return self.shapes


@dataclass
class NonPrismaticProfile(SectionProfile):
    """
    Nonprismatic profile
    
    Contains start/end section profiles for tapered extrusion.
    """
    start_profile: SectionProfile = None   # Start section profile
    end_profile: SectionProfile = None     # End section profile
    segments: List[dict] = None            # Segment information list
    
    def __post_init__(self):
        if self.segments is None:
            self.segments = []
    
    def get_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """Return start-section profile points (default)."""
        if self.start_profile:
            return self.start_profile.get_profile_points(num_segments)
        return []
    
    def get_start_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """Get start-section profile points."""
        if self.start_profile:
            return self.start_profile.get_profile_points(num_segments)
        return []
    
    def get_end_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """Get end-section profile points."""
        if self.end_profile:
            return self.end_profile.get_profile_points(num_segments)
        return []


def create_profile_from_sap_section(section_type: str, params: dict) -> SectionProfile:
    """
    Create a section profile from SAP2000 section type and parameters
    
    Args:
        section_type: Section type (`Circle`, `Rect`, `I`, `Pipe`, `Box`, `Channel`, `Tee`, `Angle`)
        params: Section parameter dictionary
        
    Returns:
        `SectionProfile` object
        
    Example:
        profile = create_profile_from_sap_section("Circle", {"diameter": 0.5})
        points = profile.get_profile_points()
    """
    section_type = section_type.upper()
    
    if section_type in ("CIRCLE", "CIRCULAR"):
        return CircleProfile(
            diameter=params.get("diameter") or params.get("outer_diameter", 0.1)
        )
    
    elif section_type in ("RECT", "RECTANGULAR"):
        return RectProfile(
            width=params.get("width", 0.2),
            height=params.get("height", 0.3)
        )
    
    elif section_type in ("I", "I_SECTION", "ISECTION"):
        return IProfile(
            height=params.get("height", 0.5),
            top_width=params.get("top_width") or params.get("width", 0.2),
            bottom_width=params.get("bottom_width") or params.get("width", 0.2),
            web_thickness=params.get("web_thickness", 0.01),
            flange_thickness=params.get("flange_thickness", 0.02),
            bottom_flange_thickness=params.get("bottom_flange_thickness")
        )
    
    elif section_type in ("PIPE", "TUBE"):
        return PipeProfile(
            outer_diameter=params.get("outer_diameter", 0.2),
            wall_thickness=params.get("wall_thickness", 0.01)
        )
    
    elif section_type in ("BOX", "RECTANGULAR_TUBE"):
        return BoxProfile(
            height=params.get("height", 0.3),
            width=params.get("width", 0.2),
            flange_thickness=params.get("flange_thickness", 0.01),
            web_thickness=params.get("web_thickness", 0.01)
        )
    
    elif section_type in ("CHANNEL", "C"):
        return ChannelProfile(
            height=params.get("height", 0.3),
            width=params.get("width", 0.1),
            flange_thickness=params.get("flange_thickness", 0.01),
            web_thickness=params.get("web_thickness", 0.008),
            mirror=params.get("mirror", False)
        )
    
    elif section_type in ("TEE", "T", "T_SECTION"):
        return TeeProfile(
            height=params.get("height", 0.3),
            width=params.get("width", 0.2),
            flange_thickness=params.get("flange_thickness", 0.015),
            web_thickness=params.get("web_thickness", 0.01),
            mirror=params.get("mirror", False)
        )
    
    elif section_type in ("ANGLE", "L"):
        return AngleProfile(
            height=params.get("height", 0.1),
            width=params.get("width", 0.1),
            flange_thickness=params.get("flange_thickness", 0.01),
            web_thickness=params.get("web_thickness", 0.01)
        )
    
    elif section_type in ("DOUBLE_ANGLE", "DBLANGLE", "2L"):
        return DblAngleProfile(
            height=params.get("height", 0.1),
            width=params.get("width", 0.1),
            flange_thickness=params.get("flange_thickness", 0.01),
            web_thickness=params.get("web_thickness", 0.01),
            separation=params.get("separation", 0.0)
        )
    
    elif section_type == "SD":
        # SD section: `params` should include a `shapes` list
        profile = SDProfile()
        for shape_data in params.get("shapes", []):
            profile.add_shape(SDShapeData(
                shape_type=shape_data.get("shape_type", 0),
                shape_name=shape_data.get("shape_name", ""),
                points=shape_data.get("points", []),
                inner_points=shape_data.get("inner_points")
            ))
        return profile
    
    elif section_type == "NONPRISMATIC":
        # Nonprismatic section: `params` includes `start_section` and `end_section`
        start_sec = params.get("start_section", {})
        end_sec = params.get("end_section", {})
        
        start_profile = create_profile_from_sap_section(
            start_sec.get("type", "Circle"),
            start_sec.get("params", {})
        ) if start_sec else None
        
        end_profile = create_profile_from_sap_section(
            end_sec.get("type", "Circle"),
            end_sec.get("params", {})
        ) if end_sec else None
        
        return NonPrismaticProfile(
            start_profile=start_profile,
            end_profile=end_profile,
            segments=params.get("segments", [])
        )
    
    else:
        # Fallback to a circular section.
        return CircleProfile(diameter=0.1)
