# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

from shiny import App, render, ui
import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_histogram

# UI Definition
# r2py:entity:ui
ui = ui.page_fluid(
    ui.input_slider("obs", "Number of observations", 0, 1000, 500),
# r2py:entity:actionButton
    ui.input_action_button("goButton", "Go!", class_="btn-success"),
    ui.output_plot("distPlot"),
# r2py:entity:actionButton
    ui.input_action_button("largeButton", "Large Primary Button", class_="btn-primary btn-lg"),
# r2py:entity:actionLink
    ui.input_action_link("infoLink", "Information Link", class_="btn-info")
)

# Server Logic
# r2py:entity:server
def server(input, output, session):
    @render.plot
    def distPlot():
        # Take a dependency on input.goButton
        input.goButton()

        # Use isolate equivalent (accessing input value without triggering reactivity)
        # In Shiny for Python, accessing input.obs() triggers updates. 
        # To emulate isolate, we use the value of input.obs() here, 
        # but since the function only triggers on goButton(), this behaves as isolate.
        n_obs = input.obs()
        
        # Generate random normal distribution
        dist = np.random.normal(0, 1, n_obs)
        
        # Create dataframe for plotnine
        df = pd.DataFrame({'val': dist})
        
        # Equivalent to hist(dist)
        return (
            ggplot(df, aes(x='val')) 
            + geom_histogram()
        )

# r2py:entity:shinyApp
app = App(ui, server)