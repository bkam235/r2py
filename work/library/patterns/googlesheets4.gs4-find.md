---
id: googlesheets4.gs4-find
package: googlesheets4
confidence: tentative
seed: true
created: 2026-07-17
last_review: 2026-07-17
tie_count: 0
---

# googlesheets4.gs4-find

## Guidance
Translate R `gs4_find` (FunctionCall from googlesheets4) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "5f82c08c", "r_snippet": "gs4_find(\"range-flood-demo\") %>%", "py_snippet": "def gs4_find(name: str) -> dict:\n    \"\"\"Find a Google Sheet by name.\"\"\"\n    return {\"name\": name, \"id\": f\"id_of_{name}\"}\n\n    file_info = gs4_find(\"range-flood-demo\")", "score": 0.8, "script_id": "auto"}
- {"r_hash": "09a061a5", "r_snippet": "ss %>% sheet_append(deaths_two)", "py_snippet": "sheets_data['deaths'] = pd.concat([sheets_data['deaths'], deaths_two], ignore_index=True)\n\n# Append deaths_three", "score": 0.8, "script_id": "auto"}

## Edit Examples
(none)
