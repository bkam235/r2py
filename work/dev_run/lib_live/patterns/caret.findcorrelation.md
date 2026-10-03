---
id: caret.findcorrelation
package: caret
confidence: tentative
seed: true
created: 2026-09-30
last_review: 2026-09-30
tie_count: 0
---

# caret.findcorrelation

## Guidance
Translate R `findCorrelation` (FunctionCall from caret) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "69c111ab", "r_snippet": "findCorrelation(R1, cutoff = .6, exact = FALSE)", "py_snippet": "def findCorrelation_exact(x, cutoff=0.9, verbose=False):\n    if isinstance(x, pd.DataFrame):\n        mat = x.values.astype(float)\n    else:\n        mat = np.asarray(x).astype(float)\n    \n    varnum = mat.shape[0]\n    if not np.allclose(mat, mat.T):\n        raise ValueError(\"correlation matrix is not symmetric\")\n    if varnum == 1:\n        raise ValueError(\"only one variable given\")\n    \n    x_abs = np.abs(mat)\n    originalOrder = np.arange(1, varnum + 1)\n    \n    tmp = x_abs.copy()\n    np.fill_diagonal(tmp, np.nan)\n    avg_corr = np.nanmean(tmp, axis=0)\n    \n    maxAbsCorOrder = np.argsort(-avg_corr)\n    \n    x_sorted = x_abs[maxAbsCorOrder, :][:, maxAbsCorOrder]\n    newOrder = originalOrder[maxAbsCorOrder]\n    \n    deletecol = np.zeros(varnum, dtype=bool)\n    x2 = x_sorted.copy()\n    np.fill_diagonal(x2, np.nan)\n    \n    for i in range(varnum - 1):\n        if not np.any(x2[~np.isnan(x2)] > cutoff):\n            if verbose:\n                print(f\"All correlations <= {cutoff} \")\n            break\n        \n        if deletecol[i]:\n            continue\n            \n        for j in range(i + 1, varnum):\n            if not deletecol[i] and not deletecol[j]:\n                if x_sorted[i, j] > cutoff:\n                    mn1 = np.nanmean(x2[i, :])\n                    rows_except_j = [r for r in range(varnum) if r != j]\n                    mn2 = np.nanmean(x2[rows_except_j, :])\n                    \n                    if verbose:\n                        print(f\"Compare row {newOrder[i]}  and column {newOrder[j]} with corr {round(x_sorted[i, j], 3)} \")\n                        print(f\"  Means:  {round(mn1, 3)} vs {round(mn2, 3)}\", end=\"\")\n                    \n                    if mn1 > mn2:\n                        deletecol[i] = True\n                        x2[i, :] = np.nan\n                        x2[:, i] = np.nan\n                        if verbose:\n                            print(f\" so flagging column {newOrder[i]} \")\n                    else:\n# ...", "score": 1.0, "script_id": "caret__rd_example__findCorrelation_Rd", "n_calls": 0}

## Edit Examples
(none)
