# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np
import shiny
from plotnine import *
import pkg_resources

# r2py:entity:tidyr_new_interface
def tidyr_new_interface():
    try:
        version = pkg_resources.get_distribution("tidyr").version
        # Note: tidyr is an R package; if using a python wrapper or 
        # simulated versioning, this is the logic.
        return version > "0.8.99"
    except pkg_resources.DistributionNotFound:
        return False