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
    # None when use_judge=False (D4 default); bool when judge is enabled.
    judge_pass:          bool | None     = None


@dataclass
class FeedbackItem:
    entity_id:    EntityId
    effect_class: EffectClass
    message:      str
    score:        float


@dataclass
class ScoreReport:
    aggregate:    float
    by_entity:    dict[EntityId, EntityScore]   = field(default_factory=dict)
    by_effect:    dict[EffectClass, float]       = field(default_factory=dict)
    uncomparable: list[EntityId]                 = field(default_factory=list)
    feedback:     list[FeedbackItem]             = field(default_factory=list)


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


@dataclass
class Candidate:
    translation: str          # the Python source text
    score:       float
    decomp:      ScoreReport


@dataclass
class Proposal:
    candidate:    str
    new_score:    float
    new_decomp:   ScoreReport
    edit:         Edit
    parent_score: float


# ---------------------------------------------------------------------------
# §12.6 — Data logging types for optional learned components (D6)
# ---------------------------------------------------------------------------

@dataclass
class RetrievalEpisodeCandidate:
    pattern_id:         str
    rank:               int
    package_match:      bool
    ast_shape_sim:      float
    token_sim:          float
    confidence:         str    # "confirmed" | "tentative"
    evidence_count:     int
    contradiction_count: int
    last_review:        str    # ISO date or ""


@dataclass
class RetrievalEpisode:
    query_entity_id:   str
    query_entity_kind: str
    query_package:     str
    query_entity_name: str
    candidates:        list[RetrievalEpisodeCandidate]
    chosen_pattern_id: str | None
    exploit_mode:      bool
    outcome:           str | None   # "accepted"|"tie"|"rejected"; None until stamped by loop
    score_delta:       float | None
    script_id:         str
    iteration:         int


@dataclass
class PolicyTransition:
    entity_id:           str
    entity_kind:         str
    package:             str
    type_match:          float
    control_flow_match:  float
    data_output:         float
    variable_output:     float
    callable_output:     float
    side_effects:        float
    edit_kind:           str        # EditKind.value
    exploit_mode:        bool
    outcome:             str | None # "accepted"|"tie"|"rejected"; None until stamped
    score_delta:         float | None
    script_id:           str
    iteration:           int


class EpisodeCollector:
    """Passed optionally through stage3 to capture retrieval + policy metadata."""
    def __init__(self) -> None:
        self.episodes: list = []    # list[RetrievalEpisode]
        self.transitions: list = [] # list[PolicyTransition]


# ---------------------------------------------------------------------------
# §3.3 — ScriptMap (minimal placeholder; stage1 fills out the full structure)
# ---------------------------------------------------------------------------

@dataclass
class ScriptMap:
    """Returned by analyze(). Stage1 populates all fields; the minimal definition
    here satisfies the top-level API type signature without importing stage1."""
    source: str = ""
