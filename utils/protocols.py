# -*- coding: utf-8 -*-
"""
protocols.py - Protocol definitions.

Defines structural protocols used throughout PySap2000 for type checking.

Usage:
    from PySap2000.utils.protocols import Creatable, Deletable

    def create_object(obj: Creatable) -> int:
        return obj._create(model)
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Creatable(Protocol):
    """Protocol for objects that can be created in SAP2000."""
    def _create(self, model) -> int:
        """Create the object in SAP2000."""
        ...


@runtime_checkable
class Deletable(Protocol):
    """Protocol for objects that can be deleted from SAP2000."""
    def _delete(self, model) -> int:
        """Delete the object from SAP2000."""
        ...


@runtime_checkable
class Gettable(Protocol):
    """Protocol for objects that can fetch their own data."""
    def _get(self, model):
        """Fetch object data from SAP2000."""
        ...


@runtime_checkable
class Updatable(Protocol):
    """Protocol for objects that can update themselves in SAP2000."""
    def _update(self, model) -> int:
        """Update the object in SAP2000."""
        ...
