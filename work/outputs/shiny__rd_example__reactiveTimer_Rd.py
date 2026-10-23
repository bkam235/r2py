# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:entity:interactive
from shiny import App, render, ui, reactive
import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_histogram

# r2py:entity:ui
app_ui = ui.page_fluid(
    ui.input_slider("n", "Number of observations", 2, 1000, 500),
    ui.output_plot("plot")
)

# r2py:entity:server
def server(input, output, session):
    # reactive.Timer is the equivalent of reactiveTimer
    auto_invalidate = reactive.Timer(2000)

    @reactive.effect
    def _():
        # This triggers every 2 seconds
        auto_invalidate()
        # Use session.isolate to ignore changes to input.n
        n_val = session.isolate(input.n())
        print(f"The value of input$n is {n_val}")

    @render.plot
    def plot():
        # Trigger update every 2 seconds
        auto_invalidate()
        
        # Isolate input.n so the plot only updates on the timer, not the slider
        n = session.isolate(input.n())
        data = pd.DataFrame({"val": np.random.randn(n)})
        
        return (
            ggplot(data, aes(x="val")) 
            + geom_histogram(bins=30)
        )

# r2py:entity:shinyApp
app = App(app_ui, server)