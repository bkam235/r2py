"""Comparator protocol and per-EffectClass implementations (§7.3)."""
from __future__ import annotations

from ...types import EffectClass
from .base import Comparator, text_similarity
from .data import DataComparator
from .env import EnvComparator
from .exit_code import ExitCodeComparator
from .files import FilesComparator
from .graphics import GraphicsComparator
from .html import HtmlComparator
from .network import NetworkComparator
from .rng import RngComparator
from .stdout import StdoutComparator
from .warnings import WarningsComparator

COMPARATORS: dict[EffectClass, Comparator] = {
    EffectClass.STDOUT:   StdoutComparator(),
    EffectClass.WARNINGS: WarningsComparator(),
    EffectClass.ENV:      EnvComparator(),
    EffectClass.FILES:    FilesComparator(),
    EffectClass.HTML:     HtmlComparator(),
    EffectClass.GRAPHICS: GraphicsComparator(),
    EffectClass.DATA:     DataComparator(),
    EffectClass.NETWORK:  NetworkComparator(),
    EffectClass.RNG:      RngComparator(),
    EffectClass.SYNTAX:   ExitCodeComparator(),
}

__all__ = [
    "Comparator",
    "COMPARATORS",
    "text_similarity",
    "DataComparator",
    "EnvComparator",
    "ExitCodeComparator",
    "FilesComparator",
    "GraphicsComparator",
    "HtmlComparator",
    "NetworkComparator",
    "RngComparator",
    "StdoutComparator",
    "WarningsComparator",
]
