# -*- coding: utf-8 -*-
"""
link.py - 连接单元数据对象
对应 SAP2000 的 LinkObj

这是一个纯数据类，只包含核心 CRUD 操作。
扩展功能请使用:
- loads/link_load.py - 荷载函数
- types_for_links/ - 其他扩展函数

API Reference:
    - AddByPoint(Point1, Point2, Name, IsSingleJoint=False, PropName="Default", UserName="") -> Long
    - AddByCoord(xi, yi, zi, xj, yj, zj, Name, IsSingleJoint=False, PropName="Default", UserName="", CSys="Global") -> Long
    - GetPoints(Name, Point1, Point2) -> Long
    - GetProperty(Name, PropName) -> Long
    - GetPropertyFD(Name, PropName) -> Long
    - SetPropertyFD(Name, PropName, ItemType) -> Long
    - GetLocalAxes(Name, Ang, Advanced) -> (Ang, Advanced, ret)
    - SetLocalAxes(Name, Ang, ItemType) -> Long
    - GetLocalAxesAdvanced(Name, Active, AxVectOpt, AxCSys, AxDir[], AxPt[], AxVect[], Plane2, PlVectOpt, PlCSys, PlDir[], PlPt[], PlVect[]) -> Long
    - SetLocalAxesAdvanced(Name, Active, AxVectOpt, AxCSys, AxDir[], AxPt[], AxVect[], Plane2, PlVectOpt, PlCSys, PlDir[], PlPt[], PlVect[], ItemType) -> Long
    - Count() -> Long
    - GetNameList() -> (NumberNames, MyName[], ret)
    - Delete(Name) -> Long
    - GetElm(Name, Elm) -> Long  # 返回单个分析单元名称

Usage:
    from PySap2000.structure_core import Link
    from PySap2000.types_for_links import LinkType, LinkItemType
    
    # 创建两节点连接单元
    link = Link(no=1, start_point="1", end_point="2", property_name="Linear1")
    link._create(model)
    
    # 创建单节点连接单元（接地）
    link = Link(no=2, start_point="3", is_single_joint=True, property_name="Spring1")
    link._create(model)
    
    # 获取连接单元
    link = Link.get_by_name(model, "1")
"""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Union, ClassVar

from link.enums import (
    LinkType, LinkDirectionalType, LinkItemType, AxisVectorOption
)
from PySap2000.com_helper import com_ret, com_data


@dataclass
class LinkLocalAxesAdvanced:
    """
    连接单元高级局部轴设置
    
    Attributes:
        link_name: 连接单元名称
        active: 是否激活高级局部轴
        ax_vect_opt: 轴向量选项 (1=坐标方向, 2=两节点, 3=用户向量)
        ax_csys: 轴坐标系
        ax_dir: 轴方向数组 [primary, secondary] (1-9, 负值表示负方向)
        ax_pt: 轴参考点数组 [pt1, pt2]
        ax_vect: 轴向量 [x, y, z]
        plane2: 平面2定义 (12 或 13)
        pl_vect_opt: 平面向量选项
        pl_csys: 平面坐标系
        pl_dir: 平面方向数组 [primary, secondary]
        pl_pt: 平面参考点数组 [pt1, pt2]
        pl_vect: 平面向量 [x, y, z]
    """
    link_name: str = ""
    active: bool = False
    ax_vect_opt: int = 1
    ax_csys: str = "Global"
    ax_dir: List[int] = field(default_factory=lambda: [0, 0])
    ax_pt: List[str] = field(default_factory=lambda: ["", ""])
    ax_vect: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    plane2: int = 12
    pl_vect_opt: int = 1
    pl_csys: str = "Global"
    pl_dir: List[int] = field(default_factory=lambda: [0, 0])
    pl_pt: List[str] = field(default_factory=lambda: ["", ""])
    pl_vect: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])


@dataclass
class Link:
    """
    连接单元数据对象
    
    对应 SAP2000 的 LinkObj
    用于模拟弹簧、阻尼器、隔震支座等
    
    Attributes:
        no: 连接单元编号/名称
        start_point: 起始节点编号 (I-End)
        end_point: 结束节点编号 (J-End)，单节点连接时为 None 或 ""
        is_single_joint: 是否为单节点连接（接地）
        property_name: 连接属性名称
        fd_property_name: 频率相关连接属性名称 (None 表示无)
        local_axis_angle: 局部轴角度 [deg]
        advanced_axes: 是否使用高级局部轴参数
        type: 连接类型
    """
    
    # 必填属性
    no: Union[int, str] = None
    
    # 通过节点定义
    start_point: Optional[Union[int, str]] = None
    end_point: Optional[Union[int, str]] = None
    
    # 通过坐标定义
    start_x: Optional[float] = None
    start_y: Optional[float] = None
    start_z: Optional[float] = None
    end_x: Optional[float] = None
    end_y: Optional[float] = None
    end_z: Optional[float] = None
    
    # 属性
    property_name: str = ""
    fd_property_name: Optional[str] = None
    type: Optional[LinkType] = None
    directional_type: LinkDirectionalType = LinkDirectionalType.TWO_JOINT
    
    # 单节点连接标志
    is_single_joint: bool = False
    
    # 局部轴角度
    local_axis_angle: float = 0.0
    advanced_axes: bool = False
    
    # 可选属性
    coordinate_system: str = "Global"
    comment: str = ""
    guid: Optional[str] = None
    
    # 类属性
    _object_type: ClassVar[str] = "LinkObj"
    
    # ==================== 核心 CRUD 方法 ====================
    
    def _create(self, model) -> int:
        """
        在 SAP2000 中创建连接单元
        
        Returns:
            0 表示成功
        """
        from PySap2000.logger import get_logger
        _log = get_logger("link")

        user_name = str(self.no) if self.no is not None else ""
        prop = self.property_name if self.property_name else "Default"

        # 检查是否已存在
        if user_name:
            try:
                existing = self.get_name_list(model)
                if user_name in existing:
                    _log.warning(f"Link '{user_name}' already exists, skipped")
                    return -1
            except Exception:
                pass

        # 通过坐标创建
        if self.start_x is not None:
            result = model.LinkObj.AddByCoord(
                self.start_x, self.start_y or 0, self.start_z or 0,
                self.end_x or 0, self.end_y or 0, self.end_z or 0,
                "", self.is_single_joint, prop, user_name, self.coordinate_system
            )
            assigned_name = com_data(result, 0)
            if assigned_name:
                self.no = assigned_name
            return com_ret(result)
        
        # 通过节点创建
        if self.start_point is not None:
            point1 = str(self.start_point)
            point2 = str(self.end_point) if self.end_point and not self.is_single_joint else ""
            
            result = model.LinkObj.AddByPoint(
                point1, point2, "", self.is_single_joint, prop, user_name
            )
            assigned_name = com_data(result, 0)
            if assigned_name:
                self.no = assigned_name
            return com_ret(result)
        
        from PySap2000.exceptions import LinkError
        raise LinkError("Link creation requires points or coordinates")
    
    def _get(self, model) -> 'Link':
        """从 SAP2000 获取连接单元数据"""
        no_str = str(self.no)
        
        # 获取端点
        result = model.LinkObj.GetPoints(no_str, "", "")
        self.start_point = com_data(result, 0)
        point2 = com_data(result, 1)
        ret = com_ret(result)
        
        if point2 == "" or point2 is None or point2 == self.start_point:
            self.is_single_joint = True
            self.end_point = point2 if point2 != self.start_point else None
        else:
            self.is_single_joint = False
            self.end_point = point2
        
        if ret != 0:
            from PySap2000.exceptions import LinkError
            raise LinkError(f"Failed to get endpoints for Link '{no_str}', ret={ret}")
        
        # 获取属性
        result = model.LinkObj.GetProperty(no_str, "")
        self.property_name = com_data(result, 0, "")
        
        # 获取频率相关属性
        self._get_property_fd(model)
        
        # 获取局部轴角度
        self._get_local_axes(model)
        
        # 获取 GUID
        self._get_guid(model)
        
        return self
    
    def _delete(self, model) -> int:
        """从 SAP2000 删除连接单元"""
        return model.LinkObj.Delete(str(self.no))
    
    def _update(self, model) -> int:
        """更新连接单元属性"""
        from PySap2000.logger import get_logger
        _log = get_logger("link")
        ret = 0
        no_str = str(self.no)
        if self.property_name:
            try:
                existing = self.get_property_name_list(model)
                if self.property_name not in existing:
                    _log.warning(f"LinkSection '{self.property_name}' not found")
            except Exception:
                pass
            ret = model.LinkObj.SetProperty(no_str, self.property_name)
        
        if self.fd_property_name is not None:
            model.LinkObj.SetPropertyFD(no_str, self.fd_property_name, LinkItemType.OBJECT)
        
        if self.local_axis_angle != 0.0:
            model.LinkObj.SetLocalAxes(no_str, self.local_axis_angle, LinkItemType.OBJECT)
        
        return ret
    
    # ==================== 内部辅助方法 ====================
    
    def _get_local_axes(self, model):
        """获取局部轴角度"""
        try:
            result = model.LinkObj.GetLocalAxes(str(self.no), 0.0, False)
            self.local_axis_angle = com_data(result, 0, 0.0)
            self.advanced_axes = com_data(result, 1, False)
        except Exception:
            pass
    
    def _get_property_fd(self, model):
        """获取频率相关属性"""
        try:
            result = model.LinkObj.GetPropertyFD(str(self.no), "")
            prop_name = com_data(result, 0)
            if prop_name and prop_name != "None":
                self.fd_property_name = prop_name
            else:
                self.fd_property_name = None
        except Exception:
            self.fd_property_name = None
    
    def _get_guid(self, model):
        """获取 GUID"""
        try:
            result = model.LinkObj.GetGUID(str(self.no), "")
            guid = com_data(result, 0)
            if guid is not None:
                self.guid = guid
        except Exception:
            pass
    
    # ==================== 静态方法 ====================
    
    @staticmethod
    def get_count(model) -> int:
        """获取连接单元总数"""
        return model.LinkObj.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """获取所有连接单元名称列表"""
        result = model.LinkObj.GetNameList(0, [])
        count = com_data(result, 0, 0)
        names = com_data(result, 1)
        if count > 0 and names:
            return list(names)
        return []
    
    @staticmethod
    def get_property_name_list(model) -> List[str]:
        """获取所有连接属性名称列表"""
        result = model.PropLink.GetNameList(0, [])
        count = com_data(result, 0, 0)
        names = com_data(result, 1)
        if count > 0 and names:
            return list(names)
        return []

    
    # ==================== 类方法 ====================
    
    @classmethod
    def get_by_name(cls, model, name: str) -> 'Link':
        """
        获取指定名称的连接单元
        
        Example:
            link = Link.get_by_name(model, "1")
            print(f"属性: {link.property_name}")
        """
        link = cls(no=name)
        link._get(model)
        return link
    
    @classmethod
    def get_all(cls, model, names: List[str] = None) -> List['Link']:
        """
        获取所有连接单元
        
        Example:
            links = Link.get_all(model)
            for lk in links:
                print(f"{lk.no}: {lk.property_name}")
        """
        if names is None:
            names = cls.get_name_list(model)
        return [cls.get_by_name(model, name) for name in names]
    
    # ==================== 实例方法 ====================
    
    def set_property(self, model, property_name: str) -> int:
        """设置连接属性"""
        self.property_name = property_name
        return model.LinkObj.SetProperty(str(self.no), property_name)
    
    def set_guid(self, model, guid: str) -> int:
        """设置 GUID"""
        self.guid = guid
        return model.LinkObj.SetGUID(str(self.no), guid)
    
    def get_local_axes(self, model) -> Tuple[float, bool]:
        """
        获取局部轴角度
        
        Returns:
            (angle, advanced) - 角度[deg]和是否使用高级参数
        """
        self._get_local_axes(model)
        return (self.local_axis_angle, self.advanced_axes)
    
    def set_local_axes(
        self, 
        model, 
        angle: float,
        item_type: LinkItemType = LinkItemType.OBJECT
    ) -> int:
        """
        设置局部轴角度
        
        Args:
            model: SapModel 对象
            angle: 局部2和3轴绕正局部1轴旋转的角度 [deg]
            item_type: 操作范围
            
        Returns:
            0 表示成功
        """
        self.local_axis_angle = angle
        return model.LinkObj.SetLocalAxes(str(self.no), angle, int(item_type))
    
    def get_property_fd(self, model) -> Optional[str]:
        """
        获取频率相关属性
        
        Returns:
            频率相关属性名称，None 表示无
        """
        self._get_property_fd(model)
        return self.fd_property_name
    
    def set_property_fd(
        self, 
        model, 
        prop_name: Optional[str],
        item_type: LinkItemType = LinkItemType.OBJECT
    ) -> int:
        """
        设置频率相关属性
        
        Args:
            model: SapModel 对象
            prop_name: 频率相关属性名称，None 或 "None" 表示清除
            item_type: 操作范围
            
        Returns:
            0 表示成功
        """
        if prop_name is None:
            prop_name = "None"
        self.fd_property_name = prop_name if prop_name != "None" else None
        return model.LinkObj.SetPropertyFD(str(self.no), prop_name, int(item_type))

    
    # ==================== 高级局部轴方法 ====================
    
    def get_local_axes_advanced(self, model) -> 'LinkLocalAxesAdvanced':
        """
        获取高级局部轴设置
        
        API: GetLocalAxesAdvanced(Name, Active, AxVectOpt, AxCSys, AxDir[], AxPt[], AxVect[], 
                                   Plane2, PlVectOpt, PlCSys, PlDir[], PlPt[], PlVect[])
        
        Returns:
            LinkLocalAxesAdvanced 数据对象
        """
        result = model.LinkObj.GetLocalAxesAdvanced(
            str(self.no), False, 0, "", [], [], [], 0, 0, "", [], [], []
        )
        
        if com_data(result, 0) is not None:
            return LinkLocalAxesAdvanced(
                link_name=str(self.no),
                active=com_data(result, 0, False),
                ax_vect_opt=com_data(result, 1, 1),
                ax_csys=com_data(result, 2) or "Global",
                ax_dir=list(com_data(result, 3, [0, 0])),
                ax_pt=list(com_data(result, 4, ["", ""])),
                ax_vect=list(com_data(result, 5, [0.0, 0.0, 0.0])),
                plane2=com_data(result, 6, 12),
                pl_vect_opt=com_data(result, 7, 1),
                pl_csys=com_data(result, 8) or "Global",
                pl_dir=list(com_data(result, 9, [0, 0])),
                pl_pt=list(com_data(result, 10, ["", ""])),
                pl_vect=list(com_data(result, 11, [0.0, 0.0, 0.0]))
            )
        
        return LinkLocalAxesAdvanced(link_name=str(self.no))
    
    def set_local_axes_advanced(
        self, 
        model,
        active: bool,
        ax_vect_opt: int = 1,
        ax_csys: str = "Global",
        ax_dir: List[int] = None,
        ax_pt: List[str] = None,
        ax_vect: List[float] = None,
        plane2: int = 12,
        pl_vect_opt: int = 1,
        pl_csys: str = "Global",
        pl_dir: List[int] = None,
        pl_pt: List[str] = None,
        pl_vect: List[float] = None,
        item_type: LinkItemType = LinkItemType.OBJECT
    ) -> int:
        """
        设置高级局部轴
        
        API: SetLocalAxesAdvanced(Name, Active, AxVectOpt, AxCSys, AxDir[], AxPt[], AxVect[],
                                   Plane2, PlVectOpt, PlCSys, PlDir[], PlPt[], PlVect[], ItemType)
        
        Args:
            model: SapModel 对象
            active: 是否激活高级局部轴
            ax_vect_opt: 轴向量选项 (1=坐标方向, 2=两节点, 3=用户向量)
            ax_csys: 轴坐标系
            ax_dir: 轴方向数组 [primary, secondary]
            ax_pt: 轴参考点数组 [pt1, pt2]
            ax_vect: 轴向量 [x, y, z]
            plane2: 平面2定义 (12 或 13)
            pl_vect_opt: 平面向量选项
            pl_csys: 平面坐标系
            pl_dir: 平面方向数组 [primary, secondary]
            pl_pt: 平面参考点数组 [pt1, pt2]
            pl_vect: 平面向量 [x, y, z]
            item_type: 操作范围
            
        Returns:
            0 表示成功
        """
        # 设置默认值
        if ax_dir is None:
            ax_dir = [0, 0]
        if ax_pt is None:
            ax_pt = ["", ""]
        if ax_vect is None:
            ax_vect = [0.0, 0.0, 0.0]
        if pl_dir is None:
            pl_dir = [0, 0]
        if pl_pt is None:
            pl_pt = ["", ""]
        if pl_vect is None:
            pl_vect = [0.0, 0.0, 0.0]
        
        return model.LinkObj.SetLocalAxesAdvanced(
            str(self.no), active, ax_vect_opt, ax_csys, ax_dir, ax_pt, ax_vect,
            plane2, pl_vect_opt, pl_csys, pl_dir, pl_pt, pl_vect, int(item_type)
        )
    
    # ==================== 便捷创建方法 ====================
    
    @staticmethod
    def add_grounded(
        model,
        no: str,
        point: Union[int, str],
        property_name: str = "Default"
    ) -> int:
        """
        创建接地连接单元（单节点）
        
        Args:
            model: SapModel 对象
            no: 连接单元编号
            point: 节点编号
            property_name: 连接属性名称
            
        Returns:
            0 表示成功
        """
        result = model.LinkObj.AddByPoint(
            str(point), "", "", True, property_name, no
        )
        return com_ret(result)
    
    # ==================== 分析单元方法 ====================
    
    def get_elm(self, model) -> Optional[str]:
        """
        获取分析单元名称
        
        API: GetElm(Name, Elm) -> Long
        注意: 每个 Link 对象对应一个分析单元，返回单个字符串
        
        Returns:
            分析单元名称，失败返回 None
        """
        result = model.LinkObj.GetElm(str(self.no), "")
        
        ret = com_ret(result)
        if ret == 0:
            return com_data(result, 0)
        
        return None
    
    # ==================== 变换矩阵方法 ====================
    
    def get_transformation_matrix(self, model, is_global: bool = True) -> List[float]:
        """
        获取变换矩阵
        
        Args:
            model: SapModel 对象
            is_global: 是否为全局坐标系
            
        Returns:
            3x3 变换矩阵 (9个值)
        """
        result = model.LinkObj.GetTransformationMatrix(str(self.no), [], is_global)
        
        matrix = com_data(result, 0)
        if matrix:
            return list(matrix)
        
        return [1, 0, 0, 0, 1, 0, 0, 0, 1]
    
    # ==================== 选择方法 ====================
    
    def get_selected(self, model) -> bool:
        """获取选择状态"""
        result = model.LinkObj.GetSelected(str(self.no), False)
        return com_data(result, 0, False)
    
    def set_selected(
        self, 
        model, 
        selected: bool,
        item_type: LinkItemType = LinkItemType.OBJECT
    ) -> int:
        """设置选择状态"""
        return model.LinkObj.SetSelected(str(self.no), selected, int(item_type))
    
    # ==================== 组分配方法 ====================
    
    def get_group_assign(self, model) -> List[str]:
        """获取组分配"""
        result = model.LinkObj.GetGroupAssign(str(self.no), 0, [])
        num_groups = com_data(result, 0, 0)
        groups = com_data(result, 1)
        if num_groups > 0 and groups:
            return list(groups)
        return []
    
    def set_group_assign(
        self, 
        model, 
        group_name: str,
        remove: bool = False,
        item_type: LinkItemType = LinkItemType.OBJECT
    ) -> int:
        """设置组分配"""
        return model.LinkObj.SetGroupAssign(str(self.no), group_name, remove, int(item_type))
    
    # ==================== 名称方法 ====================
    
    def change_name(self, model, new_name: str) -> int:
        """更改连接单元名称"""
        ret = model.LinkObj.ChangeName(str(self.no), new_name)
        if ret == 0:
            self.no = new_name
        return ret
