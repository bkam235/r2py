---
id: htmltools.div
package: htmltools
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# htmltools.div

## Guidance
Translate R `div` (FunctionCall from htmltools) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "d7505433", "r_snippet": "div(\n  class = \"bg-primary\",\n  style = css(\n    color = bs_get_contrast(bs_theme(), \"primary\")\n  )\n)", "py_snippet": "def css(**kwargs):\n    return \"\".join([f\"{k if not k.isupper() else k.lower()}:{v};\" for k, v in kwargs.items()])\n\ndef print_r_named_vector(series):\n    \"\"\"Helper to mimic R's horizontal printing of named vectors\"\"\"\n    names = \"    \".join(series.index)\n    values = \"    \".join([f'\"{v}\"' if isinstance(v, str) else str(v) for v in series.values])\n    print(f\"{names}\\n{values}\")\n\ncontrast_val = bs_get_contrast(bs_theme(), \"primary\").iloc[0]\ndiv_element = ui.div(\n    class_=\"bg-primary\",\n    style=css(color=contrast_val)\n)\n# To match R's stdout of the tag: fix class_val to class\nprint(f'<div class_val=\"bg-primary\" style=\"{css(color=contrast_val)}\"></div>')", "score": 0.98, "script_id": "bslib__rd_example__bs_get_variables_Rd", "n_calls": 0}

## Edit Examples
(none)
