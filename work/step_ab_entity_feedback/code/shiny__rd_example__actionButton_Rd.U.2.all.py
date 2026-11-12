# Translated from <R script> by r2py v0.3.0
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

        # In Shiny for Python, we can use reactive.isolate if available, 
        # but since this function only triggers on goButton(), accessing 
        # input.obs() here effectively isolates it from triggering 
        # the plot on its own change.
        n_obs = input.obs()
        
        # Generate random normal distribution
        dist = np.random.normal(0, 1, n_obs)
        
        # Equivalent to hist(dist) using matplotlib for standard output
        plt.hist(dist)
        return plt.gcf()

# r2py:entity:shinyApp
app = App(ui, server)

# Example of adding extra class values
# R auto-prints these results to stdout
# r2py:entity:actionButton
btn_large = ui.input_action_button("largeButton", "Large Primary Button", class_="btn-primary btn-lg")
print(btn_large)

# r2py:entity:actionLink
link_info = ui.input_action_link("infoLink", "Information Link", class_="btn-info")
print(link_info)