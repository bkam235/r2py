"""Optional LinUCB contextual bandit edit policy (§12.6 B).

Feature extraction and LinUCB logic are pure Python + numpy.
Training lives in scripts/train_policy.py but calls train() from this module.

The action space is the closed EditKind taxonomy (~7 arms). Context features
are the 6 EntityScore sub-scores plus a hashed entity-kind indicator and a
hashed package indicator (8 features total).
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types import EntityScore

# Number of context features (must match extract_context()).
_N_FEATURES = 8
# LinUCB exploration parameter.
_ALPHA = 1.0


@dataclass
class BanditArm:
    """Per-arm LinUCB matrices."""
    A: list = field(default_factory=list)   # d×d (stored as flat list of lists)
    b: list = field(default_factory=list)   # d-vector


@dataclass
class BanditModel:
    """LinUCB model: one arm per EditKind."""
    arms: dict[str, BanditArm] = field(default_factory=dict)
    n_features: int = _N_FEATURES
    alpha: float = _ALPHA
    trained_date: str = ""


# ---------------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------------

def extract_context(
    entity_score: "EntityScore",
    entity_kind: str,
    package: str,
) -> list[float]:
    """Return an 8-dimensional context vector for the bandit.

    Features:
      0–5  EntityScore sub-scores (type_match, control_flow_match, data_output,
           variable_output, callable_output, side_effects)
      6    entity kind hash mod 16, normalised to [0,1]
      7    package hash mod 16, normalised to [0,1]
    """
    scores = [
        getattr(entity_score, "type_match", 0.0),
        getattr(entity_score, "control_flow_match", 0.0),
        getattr(entity_score, "data_output", 0.0),
        getattr(entity_score, "variable_output", 0.0),
        getattr(entity_score, "callable_output", 0.0),
        getattr(entity_score, "side_effects", 0.0),
    ]
    kind_hash = int(hashlib.md5(entity_kind.encode()).hexdigest(), 16) % 16 / 15.0
    pkg_hash = int(hashlib.md5(package.encode()).hexdigest(), 16) % 16 / 15.0
    return scores + [kind_hash, pkg_hash]


# ---------------------------------------------------------------------------
# LinUCB scoring and action selection
# ---------------------------------------------------------------------------

def _init_arm(d: int) -> BanditArm:
    """Initialise LinUCB arm with identity A and zero b."""
    A = [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]
    b = [0.0] * d
    return BanditArm(A=A, b=b)


def ucb_score(arm: BanditArm, context: list[float], alpha: float = _ALPHA) -> float:
    """Compute LinUCB upper confidence bound for one arm."""
    d = len(context)
    A = arm.A
    b = arm.b
    # θ = A^{-1} b  (solve via Cholesky-free Gaussian elimination on small d)
    theta = _solve(A, b)
    # x^T A^{-1} x  (A_inv x via solve)
    A_inv_x = _solve(A, context)
    cb = sum(context[i] * A_inv_x[i] for i in range(d))
    exploit = sum(theta[i] * context[i] for i in range(d))
    return exploit + alpha * math.sqrt(max(0.0, cb))


def choose_action(
    model: BanditModel,
    context: list[float],
    arms: "list[str]",
) -> str:
    """Return the EditKind value with the highest LinUCB score."""
    best_arm = arms[0]
    best_score = float("-inf")
    for arm_name in arms:
        arm = model.arms.get(arm_name)
        if arm is None:
            arm = _init_arm(model.n_features)
        score = ucb_score(arm, context, model.alpha)
        if score > best_score:
            best_score = score
            best_arm = arm_name
    return best_arm


# ---------------------------------------------------------------------------
# Offline LinUCB update (used during training)
# ---------------------------------------------------------------------------

def update_arm(arm: BanditArm, context: list[float], reward: float, iw: float = 1.0) -> None:
    """Perform a weighted LinUCB update for one (context, reward) transition."""
    d = len(context)
    for i in range(d):
        for j in range(d):
            arm.A[i][j] += iw * context[i] * context[j]
        arm.b[i] += iw * reward * context[i]


# ---------------------------------------------------------------------------
# Model persistence
# ---------------------------------------------------------------------------

def save_model(
    model: BanditModel,
    out_dir: "str | Path",
    reward_learned: float = 0.0,
    reward_heuristic: float = 0.0,
) -> Path:
    out_dir = Path(out_dir)
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    run_dir = out_dir / ts
    run_dir.mkdir(parents=True, exist_ok=True)

    model_dict = {
        "n_features": model.n_features,
        "alpha": model.alpha,
        "trained_date": model.trained_date or date.today().isoformat(),
        "arms": {
            name: {"A": arm.A, "b": arm.b}
            for name, arm in model.arms.items()
        },
    }
    model_path = run_dir / "model.json"
    model_path.write_text(json.dumps(model_dict, indent=2), encoding="utf-8")

    manifest = {
        "timestamp": ts,
        "n_features": model.n_features,
        "alpha": model.alpha,
        "reward_learned": reward_learned,
        "reward_heuristic": reward_heuristic,
        "trained_date": model.trained_date or date.today().isoformat(),
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return model_path


def load_model(model_dir: "str | Path") -> "BanditModel | None":
    """Load the latest bandit model; returns None if absent."""
    model_dir = Path(model_dir)
    if not model_dir.exists():
        return None
    candidates = sorted(
        (d for d in model_dir.iterdir() if d.is_dir() and (d / "model.json").exists()),
        reverse=True,
    )
    if not candidates:
        return None
    try:
        data = json.loads((candidates[0] / "model.json").read_text(encoding="utf-8"))
        arms = {
            name: BanditArm(A=v["A"], b=v["b"])
            for name, v in data.get("arms", {}).items()
        }
        return BanditModel(
            arms=arms,
            n_features=data.get("n_features", _N_FEATURES),
            alpha=data.get("alpha", _ALPHA),
            trained_date=data.get("trained_date", ""),
        )
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Training entry point (called by scripts/train_policy.py)
# ---------------------------------------------------------------------------

def train(
    out_dir: "str | Path" = "work/models/policy",
    min_transitions: int = 200,
    min_per_arm: int = 30,
    log_glob: str = "work/outputs/*/edits.log.jsonl",
) -> int:
    """Train an offline LinUCB bandit from logged PolicyTransition records.

    Returns 0 on success, 1 on data-threshold failure, 2 on no improvement.
    """
    import glob as _glob
    from ..types import EditKind

    all_arms = [e.value for e in EditKind]

    # --- load transitions ---------------------------------------------------
    transition_files = sorted(_glob.glob(log_glob))
    transitions = []
    for fpath in transition_files:
        with open(fpath, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                # Only keep PolicyTransition records (they have "edit_kind" key).
                if "edit_kind" in obj and obj.get("outcome") is not None:
                    transitions.append(obj)

    if len(transitions) < min_transitions:
        print(
            f"ERROR: only {len(transitions)} policy transitions found "
            f"(need ≥ {min_transitions}). Run more translations first."
        )
        return 1

    # Check per-arm coverage.
    arm_counts: dict[str, int] = {}
    for tr in transitions:
        arm_counts[tr["edit_kind"]] = arm_counts.get(tr["edit_kind"], 0) + 1
    thin_arms = [a for a in all_arms if arm_counts.get(a, 0) < min_per_arm]
    if thin_arms:
        print(
            f"WARNING: arms with < {min_per_arm} transitions: {thin_arms}. "
            "Policy may not generalise well for those edit kinds."
        )

    print(f"Loaded {len(transitions)} policy transitions.")

    # --- build propensity scores (historical ε-greedy) ----------------------
    # Propensity = ε/|arms| for explore, (1-ε) + ε/|arms| for exploit.
    n_arms = len(all_arms)

    # --- offline LinUCB update ----------------------------------------------
    model = BanditModel(
        arms={},
        n_features=_N_FEATURES,
        alpha=_ALPHA,
        trained_date=date.today().isoformat(),
    )

    heuristic_total_reward = 0.0
    learned_total_reward = 0.0

    for tr in transitions:
        arm_name = tr.get("edit_kind", "")
        if arm_name not in all_arms:
            continue
        from ..types import EntityScore
        es = EntityScore(
            entity_id=tr.get("entity_id", ""),
            type_match=tr.get("type_match", 0.0),
            control_flow_match=tr.get("control_flow_match", 0.0),
            data_output=tr.get("data_output", 0.0),
            variable_output=tr.get("variable_output", 0.0),
            callable_output=tr.get("callable_output", 0.0),
            side_effects=tr.get("side_effects", 0.0),
        )
        context = extract_context(es, tr.get("entity_kind", ""), tr.get("package", ""))
        reward = max(0.0, tr.get("score_delta") or 0.0)

        # IPS weight: ε at iteration i (linear decay matching editor.py).
        iteration = tr.get("iteration", 0)
        epsilon = max(0.05, 0.30 - iteration * 0.025)
        propensity = epsilon / n_arms + (1.0 - epsilon if tr.get("exploit_mode") else 0.0)
        iw = min(1.0 / max(propensity, 1e-6), 10.0)  # clip IW at 10×

        arm = model.arms.setdefault(arm_name, _init_arm(_N_FEATURES))
        update_arm(arm, context, reward, iw=iw)

        heuristic_total_reward += reward  # baseline: whatever ε-greedy did

    # Estimate learned policy reward via expected LinUCB choices.
    for tr in transitions:
        arm_name = tr.get("edit_kind", "")
        from ..types import EntityScore
        es = EntityScore(
            entity_id=tr.get("entity_id", ""),
            type_match=tr.get("type_match", 0.0),
            control_flow_match=tr.get("control_flow_match", 0.0),
            data_output=tr.get("data_output", 0.0),
            variable_output=tr.get("variable_output", 0.0),
            callable_output=tr.get("callable_output", 0.0),
            side_effects=tr.get("side_effects", 0.0),
        )
        context = extract_context(es, tr.get("entity_kind", ""), tr.get("package", ""))
        chosen = choose_action(model, context, all_arms)
        # Credit the reward only if the learned policy agrees with what happened.
        if chosen == arm_name:
            learned_total_reward += max(0.0, tr.get("score_delta") or 0.0)

    n = max(len(transitions), 1)
    reward_h = heuristic_total_reward / n
    reward_l = learned_total_reward / n
    print(f"Expected reward per transition (heuristic): {reward_h:.4f}")
    print(f"Expected reward per transition (learned):   {reward_l:.4f}")

    if reward_l <= reward_h:
        print("No improvement over heuristic — artifact not saved.")
        return 2

    saved = save_model(model, out_dir, reward_learned=reward_l, reward_heuristic=reward_h)
    print(f"Artifact saved: {saved}")
    return 0


# ---------------------------------------------------------------------------
# Small Gaussian elimination for d×d (d=8) — avoids numpy dependency
# ---------------------------------------------------------------------------

def _solve(A: list[list[float]], b: list[float]) -> list[float]:
    """Solve Ax = b via Gaussian elimination (in-place on copies)."""
    n = len(b)
    # Augmented matrix [A | b]
    mat = [A[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        # Partial pivot
        max_row = max(range(col, n), key=lambda r: abs(mat[r][col]))
        mat[col], mat[max_row] = mat[max_row], mat[col]
        pivot = mat[col][col]
        if abs(pivot) < 1e-12:
            continue
        for row in range(n):
            if row == col:
                continue
            factor = mat[row][col] / pivot
            for j in range(col, n + 1):
                mat[row][j] -= factor * mat[col][j]
    return [mat[i][n] / mat[i][i] if abs(mat[i][i]) > 1e-12 else 0.0 for i in range(n)]
