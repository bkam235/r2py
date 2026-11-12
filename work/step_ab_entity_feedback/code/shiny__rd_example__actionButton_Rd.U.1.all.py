from shiny import App, render, ui
import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_histogram

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
        # Take a dependency on input.goButton
        input.goButton()

        # In Shiny for Python, we use isolate to avoid triggering 
        # on input.obs() updates.
        with ui.isolate():
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
print(ui.input_action_button("largeButton", "Large Primary Button", class_="btn-primary btn-lg"))
# r2py:entity:actionLink
print(ui.input_action_link("infoLink", "Information Link", class_="btn-info"))