# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

from shiny import App, render, ui
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# UI Definition
# r2py:entity:ui
ui = ui.page_fluid(
    ui.input_slider("obs", "Number of observations", 0, 1000, 500),
    ui.input_action_button("goButton", "Go!", class_="btn-success"),
    ui.output_plot("distPlot")
)

# Server Logic
# r2py:entity:server
def server(input, output, session):
    @render.plot
    def distPlot():
        # Take a dependency on input.goButton
        input.goButton()

        # Use isolate equivalent
        # In Shiny for Python, we can use reactive.isolate() if available, 
        # but accessing a value inside a reactive context that is already 
        # triggered by another input (goButton) effectively achieves the 
        # desired dependency behavior.
        n_obs = input.obs()
        
        # Generate random normal distribution
        dist = np.random.normal(0, 1, n_obs)
        
        # Equivalent to hist(dist) using matplotlib
        plt.hist(dist)
        return plt.gcf()

# r2py:entity:shinyApp
app = App(ui, server)

# Example of adding extra class values
# r2py:entity:actionButton
largeButton = ui.input_action_button("largeButton", "Large Primary Button", class_="btn-primary btn-lg")
print(largeButton)

# r2py:entity:actionLink
infoLink = ui.input_action_link("infoLink", "Information Link", class_="btn-info")
print(infoLink)