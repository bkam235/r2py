# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pytest

# Since withr provides a mechanism for deferred execution of code, 
# we can implement this logic in Python using a global list to mimic the 'global_exits' behavior.

# r2py:entity:defer
class WithrMock:
    def __init__(self):
        self.global_exits = []

    def defer(self, expr_func, priority="first"):
        if priority == "first":
            self.global_exits.insert(0, expr_func)
        else:
            self.global_exits.append(expr_func)

# r2py:entity:deferred_run
    def deferred_run(self):
        # Execute and clear the deferred events
        while self.global_exits:
            expr_func = self.global_exits.pop()
            expr_func()

withr = WithrMock()

# In R: withr::defer(print("hi"))
# Python requires a callable for deferred execution
# r2py:entity:defer
withr.defer(lambda: print("hi"))

# In R: withr::deferred_run()
# r2py:entity:deferred_run
withr.deferred_run()