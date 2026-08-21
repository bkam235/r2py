# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 4

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, render, ui, reactive

# The R functions withOtelCollect and localOtelCollect are used for OpenTelemetry 
# telemetry collection control. Shiny for Python handles telemetry via 
# standard OpenTelemetry SDKs; these specific wrappers are not part of the 
# high-level shiny-python API. We implement them as no-ops to maintain 
# execution equivalence of the structure.

def withOtelCollect(collect_level, expr):
    """
    Equivalent to withOtelCollect(collect, { expr })
    In R, this wraps a block of code. In Python, we execute the passed 
    callable or return the value.
    """
    # Telemetry logic would go here
    if callable(expr):
        return expr()
    return expr

def localOtelCollect(collect_level):
    """
    Equivalent to localOtelCollect(collect)
    """
    # Telemetry logic would go here
    pass

# r2py:entity:my_function
def my_function():
    localOtelCollect("none")
    # Rest of function executes without telemetry
    # Note: In a real app, this would be inside a server function
    # We use a lambda to mimic the reactive expression definition
    return lambda input_y: input_y * 2

# Simulate the first snippet: withOtelCollect("none", { ... })
withOtelCollect("none", lambda: 
    # Code here won't generate telemetry
    # Mimicking reactive({ input$x + 1 })
    lambda input_x: input_x + 1
)

# Simulate the second snippet: withOtelCollect("reactivity", { ... })
withOtelCollect("reactivity", lambda: 
    # Reactive execution will be traced
    # Mimicking observe({ print(input$x) })
    # r2py:entity:print
# r2py:entity:print
    print("input$x") 
)

# Use local variant in a function
my_function()