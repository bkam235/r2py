---
id: purrr.map
package: purrr
confidence: tentative
seed: true
created: 2026-10-07
last_review: 2026-10-07
tie_count: 0
---

# purrr.map

## Guidance
Translate R `map` from purrr to Python. The verified example below comes from another script that used it.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "dffc5326", "r_snippet": "  purrr::map(unlist)", "py_snippet": "# ensuring each value in the dictionary is a flattened list.\ndef map_unlist(data):\n    result = {}\n    for k, v in data.items():\n        # unlist in R flattens the structure. \n        # If v is a list, we ensure it's a flat list of elements.\n        if isinstance(v, list):\n            flat = []\n            for item in v:\n                if isinstance(item, list):\n                    flat.extend(item)\n                else:\n                    flat.append(item)\n            result[k] = flat\n        else:\n            result[k] = v\n    return result\n    # explore the export formats available for Drive files, by MIME type\n    about = drive_about()", "score": 1.0, "script_id": "googledrive__rd_example__drive_about_Rd.R", "n_calls": 0}
- {"r_hash": "79abb2f5", "r_snippet": "out <- map(1:5, slow_runif)", "py_snippet": "# out <- map(1:5, slow_runif)", "score": 1.0, "script_id": "purrr__rd_example__slowly_Rd.R", "n_calls": 0}
- {"r_hash": "25140518", "r_snippet": "out <- map(by_cyl, in_parallel(\\(df) my_lm(mpg ~ disp, data = df)))", "py_snippet": "# Helper for parallel execution to avoid pickling issues with lambda/local functions\ndef _my_lm_wrapper(args):\n    return my_lm(*args)\n\ntry:\n\n    # out <- map(by_cyl, in_parallel(\\(df) my_lm(mpg ~ disp, data = df)))\n    # Note: in_parallel logic implemented via multiprocessing Pool\n    with Pool() as pool:\n        # We map the function across the values of the split dictionary\n        # R's map() over a named list returns a named list\n        keys = list(by_cyl.keys())\n        values = list(by_cyl.values())\n        args = [(\"mpg ~ disp\", df) for df in values]\n        \n        results = pool.map(_my_lm_wrapper, args)", "score": 0.96, "script_id": "purrr__vignette__purrr_s10.R", "n_calls": 0}

## Edit Examples
(none)
