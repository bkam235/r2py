---
id: magrittr.pipe_to_chaining
package: magrittr
confidence: tentative
seed: true
created: 2026-05-28
last_review: 2026-05-28
---

# magrittr.pipe_to_chaining

## Guidance
`x %>% f() %>% g()` → `g(f(x))` (function composition) or pandas method chaining
`x.f().g()` when operating on DataFrames. For multi-step pipelines, assign intermediate
results to variables for readability and debuggability. The native R pipe `|>` (R 4.1+)
follows the same pattern. `x %>% filter(y > 0) %>% select(a, b)` →
`x[x["y"] > 0][["a", "b"]]`. Avoid deeply nested function calls; prefer sequential
assignments when the chain has more than 3 steps.

## Evidence
(none)

## Contradictions
(none)
