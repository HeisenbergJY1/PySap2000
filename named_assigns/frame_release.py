# -*- coding: utf-8 -*-
"""
frame_release.py - Named frame end releases

Wraps SAP2000 `NamedAssign.ReleaseFrame`.

Creates reusable frame end-release definitions that can be referenced by multiple frame objects.

SAP2000 API:
- NamedAssign.ReleaseFrame.ChangeName
- NamedAssign.ReleaseFrame.Count
- NamedAssign.ReleaseFrame.Delete
- NamedAssign.ReleaseFrame.GetNameList
- NamedAssign.ReleaseFrame.GetReleases
- NamedAssign.ReleaseFrame.SetReleases

Release arrays (6 booleans):
- [0] U1: Translation along local-1
- [1] U2: Translation along local-2
- [2] U3: Translation along local-3
- [3] R1: Rotation about local-1
- [4] R2: Rotation about local-2
- [5] R3: Rotation about local-3

Partial-fixity spring values:
- U1, U2, U3: [F/L] force / length
- R1, R2, R3: [FL/rad] moment / radian
"""

from dataclasses import dataclass, field
from typing import List, Optional, ClassVar
from PySap2000.com_helper import com_ret, com_data


@dataclass
class NamedFrameRelease:
    """
    Named frame end release
    
    Attributes:
        name: Release definition name
        ii: I-end releases `[U1, U2, U3, R1, R2, R3]`
        jj: J-end releases `[U1, U2, U3, R1, R2, R3]`
        start_value: I-end partial-fixity spring values `[U1, U2, U3, R1, R2, R3]`
        end_value: J-end partial-fixity spring values `[U1, U2, U3, R1, R2, R3]`
    """
    name: str = ""
    ii: List[bool] = field(default_factory=lambda: [False] * 6)
    jj: List[bool] = field(default_factory=lambda: [False] * 6)
    start_value: List[float] = field(default_factory=lambda: [0.0] * 6)
    end_value: List[float] = field(default_factory=lambda: [0.0] * 6)
    
    _object_type: ClassVar[str] = "NamedAssign.ReleaseFrame"
    
    # Convenience properties - I end
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
    
    # Convenience properties - J end
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
        """Set the I end to pinned (`R2`, `R3` released)"""
        self.ii[4] = True  # R2
        self.ii[5] = True  # R3
    
    def set_pinned_j(self):
        """Set the J end to pinned (`R2`, `R3` released)"""
        self.jj[4] = True  # R2
        self.jj[5] = True  # R3
    
    def set_pinned_both(self):
        """Set both ends to pinned"""
        self.set_pinned_i()
        self.set_pinned_j()
    
    def _create(self, model) -> int:
        """
        Create or update a named end release
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` on success
        """
        from PySap2000.com_helper import com_ret
        return com_ret(model.NamedAssign.ReleaseFrame.SetReleases(
            self.name, self.ii, self.jj, self.start_value, self.end_value
        ))
    
    def _get(self, model) -> int:
        """
        Load end-release data from the model
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` on success
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
        Delete the named end release
        
        Args:
            model: SAP2000 SapModel object
            
        Returns:
            `0` on success
        """
        from PySap2000.com_helper import com_ret
        return com_ret(model.NamedAssign.ReleaseFrame.Delete(self.name))
    
    def change_name(self, model, new_name: str) -> int:
        """
        Rename the end release
        
        Args:
            model: SAP2000 SapModel object
            new_name: New name
            
        Returns:
            `0` on success
        """
        from PySap2000.com_helper import com_ret
        ret = com_ret(model.NamedAssign.ReleaseFrame.ChangeName(self.name, new_name))
        if ret == 0:
            self.name = new_name
        return ret
    
    @staticmethod
    def get_count(model) -> int:
        """Get the number of end-release definitions"""
        return model.NamedAssign.ReleaseFrame.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """Get all end-release names"""
        result = model.NamedAssign.ReleaseFrame.GetNameList(0, [])
        names = com_data(result, 1)
        if names:
            return list(names)
        return []
    
    @classmethod
    def get_by_name(cls, model, name: str) -> Optional["NamedFrameRelease"]:
        """Get an end release by name"""
        release = cls(name=name)
        ret = release._get(model)
        if ret == 0:
            return release
        return None
    
    @classmethod
    def get_all(cls, model) -> List["NamedFrameRelease"]:
        """Get all end releases"""
        names = cls.get_name_list(model)
        result = []
        for name in names:
            release = cls.get_by_name(model, name)
            if release:
                result.append(release)
        return result
    
    @classmethod
    def create_pinned_i(cls, name: str) -> "NamedFrameRelease":
        """Create a release definition pinned at the I end"""
        release = cls(name=name)
        release.set_pinned_i()
        return release
    
    @classmethod
    def create_pinned_j(cls, name: str) -> "NamedFrameRelease":
        """Create a release definition pinned at the J end"""
        release = cls(name=name)
        release.set_pinned_j()
        return release
    
    @classmethod
    def create_pinned_both(cls, name: str) -> "NamedFrameRelease":
        """Create a release definition pinned at both ends"""
        release = cls(name=name)
        release.set_pinned_both()
        return release
