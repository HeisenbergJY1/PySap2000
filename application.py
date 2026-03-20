# -*- coding: utf-8 -*-
"""
application.py - SAP2000 Application 连接管理器
参考 dlubal.api 设计模式

Usage:
    from PySap2000 import Application
    from PySap2000.structure_core import Point, Member
    
    with Application() as app:
        # 创建节点
        app.create_object(Point(no=1, x=0, y=0, z=0))
        app.create_object(Point(no=2, x=10, y=0, z=0))
        
        # 创建杆件
        app.create_object(Member(no=1, start_point=1, end_point=2, section="W14X30"))
        
        # 运行分析
        app.calculate()
        
        # 获取结果
        results = app.get_results()
"""

import gc
import comtypes.client
from typing import Optional, List, Union, TypeVar, Type
from PySap2000.exceptions import ConnectionError, ObjectError
from PySap2000.logger import get_logger
from PySap2000.com_helper import com_ret, com_data

_logger = get_logger("application")

T = TypeVar('T')


class Application:
    """
    SAP2000 应用程序连接管理器
    
    参考 dlubal.api.rfem.Application 设计:
    - Context Manager 管理连接生命周期
    - 统一的 CRUD 接口
    - 批量操作支持
    
    Raises:
        ConnectionError: 连接或启动 SAP2000 失败时抛出
    """
    
    def __init__(self, attach_to_instance: bool = True, program_path: str = ""):
        """
        初始化 SAP2000 连接
        
        Args:
            attach_to_instance: True 连接已运行的实例，False 启动新实例
            program_path: SAP2000 程序路径（启动新实例时使用）
        """
        self._sap_object = None
        self._model = None
        self._in_modification = False
        self._owns_instance = not attach_to_instance
        
        if attach_to_instance:
            self._attach_to_instance()
        else:
            self._start_application(program_path)

    def _ensure_connected(self):
        """
        检查 COM 连接是否有效，无效时抛出 ConnectionError。
        
        所有使用 self._model 的公共方法都应先调用此方法。
        
        Raises:
            ConnectionError: 当 COM 连接已断开时
        """
        if self._model is None:
            raise ConnectionError(
                "SAP2000 连接已断开。请重新创建 Application 实例或检查 SAP2000 是否仍在运行。"
            )
    
    def _attach_to_instance(self):
        """连接到已运行的 SAP2000 实例"""
        try:
            self._sap_object = comtypes.client.GetActiveObject('CSI.SAP2000.API.SapObject')
            self._model = self._sap_object.SapModel
            self._print_connection_info()
        except Exception as e:
            raise ConnectionError(f"Cannot connect to SAP2000, please make sure it is running: {e}")
    
    def _start_application(self, program_path: str = ""):
        """启动新的 SAP2000 实例"""
        try:
            helper = comtypes.client.CreateObject('SAP2000v1.Helper')
            try:
                helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
            except AttributeError:
                _logger.warning(
                    "comtypes.gen.SAP2000v1 未生成，尝试使用默认 Helper 接口。"
                    "如果失败，请先手动运行一次 comtypes.client.GetModule('SAP2000v1.tlb')"
                )
            if program_path:
                self._sap_object = helper.CreateObject(program_path)
            else:
                self._sap_object = helper.CreateObjectProgID('CSI.SAP2000.API.SapObject')
            self._sap_object.ApplicationStart()
            self._model = self._sap_object.SapModel
            self._print_connection_info()
        except ConnectionError:
            raise
        except Exception as e:
            raise ConnectionError(f"Cannot start SAP2000: {e}")
    
    def _print_connection_info(self):
        """打印连接信息并配置日志输出到模型文件夹"""
        from PySap2000.logger import setup_logger
        import os

        version_info = self._model.GetVersion()
        version = com_data(version_info, 0, default="")
        filename = self._model.GetModelFilename(False) or "Untitled"
        print(f"Connected to SAP2000 v{version} | {filename}")

        # 自动将日志输出到模型所在文件夹
        model_path = self._model.GetModelFilepath()
        if model_path:
            log_file = os.path.join(model_path, "pysap2000.log")
            setup_logger(level="INFO", log_file=log_file)
            _logger.info(f"Log file: {log_file}")
    
    def __enter__(self):
        """Context Manager 入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context Manager 退出，确保：
        1. 结束修改模式
        2. 释放 COM 句柄
        3. 如果是自己启动的实例，退出 SAP2000
        """
        self.disconnect()
        return False
    
    def disconnect(self):
        """
        显式断开连接并释放 COM 资源。
        
        可在不使用 Context Manager 时手动调用。
        多次调用是安全的（幂等）。
        """
        # 1. 结束修改模式
        if self._in_modification and self._model is not None:
            try:
                self.finish_modification()
            except Exception:
                _logger.debug("finish_modification failed during disconnect", exc_info=True)
        
        # 2. 释放 model 引用
        self._model = None
        
        # 3. 如果是自己启动的实例，退出 SAP2000
        if self._owns_instance and self._sap_object is not None:
            try:
                self._sap_object.ApplicationExit(False)
                _logger.info("SAP2000 application exited (owned instance)")
            except Exception:
                _logger.debug("ApplicationExit failed during disconnect", exc_info=True)
        
        # 4. 释放 COM 对象引用
        self._sap_object = None
        
        # 5. 强制 GC 回收 COM ref-count
        gc.collect()
    
    @property
    def model(self):
        """获取原始 SapModel 对象（用于高级操作或兼容旧代码）"""
        self._ensure_connected()
        return self._model

    # ==================== 修改模式管理 ====================
    
    def begin_modification(self):
        """
        开始批量修改模式
        禁用视图刷新以提升性能
        """
        self._ensure_connected()
        if not self._in_modification:
            self._model.View.RefreshView(0, False)
            self._in_modification = True
    
    def finish_modification(self):
        """
        结束批量修改模式
        刷新视图
        """
        self._ensure_connected()
        if self._in_modification:
            self._model.View.RefreshView(0, True)
            self._in_modification = False
    
    # ==================== 统一 CRUD 接口 ====================
    
    def _obj_desc(self, obj) -> str:
        """生成对象的简短描述，用于日志输出"""
        type_name = type(obj).__name__
        no = getattr(obj, 'no', None)
        if type_name == "Point":
            x = getattr(obj, 'x', 0)
            y = getattr(obj, 'y', 0)
            z = getattr(obj, 'z', 0)
            return f"Point({no}, x={x}, y={y}, z={z})"
        elif type_name == "Frame":
            sp = getattr(obj, 'start_point', '')
            ep = getattr(obj, 'end_point', '')
            sec = getattr(obj, 'section', '')
            return f"Frame({no}, {sp}->{ep}, sec={sec})"
        elif type_name == "Area":
            return f"Area({no})"
        elif type_name == "Cable":
            return f"Cable({no})"
        elif type_name == "Link":
            return f"Link({no})"
        elif no is not None:
            return f"{type_name}({no})"
        return type_name

    def create_object(self, obj) -> int:
        """
        创建单个对象
        
        Args:
            obj: 要创建的对象 (Point, Member, Material, Section 等)
            
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
            ObjectError: 对象不支持 create 操作
            
        Example:
            app.create_object(Point(no=1, x=0, y=0, z=0))
            app.create_object(Member(no=1, start_point=1, end_point=2))
        """
        self._ensure_connected()
        if hasattr(obj, '_create'):
            ret = obj._create(self._model)
            desc = self._obj_desc(obj)
            if ret == 0:
                _logger.info(f"Created {desc}")
            elif ret == -1:
                pass  # already exists, skipped
            else:
                _logger.warning(f"Failed to create {desc}, ret={ret}")
            return ret
        raise ObjectError(f"{type(obj).__name__} does not support create")
    
    def create_object_list(self, objs: List) -> int:
        """
        批量创建对象
        
        Args:
            objs: 对象列表
            
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        self.begin_modification()
        try:
            success = 0
            for obj in objs:
                if self.create_object(obj) == 0:
                    success += 1
            _logger.info(f"Batch created {success}/{len(objs)} objects")
        finally:
            self.finish_modification()
        return 0
    
    def get_object(self, obj: T) -> T:
        """
        获取单个对象
        
        Args:
            obj: 带有 no 属性的对象，用于指定要获取的对象编号
            
        Returns:
            填充了数据的对象
            
        Raises:
            ConnectionError: COM 连接已断开
            ObjectError: 对象不支持 get 操作
            
        Example:
            node = app.get_object(Node(no=1))
            print(node.x, node.y, node.z)
        """
        self._ensure_connected()
        if hasattr(obj, '_get'):
            result = obj._get(self._model)
            desc = self._obj_desc(result)
            _logger.info(f"Retrieved {desc}")
            return result
        raise ObjectError(f"{type(obj).__name__} does not support get")
    
    def get_object_list(self, obj_type: Type[T], nos: List[Union[int, str]] = None) -> List[T]:
        """
        批量获取对象
        
        Args:
            obj_type: 对象类型
            nos: 对象编号列表，None 表示获取所有
            
        Returns:
            对象列表
            
        Raises:
            ConnectionError: COM 连接已断开
            ObjectError: 对象不支持 get_all 操作
        """
        self._ensure_connected()
        if hasattr(obj_type, '_get_all'):
            return obj_type._get_all(self._model, nos)
        raise ObjectError(f"{obj_type.__name__} does not support get_all")
    
    def update_object(self, obj) -> int:
        """
        更新单个对象
        
        Args:
            obj: 要更新的对象
            
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
            ObjectError: 对象不支持 update 操作
        """
        self._ensure_connected()
        if hasattr(obj, '_update'):
            ret = obj._update(self._model)
            desc = self._obj_desc(obj)
            if ret == 0:
                _logger.info(f"Updated {desc}")
            else:
                _logger.warning(f"Failed to update {desc}, ret={ret}")
            return ret
        raise ObjectError(f"{type(obj).__name__} does not support update")

    def rename_object(self, obj, new_name: str) -> int:
        """
        重命名对象
        
        Args:
            obj: 要重命名的对象（需要 change_name 方法）
            new_name: 新名称
            
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
            ObjectError: 对象不支持 rename 操作
            
        Example:
            app.rename_object(Frame(no="1"), "F1")
        """
        self._ensure_connected()
        if hasattr(obj, 'change_name'):
            old_name = getattr(obj, 'no', '?')
            ret = obj.change_name(self._model, new_name)
            type_name = type(obj).__name__
            if ret == 0:
                _logger.info(f"Renamed {type_name}({old_name}) -> {new_name}")
            else:
                _logger.warning(f"Failed to rename {type_name}({old_name}) -> {new_name}, ret={ret}")
            return ret
        raise ObjectError(f"{type(obj).__name__} does not support rename")
    
    def delete_object(self, obj) -> int:
        """
        删除单个对象
        
        Args:
            obj: 要删除的对象（需要 no 属性）
            
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
            ObjectError: 对象不支持 delete 操作
        """
        self._ensure_connected()
        if hasattr(obj, '_delete'):
            ret = obj._delete(self._model)
            desc = self._obj_desc(obj)
            if ret == 0:
                _logger.info(f"Deleted {desc}")
            else:
                _logger.warning(f"Failed to delete {desc}, ret={ret}")
            return ret
        raise ObjectError(f"{type(obj).__name__} does not support delete")

    # ==================== 模型操作 ====================
    
    def new_model(self, units: int = 6) -> int:
        """
        创建新模型
        
        Args:
            units: 单位制 (6=kN_m_C, 9=N_mm_C, 10=kN_mm_C)
            
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        return com_ret(self._model.InitializeNewModel(units))
    
    def open_model(self, path: str) -> int:
        """
        打开模型文件
        
        Args:
            path: 模型文件路径
            
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        return com_ret(self._model.File.OpenFile(path))
    
    def save_model(self, path: str = "") -> int:
        """
        保存模型
        
        Args:
            path: 保存路径，空字符串表示保存到当前位置
            
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        if path:
            return com_ret(self._model.File.Save(path))
        return com_ret(self._model.File.Save())
    
    def close_model(self, save_changes: bool = False) -> int:
        """
        关闭当前模型
        
        Args:
            save_changes: 是否保存更改（True 时先调用 save_model）
            
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        if save_changes:
            self.save_model()
        # SAP2000 没有直接的 close model API，用 InitializeNewModel 重置
        return com_ret(self._model.InitializeNewModel(6))
    
    # ==================== 分析操作 ====================
    
    def calculate(self) -> int:
        """
        运行分析
        
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        com_ret(self._model.Analyze.SetRunCaseFlag("", True, True))
        return com_ret(self._model.Analyze.RunAnalysis())
    
    def delete_results(self) -> int:
        """
        删除分析结果
        
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        return com_ret(self._model.Analyze.DeleteResults("", True))
    
    # ==================== 结果获取 ====================
    
    def get_results(self, result_type: str, load_case: str = "", load_combo: str = ""):
        """
        获取分析结果
        
        Args:
            result_type: 结果类型 ('displacement', 'reaction', 'member_force' 等)
            load_case: 荷载工况名称
            load_combo: 荷载组合名称
            
        Returns:
            结果数据
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        self._model.Results.Setup.DeselectAllCasesAndCombosForOutput()
        if load_case:
            self._model.Results.Setup.SetCaseSelectedForOutput(load_case)
        if load_combo:
            self._model.Results.Setup.SetComboSelectedForOutput(load_combo)
        
        # 具体实现在 results 模块中
        return None
    
    # ==================== 辅助方法 ====================
    
    def set_units(self, units: int) -> int:
        """
        设置单位制
        
        Args:
            units: 单位制代码
                1 = lb_in_F
                2 = lb_ft_F
                3 = kip_in_F
                4 = kip_ft_F
                5 = kN_mm_C
                6 = kN_m_C
                7 = kgf_mm_C
                8 = kgf_m_C
                9 = N_mm_C
                10 = N_m_C
                11 = Ton_mm_C
                12 = Ton_m_C
                13 = kN_cm_C
                14 = kgf_cm_C
                15 = N_cm_C
                16 = Ton_cm_C
                
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        return com_ret(self._model.SetPresentUnits(units))
    
    # 单位代码映射表
    UNIT_NAMES = {
        1: "lb_in_F",
        2: "lb_ft_F",
        3: "kip_in_F",
        4: "kip_ft_F",
        5: "kN_mm_C",
        6: "kN_m_C",
        7: "kgf_mm_C",
        8: "kgf_m_C",
        9: "N_mm_C",
        10: "N_m_C",
        11: "Ton_mm_C",
        12: "Ton_m_C",
        13: "kN_cm_C",
        14: "kgf_cm_C",
        15: "N_cm_C",
        16: "Ton_cm_C",
    }
    
    def get_units(self) -> int:
        """
        获取当前单位制代码
        
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        return self._model.GetPresentUnits()
    
    def get_units_name(self) -> str:
        """
        获取当前单位制名称
        
        Returns:
            单位名称如 "kN_m_C", "N_mm_C" 等
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        code = self.get_units()
        return self.UNIT_NAMES.get(code, "Unknown")
    
    def get_database_units(self) -> int:
        """
        获取数据库单位制
        
        注意: 所有数据在模型内部以数据库单位存储，
        需要时转换为当前显示单位
        
        Returns:
            单位制代码 (同 set_units)
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        return self._model.GetDatabaseUnits()
    
    def get_database_units_name(self) -> str:
        """
        获取数据库单位制名称
        
        Returns:
            单位名称如 "kN_m_C", "N_mm_C" 等
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        code = self.get_database_units()
        return self.UNIT_NAMES.get(code, "Unknown")
    
    def refresh_view(self):
        """
        刷新视图
        
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        self._model.View.RefreshView(0, True)

    # ==================== 模型信息 ====================
    
    def get_model_filename(self, include_path: bool = True) -> str:
        """
        获取模型文件名
        
        Args:
            include_path: 是否包含完整路径
            
        Returns:
            模型文件名
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        return self._model.GetModelFilename(include_path)
    
    def get_model_filepath(self) -> str:
        """
        获取模型文件路径
        
        Returns:
            模型文件所在目录路径
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        return self._model.GetModelFilepath()
    
    def get_model_is_locked(self) -> bool:
        """
        获取模型锁定状态
        
        注意: 模型锁定时，大部分定义和分配无法修改
        
        Returns:
            True 表示已锁定
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        return self._model.GetModelIsLocked()
    
    def set_model_is_locked(self, lock_it: bool) -> int:
        """
        设置模型锁定状态
        
        Args:
            lock_it: True 锁定模型，False 解锁模型
            
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        return com_ret(self._model.SetModelIsLocked(lock_it))
    
    # ==================== 合并容差 ====================
    
    def get_merge_tol(self) -> float:
        """
        获取自动合并容差

        Returns:
            合并容差 [L]
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        result = self._model.GetMergeTol()
        return float(com_data(result, 0, default=result))

    
    def set_merge_tol(self, merge_tol: float) -> int:
        """
        设置自动合并容差
        
        Args:
            merge_tol: 合并容差 [L]
            
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        return com_ret(self._model.SetMergeTol(merge_tol))
    
    # ==================== 坐标系 ====================
    
    def get_present_coord_system(self) -> str:
        """
        获取当前坐标系名称

        Returns:
            坐标系名称
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        result = self._model.GetPresentCoordSystem()
        if isinstance(result, str):
            if result.upper() == "GLOBAL":
                return "Global"
        return result

    
    def set_present_coord_system(self, csys: str) -> int:
        """
        设置当前坐标系
        
        Args:
            csys: 坐标系名称
            
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        return com_ret(self._model.SetPresentCoordSystem(csys))
    
    # ==================== 项目信息 ====================
    
    def get_project_info(self) -> dict:
        """
        获取项目信息
        
        Returns:
            项目信息字典 {item_name: data}
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        result = self._model.GetProjectInfo()
        if isinstance(result, tuple) and len(result) >= 3:
            num_items = result[0]
            items = result[1]
            data = result[2]
            if num_items > 0 and items and data:
                return dict(zip(items, data))
        return {}
    
    def set_project_info(self, item: str, data: str) -> int:
        """
        设置项目信息
        
        Args:
            item: 项目信息项名称 (如 "Company Name", "Project Name")
            data: 项目信息数据
            
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        return com_ret(self._model.SetProjectInfo(item, data))
    
    # ==================== 用户注释 ====================
    
    def get_user_comment(self) -> str:
        """
        获取用户注释和日志
        
        Returns:
            用户注释内容
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        result = self._model.GetUserComment()
        if isinstance(result, tuple):
            return result[0]
        return ""
    
    def set_user_comment(
        self, 
        comment: str, 
        num_lines: int = 1, 
        replace: bool = False
    ) -> int:
        """
        设置用户注释
        
        Args:
            comment: 注释内容
            num_lines: 在注释前添加的空行数 (replace=True 时忽略)
            replace: True 替换所有现有注释，False 追加
            
        Returns:
            0 表示成功
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        return com_ret(self._model.SetUserComment(comment, num_lines, replace))
    
    # ==================== 版本信息 ====================
    
    def get_version(self) -> tuple:
        """
        获取 SAP2000 版本信息
        
        Returns:
            (版本名称, 版本号) 如 ("26.3.0", 26.3)
            
        Raises:
            ConnectionError: COM 连接已断开
        """
        self._ensure_connected()
        result = self._model.GetVersion()
        version = com_data(result, 0, default="")
        version_number = com_data(result, 1, default=0.0)
        return (version, version_number)
