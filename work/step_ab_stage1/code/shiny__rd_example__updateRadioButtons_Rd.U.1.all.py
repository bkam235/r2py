from shiny import App, ui, reactive

# r2py:entity:ui
ui = ui.page_fluid(
    ui.p("The first radio button group controls the second"),
    ui.input_radio_buttons(
        "inRadioButtons", 
        "Input radio buttons", 
        ["Item A", "Item B", "Item C"]
    ),
    ui.input_radio_buttons(
        "inRadioButtons2", 
        "Input radio buttons 2", 
        ["Item A", "Item B", "Item C"]
    )
)

# r2py:entity:server
def server(input, output, session):
    @reactive.effect
    def _():
        x = input.inRadioButtons()

        # Can also set the label and select items
        session.update_radio_buttons(
            "inRadioButtons2",
            label=f"radioButtons label {x}",
            choices=[x],
            selected=x
        )

# r2py:entity:shinyApp
app = App(ui=ui, server=server)