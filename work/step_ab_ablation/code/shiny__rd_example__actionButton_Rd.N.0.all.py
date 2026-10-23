# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

from shiny import App, render, ui
import numpy as np
import matplotlib.pyplot as plt

# r2py:entity:ui
ui = ui.page_fluid(
    ui.input_slider("obs", "Number of observations", 0, 1000, 500),
    ui.action_button("goButton", "Go!", class_="btn-success"),
    ui.output_plot("distPlot"),
)

# r2py:entity:server
def server(input, output, session):
    @render.plot
    def distPlot():
        # Take a dependency on input.goButton. 
        # In shiny-python, reading the input value creates the dependency.
        _ = input.goButton()

        # Use isolate() equivalent. 
        # In shiny-python, we use reactive.isolate() to prevent triggers.
        from shiny import reactive
        with reactive.isolate():
            n_obs = input.obs()
            dist = np.random.randn(n_obs)
            plt.hist(dist)
            return plt.gcf()

# r2py:entity:shinyApp
app = App(ui, server)

# Example of adding extra class values
# r2py:entity:actionButton
actionButton = ui.action_button("largeButton", "Large Primary Button", class_="btn-primary btn-lg")
# r2py:entity:actionLink
actionLink = ui.action_link("infoLink", "Information Link", class_="btn-info")