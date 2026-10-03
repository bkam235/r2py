---
id: base.names
package: base
confidence: tentative
seed: true
created: 2026-09-20
last_review: 2026-09-20
tie_count: 0
---

# base.names

## Guidance
Translate R `names` (FunctionCall from base) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "950b96c9", "r_snippet": "names(a) <- letters[1:4]", "py_snippet": "class NamedList(list):\n    def __init__(self, items, names=None):\n        super().__init__(items)\n        self.names = names\n\n# a <- as.list(c(1:4, NA))", "score": 1.0, "script_id": "reshape2__rd_example__melt_list_Rd", "n_calls": 1}
- {"r_hash": "b5322120", "r_snippet": "  names()", "py_snippet": "result1 = [col for col in d1.columns if col.startswith(\"Species\")]\nprint(result1)\n\n# Section 2: Translation of the second recipe pipe\n# recipe( ~ ., data = iris) |> \n#   step_dummy(Species, role = \"trousers\") |> \n#   prep() |> \n#   bake(new_data = NULL, has_role(\"trousers\")) |> \n#   names()\n\n# role = \"trousers\" is a custom role.\n# has_role(\"trousers\") in bake() filters the output to only those columns with that role.", "score": 0.9333, "script_id": "recipes__vignette__Roles_chunk11", "n_calls": 1}

## Edit Examples
- {"failure_class": "crash", "old_code": "result1 = [col for col in d.columns if col.startswith(\"Species\")]\nprint(result1)\n\n# Section 2: Translation of the second recipe pipe\n# recipe(~ ., data = iris) |> step_dummy(Species, role = \"trousers\") |> prep() |> bake(new_data = NULL, has_role(\"trousers\")) |> names()\n# In recipes, assigning a role allows selective baking. \n# Here, we specifically target the dummy variables created from 'Species'.", "new_code": "result1 = [col for col in d1.columns if col.startswith(\"Species\")]\nprint(result1)\n\n# Section 2: Translation of the second recipe pipe\n# recipe( ~ ., data = iris) |> \n#   step_dummy(Species, role = \"trousers\") |> \n#   prep() |> \n#   bake(new_data = NULL, has_role(\"trousers\")) |> \n#   names()\n\n# role = \"trousers\" is a custom role.\n# has_role(\"trousers\") in bake() filters the output to only those columns with that role.", "score_delta": 0.9333, "script_id": "recipes__vignette__Roles_chunk11", "r_snippet": "  names()", "functions": ["base::names"]}
