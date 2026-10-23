from shiny import App, render, ui
import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_histogram

# UI Definition
# r2py:entity:ui
ui = ui.div(
    ui.input_slider("obs", "Number of observations", 0, 1000, 500),
    ui.input_action_button("goButton", "Go!", class_="btn-success"),
    ui.output_plot("distPlot"),
    # Wrapping in a div to simulate fluidPage's container-fluid structure if needed, 
    # but fluidPage in R is basically a div with class container-fluid.
)
ui.add_class("container-fluid")

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

# Example of adding extra class values
# r2py:entity:actionButton
large_button = ui.input_action_button("largeButton", "Large Primary Button", class_="btn-primary btn-lg")
print(large_button)

# r2py:entity:actionLink
info_link = ui.input_action_link("infoLink", "Information Link", class_="btn-info")
print(info_link)