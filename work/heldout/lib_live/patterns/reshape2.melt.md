---
id: reshape2.melt
package: reshape2
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# reshape2.melt

## Guidance
Translate R `melt` (FunctionCall from reshape2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "cbd2f18e", "r_snippet": "melt(a)", "py_snippet": "def melt(data, level=1, value_name=\"value\", varname=None):\n    # Emulate R's melt.list / melt.array / melt.default\n    \n    # Handle List-like (melt.list)\n    if isinstance(data, list):\n        parts = []\n        for item in data:\n            parts.append(melt(item, level=level + 1, value_name=value_name, varname=varname))\n        \n        if not parts:\n            return pd.DataFrame()\n        \n        # rbind.fill equivalent\n        result = pd.concat(parts, ignore_index=True, sort=False)\n        \n        # Determine labels for the current level\n        # R uses names(data) or seq_along(data)\n        names = getattr(data, 'names', None)\n        if names is None:\n            # In R, lists passed to melt.list that aren't named use 1, 2, 3...\n            # We assume the input 'data' is a standard list or our NamedList\n            names = range(1, len(data) + 1)\n        \n        # Calculate lengths of each part to repeat names\n        lengths = [len(p) for p in parts]\n        labels = []\n        for name, length in zip(names, lengths):\n            labels.extend([name] * length)\n        \n        label_var = varname if varname else f\"L{level}\"\n        result[label_var] = labels\n        \n        # Move label_var to the end to match R's cbind(labels, value_df) behavior in some contexts, \n        # but melt.list specifically appends the label.\n        # R output shows 'value L1' for simple lists.\n        cols = [c for c in result.columns if c != label_var] + [label_var]\n        return result[cols]\n\n    # Handle Array/Matrix (melt.array / melt.matrix)\n    elif isinstance(data, np.ndarray):\n        shape = data.shape\n        # Create coordinate grids (expand.grid)\n        dims = []\n        for i in range(len(shape)):\n            # R's matrix(1:4, ncol=2) has dimnames if we are lucky, \n            # but by default they are just indices.\n            dims.append(range(1, shape[i] + 1))\n        \n        coords = list(itertools.product(*dims))\n# ...", "score": 0.9138, "script_id": "reshape2__rd_example__melt_list_Rd", "n_calls": 0}

## Edit Examples
(none)
