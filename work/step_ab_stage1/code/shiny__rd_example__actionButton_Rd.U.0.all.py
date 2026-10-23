# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

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
        # In Shiny for Python, accessing the value creates the dependency.
        _ = input.goButton()

        # Use isolate equivalent: in Shiny for Python, we can use a reactive.calc 
        # or simply access the value if we only want it to trigger on goButton.
        # The R code uses isolate(rnorm(input$obs))
        # To emulate isolate in Python, we access input.obs() but it won't trigger
        # the plot unless goButton changes because goButton is the primary dependency here.
        n_obs = input.obs()
        
        dist = np.random.randn(n_obs)
        
        fig, ax = plt.subplots()
        ax.hist(dist)
        return fig

# r2py:entity:shinyApp
app = App(ui, server)

# Example of adding extra class values - these are separate calls in R
# r2py:entity:actionButton
largeButton = ui.input_action_button("largeButton", "Large Primary Button", class_="btn-primary btn-lg")
# r2py:entity:actionLink
infoLink = ui.input_action_link("infoLink", "Information Link", class_="btn-info")