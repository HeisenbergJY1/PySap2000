# -*- coding: utf-8 -*-
"""
link.py - Link element data object.

Maps to SAP2000 `LinkObj`.

This is a pure data class containing only core CRUD operations.
For extended behavior, use:
- `loads/link_load.py` for loads
- the `link/` package for local axes, properties, and related helpers

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
    - GetElm(Name, Elm) -> Long  # Returns a single analysis element name

Usage:
    from PySap2000.structure_core import Link
    from PySap2000.link.enums import LinkType, LinkItemType
    
    # Create a two-joint link
    link = Link(no=1, start_point="1", end_point="2", property_name="Linear1")
    link._create(model)
    
    # Create a grounded single-joint link
    link = Link(no=2, start_point="3", is_single_joint=True, property_name="Spring1")
    link._create(model)
    
    # Fetch a link
    link = Link.get_by_name(model, "1")
"""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Union, ClassVar

from PySap2000.link.enums import (
    LinkType, LinkDirectionalType, LinkItemType, AxisVectorOption
)
from PySap2000.com_helper import com_ret, com_data


@dataclass
class LinkLocalAxesAdvanced:
    """
    Advanced local-axis settings for a link object.
    
    Attributes:
        link_name: Link object name
        active: Whether advanced local axes are active
        ax_vect_opt: Axis vector option (1=coord direction, 2=two joints, 3=user vector)
        ax_csys: Axis coordinate system
        ax_dir: Axis direction array `[primary, secondary]`
        ax_pt: Axis reference points `[pt1, pt2]`
        ax_vect: Axis vector `[x, y, z]`
        plane2: Plane-2 definition (12 or 13)
        pl_vect_opt: Plane vector option
        pl_csys: Plane coordinate system
        pl_dir: Plane direction array `[primary, secondary]`
        pl_pt: Plane reference points `[pt1, pt2]`
        pl_vect: Plane vector `[x, y, z]`
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
    Link element data object.

    Maps to SAP2000 `LinkObj` and is used for springs, dampers,
    isolation bearings, and similar components.
    
    Attributes:
        no: Link identifier or name
        start_point: Start point name (I-End)
        end_point: End point name (J-End); `None` or `""` for single-joint links
        is_single_joint: Whether this is a grounded single-joint link
        property_name: Link property name
        fd_property_name: Frequency-dependent property name, if any
        local_axis_angle: Local axis rotation angle [deg]
        advanced_axes: Whether advanced local-axis parameters are active
        type: Link type
    """
    
    # Required fields
    no: Union[int, str] = None
    
    # Defined by point names
    start_point: Optional[Union[int, str]] = None
    end_point: Optional[Union[int, str]] = None
    
    # Defined by coordinates
    start_x: Optional[float] = None
    start_y: Optional[float] = None
    start_z: Optional[float] = None
    end_x: Optional[float] = None
    end_y: Optional[float] = None
    end_z: Optional[float] = None
    
    # Properties
    property_name: str = ""
    fd_property_name: Optional[str] = None
    type: Optional[LinkType] = None
    directional_type: LinkDirectionalType = LinkDirectionalType.TWO_JOINT
    
    # Single-joint connection flag
    is_single_joint: bool = False
    
    # Local-axis angle
    local_axis_angle: float = 0.0
    advanced_axes: bool = False
    
    # Optional properties
    coordinate_system: str = "Global"
    comment: str = ""
    guid: Optional[str] = None
    
    # Class properties
    _object_type: ClassVar[str] = "LinkObj"
    
    # ==================== Core CRUD methods ====================
    
    def _create(self, model) -> int:
        """
        Create link object in SAP2000.
        
        Returns:
            `0` on success
        """
        from PySap2000.logger import get_logger
        _log = get_logger("link")

        user_name = str(self.no) if self.no is not None else ""
        prop = self.property_name if self.property_name else "Default"

        # Check whether it already exists
        if user_name:
            try:
                existing = self.get_name_list(model)
                if user_name in existing:
                    _log.warning(f"Link '{user_name}' already exists, skipped")
                    return -1
            except Exception:
                pass

        # Create by coordinates
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
        
        # Create by point names
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
        """Fetch link-object data from SAP2000"""
        no_str = str(self.no)
        
        # Get endpoints
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
        
        # Get properties
        result = model.LinkObj.GetProperty(no_str, "")
        self.property_name = com_data(result, 0, "")
        
        # Get frequency-dependent property
        self._get_property_fd(model)
        
        # Get local-axis angle
        self._get_local_axes(model)
        
        # Get GUID
        self._get_guid(model)
        
        return self
    
    def _delete(self, model) -> int:
        """Delete link object from SAP2000"""
        return model.LinkObj.Delete(str(self.no))
    
    def _update(self, model) -> int:
        """Update link-object properties."""
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
    
    # ==================== Internal helper methods ====================
    
    def _get_local_axes(self, model):
        """Get local-axis angle."""
        try:
            result = model.LinkObj.GetLocalAxes(str(self.no), 0.0, False)
            self.local_axis_angle = com_data(result, 0, 0.0)
            self.advanced_axes = com_data(result, 1, False)
        except Exception:
            pass
    
    def _get_property_fd(self, model):
        """Get frequency-dependent property."""
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
        """Get GUID"""
        try:
            result = model.LinkObj.GetGUID(str(self.no), "")
            guid = com_data(result, 0)
            if guid is not None:
                self.guid = guid
        except Exception:
            pass
    
    # ==================== Static methods ====================
    
    @staticmethod
    def get_count(model) -> int:
        """Get total number of link objects"""
        return model.LinkObj.Count()
    
    @staticmethod
    def get_name_list(model) -> List[str]:
        """Get all link-object names"""
        result = model.LinkObj.GetNameList(0, [])
        count = com_data(result, 0, 0)
        names = com_data(result, 1)
        if count > 0 and names:
            return list(names)
        return []
    
    @staticmethod
    def get_property_name_list(model) -> List[str]:
        """Get all link-property names."""
        result = model.PropLink.GetNameList(0, [])
        count = com_data(result, 0, 0)
        names = com_data(result, 1)
        if count > 0 and names:
            return list(names)
        return []

    
    # ==================== Class methods ====================
    
    @classmethod
    def get_by_name(cls, model, name: str) -> 'Link':
        """
        Get link object by name
        
        Example:
            link = Link.get_by_name(model, "1")
            print(f"Properties: {link.property_name}")
        """
        link = cls(no=name)
        link._get(model)
        return link
    
    @classmethod
    def get_all(cls, model, names: List[str] = None) -> List['Link']:
        """
        Get all link objects
        
        Example:
            links = Link.get_all(model)
            for lk in links:
                print(f"{lk.no}: {lk.property_name}")
        """
        if names is None:
            names = cls.get_name_list(model)
        return [cls.get_by_name(model, name) for name in names]
    
    # ==================== Instance methods ====================
    
    def set_property(self, model, property_name: str) -> int:
        """Set link property."""
        self.property_name = property_name
        return model.LinkObj.SetProperty(str(self.no), property_name)
    
    def set_guid(self, model, guid: str) -> int:
        """Set GUID."""
        self.guid = guid
        return model.LinkObj.SetGUID(str(self.no), guid)
    
    def get_local_axes(self, model) -> Tuple[float, bool]:
        """
        Get local-axis angle.
        
        Returns:
            (angle, advanced) - angle[deg]and whether advanced settings are used
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
        Set local-axis angle.
        
        Args:
            model: SapModel object
            angle: Rotation angle of local-2 and local-3 about positive local-1 [deg]
            item_type: Operation scope
            
        Returns:
            `0` on success
        """
        self.local_axis_angle = angle
        return model.LinkObj.SetLocalAxes(str(self.no), angle, int(item_type))
    
    def get_property_fd(self, model) -> Optional[str]:
        """
        Get frequency-dependent property.
        
        Returns:
            Frequency-dependent property name, or `None` if not set
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
        Set frequency-dependent property.
        
        Args:
            model: SapModel object
            prop_name: Frequency-dependent property name; `None` or `"None"` clears it
            item_type: Operation scope
            
        Returns:
            `0` on success
        """
        if prop_name is None:
            prop_name = "None"
        self.fd_property_name = prop_name if prop_name != "None" else None
        return model.LinkObj.SetPropertyFD(str(self.no), prop_name, int(item_type))

    
    # ==================== Advanced local-axis methods ====================
    
    def get_local_axes_advanced(self, model) -> 'LinkLocalAxesAdvanced':
        """
        Get advanced local-axis settings
        
        API: GetLocalAxesAdvanced(Name, Active, AxVectOpt, AxCSys, AxDir[], AxPt[], AxVect[], 
                                   Plane2, PlVectOpt, PlCSys, PlDir[], PlPt[], PlVect[])
        
        Returns:
            LinkLocalAxesAdvanced data object
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
        Set advanced local axes
        
        API: SetLocalAxesAdvanced(Name, Active, AxVectOpt, AxCSys, AxDir[], AxPt[], AxVect[],
                                   Plane2, PlVectOpt, PlCSys, PlDir[], PlPt[], PlVect[], ItemType)
        
        Args:
            model: SapModel object
            active: Whether advanced local axes are active
            ax_vect_opt: axis-vector option (1=coordinate direction, 2=two points, 3=user vector)
            ax_csys: axis coordinate system
            ax_dir: axis direction array [primary, secondary]
            ax_pt: axis reference-point array [pt1, pt2]
            ax_vect: axis vector [x, y, z]
            plane2: Plane-2 definition (`12` or `13`)
            pl_vect_opt: plane-vector option
            pl_csys: plane coordinate system
            pl_dir: plane direction array [primary, secondary]
            pl_pt: plane reference-point array [pt1, pt2]
            pl_vect: plane vector [x, y, z]
            item_type: Operation scope
            
        Returns:
            `0` on success
        """
        # Set defaults
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
    
    # ==================== Convenience creation methods ====================
    
    @staticmethod
    def add_grounded(
        model,
        no: str,
        point: Union[int, str],
        property_name: str = "Default"
    ) -> int:
        """
        Create grounded link object (single-joint)
        
        Args:
            model: SapModel object
            no: Link object ID
            point: Point ID
            property_name: Link-property name
            
        Returns:
            `0` on success
        """
        result = model.LinkObj.AddByPoint(
            str(point), "", "", True, property_name, no
        )
        return com_ret(result)
    
    # ==================== Analysis-element methods ====================
    
    def get_elm(self, model) -> Optional[str]:
        """
        Get analysis-element name
        
        API: GetElm(Name, Elm) -> Long
        Note: Each `Link` object maps to one analysis element, so a single string is returned
        
        Returns:
            Analysis-element name, or `None` on failure
        """
        result = model.LinkObj.GetElm(str(self.no), "")
        
        ret = com_ret(result)
        if ret == 0:
            return com_data(result, 0)
        
        return None
    
    # ==================== Transformation-matrix methods ====================
    
    def get_transformation_matrix(self, model, is_global: bool = True) -> List[float]:
        """
        Get transformation matrix
        
        Args:
            model: SapModel object
            is_global: Whether to use global coordinate system
            
        Returns:
            3x3 transformation matrix (9values)
        """
        result = model.LinkObj.GetTransformationMatrix(str(self.no), [], is_global)
        
        matrix = com_data(result, 0)
        if matrix:
            return list(matrix)
        
        return [1, 0, 0, 0, 1, 0, 0, 0, 1]
    
    # ==================== Selection methods ====================
    
    def get_selected(self, model) -> bool:
        """Get selection state"""
        result = model.LinkObj.GetSelected(str(self.no), False)
        return com_data(result, 0, False)
    
    def set_selected(
        self, 
        model, 
        selected: bool,
        item_type: LinkItemType = LinkItemType.OBJECT
    ) -> int:
        """Set selection state"""
        return model.LinkObj.SetSelected(str(self.no), selected, int(item_type))
    
    # ==================== Group-assignment methods ====================
    
    def get_group_assign(self, model) -> List[str]:
        """Get group assignments"""
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
        """Set group assignments"""
        return model.LinkObj.SetGroupAssign(str(self.no), group_name, remove, int(item_type))
    
    # ==================== Name methods ====================
    
    def change_name(self, model, new_name: str) -> int:
        """Change link-object name"""
        ret = model.LinkObj.ChangeName(str(self.no), new_name)
        if ret == 0:
            self.no = new_name
        return ret
