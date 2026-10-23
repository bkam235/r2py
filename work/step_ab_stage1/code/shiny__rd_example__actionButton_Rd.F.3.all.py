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
        # Take a dependency on input.goButton. This will run once initially,
        # because the value changes from NULL to 0.
        input.goButton()

        # Use isolate() to avoid dependency on input$obs
        # In Shiny for Python, to isolate we can use the value of input.obs() 
        # knowing the reactivity is driven by input.goButton()
        n_obs = input.obs()
        
        dist = np.random.randn(n_obs)
        
        fig, ax = plt.subplots()
        ax.hist(dist)
        return fig

# r2py:entity:shinyApp
app = App(ui, server)

# Example of adding extra class values
# r2py:entity:actionButton
actionButton_large = ui.input_action_button("largeButton", "Large Primary Button", class_="btn-primary btn-lg")

# r2py:entity:actionLink
actionLink_info = ui.input_action_link("infoLink", "Information Link", class_="btn-info")