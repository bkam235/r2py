---
id: bslib.popover
package: bslib
confidence: tentative
seed: true
created: 2026-07-04
last_review: 2026-07-04
tie_count: 0
---

# bslib.popover

## Guidance
Translate R `popover` (FunctionCall from bslib) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "f2f7ef98", "r_snippet": "popover(\n  shiny::actionButton(\"btn\", \"A button\"),\n  \"Popover body content...\",\n  title = \"Popover title\"\n)", "py_snippet": "def popover(trigger, *args, title: Optional[str] = None, id: Optional[str] = None,\n            placement: str = \"auto\", options: Optional[Dict] = None):\n    \"\"\"\n    Create a popover element.\n    \"\"\"\n    if options is None:\n        options = {}\n    \n    content_args = list(args)\n    \n    if len(content_args) == 0:\n        raise ValueError(\"At least one value must be provided to popover content.\")\n    \n    # Create popover structure using bslib component\n    popover_elem = ui.div(\n        ui.HTML(f'<bslib-popover id=\"{id}\" placement=\"{placement}\" bsOptions=\"[]\" data-require-bs-version=\"5\" data-r", "score": 0.9503, "script_id": "auto"}

## Edit Examples
(none)
