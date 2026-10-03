# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np
from plotnine import *

# r2py:entity:plot.discrete_distr
def plot_discrete_distr(x, **kwargs):
    # Assuming x is a distribution object or a set of values
    # Since autoplot for discrete distributions usually implies a probability mass function (PMF)
    # We create a DataFrame from the data to plot using plotnine
    
    if hasattr(x, 'pmf'):
        # If x is a distribution object (like from scipy.stats)
        vals = np.arange(int(x.ppf(0.001)), int(x.ppf(0.999)) + 1)
        probs = [x.pmf(v) for v in vals]
        d = pd.DataFrame({'x': vals, 'prob': probs})
    else:
        # If x is a sequence of observations
        d = pd.Series(x).value_counts(normalize=True).reset_index()
        d.columns = ['x', 'prob']
    
    p = (ggplot(d) + 
         geom_col(mapping=aes(x='x', y='prob')) + 
         theme_minimal())
    
    print(p)