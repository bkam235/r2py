"""Comparator protocol and per-EffectClass implementations (§7.3)."""
from __future__ import annotations

from ...types import EffectClass
from .base import Comparator, text_similarity
from .data import DataComparator
from .env import EnvComparator
from .files import FilesComparator
from .graphics import GraphicsComparator
from .html import HtmlComparator
from .stdout import StdoutComparator
from .warnings import WarningsComparator

# RNG and NETWORK are capture/replay (not direct comparison) — excluded from registry.
COMPARATORS: dict[EffectClass, Comparator] = {
    EffectClass.STDOUT:   StdoutComparator(),
    EffectClass.WARNINGS: WarningsComparator(),
    EffectClass.ENV:      EnvComparator(),
    EffectClass.FILES:    FilesComparator(),
    EffectClass.HTML:     HtmlComparator(),
    EffectClass.GRAPHICS: GraphicsComparator(),
    EffectClass.DATA:     DataComparator(),
}

__all__ = [
    "Comparator",
    "COMPARATORS",
    "text_similarity",
    "DataComparator",
    "EnvComparator",
    "FilesComparator",
    "GraphicsComparator",
    "HtmlComparator",
    "StdoutComparator",
    "WarningsComparator",
]
