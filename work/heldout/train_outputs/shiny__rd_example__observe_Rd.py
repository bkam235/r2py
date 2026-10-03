# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

from shiny import reactive
import pandas as pd
import numpy as np

# In Python Shiny, there is no direct 'reactiveValues' object that allows 
# arbitrary attribute assignment like R. We use a dictionary-like 
# structure or a simple class with reactive.Value.
# r2py:entity:values
class ReactiveValues:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, reactive.Value(value))
    
    def __getattr__(self, name):
        # To mirror R's values$A returning the value, not the reactive object
        val = super().__getattribute__(name)
        if isinstance(val, reactive.Value):
            return val.get()
        return val

    def __setattr__(self, name, value):
        if isinstance(value, reactive.Value):
            super().__setattr__(name, value)
        else:
            # If assigning a raw value, wrap it in reactive.Value
            super().__setattr__(name, reactive.Value(value))

values = ReactiveValues(A=1)

# r2py:entity:obsB
@reactive.effect
def obsB():
    # values.A is accessed via our __getattr__ logic
    print(values.A + 1)

# rlang::quo and inject are for non-standard evaluation in R. 
# In Python, we use a function or lambda to store the expression.
# r2py:entity:myquo
myquo = lambda: print(values.A + 3)

# r2py:entity:obsC
@reactive.effect
def obsC():
    myquo()

# observe(quote(...), quoted=TRUE)
# r2py:entity:obsD
obsD_logic = lambda: print(values.A + 2)

@reactive.effect
def obsD():
    obsD_logic()

# shiny:::flushReact() forces the reactive graph to process.
# In Python Shiny, effects are scheduled. To simulate a flush in a script:
# r2py:entity:flushReact
def flushReact():
    # In a real Shiny app, this is handled by the asyncio loop.
    # For a standalone script, we manually trigger the logic if needed.
    pass

flushReact()