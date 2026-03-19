# -*- coding: utf-8 -*-
"""
section_profile.py - 截面轮廓生成器

根据截面类型和参数，生成截面轮廓的二维坐标点
用于后续生成三维实体（拉伸、扫掠等）

支持的截面类型：
- Circle: 圆形截面
- Rect: 矩形截面
- I: 工字钢截面
- Pipe: 圆管截面
- Box: 箱形截面
- Channel: 槽钢截面
- Tee: T型钢截面
- Angle: 角钢截面
"""

from dataclasses import dataclass
from typing import List, Tuple
import math


@dataclass
class SectionProfile:
    """截面轮廓基类"""
    
    def get_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """
        获取截面轮廓点（二维坐标，局部坐标系）
        
        Args:
            num_segments: 圆弧分段数
            
        Returns:
            [(y, z), ...] 坐标点列表（x 为单元轴向）
        """
        raise NotImplementedError


@dataclass
class CircleProfile(SectionProfile):
    """圆形截面"""
    diameter: float  # 直径（米）
    
    def get_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """生成圆形轮廓点"""
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
    """矩形截面"""
    width: float   # 宽度（y 方向，米）
    height: float  # 高度（z 方向，米）
    
    def get_profile_points(self, num_segments: int = 4) -> List[Tuple[float, float]]:
        """生成矩形轮廓点"""
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
    """工字钢截面"""
    height: float       # 总高度（米）
    top_width: float    # 上翼缘宽度（米）
    bottom_width: float # 下翼缘宽度（米）
    web_thickness: float    # 腹板厚度（米）
    flange_thickness: float # 上翼缘厚度（米）
    bottom_flange_thickness: float = None  # 下翼缘厚度（米），None 则使用 flange_thickness
    
    def get_profile_points(self, num_segments: int = 12) -> List[Tuple[float, float]]:
        """生成工字钢轮廓点"""
        h = self.height
        tw = self.top_width
        bw = self.bottom_width
        wt = self.web_thickness
        tft = self.flange_thickness  # 上翼缘厚度
        bft = self.bottom_flange_thickness if self.bottom_flange_thickness else self.flange_thickness  # 下翼缘厚度
        
        # 从左下角开始，逆时针
        points = [
            # 下翼缘
            (-bw/2, -h/2),
            (bw/2, -h/2),
            (bw/2, -h/2 + bft),
            # 腹板右侧
            (wt/2, -h/2 + bft),
            (wt/2, h/2 - tft),
            # 上翼缘
            (tw/2, h/2 - tft),
            (tw/2, h/2),
            (-tw/2, h/2),
            (-tw/2, h/2 - tft),
            # 腹板左侧
            (-wt/2, h/2 - tft),
            (-wt/2, -h/2 + bft),
            (-bw/2, -h/2 + bft),
        ]
        return points


@dataclass
class PipeProfile(SectionProfile):
    """圆管截面（空心圆）"""
    outer_diameter: float  # 外径（米）
    wall_thickness: float  # 壁厚（米）
    
    def get_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """
        生成圆管外圆轮廓点
        
        注意：Rhino 中空心截面需要分别创建外圆和内圆，然后做布尔运算
        这里返回的是外圆轮廓，内圆需要单独处理
        """
        outer_radius = self.outer_diameter / 2
        
        points = []
        
        # 只返回外圆轮廓（逆时针）
        for i in range(num_segments):
            angle = 2 * math.pi * i / num_segments
            y = outer_radius * math.cos(angle)
            z = outer_radius * math.sin(angle)
            points.append((y, z))
        
        return points
    
    def get_inner_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """获取内圆轮廓点（用于布尔运算）"""
        inner_radius = self.outer_diameter / 2 - self.wall_thickness
        
        points = []
        
        # 内圆轮廓（逆时针）
        for i in range(num_segments):
            angle = 2 * math.pi * i / num_segments
            y = inner_radius * math.cos(angle)
            z = inner_radius * math.sin(angle)
            points.append((y, z))
        
        return points


@dataclass
class BoxProfile(SectionProfile):
    """箱形截面（空心矩形）"""
    height: float          # 高度（米）
    width: float           # 宽度（米）
    flange_thickness: float  # 上下板厚度（米）
    web_thickness: float     # 左右板厚度（米）
    
    def get_profile_points(self, num_segments: int = 4) -> List[Tuple[float, float]]:
        """
        生成箱形外轮廓点
        
        注意：Rhino 中空心截面需要分别创建外矩形和内矩形，然后做布尔运算
        这里返回的是外矩形轮廓，内矩形需要单独处理
        """
        h = self.height
        w = self.width
        
        # 外矩形（逆时针）
        points = [
            (-w/2, -h/2),
            (w/2, -h/2),
            (w/2, h/2),
            (-w/2, h/2),
        ]
        
        return points
    
    def get_inner_profile_points(self, num_segments: int = 4) -> List[Tuple[float, float]]:
        """获取内矩形轮廓点（用于布尔运算）"""
        h = self.height
        w = self.width
        ft = self.flange_thickness
        wt = self.web_thickness
        
        # 内矩形（逆时针）
        points = [
            (-w/2 + wt, -h/2 + ft),
            (w/2 - wt, -h/2 + ft),
            (w/2 - wt, h/2 - ft),
            (-w/2 + wt, h/2 - ft),
        ]
        
        return points


@dataclass
class ChannelProfile(SectionProfile):
    """槽钢截面（C型）"""
    height: float          # 高度（米）
    width: float           # 翼缘宽度（米）
    flange_thickness: float  # 翼缘厚度（米）
    web_thickness: float     # 腹板厚度（米）
    mirror: bool = False     # 是否镜像
    
    def get_profile_points(self, num_segments: int = 8) -> List[Tuple[float, float]]:
        """生成槽钢轮廓点"""
        h = self.height
        w = self.width
        ft = self.flange_thickness
        wt = self.web_thickness
        
        if not self.mirror:
            # 标准方向（开口向右）
            points = [
                # 从左下角开始，逆时针
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
            # 镜像方向（开口向左）
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
    """T型钢截面"""
    height: float          # 总高度（米）
    width: float           # 翼缘宽度（米）
    flange_thickness: float  # 翼缘厚度（米）
    web_thickness: float     # 腹板厚度（米）
    mirror: bool = False     # 是否镜像（上下翻转）
    
    def get_profile_points(self, num_segments: int = 6) -> List[Tuple[float, float]]:
        """生成T型钢轮廓点"""
        h = self.height
        w = self.width
        ft = self.flange_thickness
        wt = self.web_thickness
        
        if not self.mirror:
            # 标准方向（T字正立）
            points = [
                # 从左下角开始，逆时针
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
            # 镜像方向（T字倒立）
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
    """角钢截面（L型）"""
    height: float          # 竖边高度（米）
    width: float           # 横边宽度（米）
    flange_thickness: float  # 横边厚度（米）
    web_thickness: float     # 竖边厚度（米）
    
    def get_profile_points(self, num_segments: int = 6) -> List[Tuple[float, float]]:
        """生成角钢轮廓点"""
        h = self.height
        w = self.width
        ft = self.flange_thickness
        wt = self.web_thickness
        
        # L型，从左下角开始，逆时针
        points = [
            (0, 0),
            (w, 0),
            (w, ft),
            (wt, ft),
            (wt, h),
            (0, h),
        ]
        
        # 移动到中心（近似）
        center_y = (w + wt) / 4
        center_z = (h + ft) / 4
        points = [(y - center_y, z - center_z) for y, z in points]
        
        return points


def rotate_profile_points(
    points: List[Tuple[float, float]], angle_deg: float
) -> List[Tuple[float, float]]:
    """
    将截面轮廓点绕原点旋转指定角度

    用于应用 SAP2000 的局部坐标轴旋转角度（local_axis_angle），
    使截面轮廓在 y-z 平面内绕单元轴线旋转。

    Args:
        points: 截面轮廓点 [(y, z), ...]
        angle_deg: 旋转角度（度），正值为逆时针

    Returns:
        旋转后的轮廓点列表
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
    对轮廓点应用旋转和平移变换（SD截面子形状用）
    
    Args:
        points: 原始轮廓点（相对于形状中心）
        x_center: 形状中心 X 坐标（SD坐标系）
        y_center: 形状中心 Y 坐标（SD坐标系）
        rotation: 逆时针旋转角度 [deg]
    
    Returns:
        变换后的轮廓点
    """
    # 先旋转
    if abs(rotation) > 1e-10:
        points = rotate_profile_points(points, rotation)
    # 再平移
    return [(y + x_center, z + y_center) for y, z in points]


@dataclass
class DblAngleProfile(SectionProfile):
    """双角钢截面"""
    height: float           # 竖边高度（米）
    width: float            # 横边宽度（米）
    flange_thickness: float # 横边厚度（米）
    web_thickness: float    # 竖边厚度（米）
    separation: float = 0.0 # 两角钢间距（米）
    
    def get_profile_points(self, num_segments: int = 12) -> List[Tuple[float, float]]:
        """生成双角钢轮廓点（两个L型组合）"""
        h = self.height
        w = self.width
        ft = self.flange_thickness
        wt = self.web_thickness
        gap = self.separation / 2
        
        # 右侧角钢（标准L型）
        right = [
            (gap, -h/2),
            (gap + wt, -h/2),
            (gap + wt, -h/2 + ft),
            (gap + w, -h/2 + ft),
            (gap + w, -h/2),
            # 这里简化为外轮廓
        ]
        
        # 简化：返回两个独立的角钢轮廓（右侧）
        right_points = [
            (gap, -h/2),
            (gap + w, -h/2),
            (gap + w, -h/2 + ft),
            (gap + wt, -h/2 + ft),
            (gap + wt, h/2),
            (gap, h/2),
        ]
        
        # 左侧角钢（镜像）
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
    """SD截面中单个子形状的数据"""
    shape_type: int                              # 形状类型编号
    shape_name: str                              # 形状名称
    points: List[Tuple[float, float]]            # 轮廓点
    inner_points: List[Tuple[float, float]] = None  # 内轮廓点（空心截面）


@dataclass
class SDProfile(SectionProfile):
    """
    Section Designer 自定义截面
    
    由多个子形状组合而成，每个子形状有自己的轮廓点。
    支持实心和空心子形状。
    """
    shapes: List[SDShapeData] = None
    
    def __post_init__(self):
        if self.shapes is None:
            self.shapes = []
    
    def add_shape(self, shape: SDShapeData):
        """添加子形状"""
        self.shapes.append(shape)
    
    def get_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """
        获取所有子形状的外轮廓点
        
        注意：SD截面可能包含多个不相连的子形状，
        这里返回第一个子形状的轮廓点（用于简单拉伸），
        完整渲染应使用 get_all_shapes() 方法。
        """
        if not self.shapes:
            return []
        # 返回第一个形状的轮廓点
        return self.shapes[0].points
    
    def get_all_shapes(self) -> List[SDShapeData]:
        """获取所有子形状数据（用于完整渲染）"""
        return self.shapes


@dataclass
class NonPrismaticProfile(SectionProfile):
    """
    变截面轮廓
    
    包含起点截面和终点截面的轮廓，用于渐变拉伸。
    """
    start_profile: SectionProfile = None   # 起点截面轮廓
    end_profile: SectionProfile = None     # 终点截面轮廓
    segments: List[dict] = None            # 段信息列表
    
    def __post_init__(self):
        if self.segments is None:
            self.segments = []
    
    def get_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """返回起点截面轮廓点（默认）"""
        if self.start_profile:
            return self.start_profile.get_profile_points(num_segments)
        return []
    
    def get_start_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """获取起点截面轮廓点"""
        if self.start_profile:
            return self.start_profile.get_profile_points(num_segments)
        return []
    
    def get_end_profile_points(self, num_segments: int = 16) -> List[Tuple[float, float]]:
        """获取终点截面轮廓点"""
        if self.end_profile:
            return self.end_profile.get_profile_points(num_segments)
        return []


def create_profile_from_sap_section(section_type: str, params: dict) -> SectionProfile:
    """
    根据 SAP2000 截面类型和参数创建截面轮廓
    
    Args:
        section_type: 截面类型（Circle, Rect, I, Pipe, Box, Channel, Tee, Angle）
        params: 截面参数字典
        
    Returns:
        SectionProfile 对象
        
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
        # SD 截面：params 中应包含 "shapes" 列表
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
        # 变截面：params 中包含 start_section 和 end_section
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
        # 默认返回圆形截面
        return CircleProfile(diameter=0.1)
