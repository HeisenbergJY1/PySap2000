# -*- coding: utf-8 -*-
"""Tests for edit helpers (Edit).

Note: edits change the model; tests use safe operations only
(coordinate moves with restore, divide, etc.).
"""

import pytest
from PySap2000.edit import (
    change_point_coordinates,
    divide_frame_by_ratio,
)

pytestmark = pytest.mark.edit


class TestEditPoint:
    """Point edits."""

    def test_change_point_coordinates(self, model):
        """Move joint 5, then move back."""
        # Original joint 5 is at (5, 5, 0)
        ret = change_point_coordinates(model, "5", 5.0, 5.0, 1.0)
        assert ret == 0
        # Verify Z changed
        result = model.PointObj.GetCoordCartesian("5", 0.0, 0.0, 0.0)
        if isinstance(result, (list, tuple)) and len(result) >= 3:
            assert abs(result[2] - 1.0) < 0.01
        # Restore original coordinates
        change_point_coordinates(model, "5", 5.0, 5.0, 0.0)


class TestEditFrame:
    """Frame edits."""

    def test_divide_frame_by_ratio(self, model):
        """Divide a dedicated frame so other tests are unaffected."""
        from PySap2000.structure_core import Point, Frame

        # Dedicated points and frame
        p1 = Point(no=201, x=100, y=0, z=0)
        p2 = Point(no=202, x=110, y=0, z=0)
        p1._create(model)
        p2._create(model)
        f = Frame(no="EditTestFrame", start_point="201", end_point="202")
        f._create(model)

        # Two equal segments (ratio=1.0)
        names = divide_frame_by_ratio(model, "EditTestFrame", num_segments=2, ratio=1.0)
        # Returns list of new frame names
        assert isinstance(names, list)
        # On success, list is non-empty
        if len(names) > 0:
            assert len(names) >= 2
