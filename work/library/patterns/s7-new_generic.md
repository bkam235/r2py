---
id: s7-new_generic
package: S7
confidence: tentative
seed: false
created: 2026-06-26
last_review: 2026-06-28
tie_count: 0
---

# s7-new_generic

## Guidance
Translate `new_generic` as a metadata-bearing structure (like a dictionary) containing 'class', 'formals', and 'attributes' to preserve R's object-oriented metadata for verification.

Represent S7 generics as a class wrapper (e.g., S7Generic) that stores the function, the generic name, dispatch arguments, and formal parameters to mimic R's object-oriented dispatch metadata.

Translate S7 generics by creating a wrapper class (e.g., S7_Generic) that stores the function, name, and dispatch arguments, rather than simply attaching attributes to a function object.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
