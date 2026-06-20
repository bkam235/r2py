---
id: r2py.param-name-mapping
package: 
confidence: tentative
seed: false
created: 2026-06-16
last_review: 2026-06-16
tie_count: 0
---

# r2py.param-name-mapping

## Guidance
When wrapping R functions that use different parameter names than their Python equivalents, ensure all parameter name mappings are included in the translation, including common abbreviations like 'length' mapping to 'length_out'.

## Evidence
- ca1440d6104b → score 0.271 (path: exact, variable: )

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
- {"failure_class": "syntax", "old_code": "ret = chunks(**{k.replace('from', 'from_val').replace('to', 'to_val').replace('by', 'by').replace('length_out', 'length_out').replace('along_with', 'along_with').replace('overlap', 'overlap').replace('method', 'method').replace('maxindex', 'maxindex'): v for k, v in l.items()})", "new_code": "ret = chunks(**{k.replace('from', 'from_val').replace('to', 'to_val').replace('by', 'by').replace('length', 'length_out').replace('length_out', 'length_out').replace('along_with', 'along_with').replace('overlap', 'overlap').replace('method', 'method').replace('maxindex', 'maxindex'): v for k, v in l", "score_delta": 0.2711, "script_id": "ca1440d6104b"}
