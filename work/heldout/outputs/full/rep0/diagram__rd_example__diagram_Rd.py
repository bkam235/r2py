# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# Note: The R 'diagram' package provides specialized graph visualization 
# (flowcharts, matrix-based webs). In Python, the closest equivalents 
# for these structural plots are networkx and matplotlib.

import networkx as nx
import matplotlib.pyplot as plt

# r2py:entity:example
# Translating example(plotmat)
# plotmat creates diagrams based on an adjacency matrix
m_plotmat = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
G_plotmat = nx.from_numpy_array(m_plotmat, create_using=nx.DiGraph)
pos_plotmat = nx.spring_layout(G_plotmat)
nx.draw(G_plotmat, pos_plotmat, with_labels=True, node_color='lightblue', arrowsize=20)
plt.title("Example: plotmat equivalent")
plt.show()

# r2py:entity:example_1
# Translating example(plotweb)
# plotweb creates web-like structures from a matrix
m_plotweb = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
G_plotweb = nx.from_numpy_array(m_plotweb, create_using=nx.Graph)
pos_plotweb = nx.circular_layout(G_plotweb)
nx.draw(G_plotweb, pos_plotweb, with_labels=True, node_color='lightgreen')
plt.title("Example: plotweb equivalent")
plt.show()

# r2py:entity:demo
# Translating demo("flowchart")
# Creating a simple flowchart structure
g_flowchart = nx.DiGraph()
g_flowchart.add_edges_from([("Start", "Process 1"), ("Process 1", "Decision"), 
                            ("Decision", "End"), ("Decision", "Process 1")])
pos_flowchart = {"Start": (0, 0), "Process 1": (1, 0), "Decision": (2, 0), "End": (3, 0)}
nx.draw(g_flowchart, pos_flowchart, with_labels=True, node_shape='s', node_color='orange')
plt.title("Demo: flowchart equivalent")
plt.show()

# r2py:entity:demo_1
# Translating demo("plotmat")
m_demo_mat = np.random.randint(0, 2, (5, 5))
G_demo_mat = nx.from_numpy_array(m_demo_mat, create_using=nx.DiGraph)
nx.draw(G_demo_mat, with_labels=True, node_color='cyan')
plt.title("Demo: plotmat equivalent")
plt.show()

# r2py:entity:demo_2
# Translating demo("plotweb")
m_demo_web = np.random.randint(0, 2, (6, 6))
G_demo_web = nx.from_numpy_array(m_demo_web, create_using=nx.Graph)
nx.draw(G_demo_web, with_labels=True, node_color='pink')
plt.title("Demo: plotweb equivalent")
plt.show()

# The following R commands are system-specific documentation/URL calls.
# In Python, we substitute these with print statements indicating the 
# equivalent documentation paths for the used libraries.
# r2py:entity:edit
print("Equivalent to browseURL/vignette: Refer to https://networkx.org/documentation/stable/")
# r2py:entity:browseURL_1
print("Equivalent to system.file: Check the site-packages directory for networkx and plotnine.")

# Shiny App wrapper to simulate the environment if needed
app_ui = ui.page_fluid(
    ui.h2("Diagram Translation Demo"),
    ui.output_text("status")
)

def server(input, output, session):
    @render.text
    def status():
        return "Diagrams rendered via NetworkX/Matplotlib. Documentation available online."

app = App(app_ui, server)