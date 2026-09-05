# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np
import pandas as pd
from shiny import App, render, ui, reactive

# r2py:entity:ui
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_task_button("resample", "Resample"),
        open="always"
    ),
    ui.output_text_verbatim("summary"),
)

# r2py:entity:server
def server(input, output, session):
    # eventReactive(input$resample, ignoreNULL=FALSE, ...)
    # reactive.event creates a reactive calculation that triggers when the specified input changes
    @reactive.event(input.resample)
    def sample_data():
        import time
        time.sleep(2)  # Make this artificially slow
        return np.random.randn(100)

    @output
    @render.text
    def summary():
        # R's summary(numeric_vector) output:
        # Min. 1st Qu.  Median Mean 3rd Qu. Max.
        data = sample_data()
        
        # Compute R-equivalent summary statistics
        s_min = np.min(data)
        s_1st = np.percentile(data, 25)
        s_med = np.median(data)
        s_mean = np.mean(data)
        s_3rd = np.percentile(data, 75)
        s_max = np.max(data)
        
        # Format string to match R's output style for numeric vectors
        res = (
            f"Min. 1st Qu.  Median Mean 3rd Qu. Max.\n"
            f"{s_min:g} {s_1st:g} {s_med:g} {s_mean:g} {s_3rd:g} {s_max:g}"
        )
        return res

# r2py:entity:shinyApp
app = App(app_ui, server)