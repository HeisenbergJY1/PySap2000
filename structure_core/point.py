# -*- coding: utf-8 -*-
"""
point.py - 节点数据对象
对应 SAP2000 的 PointObj

设计原则 (参考 Dlubal API):
- Point 类是纯数据类，只包含节点的基本属性
- 扩展功能 (支座、弹簧、质量、荷载等) 通过 types_for_points/ 模块的函数实现
- 这样设计便于 AI Agent 理解和使用

使用示例:
    from PySap2000.structure_core import Point
    from PySap2000.types_for_points import set_point_support, PointSupportType
    
    # 创建节点
    p = Point(no="1", x=0, y=0, z=0)
    p._create(model)
    
    # 设置支座 (使用 types_for_points 函数)
    set_point_support(model, "1", PointSupportType.FIXED)
"""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Union, ClassVar
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class PointCoordinateSystemType(IntEnum):
    """节点坐标系类型"""
    CARTESIAN = 0
    CYLINDRICAL = 1
    SPHERICAL = 2


@dataclass
class Point:
    """
    节点数据对象
    对应 SAP2000 的 PointObj
    
    这是一个纯数据类，只包含节点的基本属性。
    扩展功能请使用 types_for_points 模块:
    - 支座: types_for_points.set_point_support()
    - 弹簧: types_for_points.set_point_spring()
    - 质量: types_for_points.set_point_mass()
    - 荷载: types_for_points.set_point_load_force()
    - 约束: types_for_points.set_point_constraint()
    - 局部轴: types_for_points.set_point_local_axes()
    - 节点域: types_for_points.set_point_panel_zone()
    
    Attributes:
        no: 节点名称/编号
        x, y, z: 笛卡尔坐标
        coordinate_system: 坐标系名称
        merge_off: 是否禁用合并
        merge_number: 合并编号
        comment: 注释
        guid: 全局唯一标识符
    """
    
    # 必填属性
    no: Union[int, str] = None
    
    # 笛卡尔坐标
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    # 柱坐标 (r, theta, z)
    r: Optional[float] = None
    theta: Optional[float] = None
    
    # 球坐标 (r, a, b)
    a: Optional[float] = None
    b: Optional[float] = None
    
    # 可选属性
    coordinate_system: str = "Global"
    coordinate_system_type: PointCoordinateSystemType = PointCoordinateSystemType.CARTESIAN
    
    # 合并控制
    merge_off: bool = False
    merge_number: int = 0
    
    # 选择状态
    selected: bool = False
    
    # 其他
    comment: str = ""
    guid: Optional[str] = None
    
    # 类属性
    _object_type: ClassVar[str] = "PointObj"

    # ==================== 创建方法 ====================
    
    def _create(self, model) -> int:
        """
        在 SAP2000 中创建节点
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功，非 0 表示失败
        """
        from PySap2000.logger import get_logger
        _log = get_logger("point")

        user_name = str(self.no) if self.no is not None else ""

        # 检查是否已存在
        if user_name:
            try:
                existing = self.get_name_list(model)
                if user_name in existing:
                    _log.warning(f"Point '{user_name}' already exists, skipped")
                    return -1
            except Exception:
                pass

        if self.coordinate_system_type == PointCoordinateSystemType.CYLINDRICAL:
            return self._create_cylindrical(model, user_name)
        elif self.coordinate_system_type == PointCoordinateSystemType.SPHERICAL:
            return self._create_spherical(model, user_name)
        else:
            return self._create_cartesian(model, user_name)
    
    def _create_cartesian(self, model, user_name: str) -> int:
        """使用笛卡尔坐标创建节点"""
        result = model.PointObj.AddCartesian(
            self.x, self.y, self.z,
            "",
            user_name,
            self.coordinate_system,
            self.merge_off,
            self.merge_number
        )
        return self._parse_create_result(result)
    
    def _create_cylindrical(self, model, user_name: str) -> int:
        """使用柱坐标创建节点"""
        r = self.r if self.r is not None else 0.0
        theta = self.theta if self.theta is not None else 0.0
        
        result = model.PointObj.AddCylindrical(
            r, theta, self.z,
            "",
            user_name,
            self.coordinate_system,
            self.merge_off,
            self.merge_number
        )
        return self._parse_create_result(result)
    
    def _create_spherical(self, model, user_name: str) -> int:
        """使用球坐标创建节点"""
        r = self.r if self.r is not None else 0.0
        a = self.a if self.a is not None else 0.0
        b = self.b if self.b is not None else 0.0
        
        result = model.PointObj.AddSpherical(
            r, a, b,
            "",
            user_name,
            self.coordinate_system,
            self.merge_off,
            self.merge_number
        )
        return self._parse_create_result(result)
    
    def _parse_create_result(self, result) -> int:
        """解析创建结果"""
        assigned_name = com_data(result, 0)
        ret = com_ret(result)
        if assigned_name:
            self.no = assigned_name
        return ret

    # ==================== 获取方法 ====================
    
    def _get(self, model) -> 'Point':
        """
        从 SAP2000 获取节点基本数据
        
        只获取坐标、选择状态、GUID 等基本属性。
        扩展属性 (支座、弹簧等) 请使用 types_for_points 模块的函数获取。
        
        Args:
            model: SapModel 对象
            
        Returns:
            填充了数据的 Point 对象
        """
        self._get_coord_cartesian(model)
        self._get_selected(model)
        self._get_guid(model)
        return self
    
    def _get_coord_cartesian(self, model) -> Tuple[float, float, float]:
        """
        获取笛卡尔坐标
        
        API: GetCoordCartesian(Name, x, y, z, CSys="Global")
        返回: [x, y, z, ret]
        """
        result = model.PointObj.GetCoordCartesian(
            str(self.no), 0.0, 0.0, 0.0, self.coordinate_system
        )
        
        self.x = com_data(result, 0, default=self.x)
        self.y = com_data(result, 1, default=self.y)
        self.z = com_data(result, 2, default=self.z)
        ret = com_data(result, 3, default=-1)
        
        if ret != 0:
            from PySap2000.exceptions import PointError
            raise PointError(f"Failed to get coordinates for Point '{self.no}', ret={ret}")
        
        return (self.x, self.y, self.z)
    
    def get_coord_cylindrical(self, model) -> Tuple[float, float, float]:
        """获取柱坐标"""
        result = model.PointObj.GetCoordCylindrical(
            str(self.no), 0.0, 0.0, 0.0, self.coordinate_system
        )
        
        self.r = com_data(result, 0, default=0.0)
        self.theta = com_data(result, 1, default=0.0)
        self.z = com_data(result, 2, default=self.z)
        return (self.r, self.theta, self.z)
    
    def get_coord_spherical(self, model) -> Tuple[float, float, float]:
        """获取球坐标"""
        result = model.PointObj.GetCoordSpherical(
            str(self.no), 0.0, 0.0, 0.0, self.coordinate_system
        )
        
        self.r = com_data(result, 0, default=0.0)
        self.a = com_data(result, 1, default=0.0)
        self.b = com_data(result, 2, default=0.0)
        return (self.r, self.a, self.b)
    
    def _get_selected(self, model) -> bool:
        """获取选择状态"""
        try:
            result = model.PointObj.GetSelected(str(self.no), False)
            self.selected = com_data(result, 0, default=False)
            return self.selected
        except Exception:
            pass
        return False
    
    def _get_guid(self, model):
        """获取节点 GUID"""
        try:
            result = model.PointObj.GetGUID(str(self.no))
            self.guid = com_data(result, 0, default=self.guid)
        except Exception:
            pass

    # ==================== 公开查询方法 ====================
    
    @classmethod
    def get_all(cls, model, names: List[str] = None) -> List['Point']:
        """
        获取所有节点（使用 Database Tables API 批量获取，性能远优于逐个 COM 调用）

        Args:
            model: SapModel 对象
            names: 可选，指定节点名称列表。如果为 None，获取所有节点

        Returns:
            Point 对象列表，每个对象已填充基本数据

        Example:
            points = Point.get_all(model)
            for p in points:
                print(f"{p.no}: ({p.x}, {p.y}, {p.z})")
        """
        from PySap2000.database_tables import DatabaseTables

        # 一次 COM 调用获取所有节点坐标
        table_data = DatabaseTables.get_table_for_display(
            model, "Joint Coordinates"
        )

        if table_data is None or table_data.num_records == 0:
            return []

        # 将 names 转为 set 用于快速过滤
        name_filter = set(str(n) for n in names) if names else None

        points = []
        for row in table_data.to_dict_list():
            joint_name = row.get("Joint", "")
            if name_filter and joint_name not in name_filter:
                continue

            point = cls(
                no=joint_name,
                x=float(row.get("XorR", 0)),
                y=float(row.get("Y", 0)),
                z=float(row.get("Z", 0)),
                coordinate_system=row.get("CoordSys", "Global"),
            )
            points.append(point)

        return points

    
    @classmethod
    def get_by_name(cls, model, name: str) -> 'Point':
        """
        获取指定名称的节点
        
        Args:
            model: SapModel 对象
            name: 节点名称
            
        Returns:
            填充了基本数据的 Point 对象
            
        Example:
            point = Point.get_by_name(model, "1")
            print(f"坐标: {point.x}, {point.y}, {point.z}")
        """
        point = cls(no=name)
        point._get(model)
        return point
    
    @staticmethod
    def get_count(model) -> int:
        """
        获取节点总数
        
        Args:
            model: SapModel 对象
            
        Returns:
            节点数量
        """
        return model.PointObj.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """
        获取所有节点名称列表
        
        Args:
            model: SapModel 对象
            
        Returns:
            节点名称列表
        """
        result = model.PointObj.GetNameList(0, [])
        
        names = com_data(result, 1)
        if names is not None:
            return list(names)
        return []

    # ==================== 删除方法 ====================
    
    def _delete(self, model) -> int:
        """
        从 SAP2000 删除特殊节点
        
        注意: SAP2000 API 没有 PointObj.Delete() 方法!
        
        SAP2000 节点删除规则:
        - 普通节点: 当没有其他对象 (frame, area, link 等) 连接时，程序自动删除
        - 特殊节点: 必须先删除所有连接的对象，然后调用 DeleteSpecialPoint()
        
        Returns:
            0 表示成功，非 0 表示失败
        """
        from PySap2000.point.enums import ItemType
        return model.PointObj.DeleteSpecialPoint(str(self.no), ItemType.OBJECT)

    # ==================== 特殊节点方法 ====================
    
    def set_special_point(self, model, special: bool = True) -> int:
        """
        设置节点为特殊节点
        
        特殊节点不会在没有连接对象时被自动删除。
        
        Args:
            model: SapModel 对象
            special: True=设为特殊节点, False=取消特殊节点
            
        Returns:
            0 表示成功
        """
        from PySap2000.point.enums import ItemType
        return model.PointObj.SetSpecialPoint(str(self.no), special, ItemType.OBJECT)
    
    def get_special_point(self, model) -> bool:
        """
        获取节点是否为特殊节点
        
        Returns:
            True=是特殊节点, False=不是
        """
        try:
            result = model.PointObj.GetSpecialPoint(str(self.no), False)
            return com_data(result, 0, default=False)
        except Exception:
            pass
        return False

    # ==================== 选择方法 ====================
    
    def set_selected(self, model, selected: bool = True) -> int:
        """
        设置选择状态
        
        Args:
            model: SapModel 对象
            selected: True=选中, False=取消选中
            
        Returns:
            0 表示成功
        """
        from PySap2000.point.enums import ItemType
        self.selected = selected
        return model.PointObj.SetSelected(str(self.no), selected, ItemType.OBJECT)
    
    def get_selected(self, model) -> bool:
        """获取选择状态"""
        return self._get_selected(model)

    # ==================== 名称和 GUID 方法 ====================
    
    def change_name(self, model, new_name: str) -> int:
        """
        更改节点名称
        
        Args:
            model: SapModel 对象
            new_name: 新名称
            
        Returns:
            0 表示成功
        """
        ret = model.PointObj.ChangeName(str(self.no), new_name)
        if ret == 0:
            self.no = new_name
        return ret
    
    def get_guid(self, model) -> Optional[str]:
        """
        获取节点 GUID
        
        Returns:
            GUID 字符串，失败返回 None
        """
        self._get_guid(model)
        return self.guid
    
    def set_guid(self, model, guid: str = "") -> int:
        """
        设置节点 GUID
        
        Args:
            model: SapModel 对象
            guid: GUID 字符串。如果为空字符串，程序将自动创建新的 GUID
            
        Returns:
            0 表示成功
        """
        ret = model.PointObj.SetGUID(str(self.no), guid)
        if ret == 0:
            self._get_guid(model)
        return ret

    # ==================== 组方法 ====================
    
    def set_group_assign(self, model, group_name: str, remove: bool = False) -> int:
        """
        设置节点组分配
        
        Args:
            model: SapModel 对象
            group_name: 组名称
            remove: True=从组中移除, False=添加到组
            
        Returns:
            0 表示成功
        """
        from PySap2000.point.enums import ItemType
        return model.PointObj.SetGroupAssign(str(self.no), group_name, remove, ItemType.OBJECT)
    
    def get_group_assign(self, model) -> Optional[List[str]]:
        """
        获取节点所属组
        
        Returns:
            组名称列表
        """
        try:
            result = model.PointObj.GetGroupAssign(str(self.no))
            num_groups = com_data(result, 0, default=0)
            groups = com_data(result, 1)
            if num_groups > 0 and groups:
                return list(groups)
        except Exception:
            pass
        return None

    # ==================== 连接信息方法 ====================
    
    def get_connectivity(self, model) -> dict:
        """
        获取节点连接信息
        
        返回连接到此节点的所有对象信息。
        
        Returns:
            dict: {
                'num_items': int,
                'object_types': list,  # 对象类型 (1=Point, 2=Frame, 3=Cable, etc.)
                'object_names': list,  # 对象名称
                'point_numbers': list  # 对象上的节点编号
            }
        """
        try:
            result = model.PointObj.GetConnectivity(str(self.no), 0, [], [], [])
            num_items = com_data(result, 0, default=0)
            obj_types = com_data(result, 1)
            obj_names = com_data(result, 2)
            pt_numbers = com_data(result, 3)
            return {
                'num_items': num_items,
                'object_types': list(obj_types) if obj_types else [],
                'object_names': list(obj_names) if obj_names else [],
                'point_numbers': list(pt_numbers) if pt_numbers else []
            }
        except Exception:
            pass
        return {'num_items': 0, 'object_types': [], 'object_names': [], 'point_numbers': []}

    # ==================== 元素信息方法 ====================
    
    def get_elm(self, model) -> Optional[str]:
        """
        获取对应的分析模型节点元素名称
        
        Returns:
            元素名称，如果没有对应元素返回 None
        """
        try:
            result = model.PointObj.GetElm(str(self.no), "")
            elm_name = com_data(result, 0)
            ret = com_data(result, 1, default=-1)
            return elm_name if ret == 0 else None
        except Exception:
            pass
        return None

    # ==================== 变换矩阵方法 ====================
    
    def get_transformation_matrix(self, model, is_global: bool = True) -> Optional[List[float]]:
        """
        获取节点变换矩阵
        
        Args:
            model: SapModel 对象
            is_global: True=全局坐标系, False=局部坐标系
            
        Returns:
            12个元素的变换矩阵列表，失败返回 None
        """
        try:
            result = model.PointObj.GetTransformationMatrix(str(self.no), [0.0]*12, is_global)
            matrix = com_data(result, 0)
            ret = com_data(result, 1, default=-1)
            if ret == 0 and matrix:
                return list(matrix)
        except Exception:
            pass
        return None
