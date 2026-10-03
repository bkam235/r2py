---
id: base.split
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.split

## Guidance
Translate R `split` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "23fe28b5", "r_snippet": "by_cyl <- split(mtcars, mtcars$cyl)", "py_snippet": "    by_cyl = {str(cyl): group for cyl, group in mtcars.groupby('cyl')}\n\n    # out <- map(by_cyl, in_parallel(\\(df) my_lm(mpg ~ disp, data = df)))\n    # Note: in_parallel logic implemented via multiprocessing Pool\n    # r2py:entity:out\n    with Pool() as pool:\n        # We map the function across the values of the split dictionary\n        # R's map() over a named list returns a named list\n        keys = list(by_cyl.keys())\n        values = list(by_cyl.values())\n        args = [(\"mpg ~ disp\", df) for df in values]\n        \n        results = pool.map(_my_lm_wrapper, args)\n        out = dict(zip(keys, results))\n\nexcept Exception as e:\n    pass", "score": 1.0, "script_id": "purrr__vignette__purrr_s10", "n_calls": 1}

## Edit Examples
- {"failure_class": "crash", "old_code": "by_cyl = {cyl: group for cyl, group in mtcars.groupby('cyl')}\n\n# out <- map(by_cyl, in_parallel(\\(df) my_lm(mpg ~ disp, data = df)))\n# Note: in_parallel logic implemented via multiprocessing Pool", "new_code": "    by_cyl = {str(cyl): group for cyl, group in mtcars.groupby('cyl')}\n\n    # out <- map(by_cyl, in_parallel(\\(df) my_lm(mpg ~ disp, data = df)))\n    # Note: in_parallel logic implemented via multiprocessing Pool\n    # r2py:entity:out\n    with Pool() as pool:\n        # We map the function across the values of the split dictionary\n        # R's map() over a named list returns a named list\n        keys = list(by_cyl.keys())\n        values = list(by_cyl.values())\n        args = [(\"mpg ~ disp\", df) for df in values]\n        \n        results = pool.map(_my_lm_wrapper, args)\n        out = dict(zip(keys, results))\n\nexcept Exception as e:\n    pass", "score_delta": 1.0, "script_id": "purrr__vignette__purrr_s10", "r_snippet": "by_cyl <- split(mtcars, mtcars$cyl)", "functions": ["base::split"]}
