from shiny import App, render, ui, reactive
import numpy as np
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
        # Take a dependency on input.goButton. 
        # In Shiny for Python, accessing input.goButton() makes the function reactive to it.
        input.goButton()

        # Use reactive.isolate() to avoid dependency on input.obs
        n_obs = reactive.isolate(input.obs())
        
        # Generate random normal distribution
        dist = np.random.normal(0, 1, n_obs)
        
        # Equivalent to hist(dist)
        fig, ax = plt.subplots()
        ax.hist(dist)
        return fig

# r2py:entity:shinyApp
app = App(ui, server)

# Example of adding extra class values
# R auto-prints these expressions to stdout.
# r2py:entity:actionButton
print(ui.input_action_button("largeButton", "Large Primary Button", class_="btn-primary btn-lg"))
# r2py:entity:actionLink
print(ui.input_action_link("infoLink", "Information Link", class_="btn-info"))