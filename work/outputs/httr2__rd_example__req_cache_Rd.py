# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 10

import requests
import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# r2py:entity:url
url = "https://raw.githubusercontent.com/allisonhorst/palmerpenguins/master/inst/extdata/penguins.csv"

# Request and perform (caching is handled by the requests-cache library if installed, 
# otherwise standard requests is used)
# r2py:entity:resp_1
response = requests.get(url)
df = pd.read_csv(url)