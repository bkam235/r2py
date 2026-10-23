# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

from shiny import App, render, ui
import numpy as np
import matplotlib.pyplot as plt
from shiny.reactive import isolate

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

        # Use isolate() to avoid dependency on input.obs
        # In Shiny for Python, isolate() is used to prevent reactivity
        n_obs = isolate(input.obs())
        
        # Generate random normal distribution (rnorm)
        dist = np.random.normal(0, 1, int(n_obs))
        
        # Equivalent to hist(dist) using matplotlib
        fig, ax = plt.subplots()
        ax.hist(dist)
        return fig

# r2py:entity:shinyApp
app = App(ui, server)

# Example of adding extra class values
# r2py:entity:actionButton
largeButton = ui.input_action_button("largeButton", "Large Primary Button", class_="btn-primary btn-lg")

# r2py:entity:actionLink
infoLink = ui.input_action_link("infoLink", "Information Link", class_="btn-info")