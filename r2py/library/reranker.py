"""Optional LightGBM LambdaMART retrieval reranker (§12.6 A).

Feature extraction and model inference are pure Python (no LightGBM import),
so tests run without LightGBM installed. Training lives in scripts/train_reranker.py
but calls train() from this module.
"""
from __future__ import annotations

import hashlib
import json
from datetime import date, datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pattern import Pattern

FEATURE_NAMES = [
    "package_match",
    "ast_shape_sim",
    "token_sim",
    "confidence_int",
    "evidence_count",
    "contradiction_count",
    "accept_rate",
    "recency_norm",
]


# ---------------------------------------------------------------------------
# Feature extraction (no LightGBM dependency)
# ---------------------------------------------------------------------------

def extract_features(entity: object, patterns: "list[Pattern]") -> "list[list[float]]":
    """Return one feature vector per pattern (8 features per §12.6 A).

    Features:
      0  package_match      — 1.0 if pattern.package == entity.package
      1  ast_shape_sim      — Jaccard token overlap of entity kind vs pattern.id
      2  token_sim          — Jaccard token overlap of entity name vs pattern.guidance
      3  confidence_int     — 1.0 if confirmed, 0.0 if tentative
      4  evidence_count     — raw count (unscaled)
      5  contradiction_count — raw count (unscaled)
      6  accept_rate        — evidence / (evidence + contradictions + 1)  [Laplace]
      7  recency_norm       — days since last_review / 365 (0 if unknown), inverted
    """
    from .retrieval import _token_overlap, _entity_kind_str

    package = getattr(entity, "package", None) or ""
    entity_name = getattr(entity, "name", "") or ""
    entity_kind = _entity_kind_str(entity)
    today = date.today()

    rows: list[list[float]] = []
    for pat in patterns:
        pkg_match = 1.0 if (pat.package == package and package) else 0.0
        ast_sim = _token_overlap(entity_kind, pat.id)
        tok_sim = _token_overlap(entity_name, pat.guidance)
        conf_int = 1.0 if pat.confidence == "confirmed" else 0.0
        ev = len(pat.evidence)
        ct = len(pat.contradictions)
        accept_rate = ev / (ev + ct + 1.0)
        recency = _recency_norm(pat.last_review, today)
        rows.append([pkg_match, ast_sim, tok_sim, conf_int, float(ev), float(ct),
                     accept_rate, recency])
    return rows


def _recency_norm(last_review: str, today: date) -> float:
    """Inverted recency: 1.0 = reviewed today, 0.0 = never or ≥365 days ago."""
    if not last_review:
        return 0.0
    try:
        d = date.fromisoformat(last_review)
        age_days = (today - d).days
        return max(0.0, 1.0 - age_days / 365.0)
    except ValueError:
        return 0.0


# ---------------------------------------------------------------------------
# Reranking inference
# ---------------------------------------------------------------------------

def rerank(entity: object, patterns: "list[Pattern]", model: object) -> "list[Pattern]":
    """Reorder patterns by learned score; returns patterns unchanged if model is None."""
    if model is None or not patterns:
        return patterns
    feats = extract_features(entity, patterns)
    try:
        scores = model.predict(feats)
    except Exception:
        return patterns
    paired = sorted(zip(scores, patterns), key=lambda x: x[0], reverse=True)
    return [p for _, p in paired]


# ---------------------------------------------------------------------------
# Model persistence
# ---------------------------------------------------------------------------

def save_model(
    model: object,
    out_dir: "str | Path",
    ndcg3_learned: float = 0.0,
    ndcg3_heuristic: float = 0.0,
) -> Path:
    """Save a trained LightGBM model to a timestamped subdirectory.

    Returns the path to the saved model file.
    """
    import lightgbm as lgb  # noqa: F401 — confirms lgb is available at save time

    out_dir = Path(out_dir)
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    run_dir = out_dir / ts
    run_dir.mkdir(parents=True, exist_ok=True)

    model_path = run_dir / "model.lgb"
    model.save_model(str(model_path))

    artifact_hash = hashlib.sha256(model_path.read_bytes()).hexdigest()[:16]
    manifest = {
        "timestamp": ts,
        "feature_names": FEATURE_NAMES,
        "artifact_hash": artifact_hash,
        "ndcg3_learned": ndcg3_learned,
        "ndcg3_heuristic": ndcg3_heuristic,
        "trained_date": date.today().isoformat(),
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return model_path


def load_model(model_dir: "str | Path") -> object:
    """Load the latest LightGBM model from model_dir; returns None if absent."""
    model_dir = Path(model_dir)
    if not model_dir.exists():
        return None
    # Pick the most recently timestamped subdirectory that contains model.lgb.
    candidates = sorted(
        (d for d in model_dir.iterdir() if d.is_dir() and (d / "model.lgb").exists()),
        reverse=True,
    )
    if not candidates:
        return None
    try:
        import lightgbm as lgb
        return lgb.Booster(model_file=str(candidates[0] / "model.lgb"))
    except ImportError:
        return None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Training entry point (called by scripts/train_reranker.py and CLI)
# ---------------------------------------------------------------------------

def train(
    out_dir: "str | Path" = "work/models/reranker",
    min_episodes: int = 500,
    log_glob: str = "work/outputs/*/edits.log.jsonl",
    library_dir: "str | Path" = "work/library",
) -> int:
    """Train a LambdaMART reranker from logged retrieval episodes.

    Returns 0 on success (artifact saved), 1 on data-threshold failure,
    2 on no improvement vs heuristic.
    """
    try:
        import lightgbm as lgb
        import numpy as np
    except ImportError:
        print("ERROR: lightgbm and numpy are required: pip install lightgbm numpy")
        return 1

    import glob as _glob

    from ..library import get_library

    # --- load episodes --------------------------------------------------------
    episode_files = sorted(_glob.glob(log_glob))
    episodes = []
    for fpath in episode_files:
        with open(fpath, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                # Only keep retrieval episodes (they have "candidates" key).
                if "candidates" in obj and obj.get("outcome") is not None:
                    episodes.append(obj)

    if len(episodes) < min_episodes:
        print(
            f"ERROR: only {len(episodes)} retrieval episodes found "
            f"(need ≥ {min_episodes}). Run more translations first."
        )
        return 1

    print(f"Loaded {len(episodes)} retrieval episodes from {len(episode_files)} files.")

    # --- build feature matrix -------------------------------------------------
    library = get_library(library_dir)

    X_rows: list[list[float]] = []
    y_labels: list[float] = []
    groups: list[int] = []        # LightGBM group sizes (one per query)
    script_ids: list[str] = []    # for grouped CV split

    for ep in episodes:
        candidates = ep.get("candidates", [])
        if not candidates:
            continue
        outcome = ep.get("outcome", "rejected")
        score_delta = ep.get("score_delta") or 0.0
        chosen_id = ep.get("chosen_pattern_id")

        feats_for_query: list[list[float]] = []
        labels_for_query: list[float] = []

        for cand in candidates:
            pid = cand.get("pattern_id", "")
            pat = library.store.get(pid) if hasattr(library, "store") else None
            if pat is None:
                # Use logged features directly as fallback.
                feat = [
                    float(cand.get("package_match", 0)),
                    float(cand.get("ast_shape_sim", 0)),
                    float(cand.get("token_sim", 0)),
                    1.0 if cand.get("confidence") == "confirmed" else 0.0,
                    float(cand.get("evidence_count", 0)),
                    float(cand.get("contradiction_count", 0)),
                    0.0, 0.0,
                ]
            else:
                # Re-compute from current library state (fresher counts).
                ev = len(pat.evidence)
                ct = len(pat.contradictions)
                from datetime import date as _date
                feat = [
                    float(cand.get("package_match", 0)),
                    float(cand.get("ast_shape_sim", 0)),
                    float(cand.get("token_sim", 0)),
                    1.0 if pat.confidence == "confirmed" else 0.0,
                    float(ev),
                    float(ct),
                    ev / (ev + ct + 1.0),
                    _recency_norm(pat.last_review, _date.today()),
                ]

            # Label: chosen + accepted → score_delta; otherwise 0.
            if pid == chosen_id and outcome == "accepted":
                label = max(0.0, score_delta)
            elif pid == chosen_id and outcome == "tie":
                label = 0.0
            else:
                label = 0.0

            feats_for_query.append(feat)
            labels_for_query.append(label)

        X_rows.extend(feats_for_query)
        y_labels.extend(labels_for_query)
        groups.append(len(feats_for_query))
        script_ids.append(ep.get("script_id", ""))

    X = np.array(X_rows, dtype=np.float32)
    y = np.array(y_labels, dtype=np.float32)
    group = np.array(groups, dtype=np.int32)

    # --- grouped k-fold CV (split by script_id) --------------------------------
    unique_scripts = list(dict.fromkeys(script_ids))
    n_folds = min(5, len(unique_scripts))
    if n_folds < 2:
        print("WARNING: fewer than 2 unique scripts — skipping CV, training on all data.")
        cv_ndcg3 = float("nan")
    else:
        cv_ndcg3 = _grouped_cv(X, y, group, script_ids, unique_scripts, n_folds, lgb, np)

    # --- heuristic baseline NDCG@3 -------------------------------------------
    heuristic_ndcg3 = _heuristic_ndcg3(episodes, library)

    print(f"CV NDCG@3 (learned):   {cv_ndcg3:.4f}")
    print(f"Heuristic NDCG@3:      {heuristic_ndcg3:.4f}")

    import math
    if not math.isnan(cv_ndcg3) and cv_ndcg3 <= heuristic_ndcg3:
        print("No improvement over heuristic — artifact not saved.")
        return 2

    # --- train final model (hold out last ~20% of scripts for early stopping) ---
    params = dict(
        objective="lambdarank",
        metric="ndcg",
        ndcg_eval_at=[1, 3],
        boosting_type="gbdt",
        num_leaves=15,
        min_data_in_leaf=30,
        learning_rate=0.05,
        feature_fraction=0.8,
        bagging_fraction=0.8,
        bagging_freq=1,
        lambda_l1=1.0,
        lambda_l2=1.0,
        max_position=3,
        verbosity=-1,
    )
    val_cutoff = max(1, int(len(unique_scripts) * 0.8))
    val_scripts_final = set(unique_scripts[val_cutoff:])
    tr_rows_f, va_rows_f = [], []
    tr_groups_f, va_groups_f = [], []
    pos = 0
    for q_idx, q_size in enumerate(group):
        idxs = list(range(pos, pos + int(q_size)))
        if script_ids[q_idx] in val_scripts_final:
            va_rows_f.extend(idxs)
            va_groups_f.append(int(q_size))
        else:
            tr_rows_f.extend(idxs)
            tr_groups_f.append(int(q_size))
        pos += int(q_size)

    if va_rows_f:
        train_data = lgb.Dataset(X[tr_rows_f], label=y[tr_rows_f],
                                 group=np.array(tr_groups_f), feature_name=FEATURE_NAMES)
        val_data = lgb.Dataset(X[va_rows_f], label=y[va_rows_f],
                               group=np.array(va_groups_f), reference=train_data)
        model = lgb.train(
            params, train_data, num_boost_round=500,
            valid_sets=[val_data],
            callbacks=[lgb.early_stopping(50, verbose=False), lgb.log_evaluation(period=-1)],
        )
    else:
        train_data = lgb.Dataset(X, label=y, group=group, feature_name=FEATURE_NAMES)
        model = lgb.train(params, train_data, num_boost_round=500)

    saved = save_model(model, out_dir, ndcg3_learned=cv_ndcg3, ndcg3_heuristic=heuristic_ndcg3)
    print(f"Artifact saved: {saved}")
    return 0


def _grouped_cv(
    X: "np.ndarray",
    y: "np.ndarray",
    group: "np.ndarray",
    script_ids: list[str],
    unique_scripts: list[str],
    n_folds: int,
    lgb: object,
    np: object,
) -> float:
    """Grouped k-fold CV returning mean NDCG@3 across folds."""
    import math
    fold_size = len(unique_scripts) // n_folds
    ndcg_scores: list[float] = []

    for fold in range(n_folds):
        val_scripts = set(unique_scripts[fold * fold_size: (fold + 1) * fold_size])
        tr_mask = [sid not in val_scripts for sid in script_ids]
        va_mask = [sid in val_scripts for sid in script_ids]

        # Reconstruct row-level masks from query-level masks.
        tr_rows, va_rows = [], []
        tr_groups, va_groups = [], []
        pos = 0
        for q_idx, q_size in enumerate(group):
            idxs = list(range(pos, pos + q_size))
            if tr_mask[q_idx]:
                tr_rows.extend(idxs)
                tr_groups.append(q_size)
            else:
                va_rows.extend(idxs)
                va_groups.append(q_size)
            pos += q_size

        if not tr_rows or not va_rows:
            continue

        X_tr, y_tr = X[tr_rows], y[tr_rows]
        X_va, y_va = X[va_rows], y[va_rows]

        params = dict(
            objective="lambdarank", metric="ndcg", ndcg_eval_at=[3],
            boosting_type="gbdt", num_leaves=15, min_data_in_leaf=10,
            learning_rate=0.05, lambda_l1=1.0, lambda_l2=1.0,
            max_position=3, verbosity=-1,
        )
        ds_tr = lgb.Dataset(X_tr, label=y_tr, group=np.array(tr_groups))
        ds_va = lgb.Dataset(X_va, label=y_va, group=np.array(va_groups), reference=ds_tr)
        m = lgb.train(
            params, ds_tr,
            num_boost_round=200,
            valid_sets=[ds_va],
            callbacks=[lgb.early_stopping(30, verbose=False), lgb.log_evaluation(period=-1)],
        )
        preds = m.predict(X_va)
        ndcg_scores.append(_ndcg_at_k(y_va, preds, np.array(va_groups), k=3, np=np))

    return sum(ndcg_scores) / len(ndcg_scores) if ndcg_scores else float("nan")


def _ndcg_at_k(
    y_true: "np.ndarray",
    y_pred: "np.ndarray",
    groups: "np.ndarray",
    k: int,
    np: object,
) -> float:
    """Compute mean NDCG@k over all queries."""
    import math
    scores: list[float] = []
    pos = 0
    for g in groups:
        yt = y_true[pos: pos + g]
        yp = y_pred[pos: pos + g]
        pos += g
        order = np.argsort(yp)[::-1][:k]
        ideal_order = np.argsort(yt)[::-1][:k]
        dcg = sum(yt[i] / math.log2(r + 2) for r, i in enumerate(order))
        idcg = sum(yt[i] / math.log2(r + 2) for r, i in enumerate(ideal_order))
        scores.append(dcg / idcg if idcg > 0 else 0.0)
    return sum(scores) / len(scores) if scores else 0.0


def _heuristic_ndcg3(episodes: list[dict], library: object) -> float:
    """Compute NDCG@3 of the original heuristic rank order (rank 0 = best)."""
    import math
    scores: list[float] = []
    for ep in episodes:
        candidates = ep.get("candidates", [])
        if not candidates:
            continue
        chosen_id = ep.get("chosen_pattern_id")
        outcome = ep.get("outcome", "rejected")
        score_delta = ep.get("score_delta") or 0.0
        k = min(3, len(candidates))
        dcg = idcg = 0.0
        for r, cand in enumerate(candidates[:k]):
            rel = (max(0.0, score_delta)
                   if (cand.get("pattern_id") == chosen_id and outcome == "accepted")
                   else 0.0)
            dcg += rel / math.log2(r + 2)
        ideal_labels = sorted(
            (max(0.0, score_delta)
             if (c.get("pattern_id") == chosen_id and outcome == "accepted") else 0.0
             for c in candidates[:k]),
            reverse=True,
        )
        for r, rel in enumerate(ideal_labels):
            idcg += rel / math.log2(r + 2)
        scores.append(dcg / idcg if idcg > 0 else 0.0)
    return sum(scores) / len(scores) if scores else 0.0
