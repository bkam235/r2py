# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

from shiny import App, ui, reactive

# r2py:entity:shinyApp
app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            ui.markdown("The first slider controls the second"),
            ui.input_slider("control", "Controller:", min=0, max=20, value=10, step=1),
            ui.input_slider("receive", "Receiver:", min=0, max=20, value=10, step=1),
        ),
        # The main panel in layout_sidebar is just the second positional argument.
        # If empty in R (mainPanel()), we provide an empty div or nothing.
        ui.div() 
    )
)

def server(input, output, session):
    @reactive.effect
    def _():
        val = input.control()
        # Step size is 2 when input value is even; 1 when value is odd.
        # R: (val+1)%%2 + 1
        step_val = ((val + 1) % 2) + 1
        
        # Correct Python method to update slider inputs: ui.update_slider
        ui.update_slider(
            "receive",
            value=val,
            min=val // 2,
            max=val + 4,
            step=step_val
        )

app = App(app_ui, server)