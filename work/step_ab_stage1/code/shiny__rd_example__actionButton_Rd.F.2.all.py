# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

from shiny import App, render, ui
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# r2py:entity:ui
ui = ui.page_fluid(
    ui.input_slider("obs", "Number of observations", 0, 1000, 500),
    ui.input_action_button("goButton", "Go!", class_="btn-success"),
    ui.output_plot("distPlot")
)

# r2py:entity:server
def server(input, output, session):
    @render.plot
    def distPlot():
        # Take a dependency on input.goButton. This will run once initially,
        # because the value changes from NULL to 0.
        input.goButton()

        # Use isolate() to avoid dependency on input$obs
        # In shiny for python, we can use reactive.isolate or simply access the value
        # since the trigger is already constrained by input.goButton()
        n_obs = ui.reactive.isolate(input.obs())
        
        dist = np.random.normal(0, 1, n_obs)
        
        plt.hist(dist)
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        return plt.gcf()

# r2py:entity:shinyApp
app = App(ui, server)

# Example of adding extra class values
# r2py:entity:actionButton
actionButton_large = ui.input_action_button("largeButton", "Large Primary Button", class_="btn-primary btn-lg")

# r2py:entity:actionLink
actionLink_info = ui.input_action_link("infoLink", "Information Link", class_="btn-info")