"""Stage 1 SideEffect type and static prediction table."""
from __future__ import annotations

from dataclasses import dataclass

from ..types import EntityId, EffectClass, EffectBundle


@dataclass
class SideEffect:
    kind: EffectClass
    entity_id: EntityId
    is_predicted: bool          # True = static AST inference; False = confirmed by sandbox
    actual_bundle: EffectBundle | None = None


# Maps an R function name (unqualified) to the effect classes it is predicted to produce.
# Minimal set — Stage 0 dynamic execution fills in anything not listed here.
STATIC_PREDICTIONS: dict[str, list[EffectClass]] = {
    # File I/O
    "write.csv":    [EffectClass.FILES],
    "write.table":  [EffectClass.FILES],
    "write.csv2":   [EffectClass.FILES],
    "writeLines":   [EffectClass.FILES],
    "saveRDS":      [EffectClass.FILES],
    "save":         [EffectClass.FILES],
    "sink":         [EffectClass.FILES],
    # Graphics
    "plot":         [EffectClass.GRAPHICS],
    "barplot":      [EffectClass.GRAPHICS],
    "hist":         [EffectClass.GRAPHICS],
    "boxplot":      [EffectClass.GRAPHICS],
    "ggplot":       [EffectClass.GRAPHICS],
    "ggsave":       [EffectClass.GRAPHICS, EffectClass.FILES],
    "dev.copy":     [EffectClass.GRAPHICS],
    "png":          [EffectClass.GRAPHICS],
    "pdf":          [EffectClass.GRAPHICS],
    # Stdout
    "print":        [EffectClass.STDOUT],
    "cat":          [EffectClass.STDOUT],
    "sprintf":      [EffectClass.STDOUT],
    "writeLines":   [EffectClass.STDOUT],
    # Warnings / messages
    "message":      [EffectClass.WARNINGS],
    "warning":      [EffectClass.WARNINGS],
    "stop":         [EffectClass.WARNINGS],
    # Environment
    "library":      [EffectClass.ENV],
    "require":      [EffectClass.ENV],
    "Sys.setenv":   [EffectClass.ENV],
    "options":      [EffectClass.ENV],
    "setwd":        [EffectClass.ENV],
    # RNG
    "set.seed":     [EffectClass.RNG],
    "runif":        [EffectClass.RNG],
    "rnorm":        [EffectClass.RNG],
    "sample":       [EffectClass.RNG],
    "rbinom":       [EffectClass.RNG],
}
