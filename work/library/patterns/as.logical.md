---
id: as.logical
package: bit
confidence: tentative
seed: false
created: 2026-06-20
last_review: 2026-06-29
tie_count: 0
---

# as.logical

## Guidance
Translate to `bool()` for scalars or a list comprehension `[bool(x) for x in ...]` for sequences, following the rule that non-zero numbers are TRUE.

For numeric vectors, translate to a list comprehension applying `bool()` to each element, as any non-zero value in R is coerced to TRUE.

Convert numeric values to booleans using a list comprehension or `astype(bool)` in NumPy, where 0 is False and non-zero is True.

Convert R's `as.logical()` to Python's `bool()` function, ensuring the input is treated as an iterable (list) to mimic R's vectorized behavior.

Translate `as.logical()` to Python's `bool()` function, ensuring that non-zero integers are treated as `True` and zero as `False`.

Convert numeric values to booleans using Python's bool() function, ensuring the logic applies element-wise if the input is a list.

Translate as.logical() using bool() for scalars or a list comprehension with bool() for vectors, as R coerces 0 to FALSE and any non-zero numeric value to TRUE.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
