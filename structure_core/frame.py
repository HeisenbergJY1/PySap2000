# -*- coding: utf-8 -*-
"""
frame.py - 框架杆件数据对象
对应 SAP2000 的 FrameObj

这是一个纯数据类，只包含核心 CRUD 操作。
扩展功能（荷载、释放、修改器等）请使用:
- loads/frame_load.py - 荷载函数
- types_for_frames/ - 其他扩展函数

API Reference:
    - AddByCoord(xi, yi, zi, xj, yj, zj, Name, PropName, UserName, CSys) -> Long
    - AddByPoint(Point1, Point2, Name, PropName, UserName) -> Long
    - GetPoints(Name, Point1, Point2) -> Long
    - GetSection(Name, PropName, SAuto) -> Long
    - SetSection(Name, PropName, ItemType) -> Long
    - Count() -> Long
    - GetNameList() -> (NumberNames, MyName[], ret)
    - Delete(Name) -> Long

Usage:
    from PySap2000.structure_core import Frame
    
    # 通过节点创建杆件
    frame = Frame(no=1, start_point="1", end_point="2", section="W14X30")
    frame._create(model)
    
    # 通过坐标创建杆件
    frame = Frame(
        no=2, 
        start_x=0, start_y=0, start_z=0,
        end_x=10, end_y=0, end_z=0,
        section="W14X30"
    )
    frame._create(model)
    
    # 获取杆件
    frame = Frame.get_by_name(model, "1")
    print(f"截面: {frame.section}")
"""

import math
from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Union, ClassVar

# 从 frame 模块导入枚举 (避免重复定义)
from PySap2000.frame.enums import (
    FrameType,
    FrameSectionType,
    FrameReleaseType,
    ItemType,
    SECTION_TYPE_NAMES,
)
from PySap2000.com_helper import com_ret, com_data


# 截面类型到获取方法的映射
SECTION_TYPE_METHOD_MAP = {
    FrameSectionType.I_SECTION: 'GetISection_1',
    FrameSectionType.PIPE: 'GetPipe',
    FrameSectionType.BOX: 'GetTube_1',
    FrameSectionType.CIRCLE: 'GetCircle',
    FrameSectionType.RECTANGULAR: 'GetRectangle',
}


@dataclass
class Frame:
    """
    框架杆件数据对象
    
    对应 SAP2000 的 FrameObj
    
    Attributes:
        no: 杆件编号/名称
        start_point: 起始节点编号 (I-End)
        end_point: 结束节点编号 (J-End)
        section: 截面名称
        s_auto: 自动选择列表名称
        material: 材料名称
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
    
    # 截面和材料
    section: str = ""
    s_auto: str = ""
    section_type: Optional[FrameSectionType] = None
    section_type_name: str = ""
    material: Optional[str] = None
    
    # 杆件属性
    type: FrameType = FrameType.BEAM
    local_axis_angle: float = 0.0
    advanced_axes: bool = False
    
    # 端部释放 (U1, U2, U3, R1, R2, R3)
    release_i: Tuple[bool, ...] = field(default_factory=lambda: (False,)*6)
    release_j: Tuple[bool, ...] = field(default_factory=lambda: (False,)*6)
    
    # 只读属性
    length: Optional[float] = field(default=None, repr=False)
    weight: float = 0.0  # 杆件重量 [kg]
    guid: Optional[str] = None
    
    # 可选属性
    coordinate_system: str = "Global"
    comment: str = ""
    
    # 类属性
    _object_type: ClassVar[str] = "FrameObj"
    
    # ==================== 核心 CRUD 方法 ====================
    
    def _create(self, model) -> int:
        """
        在 SAP2000 中创建杆件
        
        Returns:
            0 表示成功
        """
        from PySap2000.logger import get_logger
        _log = get_logger("frame")

        user_name = str(self.no) if self.no is not None else ""
        section = self.section if self.section else "Default"

        # 检查杆件名称是否已存在
        if user_name:
            try:
                existing = self.get_name_list(model)
                if user_name in existing:
                    _log.warning(f"Frame '{user_name}' already exists, skipped")
                    return -1
            except Exception:
                pass

        # 通过坐标创建
        if self.start_x is not None and self.end_x is not None:
            # 检查截面是否存在
            self._check_section_exists(model, section, _log)
            result = model.FrameObj.AddByCoord(
                self.start_x, self.start_y or 0, self.start_z or 0,
                self.end_x, self.end_y or 0, self.end_z or 0,
                "", section, user_name, self.coordinate_system
            )
            assigned_name = com_data(result, index=0)
            if assigned_name:
                self.no = assigned_name
            return com_ret(result)
        
        # 通过节点创建
        if self.start_point is not None and self.end_point is not None:
            # 检查节点是否存在
            self._check_points_exist(model, _log)
            # 检查截面是否存在
            self._check_section_exists(model, section, _log)

            result = model.FrameObj.AddByPoint(
                str(self.start_point), str(self.end_point),
                "", section, user_name
            )
            assigned_name = com_data(result, index=0)
            if assigned_name:
                self.no = assigned_name
            return com_ret(result)
        
        from PySap2000.exceptions import FrameError
        raise FrameError("Frame creation requires points or coordinates")

    def _check_points_exist(self, model, _log):
        """检查端点是否存在于模型中"""
        try:
            ret = model.PointObj.GetNameList(0, [])
            raw_names = com_data(ret, index=1)
            names = list(raw_names) if raw_names else []
            for pt, label in [(self.start_point, "start_point"), (self.end_point, "end_point")]:
                if str(pt) not in names:
                    _log.warning(f"Point {pt} ({label}) not found")
        except Exception:
            pass

    def _check_section_exists(self, model, section, _log):
        """检查截面是否存在于模型中"""
        if section == "Default":
            return
        try:
            ret = model.PropFrame.GetNameList(0, [])
            raw_names = com_data(ret, index=1)
            names = list(raw_names) if raw_names else []
            if section not in names:
                _log.warning(f"Section '{section}' not found")
        except Exception:
            pass
    
    def _get(self, model) -> 'Frame':
        """从 SAP2000 获取杆件数据"""
        no_str = str(self.no)
        
        # 获取端点
        result = model.FrameObj.GetPoints(no_str)
        self.start_point = com_data(result, index=0)
        self.end_point = com_data(result, index=1)
        if com_ret(result) != 0:
            from PySap2000.exceptions import FrameError
            raise FrameError(f"Failed to get endpoints for Frame '{no_str}'")
        
        # 获取截面
        result = model.FrameObj.GetSection(no_str)
        self.section = com_data(result, index=0, default="")
        s_auto_val = com_data(result, index=1)
        self.s_auto = s_auto_val if s_auto_val else ""
        
        # 获取截面类型
        self._get_section_type(model)
        
        # 获取局部轴
        self._get_local_axes(model)
        
        # 获取端部释放
        self._get_releases(model)
        
        # 获取 GUID
        self._get_guid(model)
        
        # 计算长度
        self._calculate_length(model)
        
        # 计算重量
        self._calculate_weight(model)
        
        return self
    
    def _delete(self, model) -> int:
        """从 SAP2000 删除杆件"""
        return model.FrameObj.Delete(str(self.no))

    def change_name(self, model, new_name: str) -> int:
        """
        更改杆件名称

        Args:
            model: SapModel 对象
            new_name: 新名称

        Returns:
            0 表示成功
        """
        ret = model.FrameObj.ChangeName(str(self.no), new_name)
        if ret == 0:
            self.no = new_name
        return ret
    
    def _update(self, model) -> int:
        """更新杆件截面"""
        from PySap2000.logger import get_logger
        _log = get_logger("frame")
        if self.section:
            self._check_section_exists(model, self.section, _log)
            return model.FrameObj.SetSection(str(self.no), self.section, ItemType.OBJECT)
        return 0
    
    # ==================== 内部辅助方法 ====================
    
    def _get_section_type(self, model):
        """获取截面类型"""
        if self.section:
            try:
                result = model.PropFrame.GetTypeOAPI(self.section)
                type_val = com_data(result, index=0)
                if type_val is not None:
                    self.section_type = FrameSectionType(type_val)
                    self.section_type_name = SECTION_TYPE_NAMES.get(
                        self.section_type, self.section_type.name
                    )
            except (ValueError, Exception):
                pass
    
    def _get_local_axes(self, model):
        """获取局部轴角度"""
        try:
            result = model.FrameObj.GetLocalAxes(str(self.no))
            self.local_axis_angle = com_data(result, index=0, default=0.0)
            self.advanced_axes = com_data(result, index=1, default=False)
        except Exception:
            pass
    
    def _get_releases(self, model):
        """获取端部释放"""
        try:
            result = model.FrameObj.GetReleases(str(self.no))
            ri = com_data(result, index=0)
            rj = com_data(result, index=1)
            if ri is not None:
                self.release_i = tuple(ri)
            if rj is not None:
                self.release_j = tuple(rj)
        except Exception:
            pass
    
    def _get_guid(self, model):
        """获取 GUID"""
        try:
            result = model.FrameObj.GetGUID(str(self.no))
            self.guid = com_data(result, index=0)
        except Exception:
            pass
    
    def _calculate_length(self, model, point_cache: dict = None):
        """
        计算杆件长度
        
        Args:
            model: SapModel 对象
            point_cache: 可选的节点坐标缓存 {name: (x, y, z)}，
                         批量操作时传入可避免重复 COM 调用
        """
        try:
            if point_cache is not None:
                p1 = point_cache.get(str(self.start_point))
                p2 = point_cache.get(str(self.end_point))
                if p1 and p2:
                    self.length = round(
                        math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2),
                        3
                    )
                    return
            # 回退到逐个查询
            from PySap2000.structure_core.point import Point
            p1 = Point(no=self.start_point)._get(model)
            p2 = Point(no=self.end_point)._get(model)
            self.length = round(
                math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2 + (p2.z - p1.z)**2),
                3
            )
        except Exception:
            self.length = None
    
    def _calculate_weight(self, model, *, _units_context: bool = False) -> float:
        """
        计算杆件重量 (kg)
        
        weight = weight_per_meter × length
        
        如果当前不是 N-m-C 单位，会临时切换获取数据。
        批量调用时可由调用方统一切换单位后传入 _units_context=True 避免反复切换。
        
        Args:
            model: SapModel 对象
            _units_context: True 表示调用方已切换到 N_M_C 单位，跳过切换
            
        Returns:
            杆件重量 (kg)，如果截面或长度无效则返回 0.0
        """
        if not self.section:
            self.weight = 0.0
            return 0.0
        
        try:
            from PySap2000.section.frame_section import FrameSection
            from PySap2000.global_parameters.units import Units, UnitSystem
            
            # _units_context 为 True 时表示调用方已切换到 N_M_C，跳过切换
            need_switch = False
            if not _units_context:
                current_units = Units.get_present_units(model)
                need_switch = current_units != UnitSystem.N_M_C
                if need_switch:
                    Units.set_present_units(model, UnitSystem.N_M_C)
            
            try:
                # 获取截面的单位长度重量 (kg/m)
                section = FrameSection.get_by_name(model, self.section)
                weight_per_meter = section.weight_per_meter
                
                if weight_per_meter <= 0:
                    self.weight = 0.0
                    return 0.0
                
                # 计算长度 (m)
                from PySap2000.structure_core.point import Point
                p1 = Point(no=self.start_point)._get(model)
                p2 = Point(no=self.end_point)._get(model)
                length_m = math.sqrt(
                    (p2.x - p1.x)**2 + (p2.y - p1.y)**2 + (p2.z - p1.z)**2
                )
                
                self.weight = weight_per_meter * length_m
            finally:
                if need_switch:
                    Units.set_present_units(model, current_units)
            
        except Exception:
            self.weight = 0.0
        
        return self.weight
    
    # ==================== 静态方法 ====================
    
    @staticmethod
    def get_count(model) -> int:
        """获取杆件总数"""
        return model.FrameObj.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """获取所有杆件名称列表"""
        result = model.FrameObj.GetNameList(0, [])
        names = com_data(result, index=1)
        if names is not None:
            return list(names)
        return []
    
    @staticmethod
    def get_section_name_list(model) -> List[str]:
        """获取所有截面名称列表"""
        result = model.PropFrame.GetNameList(0, [])
        names = com_data(result, index=1)
        if names is not None:
            return list(names)
        return []
    
    # ==================== 类方法 ====================
    
    @classmethod
    def get_by_name(cls, model, name: str) -> 'Frame':
        """
        获取指定名称的杆件
        
        Example:
            frame = Frame.get_by_name(model, "1")
            print(f"截面: {frame.section}")
        """
        frame = cls(no=name)
        frame._get(model)
        return frame
    
    @classmethod
    def get_all(cls, model, names: List[str] = None) -> List['Frame']:
        """
        获取所有杆件（使用 Database Tables API 批量获取，性能远优于逐个 COM 调用）
        
        原实现: N 个杆件 = N×6+ 次 COM 调用 + 2N 次节点查询
        新实现: 3 次 DB Tables 调用获取全部数据
        
        Args:
            model: SapModel 对象
            names: 可选，指定杆件名称列表。如果为 None，获取所有杆件
            
        Returns:
            Frame 对象列表
            
        Example:
            frames = Frame.get_all(model)
            for f in frames:
                print(f"{f.no}: {f.section}, L={f.length}")
        """
        from PySap2000.database_tables import DatabaseTables
        
        # 1) 批量获取杆件连接关系 (Frame名, 起点, 终点)
        conn_table = DatabaseTables.get_table_for_display(
            model, "Connectivity - Frame"
        )
        if conn_table is None or conn_table.num_records == 0:
            return []
        
        # 2) 批量获取截面分配
        sec_table = DatabaseTables.get_table_for_display(
            model, "Frame Section Assignments"
        )
        section_map = {}  # {frame_name: (section, s_auto)}
        if sec_table and sec_table.num_records > 0:
            for row in sec_table.to_dict_list():
                fname = row.get("Frame", "")
                section_map[fname] = (
                    row.get("AnalSect", ""),
                    row.get("AutoSelect", ""),
                )
        
        # 3) 批量获取节点坐标（用于计算长度）
        coord_table = DatabaseTables.get_table_for_display(
            model, "Joint Coordinates"
        )
        point_cache = {}  # {joint_name: (x, y, z)}
        if coord_table and coord_table.num_records > 0:
            for row in coord_table.to_dict_list():
                jname = row.get("Joint", "")
                try:
                    point_cache[jname] = (
                        float(row.get("XorR", 0)),
                        float(row.get("Y", 0)),
                        float(row.get("Z", 0)),
                    )
                except (ValueError, TypeError):
                    pass
        
        # 构建 name filter
        name_filter = set(str(n) for n in names) if names else None
        
        frames = []
        for row in conn_table.to_dict_list():
            frame_name = row.get("Frame", "")
            if name_filter and frame_name not in name_filter:
                continue
            
            start_pt = row.get("JointI", "")
            end_pt = row.get("JointJ", "")
            sec_info = section_map.get(frame_name, ("", ""))
            
            frame = cls(
                no=frame_name,
                start_point=start_pt,
                end_point=end_pt,
                section=sec_info[0],
                s_auto=sec_info[1] if sec_info[1] else "",
            )
            
            # 用缓存计算长度，不产生额外 COM 调用
            frame._calculate_length(model, point_cache=point_cache)
            
            frames.append(frame)
        
        return frames
    
    # ==================== 批量操作方法 ====================
    
    @classmethod
    def calculate_weights_batch(
        cls, 
        model, 
        frames: List['Frame'] = None
    ) -> dict:
        """
        批量计算杆件重量，只切换一次单位，用 Database Tables 预加载节点坐标
        
        Args:
            model: SapModel 对象
            frames: 杆件列表，如果为 None 则获取所有杆件
            
        Returns:
            dict: {杆件名称: 重量(kg)}
            
        Example:
            weights = Frame.calculate_weights_batch(model)
            total = sum(weights.values())
            print(f"总重量: {total:.2f} kg")
        """
        from PySap2000.global_parameters.units import Units, UnitSystem
        from PySap2000.section.frame_section import FrameSection
        from PySap2000.database_tables import DatabaseTables
        
        if frames is None:
            frames = cls.get_all(model)
        
        if not frames:
            return {}
        
        # 保存当前单位
        current_units = Units.get_present_units(model)
        need_switch = current_units != UnitSystem.N_M_C
        
        if need_switch:
            Units.set_present_units(model, UnitSystem.N_M_C)
        
        weights = {}
        section_cache = {}  # 缓存截面数据
        
        try:
            # 用 Database Tables 一次性获取所有节点坐标（替代逐个 COM 调用）
            point_cache = {}
            coord_table = DatabaseTables.get_table_for_display(
                model, "Joint Coordinates"
            )
            if coord_table and coord_table.num_records > 0:
                for row in coord_table.to_dict_list():
                    jname = row.get("Joint", "")
                    try:
                        point_cache[jname] = (
                            float(row.get("XorR", 0)),
                            float(row.get("Y", 0)),
                            float(row.get("Z", 0)),
                        )
                    except (ValueError, TypeError):
                        pass
            
            for frame in frames:
                try:
                    # 获取截面重量（带缓存）
                    if frame.section not in section_cache:
                        section = FrameSection.get_by_name(model, frame.section)
                        section_cache[frame.section] = section.weight_per_meter
                    
                    weight_per_meter = section_cache[frame.section]
                    if weight_per_meter <= 0:
                        weights[str(frame.no)] = 0.0
                        continue
                    
                    p1 = point_cache.get(str(frame.start_point))
                    p2 = point_cache.get(str(frame.end_point))
                    
                    if not p1 or not p2:
                        weights[str(frame.no)] = 0.0
                        continue
                    
                    # 计算长度和重量
                    length = math.sqrt(
                        (p2[0] - p1[0])**2 + 
                        (p2[1] - p1[1])**2 + 
                        (p2[2] - p1[2])**2
                    )
                    weights[str(frame.no)] = weight_per_meter * length
                    
                except Exception:
                    weights[str(frame.no)] = 0.0
        finally:
            if need_switch:
                Units.set_present_units(model, current_units)
        
        return weights
    
    @classmethod
    def create_batch(
        cls, 
        model, 
        frames: List['Frame']
    ) -> Tuple[List['Frame'], List[Tuple[str, str]]]:
        """
        批量创建杆件
        
        Args:
            model: SapModel 对象
            frames: 待创建的杆件列表
            
        Returns:
            Tuple[成功列表, 失败列表(名称, 错误信息)]
            
        Example:
            frames = [
                Frame(no="F1", start_point="1", end_point="2", section="W14X30"),
                Frame(no="F2", start_point="2", end_point="3", section="W14X30"),
            ]
            succeeded, failed = Frame.create_batch(model, frames)
            print(f"成功: {len(succeeded)}, 失败: {len(failed)}")
        """
        succeeded = []
        failed = []
        
        for frame in frames:
            try:
                ret = frame._create(model)
                if ret == 0:
                    succeeded.append(frame)
                else:
                    failed.append((str(frame.no), f"返回码: {ret}"))
            except Exception as e:
                failed.append((str(frame.no), str(e)))
        
        return succeeded, failed
    
    @classmethod
    def delete_batch(
        cls, 
        model, 
        names: List[str]
    ) -> Tuple[List[str], List[Tuple[str, str]]]:
        """
        批量删除杆件
        
        Args:
            model: SapModel 对象
            names: 待删除的杆件名称列表
            
        Returns:
            Tuple[成功名称列表, 失败列表(名称, 错误信息)]
            
        Example:
            succeeded, failed = Frame.delete_batch(model, ["F1", "F2", "F3"])
        """
        succeeded = []
        failed = []
        
        for name in names:
            try:
                ret = model.FrameObj.Delete(str(name))
                if ret == 0:
                    succeeded.append(name)
                else:
                    failed.append((name, f"返回码: {ret}"))
            except Exception as e:
                failed.append((name, str(e)))
        
        return succeeded, failed
    
    @classmethod
    def set_section_batch(
        cls, 
        model, 
        names: List[str], 
        section: str
    ) -> Tuple[List[str], List[Tuple[str, str]]]:
        """
        批量设置杆件截面
        
        Args:
            model: SapModel 对象
            names: 杆件名称列表
            section: 截面名称
            
        Returns:
            Tuple[成功名称列表, 失败列表(名称, 错误信息)]
            
        Example:
            succeeded, failed = Frame.set_section_batch(
                model, 
                ["F1", "F2", "F3"], 
                "W21X44"
            )
        """
        succeeded = []
        failed = []
        
        for name in names:
            try:
                ret = model.FrameObj.SetSection(str(name), section, ItemType.OBJECT)
                if ret == 0:
                    succeeded.append(name)
                else:
                    failed.append((name, f"返回码: {ret}"))
            except Exception as e:
                failed.append((name, str(e)))
        
        return succeeded, failed
