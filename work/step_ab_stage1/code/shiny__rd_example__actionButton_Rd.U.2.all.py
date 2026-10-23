from shiny import App, render, ui, reactive
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
        # Take a dependency on input.goButton. 
        # This will run once initially, because the value changes from NULL to 0.
        input.goButton()

        # Use reactive.isolate() to avoid dependency on input.obs
        n_obs = reactive.isolate(input.obs())
        
        # Generate random normal distribution (rnorm)
        dist = np.random.randn(n_obs)
        
        # Create dataframe for plotnine (equivalent to hist(dist))
        df = pd.DataFrame({'val': dist})
        return (
            ggplot(df, aes(x='val')) 
            + geom_histogram()
        )

# r2py:entity:shinyApp
app = App(ui, server)

# Example of adding extra class values
# r2py:entity:actionButton
largeButton = ui.input_action_button("largeButton", "Large Primary Button", class_="btn-primary btn-lg")
# r2py:entity:actionLink
infoLink = ui.input_action_link("infoLink", "Information Link", class_="btn-info")