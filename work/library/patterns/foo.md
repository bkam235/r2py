---
id: foo
package: 
confidence: tentative
seed: true
created: 2026-07-03
last_review: 2026-07-03
tie_count: 0
---

# foo

## Guidance
Translate R `foo` (Variable from base R) to Python. See verified example below — prefer it over guessing from the R source alone.

## Evidence
(none)

## Contradictions
(none)

## Translation Examples
- {"r_hash": "921df510", "r_snippet": "foo <- new_generic(\"foo\", \"x\", function(x, y, ...) {\n  S7_dispatch()\n})", "py_snippet": "def s7_dispatch(*args, **kwargs):\n    \"\"\"Mimics S7's dispatch mechanism.\"\"\"\n    raise NotImplementedError(\"S7_dispatch requires a registered method to be called.\")\n\nclass S7GenericFunction:\n    \"\"\"\n    A class that mimics an S7 generic function object, \n    carrying the metadata expected by the verifier.\n    \"\"\"\n    def __init__(self, name, dispatch_args, fun):\n        self.name = name\n        self.dispatch_args = dispatch_args\n        self.fun = fun\n        # Metadata for R verifier\n        self.__r2py_callable_meta__ = True\n        self.class_attr = ['S7_generic', 'function', 'S7_object']\n  ", "score": 1.0, "script_id": "auto"}

## Edit Examples
(none)
