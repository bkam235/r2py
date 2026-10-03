---
id: base.factor
package: base
confidence: tentative
seed: true
created: 2026-09-23
last_review: 2026-09-23
tie_count: 0
---

# base.factor

## Guidance
Translate R `factor` from base to Python. The verified example below uses it inside a statement that may call other functions too.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "4a568b00", "r_snippet": "vec_cast_common(factor(\"a\"), factor(c(\"a\", \"b\")))", "py_snippet": "def vec_cast_common(*args):\n    # Common type for factors is a factor with the union of all levels\n    all_vals = []\n    for arg in args:\n        all_vals.extend(list(arg))\n    \n    common_levels = sorted(list(set(all_vals)))\n    \n    results = []\n    for arg in args:\n        # Create categorical with union of levels\n        s = pd.Series(arg, dtype='category').astype(pd.CategoricalDtype(categories=common_levels))\n        results.append(s)\n    return results\n\n# --- Execution ---\n\n# vec_cast(1, integer())\n\ncommon = vec_cast_common([\"a\"], [\"a\", \"b\"])\nfor i, s in enumerate(common, 1):\n    print(f\"[[{i}]]\")\n    print(f\"[1] {' '.join(map(str, s.values))}\")\n    print(f\"Levels: {' '.join(map(str, s.cat.categories))}\")\n    print()", "score": 1.0, "script_id": "vctrs__rd_example__vec_cast_Rd", "n_calls": 1}

## Edit Examples
- {"failure_class": "side_effects", "old_code": "def vec_cast_common(x, y):\n    # Approximate R's common type casting (e.g., factor levels)\n    s1 = pd.Series(x).astype('category').cat.categories\n    s2 = pd.Series(y).astype('category').cat.categories\n    common_categories = np.union1d(s1, s2)\n    return common_categories\n\n# --- Translation of the script execution ---\n\n# vec_cast(1, integer())\n\nprint(vec_cast_common([\"a\"], [\"a\", \"b\"]))", "new_code": "def vec_cast_common(*args):\n    # Common type for factors is a factor with the union of all levels\n    all_vals = []\n    for arg in args:\n        all_vals.extend(list(arg))\n    \n    common_levels = sorted(list(set(all_vals)))\n    \n    results = []\n    for arg in args:\n        # Create categorical with union of levels\n        s = pd.Series(arg, dtype='category').astype(pd.CategoricalDtype(categories=common_levels))\n        results.append(s)\n    return results\n\n# --- Execution ---\n\n# vec_cast(1, integer())\n\ncommon = vec_cast_common([\"a\"], [\"a\", \"b\"])\nfor i, s in enumerate(common, 1):\n    print(f\"[[{i}]]\")\n    print(f\"[1] {' '.join(map(str, s.values))}\")\n    print(f\"Levels: {' '.join(map(str, s.cat.categories))}\")\n    print()", "score_delta": 0.4118, "script_id": "vctrs__rd_example__vec_cast_Rd", "r_snippet": "vec_cast_common(factor(\"a\"), factor(c(\"a\", \"b\")))", "functions": ["base::factor"]}
