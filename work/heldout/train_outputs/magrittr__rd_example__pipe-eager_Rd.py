# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 17

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# r2py:entity:f
def f(x):
    print("foo")
    return x

# r2py:entity:g
def g(x):
    print("bar")
    return x

# r2py:entity:h
def h(x):
    print("baz")
    return x

# Translation of NULL %>% f() %>% g() %>% h()
# r2py:entity:h_1
res1 = h(g(f(None)))

# Translation of NULL %!>% f() %!>% g() %!>% h()
# Note: %!>% is the exposition pipe which forces evaluation of the LHS.
# In Python, arguments are evaluated before the function call, so it behaves similarly to %>%
# r2py:entity:h_2
res2 = h(g(f(None)))

# r2py:entity:f_3
def f(x):
    # force(x) in R ensures the promise is evaluated. 
    # Python evaluates arguments eagerly by default.
    print("foo")
    return x

# r2py:entity:g_3
def g(x):
    print("bar")
    return x

# r2py:entity:h_3
def h(x):
    print("baz")
    return x

# Translation of NULL %>% f() %>% g() %>% h()
# r2py:entity:h_4
res3 = h(g(f(None)))