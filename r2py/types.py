"""Shared types used across all r2py stages."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ---------------------------------------------------------------------------
# Primitive aliases
# ---------------------------------------------------------------------------

EntityId = str
BranchId = str
PatternId = str


# ---------------------------------------------------------------------------
# §2.2 — Effect classes (one per row in the capture table)
# ---------------------------------------------------------------------------

class EffectClass(Enum):
    STDOUT   = "stdout"
    FILES    = "files"
    GRAPHICS = "graphics"
    DATA     = "data"
    HTML     = "html"
    ENV      = "env"
    WARNINGS = "warnings"
    RNG      = "rng"
    NETWORK  = "network"
    SYNTAX   = "syntax"   # used for SyntaxError FeedbackItems


# Set of effect classes a Sandbox.run() should capture.
CaptureSpec = frozenset[EffectClass]


# ---------------------------------------------------------------------------
# §3.3 — Entity kinds
# ---------------------------------------------------------------------------

class EntityKind(Enum):
    VARIABLE         = "Variable"
    CONSTANT         = "Constant"
    FUNCTION_DEF     = "FunctionDef"
    FUNCTION_CALL    = "FunctionCall"
    LIBRARY_IMPORT   = "LibraryImport"
    FORMULA          = "Formula"
    S4_CLASS         = "S4Class"
    R6_CLASS         = "R6Class"
    ENVIRONMENT      = "Environment"
    EXTERNAL_SYMBOL  = "ExternalSymbol"


# ---------------------------------------------------------------------------
# §8.3 — Edit kinds (closed taxonomy)
# ---------------------------------------------------------------------------

class EditKind(Enum):
    REPLACE_CALL              = "ReplaceCall"
    WRAP_VALUE                = "WrapValue"
    CHANGE_IMPORT             = "ChangeImport"
    INSERT_PREAMBLE           = "InsertPreamble"
    RENAME_VARIABLE           = "RenameVariable"
    RESTRUCTURE_CONTROL_FLOW  = "RestructureControlFlow"
    REPLACE_LIBRARY           = "ReplaceLibrary"
    RETRANSLATE_ENTITY        = "RetranslateEntity"
    RETRANSLATE_SCRIPT        = "RetranslateScript"


# ---------------------------------------------------------------------------
# §2.2, §2.3 — EffectBundle (ground truth of what a script did)
# ---------------------------------------------------------------------------

@dataclass
class EffectBundle:
    stdout:       str                    = ""
    stderr:       str                    = ""
    files:        dict[str, str]         = field(default_factory=dict)   # path → sha256 hex
    graphics:     list[bytes]            = field(default_factory=list)   # PNG bytes per figure
    data:         dict[str, object]      = field(default_factory=dict)   # var name → value
    html:         list[str]              = field(default_factory=list)   # rendered HTML strings
    env:          dict[str, object]      = field(default_factory=dict)   # options/envvar diff
    warnings:     list[str]             = field(default_factory=list)
    rng_log:      list[tuple]            = field(default_factory=list)   # (fn, args, value)
    network_log:  list[tuple]            = field(default_factory=list)   # (verb, target, hash)
    # Never silently empty — D2: every uncapturable call site must be named here.
    uncapturable: list[str]              = field(default_factory=list)
    exit_code:    int                    = 0
    run_time_s:   float                  = 0.0
    preamble_lines: int                  = 0   # lines before source in _r2py_script.py (for crash attribution)


# ---------------------------------------------------------------------------
# §7.3 — ComparatorResult
# ---------------------------------------------------------------------------

@dataclass
class ComparatorResult:
    effect_class: EffectClass
    score:        float                  # [0.0, 1.0]
    # "pass" | "fail" | "pass_via_fallback" | "uncomparable"
    # pass_via_fallback: infra-tagged failure rescued by embedding (§7.3.1)
    verdict:      str
    explanation:  str                    = ""
    # "value" = real numeric disagreement (never masked by fallback)
    # "infra"  = structural/serialisation mismatch (auto fallback allowed)
    failure_tag:  str | None             = None
    # Per-variable scores for DATA comparisons (variable_name → score in [0,1]).
    # Populated by DataComparator; empty for other effect classes.
    per_variable: dict[str, float]       = field(default_factory=dict)


# ---------------------------------------------------------------------------
# §7.4 — Score decomposition
# ---------------------------------------------------------------------------

@dataclass
class EntityScore:
    entity_id:           EntityId
    executed_ok:         bool            = False
    type_match:          float           = 0.0
    control_flow_match:  float           = 0.0
    data_output:         float           = 0.0
    variable_output:     float           = 0.0
    callable_output:     float           = 0.0
    side_effects:        float           = 0.0
    # Dimensions included in the weighted aggregate for this entity.
    active_dims:         frozenset[str]  = frozenset((
        "type_match", "control_flow_match", "data_output",
        "variable_output", "callable_output", "side_effects",
    ))
    # None when use_judge=False (D4 default); bool when judge is enabled.
    judge_pass:          bool | None     = None


@dataclass
class FeedbackItem:
    entity_id:    EntityId
    effect_class: EffectClass
    message:      str
    score:        float


@dataclass
class ComparisonDetail:
    """Concrete R-vs-Python output comparison for a single effect/entity pair."""
    effect_class: EffectClass
    entity_id:    EntityId
    r_value:      str       # serialized R output (truncated for prompt inclusion)
    py_value:     str       # serialized Python output (truncated for prompt inclusion)
    score:        float
    diff_summary: str       # human-readable "expected X, got Y" one-liner


@dataclass
class ScoreReport:
    aggregate:    float
    by_entity:    dict[EntityId, EntityScore]   = field(default_factory=dict)
    by_effect:    dict[EffectClass, float]       = field(default_factory=dict)
    uncomparable: list[EntityId]                 = field(default_factory=list)
    feedback:     list[FeedbackItem]             = field(default_factory=list)
    comparisons:  list[ComparisonDetail]         = field(default_factory=list)
    py_exit_code: int                            = 0
    py_entity_bundles: dict[EntityId, EffectBundle] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# §9.1 — TranslateResult (top-level API return type)
# ---------------------------------------------------------------------------

@dataclass
class TranslateResult:
    python_source:                str
    final_score:                  float
    iterations:                   int
    score_history:                list[ScoreReport]   = field(default_factory=list)
    pattern_evidence_added:       list[PatternId]     = field(default_factory=list)
    pattern_contradictions_added: list[PatternId]     = field(default_factory=list)
    final_exit_code:              int                 = 0
    final_score_report:           "ScoreReport | None" = None


# ---------------------------------------------------------------------------
# §4.1 — Beam search types
# ---------------------------------------------------------------------------

@dataclass
class Edit:
    """A typed edit proposal from Stage 3. Must be attributed before it can be
    applied (§8.5): pattern_id references an existing pattern or names a new one."""
    kind:        EditKind
    entity_ids:  list[EntityId]          = field(default_factory=list)
    params:      dict[str, object]       = field(default_factory=dict)
    # Required at proposal time; None only during construction before attribution.
    pattern_id:  PatternId | None        = None
    # LLM-authored guidance for a new pattern proposal (explore mode). Empty
    # string means the pattern is existing or the LLM didn't propose guidance.
    guidance:    str                     = ""


@dataclass
class Candidate:
    translation: str          # the Python source text
    score:       float
    decomp:      ScoreReport


# ---------------------------------------------------------------------------
# §3.3 — ScriptMap (minimal placeholder; stage1 fills out the full structure)
# ---------------------------------------------------------------------------

@dataclass
class ScriptMap:
    """Returned by analyze(). Stage1 populates all fields; the minimal definition
    here satisfies the top-level API type signature without importing stage1."""
    source: str = ""


# ---------------------------------------------------------------------------
# Progress events — emitted by the library, consumed by caller callbacks
# ---------------------------------------------------------------------------

@dataclass
class ProgressEvent:
    kind: str           # "analysis_done" | "seed_done" | "agent_start" | "done" | "seeded"
    iteration: "int | None" = None
    score: "float | None" = None
    entity_count: "int | None" = None
    count: "int | None" = None
    edit_kind: "str | None" = None
    entity_id: "str | None" = None
    outcome: "str | None" = None    # "accepted" | "tie" | "rejected"
