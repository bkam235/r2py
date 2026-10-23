# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

from shiny import App, ui, reactive

# r2py:entity:ui
ui = ui.page_fluid(
    ui.p("The first radio button group controls the second"),
    ui.input_radio_buttons(
        "inRadioButtons", 
        "Input radio buttons", 
        choices=["Item A", "Item B", "Item C"]
    ),
    ui.input_radio_buttons(
        "inRadioButtons2", 
        "Input radio buttons 2", 
        choices=["Item A", "Item B", "Item C"]
    )
)

# r2py:entity:server
def server(input, output, session):
    @reactive.effect
    def _():
        x = input.inRadioButtons()
        
        # Can also set the label and select items
        ui.update_radio_buttons(
            session,
            "inRadioButtons2",
            label=f"radioButtons label {x}",
            choices=[x],
            selected=x
        )

# r2py:entity:shinyApp
app = App(
    ui=ui,
    server=server
)