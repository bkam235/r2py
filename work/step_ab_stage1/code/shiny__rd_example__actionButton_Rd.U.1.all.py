# Translated from <R script> by r2py v0.3.0
from shiny import App, render, ui
import numpy as np
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
        # Take a dependency on input.goButton. 
        # In shiny for python, reading the value creates the dependency.
        _ = input.goButton()

        # Use isolate() to avoid dependency on input.obs.
        # In Python, we can use session.isolate if available or simply
        # access the value without it being a reactive trigger.
        # Since the function only triggers on goButton, we use the value of input.obs()
        # while ensuring we don't create a reactive dependency if isolate is required.
        # For simplicity and compatibility with the R 'isolate', we wrap it.
        with ui.isolate():
            n_obs = input.obs()
        
        dist = np.random.randn(n_obs)
        
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