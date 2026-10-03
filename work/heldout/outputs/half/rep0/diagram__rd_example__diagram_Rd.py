# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

import pandas as pd
import numpy as np
from plotnine import *
import shiny
from shiny import App, ui, render

# Python does not have a direct 1:1 mirror of the 'diagram' package's plotmat/plotweb.
# The functionality is approximated using plotnine for visualization of matrices/webs.

# r2py:entity:example
# Approximation of plotmat: Visualizing a matrix as a directed graph/adjacency plot
# Example data representing a matrix for plotmat
m = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
d = pd.DataFrame({
    'from': np.repeat(np.arange(3), 3),
    'to': np.tile(np.arange(3), 3),
    'weight': m.flatten()
})
d = d[d['weight'] > 0]

# Visualizing the relationship (similar to plotmat/flowchart)
g = (
    ggplot(d, aes(x='from', y='to')) 
    + geom_point(size=5) 
    + labs(title="Approximation of plotmat/flowchart")
)
print(g)

# r2py:entity:example_1
# Approximation of plotweb: Visualizing a web/connectivity matrix
# Creating a dummy connectivity matrix
w = np.random.randint(0, 2, (5, 5))
d_web = pd.DataFrame(w)
d_web = d_web.stack().reset_index()
d_web.columns = ['node_a', 'node_b', 'connection']
d_web = d_web[d_web['connection'] == 1]

g_web = (
    ggplot(d_web, aes(x='node_a', y='node_b')) 
    + geom_tile(fill="steelblue") 
    + labs(title="Approximation of plotweb")
)
print(g_web)

# r2py:entity:demo_2
# Shiny app to simulate the demo/vignette interactive environment
app_ui = ui.page_fluid(
    ui.h2("Diagram Package Simulation"),
    ui.p("This app simulates the demo/vignette functionality of the R diagram package."),
    ui.output_plot("matrix_plot")
)

def server(input, output, session):
    @render.plot
    def matrix_plot():
        return g

app = App(app_ui, server)

# The following lines simulate the browseURL/vignette behavior by printing paths
import os
# r2py:entity:browseURL_1
print(f"Simulated Documentation Path: {os.getcwd()}/doc")
# r2py:entity:edit
print("Vignette: Diagram Package Documentation loaded in simulation mode.")