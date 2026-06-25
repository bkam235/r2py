---
id: withautoprint
package: broom
confidence: tentative
seed: false
created: 2026-06-23
last_review: 2026-06-23
tie_count: 0
---

# withautoprint

## Guidance
This is an R idiom for interactive execution; in Python, replace it with standard sequential execution and explicit print() calls for objects that need to be displayed.

The logic inside this block should be executed sequentially; in Python, simply call the functions or use print statements to replicate the automatic printing of returned objects.

In Python, this should be handled by ensuring the return values of function calls (like tidy() or glance()) are explicitly passed to print() or printed via a formatted string.

This R idiom simply ensures that the result of the last expression is printed; in Python, explicitly call print() on the objects to be displayed.

In Python, this idiom is typically handled by explicitly printing variables or using a Jupyter cell's automatic output; for scripts, use explicit print() calls.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
(none)

## Edit Examples
(none)
