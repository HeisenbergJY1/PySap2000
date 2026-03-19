# -*- coding: utf-8 -*-
"""
cable.py - 索单元数据对象
对应 SAP2000 的 CableObj

API Reference:
    - AddByPoint(Point1, Point2, Name, PropName="Default", UserName="") -> Long
    - AddByCoord(xi, yi, zi, xj, yj, zj, Name, PropName="Default", UserName="", CSys="Global") -> Long
    - GetPoints(Name, Point1, Point2) -> Long
    - GetProperty(Name, PropName) -> Long
    - GetCableData(Name, CableType, NumSegs, Weight, ProjectedLoad, UseDeformedGeom, ModelUsingFrames, Parameter[]) -> Long
    - SetCableData(Name, CableType, NumSegs, Weight, ProjectedLoad, Value, UseDeformedGeom, ModelUsingFrames) -> Long
    - GetCableGeometry(Name, NumberPoints, x[], y[], z[], Sag[], Dist[], RD[], CSys) -> Long
    - Count() -> Long
    - GetNameList() -> (NumberNames, MyName[], ret)

Usage:
    from PySap2000 import Application
    from PySap2000.structure_core import Cable, CableType
    
    with Application() as app:
        # 通过节点创建索
        app.create_object(Cable(no=1, start_point="1", end_point="2", section="CAB1"))
        
        # 设置索数据
        cable.set_cable_data(model, CableType.LOW_POINT_VERTICAL_SAG, value=24)
        
        # 获取索几何
        geometry = cable.get_cable_geometry(model)
"""

import math
from dataclasses import dataclass, field
from typing import Optional, List, Union, ClassVar, Tuple

from cable.enums import CableType
from PySap2000.com_helper import com_ret, com_data


@dataclass
class CableGeometry:
    """
    索几何数据
    
    从 GetCableGeometry API 返回的数据
    """
    number_points: int = 0
    x: Tuple[float, ...] = ()  # X坐标数组 [L]
    y: Tuple[float, ...] = ()  # Y坐标数组 [L]
    z: Tuple[float, ...] = ()  # Z坐标数组 [L]
    sag: Tuple[float, ...] = ()  # 垂度数组 [L]
    distance: Tuple[float, ...] = ()  # 沿索距离数组 [L]
    relative_distance: Tuple[float, ...] = ()  # 相对距离数组


@dataclass
class CableParameters:
    """
    索参数数据
    
    从 GetCableData API 返回的 Parameter 数组
    """
    tension_i_end: float = 0.0           # Parameter(0): I端张力 [F]
    tension_j_end: float = 0.0           # Parameter(1): J端张力 [F]
    horizontal_tension: float = 0.0      # Parameter(2): 水平张力分量 [F]
    max_deformed_sag: float = 0.0        # Parameter(3): 最大变形垂度 [L]
    deformed_low_point_sag: float = 0.0  # Parameter(4): 变形最低点垂度 [L]
    deformed_length: float = 0.0         # Parameter(5): 变形长度 [L]
    deformed_relative_length: float = 0.0  # Parameter(6): 变形相对长度
    max_undeformed_sag: float = 0.0      # Parameter(7): 最大未变形垂度 [L]
    undeformed_low_point_sag: float = 0.0  # Parameter(8): 未变形最低点垂度 [L]
    undeformed_length: float = 0.0       # Parameter(9): 未变形长度 [L]
    undeformed_relative_length: float = 0.0  # Parameter(10): 未变形相对长度


@dataclass
class Cable:
    """
    索单元数据对象
    
    对应 SAP2000 的 CableObj
    
    Attributes:
        no: 索单元编号/名称
        start_point: 起始节点编号 (I-End)
        end_point: 结束节点编号 (J-End)
        section: 截面名称
        cable_type: 索定义类型
        tension: 张力值（根据 cable_type 使用）
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
    
    # 截面
    section: str = ""
    
    # 索属性 (API: GetCableData/SetCableData)
    cable_type: CableType = CableType.MINIMUM_TENSION_AT_I_END
    num_segs: int = 1  # 程序内部分段数
    added_weight: float = 0.0  # 附加重量 [F/L]
    projected_load: float = 0.0  # 投影均布荷载 [F/L]
    cable_value: float = 0.0  # 定义参数值（根据 cable_type 使用）
    use_deformed_geom: bool = False  # 是否使用变形几何
    model_using_frames: bool = False  # 是否使用框架单元建模
    
    # 索参数（只读，从 GetCableData 获取）
    parameters: Optional[CableParameters] = None
    
    # 可选属性
    coordinate_system: str = "Global"
    comment: str = ""
    guid: Optional[str] = None
    
    # 只读属性
    length: Optional[float] = field(default=None, repr=False)
    
    # 类属性
    _object_type: ClassVar[str] = "CableObj"
    
    def _create(self, model) -> int:
        """
        在 SAP2000 中创建索单元
        
        API (节点): AddByPoint(Point1, Point2, Name, PropName, UserName)
        API (坐标): AddByCoord(xi, yi, zi, xj, yj, zj, Name, PropName, UserName, CSys)
        
        Returns:
            0 表示成功
        """
        user_name = str(self.no) if self.no is not None else ""
        section = self.section if self.section else "Default"

        # 检查索单元是否已存在
        if user_name:
            from PySap2000.logger import get_logger
            _log = get_logger("cable")
            try:
                existing = self.get_name_list(model)
                if user_name in existing:
                    _log.warning(f"Cable '{user_name}' already exists, skipped")
                    return -1
            except Exception:
                pass

        # 通过坐标创建
        if self.start_x is not None and self.end_x is not None:
            result = model.CableObj.AddByCoord(
                self.start_x, self.start_y or 0, self.start_z or 0,
                self.end_x, self.end_y or 0, self.end_z or 0,
                "",  # Name - 由程序返回
                section,  # PropName
                user_name,  # UserName
                self.coordinate_system  # CSys
            )
            
            assigned_name = com_data(result, 0)
            if assigned_name:
                self.no = assigned_name
            return com_ret(result)
        
        # 通过节点创建
        if self.start_point is not None and self.end_point is not None:
            # API: AddByPoint(Point1, Point2, Name, PropName, UserName)
            result = model.CableObj.AddByPoint(
                str(self.start_point),  # Point1
                str(self.end_point),    # Point2
                "",                      # Name - 由程序返回
                section,                 # PropName
                user_name                # UserName
            )
            
            assigned_name = com_data(result, 0)
            if assigned_name:
                self.no = assigned_name
            return com_ret(result)
        
        from PySap2000.exceptions import CableError
        raise CableError("Cable creation requires points or coordinates")
    
    def _get(self, model) -> 'Cable':
        """
        从 SAP2000 获取索单元数据
        
        API: GetPoints(Name, Point1, Point2) -> (Point1, Point2, ret)
        API: GetProperty(Name, PropName) -> (PropName, ret)
        """
        no_str = str(self.no)
        
        # 获取端点
        # API: GetPoints(Name, Point1, Point2) -> (Point1, Point2, ret)
        result = model.CableObj.GetPoints(no_str)
        self.start_point = com_data(result, 0)
        self.end_point = com_data(result, 1)
        ret = com_ret(result)
        
        if ret != 0:
            from PySap2000.exceptions import CableError
            raise CableError(f"Failed to get endpoints for Cable '{no_str}', ret={ret}")
        
        # 获取截面
        result = model.CableObj.GetProperty(no_str)
        section = com_data(result, 0)
        if section is not None:
            self.section = section
        
        # 获取索数据
        self._get_cable_data(model)
        
        # 获取 GUID
        self._get_guid(model)
        
        # 计算长度
        self._calculate_length(model)
        
        return self
    
    def _get_cable_data(self, model):
        """
        获取索数据
        
        API: GetCableData(Name, CableType, NumSegs, Weight, ProjectedLoad, 
                          UseDeformedGeom, ModelUsingFrames, Parameter[])
        返回: (CableType, NumSegs, Weight, ProjectedLoad, UseDeformedGeom, 
               ModelUsingFrames, Parameter[], ret)
        """
        try:
            result = model.CableObj.GetCableData(str(self.no))
            if com_data(result, 0) is not None:
                self.cable_type = CableType(com_data(result, 0))
                self.num_segs = com_data(result, 1)
                self.added_weight = com_data(result, 2)
                self.projected_load = com_data(result, 3)
                self.use_deformed_geom = com_data(result, 4)
                self.model_using_frames = com_data(result, 5)
                
                # 解析参数数组
                params = com_data(result, 6)
                if params and len(params) >= 11:
                    self.parameters = CableParameters(
                        tension_i_end=params[0],
                        tension_j_end=params[1],
                        horizontal_tension=params[2],
                        max_deformed_sag=params[3],
                        deformed_low_point_sag=params[4],
                        deformed_length=params[5],
                        deformed_relative_length=params[6],
                        max_undeformed_sag=params[7],
                        undeformed_low_point_sag=params[8],
                        undeformed_length=params[9],
                        undeformed_relative_length=params[10]
                    )
        except Exception:
            pass
    
    def _get_guid(self, model):
        """获取 GUID"""
        try:
            result = model.CableObj.GetGUID(str(self.no))
            guid = com_data(result, 0)
            if guid is not None:
                self.guid = guid
        except Exception:
            pass
    
    def _calculate_length(self, model):
        """计算索长度"""
        try:
            from PySap2000.structure_core.point import Point
            p1 = Point(no=self.start_point)._get(model)
            p2 = Point(no=self.end_point)._get(model)
            self.length = round(
                math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2 + (p2.z - p1.z)**2),
                3
            )
        except Exception:
            self.length = None
    
    @classmethod
    def _get_all(cls, model, nos: List = None) -> List['Cable']:
        """获取所有索单元或指定索单元"""
        if nos is None:
            nos = cls.get_name_list(model)
        
        cables = []
        for no in nos:
            cable = cls(no=no)
            cable._get(model)
            cables.append(cable)
        
        return cables
    
    def _delete(self, model) -> int:
        """从 SAP2000 删除索单元"""
        return model.CableObj.Delete(str(self.no))

    def change_name(self, model, new_name: str) -> int:
        """
        更改索单元名称

        Args:
            model: SapModel 对象
            new_name: 新名称

        Returns:
            0 表示成功
        """
        ret = model.CableObj.ChangeName(str(self.no), new_name)
        if ret == 0:
            self.no = new_name
        return ret
    
    def _update(self, model) -> int:
        """更新索单元属性"""
        from PySap2000.logger import get_logger
        _log = get_logger("cable")
        no_str = str(self.no)
        ret = 0
        if self.section:
            try:
                existing = self.get_section_name_list(model)
                if self.section not in existing:
                    _log.warning(f"CableSection '{self.section}' not found")
            except Exception:
                pass
            ret = model.CableObj.SetProperty(no_str, self.section)
        return ret
    
    # ==================== 静态方法 ====================
    
    @staticmethod
    def get_count(model) -> int:
        """
        获取索单元总数
        
        API: Count() -> Long
        """
        return model.CableObj.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """
        获取所有索单元名称列表
        
        API: GetNameList() -> (NumberNames, MyName[], ret)
        """
        result = model.CableObj.GetNameList(0, [])
        count = com_data(result, 0, 0)
        names = com_data(result, 1)
        if count > 0 and names:
            return list(names)
        return []
    
    @staticmethod
    def get_section_name_list(model) -> List[str]:
        """获取所有索截面名称列表"""
        result = model.PropCable.GetNameList(0, [])
        count = com_data(result, 0, 0)
        names = com_data(result, 1)
        if count > 0 and names:
            return list(names)
        return []
    
    # ==================== 实例方法 ====================
    
    def set_section(self, model, section_name: str) -> int:
        """设置截面"""
        self.section = section_name
        return model.CableObj.SetProperty(str(self.no), section_name)
    
    def set_guid(self, model, guid: str) -> int:
        """设置 GUID"""
        self.guid = guid
        return model.CableObj.SetGUID(str(self.no), guid)
    
    def set_cable_data(
        self,
        model,
        cable_type: CableType = None,
        num_segs: int = None,
        weight: float = None,
        projected_load: float = None,
        value: float = None,
        use_deformed_geom: bool = None,
        model_using_frames: bool = None
    ) -> int:
        """
        设置索数据
        
        API: SetCableData(Name, CableType, NumSegs, Weight, ProjectedLoad, 
                          Value, UseDeformedGeom, ModelUsingFrames) -> Long
        
        Args:
            model: SapModel 对象
            cable_type: 索定义类型
            num_segs: 内部分段数
            weight: 附加重量 [F/L]
            projected_load: 投影均布荷载 [F/L]
            value: 定义参数值，含义取决于 cable_type:
                   - CableType 1,2: 不使用
                   - CableType 3: I端张力 [F]
                   - CableType 4: J端张力 [F]
                   - CableType 5: 水平张力分量 [F]
                   - CableType 6: 最大垂直垂度 [L]
                   - CableType 7: 最低点垂直垂度 [L]
                   - CableType 8: 未变形长度 [L]
                   - CableType 9: 相对未变形长度
            use_deformed_geom: 是否使用变形几何
            model_using_frames: 是否使用框架单元建模
            
        Returns:
            0 表示成功
        """
        # 使用当前值或默认值
        if cable_type is not None:
            self.cable_type = cable_type
        if num_segs is not None:
            self.num_segs = num_segs
        if weight is not None:
            self.added_weight = weight
        if projected_load is not None:
            self.projected_load = projected_load
        if value is not None:
            self.cable_value = value
        if use_deformed_geom is not None:
            self.use_deformed_geom = use_deformed_geom
        if model_using_frames is not None:
            self.model_using_frames = model_using_frames
        
        return model.CableObj.SetCableData(
            str(self.no),
            int(self.cable_type),
            self.num_segs,
            self.added_weight,
            self.projected_load,
            self.cable_value,
            self.use_deformed_geom,
            self.model_using_frames
        )
    
    def get_cable_data(self, model) -> Optional[CableParameters]:
        """
        获取索数据
        
        Returns:
            CableParameters 对象，包含所有索参数
        """
        self._get_cable_data(model)
        return self.parameters
    
    def get_cable_geometry(
        self, 
        model, 
        csys: str = "Global"
    ) -> Optional[CableGeometry]:
        """
        获取索几何数据
        
        API: GetCableGeometry(Name, NumberPoints, x[], y[], z[], 
                              Sag[], Dist[], RD[], CSys) -> Long
        
        Args:
            model: SapModel 对象
            csys: 坐标系名称
            
        Returns:
            CableGeometry 对象
        """
        try:
            result = model.CableObj.GetCableGeometry(str(self.no), csys)
            if com_data(result, 0) is not None:
                return CableGeometry(
                    number_points=com_data(result, 0, 0),
                    x=tuple(com_data(result, 1, ())),
                    y=tuple(com_data(result, 2, ())),
                    z=tuple(com_data(result, 3, ())),
                    sag=tuple(com_data(result, 4, ())),
                    distance=tuple(com_data(result, 5, ())),
                    relative_distance=tuple(com_data(result, 6, ()))
                )
        except Exception:
            pass
        return None
