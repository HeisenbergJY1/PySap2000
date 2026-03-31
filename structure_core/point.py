# -*- coding: utf-8 -*-
"""
point.py - Point data object.

Maps to SAP2000 `PointObj`.

Design principles:
- `Point` is a pure data class containing only core point attributes
- extended behavior such as supports, springs, mass, and loads lives in the
  `point/` and `loads/` modules
- this keeps the object model simple and agent-friendly

Usage example:
    from PySap2000.structure_core import Point
    from PySap2000.point import set_point_support, PointSupportType
    
    # Create a point
    p = Point(no="1", x=0, y=0, z=0)
    p._create(model)
    
    # Assign supports using point-module helpers
    set_point_support(model, "1", PointSupportType.FIXED)
"""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Union, ClassVar
from enum import IntEnum

from PySap2000.com_helper import com_ret, com_data


class PointCoordinateSystemType(IntEnum):
    """Point coordinate system type."""
    CARTESIAN = 0
    CYLINDRICAL = 1
    SPHERICAL = 2


@dataclass
class Point:
    """
    Point data object corresponding to SAP2000 `PointObj`.

    This is a pure data class containing only basic point attributes.
    Use helper functions from the `point` and `loads` modules for extended
    behavior:
    - supports: `point.set_point_support()`
    - springs: `point.set_point_spring()`
    - mass: `point.set_point_mass()`
    - loads: `loads.set_point_load_force()`
    - constraints: `point.set_point_constraint()`
    - local axes: `point.set_point_local_axes()`
    - panel zone data: `point.set_point_panel_zone()`
    
    Attributes:
        no: Point name or identifier
        x, y, z: Cartesian coordinates
        coordinate_system: Coordinate system name
        merge_off: Whether automatic merge is disabled
        merge_number: Merge group identifier
        comment: Comment text
        guid: Globally unique identifier
    """
    
    # Required attribute
    no: Union[int, str] = None
    
    # Cartesian coordinates
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    
    # Cylindrical coordinates (r, theta, z)
    r: Optional[float] = None
    theta: Optional[float] = None
    
    # Spherical coordinates (r, a, b)
    a: Optional[float] = None
    b: Optional[float] = None
    
    # Optional attributes
    coordinate_system: str = "Global"
    coordinate_system_type: PointCoordinateSystemType = PointCoordinateSystemType.CARTESIAN
    
    # Merge control
    merge_off: bool = False
    merge_number: int = 0
    
    # Selection state
    selected: bool = False
    
    # Other metadata
    comment: str = ""
    guid: Optional[str] = None
    
    # Class metadata
    _object_type: ClassVar[str] = "PointObj"

    # ==================== Create Methods ====================
    
    def _create(self, model) -> int:
        """
        Create the point in SAP2000.
        
        Args:
            model: `SapModel` object
            
        Returns:
            `0` on success, non-zero on failure
        """
        from PySap2000.logger import get_logger
        from PySap2000.utils.validation import validate_coordinate
        _log = get_logger("point")

        validate_coordinate(self.x, "x")
        validate_coordinate(self.y, "y")
        validate_coordinate(self.z, "z")

        user_name = str(self.no) if self.no is not None else ""

        # Check whether the point already exists
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
        """Create the point using Cartesian coordinates."""
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
        """Create the point using cylindrical coordinates."""
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
        """Create the point using spherical coordinates."""
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
        """Parse the result returned by the create call."""
        assigned_name = com_data(result, 0)
        ret = com_ret(result)
        if assigned_name:
            self.no = assigned_name
        return ret

    # ==================== Get Methods ====================
    
    def _get(self, model) -> 'Point':
        """
        Fetch basic point data from SAP2000.

        Only core attributes such as coordinates, selection state, and GUID are
        loaded here. Extended attributes such as supports and springs should be
        fetched through helper functions in the `point` module.
        
        Args:
            model: `SapModel` object
            
        Returns:
            The same `Point` object populated with data
        """
        self._get_coord_cartesian(model)
        self._get_selected(model)
        self._get_guid(model)
        return self
    
    def _get_coord_cartesian(self, model) -> Tuple[float, float, float]:
        """
        Fetch Cartesian coordinates.

        API: `GetCoordCartesian(Name, x, y, z, CSys="Global")`
        Returns: `[x, y, z, ret]`
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
        """Fetch cylindrical coordinates."""
        result = model.PointObj.GetCoordCylindrical(
            str(self.no), 0.0, 0.0, 0.0, self.coordinate_system
        )
        
        self.r = com_data(result, 0, default=0.0)
        self.theta = com_data(result, 1, default=0.0)
        self.z = com_data(result, 2, default=self.z)
        return (self.r, self.theta, self.z)
    
    def get_coord_spherical(self, model) -> Tuple[float, float, float]:
        """Fetch spherical coordinates."""
        result = model.PointObj.GetCoordSpherical(
            str(self.no), 0.0, 0.0, 0.0, self.coordinate_system
        )
        
        self.r = com_data(result, 0, default=0.0)
        self.a = com_data(result, 1, default=0.0)
        self.b = com_data(result, 2, default=0.0)
        return (self.r, self.a, self.b)
    
    def _get_selected(self, model) -> bool:
        """Fetch the point selection state."""
        try:
            result = model.PointObj.GetSelected(str(self.no), False)
            self.selected = com_data(result, 0, default=False)
            return self.selected
        except Exception:
            pass
        return False
    
    def _get_guid(self, model):
        """Fetch the point GUID."""
        try:
            result = model.PointObj.GetGUID(str(self.no))
            self.guid = com_data(result, 0, default=self.guid)
        except Exception:
            pass

    # ==================== Public Query Methods ====================
    
    @classmethod
    def get_all(cls, model, names: List[str] = None) -> List['Point']:
        """
        Fetch all points using the Database Tables API.

        Args:
            model: `SapModel` object
            names: Optional list of point names; `None` fetches all points

        Returns:
            List of populated `Point` objects

        Example:
            points = Point.get_all(model)
            for p in points:
                print(f"{p.no}: ({p.x}, {p.y}, {p.z})")
        """
        from PySap2000.database_tables import DatabaseTables

        # Retrieve all point coordinates in a single call
        table_data = DatabaseTables.get_table_for_display(
            model, "Joint Coordinates"
        )

        if table_data is None or table_data.num_records == 0:
            return []

        # Convert names to a set for fast filtering
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
        Fetch a point by name.
        
        Args:
            model: `SapModel` object
            name: Point name
            
        Returns:
            A populated `Point` object
            
        Example:
            point = Point.get_by_name(model, "1")
            print(f"Coordinates: {point.x}, {point.y}, {point.z}")
        """
        point = cls(no=name)
        point._get(model)
        return point
    
    @staticmethod
    def get_count(model) -> int:
        """
        Return the total number of points.
        
        Args:
            model: `SapModel` object
            
        Returns:
            Number of points
        """
        return model.PointObj.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """
        Return the list of all point names.
        
        Args:
            model: `SapModel` object
            
        Returns:
            List of point names
        """
        result = model.PointObj.GetNameList(0, [])
        
        names = com_data(result, 1)
        if names is not None:
            return list(names)
        return []

    # ==================== Delete Methods ====================
    
    def _delete(self, model) -> int:
        """
        Delete a special point in SAP2000.

        Note:
            SAP2000 does not provide `PointObj.Delete()`.

        SAP2000 point deletion rules:
        - regular points are deleted automatically when no objects are attached
        - special points must be deleted with `DeleteSpecialPoint()` after all
          connected objects are removed
        
        Returns:
            `0` on success, non-zero on failure
        """
        from PySap2000.point.enums import ItemType
        return model.PointObj.DeleteSpecialPoint(str(self.no), ItemType.OBJECT)

    # ==================== Special Point Methods ====================
    
    def set_special_point(self, model, special: bool = True) -> int:
        """
        Mark or unmark the point as a special point.

        Special points are not auto-deleted when they have no connected objects.
        
        Args:
            model: `SapModel` object
            special: `True` to mark as special, `False` to clear the flag
            
        Returns:
            `0` on success
        """
        from PySap2000.point.enums import ItemType
        return model.PointObj.SetSpecialPoint(str(self.no), special, ItemType.OBJECT)
    
    def get_special_point(self, model) -> bool:
        """
        Return whether the point is marked as a special point.
        
        Returns:
            `True` if special, otherwise `False`
        """
        try:
            result = model.PointObj.GetSpecialPoint(str(self.no), False)
            return com_data(result, 0, default=False)
        except Exception:
            pass
        return False

    # ==================== Selection Methods ====================
    
    def set_selected(self, model, selected: bool = True) -> int:
        """
        Set the point selection state.
        
        Args:
            model: `SapModel` object
            selected: `True` to select, `False` to deselect
            
        Returns:
            `0` on success
        """
        from PySap2000.point.enums import ItemType
        self.selected = selected
        return model.PointObj.SetSelected(str(self.no), selected, ItemType.OBJECT)
    
    def get_selected(self, model) -> bool:
        """Return the point selection state."""
        return self._get_selected(model)

    # ==================== Name and GUID Methods ====================
    
    def change_name(self, model, new_name: str) -> int:
        """
        Change the point name.
        
        Args:
            model: `SapModel` object
            new_name: New point name
            
        Returns:
            `0` on success
        """
        ret = model.PointObj.ChangeName(str(self.no), new_name)
        if ret == 0:
            self.no = new_name
        return ret
    
    def get_guid(self, model) -> Optional[str]:
        """
        Return the point GUID.
        
        Returns:
            GUID string, or `None` on failure
        """
        self._get_guid(model)
        return self.guid
    
    def set_guid(self, model, guid: str = "") -> int:
        """
        Set the point GUID.
        
        Args:
            model: `SapModel` object
            guid: GUID string. If empty, SAP2000 creates a new one automatically
            
        Returns:
            `0` on success
        """
        ret = model.PointObj.SetGUID(str(self.no), guid)
        if ret == 0:
            self._get_guid(model)
        return ret

    # ==================== Group Methods ====================
    
    def set_group_assign(self, model, group_name: str, remove: bool = False) -> int:
        """
        Assign the point to a group or remove it from a group.
        
        Args:
            model: `SapModel` object
            group_name: Group name
            remove: `True` to remove, `False` to add
            
        Returns:
            `0` on success
        """
        from PySap2000.point.enums import ItemType
        return model.PointObj.SetGroupAssign(str(self.no), group_name, remove, ItemType.OBJECT)
    
    def get_group_assign(self, model) -> Optional[List[str]]:
        """
        Return the groups assigned to the point.
        
        Returns:
            List of group names
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

    # ==================== Connectivity Methods ====================
    
    def get_connectivity(self, model) -> dict:
        """
        Return connectivity information for the point.
        
        Returns:
            dict: {
                'num_items': int,
                'object_types': list,  # Object types (1=Point, 2=Frame, 3=Cable, etc.)
                'object_names': list,  # Object names
                'point_numbers': list  # Point numbers on those objects
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

    # ==================== Element Methods ====================
    
    def get_elm(self, model) -> Optional[str]:
        """
        Return the corresponding analysis element name for the point.
        
        Returns:
            Element name, or `None` if unavailable
        """
        try:
            result = model.PointObj.GetElm(str(self.no), "")
            elm_name = com_data(result, 0)
            ret = com_data(result, 1, default=-1)
            return elm_name if ret == 0 else None
        except Exception:
            pass
        return None

    # ==================== Transformation Matrix Methods ====================
    
    def get_transformation_matrix(self, model, is_global: bool = True) -> Optional[List[float]]:
        """
        Return the point transformation matrix.
        
        Args:
            model: `SapModel` object
            is_global: `True` for global coordinates, `False` for local
            
        Returns:
            A 12-value transformation matrix list, or `None` on failure
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
