# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import numpy as np
import pandas as pd
from plotnine import *

# Approximation of e1071 sigmoid functions
# r2py:entity:plot
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# r2py:entity:plot_1
def dsigmoid(x):
    s = sigmoid(x)
    return s * (1 - s)

# r2py:entity:plot_2
def d2sigmoid(x):
    s = sigmoid(x)
    return s * (1 - s) * (1 - 2 * s)

# r2py:entity:plot
# Generate data for plotting
x_vals = np.linspace(-5, 5, 100)
df = pd.DataFrame({
    'x': np.tile(x_vals, 3),
    'y': np.concatenate([sigmoid(x_vals), dsigmoid(x_vals), d2sigmoid(x_vals)]),
    'group': np.repeat(['sigmoid', 'dsigmoid', 'd2sigmoid'], 100)
})

# Equivalent of plot calls
plot_obj = (
    ggplot(df, aes(x='x', y='y', color='group'))
    + geom_line()
    + scale_y_continuous(limits=(-0.2, 1))
    + scale_color_manual(values={'sigmoid': 'black', 'dsigmoid': 'red', 'd2sigmoid': 'green'})
    + theme_minimal()
)

print(plot_obj)