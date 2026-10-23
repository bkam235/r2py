# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import pandas as pd
import numpy as np

# The R package 'lava' and 'prodlim' provide specialized survival analysis 
# and simulation for competing risks models (crModel).
# Since there is no direct Python port of the lava package, 
# we simulate the structural output of a competing risks model.

# m <- crModel() 
# This defines a default competing risks model.
# We represent the model parameters (e.g., hazard ratios/probabilities) as a dict.
# r2py:entity:m
m = {
    "n_events": 2,
    "baseline_hazard": [0.1, 0.05]
}

# d <- sim(m, 6)
# This simulates data for 6 individuals based on the model m.
# In a competing risks simulation, we typically generate 
# survival times and the event type (1, 2, or 0 for censored).
# r2py:entity:d
np.random.seed(42)
n_sim = 6

# Approximate simulation: 
# Using an exponential distribution to simulate times to failure for competing risks
# T = -log(U) / lambda
lambdas = np.array(m["baseline_hazard"])
u = np.random.uniform(0, 1, (n_sim, len(lambdas)))
times = -np.log(u) / lambdas

# For each individual, the event is the one that occurs first (minimum time)
event_times = np.min(times, axis=1)
event_types = np.argmin(times, axis=1) + 1 # 1-indexed to match R

# Create the dataframe d
d = pd.DataFrame({
    "time": event_times,
    "status": event_types
})

# print(d)
# r2py:entity:print
print(d)