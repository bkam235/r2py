# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# r2py:entity:dog
dog = "The quick brown dog"

# r2py:entity:toupper
print(dog.upper())
# r2py:entity:tolower
print(dog.lower())
# r2py:entity:toTitleCase
print(dog.title())

# The stringr equivalents in Python are the built-in string methods
# r2py:entity:str_to_upper
print(dog.upper())
# r2py:entity:str_to_lower
print(dog.lower())
# r2py:entity:str_to_title
print(dog.title())