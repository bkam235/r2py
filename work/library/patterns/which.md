---
id: which
package: bit
confidence: tentative
seed: false
created: 2026-06-20
last_review: 2026-06-29
tie_count: 0
---

# which

## Guidance
Translate to a list comprehension using `enumerate(l, 1)` to capture 1-based indices of TRUE elements; if R expects a scalar result, handle the case where the list contains only one element.

Translate to a list comprehension using `enumerate(l)` and add 1 to the index to maintain R's 1-based indexing.

Use `np.where(condition)[0] + 1` to mimic R's 1-based indexing for elements that satisfy a condition.

Translate R's `which()` to a list comprehension using `enumerate(iterable, 1)` to maintain 1-based indexing of elements that evaluate to TRUE.

Translate R's `which()` to a list comprehension using `enumerate(iterable, 1)` or `i + 1` to preserve R's 1-based indexing.

Translate R's which() by using a list comprehension with enumerate(l) and adding 1 to the index to maintain R's 1-based indexing.

Translate which() using a list comprehension with enumerate(..., 1). If the R output expects a scalar when only one match is found, handle the result by extracting the first element of the list if its length is 1.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
