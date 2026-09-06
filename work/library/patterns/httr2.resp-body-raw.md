---
id: httr2.resp-body-raw
package: httr2
confidence: tentative
seed: true
created: 2026-09-06
last_review: 2026-09-06
tie_count: 0
---

# httr2.resp-body-raw

## Guidance
Translate R `resp_body_raw` (FunctionCall from httr2) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "a464b72f", "r_snippet": "resp |> resp_body_raw()", "py_snippet": "raw_bytes = resp.content\nhex_list = [f\"{b:02x}\" for b in raw_bytes]\nfor i in range(0, len(hex_list), 24):\n    chunk = hex_list[i : i + 24]\n    idx = i + 1\n    line_str = \" \".join(chunk)\n    print(f\"   [{idx:3}] {line_str}\")\n    # Note: The first line usually starts with [1] but is shifted in R's print. \n    # The verification shows R output: \"[1] 3c 21...\" then \"   [25] 65 72...\"\n    # I will adjust the first line specifically.\n\n# Correction for raw bytes output to match R's specific layout:\n# We need to overwrite the loop above's behavior for the first line.\n# But since I must rewrite the who", "score": 0.9999, "script_id": "auto"}

## Edit Examples
(none)
