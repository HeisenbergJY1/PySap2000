# -*- coding: utf-8 -*-
"""
frame_release.py - 命名杆件端部释放

对应 SAP2000 的 NamedAssign.ReleaseFrame API

创建可复用的杆件端部释放定义，可被多个杆件引用。

SAP2000 API:
- NamedAssign.ReleaseFrame.ChangeName
- NamedAssign.ReleaseFrame.Count
- NamedAssign.ReleaseFrame.Delete
- NamedAssign.ReleaseFrame.GetNameList
- NamedAssign.ReleaseFrame.GetReleases
- NamedAssign.ReleaseFrame.SetReleases

释放数组 (6个布尔值):
- [0] U1: 局部1方向平动
- [1] U2: 局部2方向平动
- [2] U3: 局部3方向平动
- [3] R1: 绕局部1轴转动
- [4] R2: 绕局部2轴转动
- [5] R3: 绕局部3轴转动

部分固定弹簧值:
- U1, U2, U3: [F/L] 力/长度
- R1, R2, R3: [FL/rad] 力矩/弧度
"""

from dataclasses import dataclass, field
from typing import List, Optional, ClassVar
from PySap2000.com_helper import com_ret, com_data


@dataclass
class NamedFrameRelease:
    """
    命名杆件端部释放
    
    Attributes:
        name: 释放定义名称
        ii: I端释放 [U1, U2, U3, R1, R2, R3]
        jj: J端释放 [U1, U2, U3, R1, R2, R3]
        start_value: I端部分固定弹簧值 [U1, U2, U3, R1, R2, R3]
        end_value: J端部分固定弹簧值 [U1, U2, U3, R1, R2, R3]
    """
    name: str = ""
    ii: List[bool] = field(default_factory=lambda: [False] * 6)
    jj: List[bool] = field(default_factory=lambda: [False] * 6)
    start_value: List[float] = field(default_factory=lambda: [0.0] * 6)
    end_value: List[float] = field(default_factory=lambda: [0.0] * 6)
    
    _object_type: ClassVar[str] = "NamedAssign.ReleaseFrame"
    
    # 便捷属性 - I端
    @property
    def i_u1(self) -> bool:
        return self.ii[0]
    
    @i_u1.setter
    def i_u1(self, value: bool):
        self.ii[0] = value
    
    @property
    def i_u2(self) -> bool:
        return self.ii[1]
    
    @i_u2.setter
    def i_u2(self, value: bool):
        self.ii[1] = value
    
    @property
    def i_u3(self) -> bool:
        return self.ii[2]
    
    @i_u3.setter
    def i_u3(self, value: bool):
        self.ii[2] = value
    
    @property
    def i_r1(self) -> bool:
        return self.ii[3]
    
    @i_r1.setter
    def i_r1(self, value: bool):
        self.ii[3] = value
    
    @property
    def i_r2(self) -> bool:
        return self.ii[4]
    
    @i_r2.setter
    def i_r2(self, value: bool):
        self.ii[4] = value
    
    @property
    def i_r3(self) -> bool:
        return self.ii[5]
    
    @i_r3.setter
    def i_r3(self, value: bool):
        self.ii[5] = value
    
    # 便捷属性 - J端
    @property
    def j_u1(self) -> bool:
        return self.jj[0]
    
    @j_u1.setter
    def j_u1(self, value: bool):
        self.jj[0] = value
    
    @property
    def j_u2(self) -> bool:
        return self.jj[1]
    
    @j_u2.setter
    def j_u2(self, value: bool):
        self.jj[1] = value
    
    @property
    def j_u3(self) -> bool:
        return self.jj[2]
    
    @j_u3.setter
    def j_u3(self, value: bool):
        self.jj[2] = value
    
    @property
    def j_r1(self) -> bool:
        return self.jj[3]
    
    @j_r1.setter
    def j_r1(self, value: bool):
        self.jj[3] = value
    
    @property
    def j_r2(self) -> bool:
        return self.jj[4]
    
    @j_r2.setter
    def j_r2(self, value: bool):
        self.jj[4] = value
    
    @property
    def j_r3(self) -> bool:
        return self.jj[5]
    
    @j_r3.setter
    def j_r3(self, value: bool):
        self.jj[5] = value
    
    def set_pinned_i(self):
        """设置I端为铰接 (释放R2, R3)"""
        self.ii[4] = True  # R2
        self.ii[5] = True  # R3
    
    def set_pinned_j(self):
        """设置J端为铰接 (释放R2, R3)"""
        self.jj[4] = True  # R2
        self.jj[5] = True  # R3
    
    def set_pinned_both(self):
        """设置两端为铰接"""
        self.set_pinned_i()
        self.set_pinned_j()
    
    def _create(self, model) -> int:
        """
        创建或更新命名端部释放
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
        """
        from PySap2000.com_helper import com_ret
        return com_ret(model.NamedAssign.ReleaseFrame.SetReleases(
            self.name, self.ii, self.jj, self.start_value, self.end_value
        ))
    
    def _get(self, model) -> int:
        """
        从模型获取端部释放数据
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
        """
        result = model.NamedAssign.ReleaseFrame.GetReleases(
            self.name,
            [False] * 6,
            [False] * 6,
            [0.0] * 6,
            [0.0] * 6
        )
        
        ii = com_data(result, 0)
        jj = com_data(result, 1)
        start_val = com_data(result, 2)
        end_val = com_data(result, 3)
        ret = com_ret(result)
        
        if isinstance(ret, int) and ret == 0:
            if ii and len(ii) >= 6:
                self.ii = list(ii)
            if jj and len(jj) >= 6:
                self.jj = list(jj)
            if start_val and len(start_val) >= 6:
                self.start_value = list(start_val)
            if end_val and len(end_val) >= 6:
                self.end_value = list(end_val)
        return ret if isinstance(ret, int) else -1
    
    def _delete(self, model) -> int:
        """
        删除命名端部释放
        
        Args:
            model: SapModel 对象
            
        Returns:
            0 表示成功
        """
        from PySap2000.com_helper import com_ret
        return com_ret(model.NamedAssign.ReleaseFrame.Delete(self.name))
    
    def change_name(self, model, new_name: str) -> int:
        """
        重命名端部释放
        
        Args:
            model: SapModel 对象
            new_name: 新名称
            
        Returns:
            0 表示成功
        """
        from PySap2000.com_helper import com_ret
        ret = com_ret(model.NamedAssign.ReleaseFrame.ChangeName(self.name, new_name))
        if ret == 0:
            self.name = new_name
        return ret
    
    @staticmethod
    def get_count(model) -> int:
        """获取端部释放数量"""
        return model.NamedAssign.ReleaseFrame.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """获取所有端部释放名称"""
        result = model.NamedAssign.ReleaseFrame.GetNameList(0, [])
        names = com_data(result, 1)
        if names:
            return list(names)
        return []
    
    @classmethod
    def get_by_name(cls, model, name: str) -> Optional["NamedFrameRelease"]:
        """按名称获取端部释放"""
        release = cls(name=name)
        ret = release._get(model)
        if ret == 0:
            return release
        return None
    
    @classmethod
    def get_all(cls, model) -> List["NamedFrameRelease"]:
        """获取所有端部释放"""
        names = cls.get_name_list(model)
        result = []
        for name in names:
            release = cls.get_by_name(model, name)
            if release:
                result.append(release)
        return result
    
    @classmethod
    def create_pinned_i(cls, name: str) -> "NamedFrameRelease":
        """创建I端铰接的释放定义"""
        release = cls(name=name)
        release.set_pinned_i()
        return release
    
    @classmethod
    def create_pinned_j(cls, name: str) -> "NamedFrameRelease":
        """创建J端铰接的释放定义"""
        release = cls(name=name)
        release.set_pinned_j()
        return release
    
    @classmethod
    def create_pinned_both(cls, name: str) -> "NamedFrameRelease":
        """创建两端铰接的释放定义"""
        release = cls(name=name)
        release.set_pinned_both()
        return release
