# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 13

from shiny import App, render, ui, reactive

# r2py:entity:counterUI
def counter_ui(id, label="Counter"):
    return ui.div(
        ui.input_action_button(id + "_button", label),
        ui.output_text(id + "_out"),
    )

# r2py:entity:counterServer2
def create_counter_server(id, prefix=""):
    # In shiny-python, we use a closure or a class to simulate module server logic
    # since there isn't a direct 1:1 'moduleServer' function.
    
    count = reactive.Value(0)

    @reactive.effect
    @reactive.event(lambda: None) # Placeholder, logic handled by the button trigger
    def increment():
        pass # Logic handled inside the specific button callback below

    def handle_click():
        count.set(count.get() + 1)

    @render.text
    def output_text():
        return f"{prefix}{count.get()}"

    return handle_click, output_text, count

# Example 1: Multiple Counters
# r2py:entity:ui
app_ui1 = ui.page_fluid(
    counter_ui("counter1", "Counter #1"),
    counter_ui("counter2", "Counter #2"),
)

# r2py:entity:server
def server1(input, output, session):
    # Counter 1
    btn1_fn, out1_fn, _ = create_counter_server("counter1")
    @reactive.effect
    @reactive.event(input.counter1_button)
    def _(): btn1_fn()
    
    # Map the render function to the output id
    @render.text
    def counter1_out():
        return out1_fn()

    # Counter 2
    btn2_fn, out2_fn, _ = create_counter_server("counter2")
    @reactive.effect
    @reactive.event(input.counter2_button)
    def __(): btn2_fn()
    
    @render.text
    def counter2_out():
        return out2_fn()

# Example 2: Counter with Prefix
# r2py:entity:ui_1
app_ui2 = ui.page_fluid(
    counter_ui("counter", "Counter"),
)

# r2py:entity:server_1
def server2(input, output, session):
    btn_fn, out_fn, _ = create_counter_server("counter", prefix="The current count is: ")
    
    @reactive.effect
    @reactive.event(input.counter_button)
    def _():
        btn_fn()

    @render.text
    def counter_out():
        return out_fn()

# To run one of these:
# r2py:entity:shinyApp
app = App(app_ui2, server2)