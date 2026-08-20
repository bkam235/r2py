"""Type/grammar-derived input generators for differential fuzzing (§7.8).

Generators are constrained to the observed domain — they vary lengths and
magnitudes of observed values, never invent new column names or data types.
"""
from __future__ import annotations

import random
from typing import Any, Protocol


class InputGenerator(Protocol):
    def sample(self, rng: random.Random) -> object: ...
    def boundary_cases(self) -> list[object]: ...


# ---------------------------------------------------------------------------
# Scalar generator
# ---------------------------------------------------------------------------

class ScalarGenerator:
    """Generates scalars of the same type as the observed value."""

    def __init__(self, observed: int | float | bool | str | None) -> None:
        self._observed = observed

    def sample(self, rng: random.Random) -> object:
        if self._observed is None:
            return None
        if isinstance(self._observed, bool):
            return rng.choice([True, False])
        if isinstance(self._observed, int):
            mag = max(abs(self._observed), 1)
            return rng.randint(-2 * mag, 2 * mag)
        if isinstance(self._observed, float):
            mag = max(abs(self._observed), 1.0)
            return rng.uniform(-2 * mag, 2 * mag)
        if isinstance(self._observed, str):
            # Vary length slightly; keep same charset
            chars = list(self._observed) or ["x"]
            length = rng.randint(max(0, len(self._observed) - 2), len(self._observed) + 3)
            return "".join(rng.choice(chars) for _ in range(length))
        return self._observed

    def boundary_cases(self) -> list[object]:
        if self._observed is None:
            return [None]
        if isinstance(self._observed, bool):
            return [True, False]
        if isinstance(self._observed, (int, float)) and not isinstance(self._observed, bool):
            return [0, 1, -1, 1e15, -1e15, None]
        if isinstance(self._observed, str):
            return ["", "x", self._observed]
        return [self._observed]


# ---------------------------------------------------------------------------
# Vector generator
# ---------------------------------------------------------------------------

class VectorGenerator:
    """Generates lists with the same element type as the observed list."""

    def __init__(self, observed: list) -> None:
        self._observed = observed
        self._elem_gen: InputGenerator
        if observed:
            self._elem_gen = generator_from_observed(observed[0])
        else:
            self._elem_gen = ScalarGenerator(0)
        self._obs_len = len(observed)

    def sample(self, rng: random.Random) -> list:
        candidates = [0, 1, self._obs_len, self._obs_len + 1, self._obs_len * 2]
        length = rng.choice([c for c in candidates if c >= 0])
        return [self._elem_gen.sample(rng) for _ in range(length)]

    def boundary_cases(self) -> list[object]:
        elem = self._observed[0] if self._observed else None
        cases: list[object] = [
            [],                         # empty
            [elem],                     # length-1 (the R scalar-vs-vector trap §3.7)
        ]
        if self._observed:
            cases.append([None] + list(self._observed[:2]))  # NA-present
        return cases


# ---------------------------------------------------------------------------
# DataFrame generator
# ---------------------------------------------------------------------------

class DataFrameGenerator:
    """Generates dicts-of-columns with the same schema as the observed dict."""

    def __init__(self, observed: dict) -> None:
        self._observed = observed
        self._col_gens: dict[str, InputGenerator] = {}
        for col, values in observed.items():
            if isinstance(values, list) and values:
                self._col_gens[col] = generator_from_observed(values[0])
            else:
                self._col_gens[col] = ScalarGenerator(0)
        self._obs_nrow = max((len(v) for v in observed.values() if isinstance(v, list)), default=1)

    def sample(self, rng: random.Random) -> dict:
        candidates = [0, 1, self._obs_nrow, self._obs_nrow * 2]
        nrow = rng.choice(candidates)
        return {
            col: [gen.sample(rng) for _ in range(nrow)]
            for col, gen in self._col_gens.items()
        }

    def boundary_cases(self) -> list[object]:
        return [
            {col: [] for col in self._col_gens},                    # 0 rows
            {col: [next(iter(self._observed.get(col, [0])))] for col in self._col_gens},  # 1 row
            {col: list(v) * 2 for col, v in self._observed.items() if isinstance(v, list)},  # ×2 rows
        ]


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def generator_from_observed(value: Any) -> InputGenerator:
    """Return the appropriate generator for an observed value."""
    if isinstance(value, dict):
        return DataFrameGenerator(value)
    if isinstance(value, list):
        return VectorGenerator(value)
    return ScalarGenerator(value)


def boundary_cases(value: Any) -> list[object]:
    """Return boundary cases for the observed value's type."""
    return generator_from_observed(value).boundary_cases()
