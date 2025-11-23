"""
Composites and Advanced Materials Module

Provides data on composite materials including carbon fiber,
fiberglass, Kevlar, and technical ceramics.
"""

from .database import CompositeDatabase, CompositeSpec, FiberType

__all__ = [
    "CompositeDatabase",
    "CompositeSpec",
    "FiberType",
]
