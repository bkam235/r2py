# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# The R function plotIllnessDeathModel() is a specialized visualization 
# from the 'prodlim' package used to illustrate a multi-state model 
# (specifically an illness-death model). 
# Since there is no direct Python library for this specific diagram, 
# we implement the logic using plotnine to recreate the state transition plots.

# r2py:entity:plotIllnessDeathModel
def create_illness_death_plot(style=1, state_labels=None, box1_col="white", box2_col="white", box3_col="white"):
    # Default labels for the illness-death model states
    if state_labels is None:
        state_labels = ["Healthy", "Ill", "Dead"]
    
    # Define coordinates for the states
    # State 1: Healthy, State 2: Ill, State 3: Dead
    nodes = pd.DataFrame({
        'x': [1, 2, 1.5],
        'y': [2, 2, 1],
        'label': state_labels,
        'color': [box1_col, box2_col, box3_col]
    })

    # Define transitions (edges)
    # 1 -> 2 (Illness), 1 -> 3 (Death from Healthy), 2 -> 3 (Death from Ill)
    edges = pd.DataFrame({
        'x': [1, 1, 2, 1, 1.5, 1.5],
        'y': [2, 2, 2, 2, 1, 1],
        'xend': [2, 1.5, 1.5, 2, 1.5, 1.5],
        'yend': [2, 1, 1, 2, 1, 1]
    })

    # Create the plot
    p = (
        ggplot() 
        + geom_segment(aes(x='x', y='y', xend='xend', yend='yend'), data=edges, arrow=arrow(length=0.1), size=1)
        + geom_point(aes(x='x', y='y', color='color'), data=nodes, size=10, shape=15)
        + geom_text(aes(x='x', y='y', label='label'), data=nodes, va='bottom', nudge_y=0.1)
        + scale_color_identity()
        + theme_void()
        + labs(title=f"Illness-Death Model (Style {style})")
    )
    return p

# Translation of the specific R calls:

# plotIllnessDeathModel()
# r2py:entity:plotIllnessDeathModel
p1 = create_illness_death_plot()

# plotIllnessDeathModel(style=2)
# r2py:entity:plotIllnessDeathModel_1
p2 = create_illness_death_plot(style=2)

# plotIllnessDeathModel(style=2, stateLabels=c("a","b\nc","d"), box1.col="yellow", box2.col="green", box3.col="red")
# r2py:entity:plotIllnessDeathModel_2
p3 = create_illness_death_plot(
    style=2, 
    state_labels=["a", "b\nc", "d"], 
    box1_col="yellow", 
    box2_col="green", 
    box3_col="red"
)

# Displaying plots (equivalent to R's plotting behavior)
print(p1)
print(p2)
print(p3)