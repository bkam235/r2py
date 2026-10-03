# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

from shiny import App, render, ui, reactive

# options(shiny.testmode = TRUE)
# In Python shiny, there is no direct equivalent to options(shiny.testmode = TRUE).
# We can use a global variable to mimic this setting.
# r2py:entity:options
SHINY_TESTMODE = True

def exportTestValues(**kwargs):
    """
    Mock for R's exportTestValues.
    In R, this exports reactive values to the session for snapshot testing.
    """
    pass

# UI Definition
# r2py:entity:shinyApp
app_ui = ui.page_fluid(
    ui.h4("Snapshot URL: "),
    ui.output_ui("url"),
    ui.h4("Current values:"),
    ui.output_text_verbatim("values"),
    ui.input_action_button("inc", "Increment x"),
)

def server(input, output, session):
    # vals <- reactiveValues(x = 1)
    vals = reactive.Value(1)

    # y <- reactive({ vals$x + 1 })
    @reactive.calc
    def y():
        return vals() + 1

    # observeEvent(input$inc, { vals$x <<- vals$x + 1 })
    @reactive.effect
    @reactive.event(input.inc)
    def _():
        vals.set(vals() + 1)

    # exportTestValues(x = vals$x, y = y())
    # We wrap this in an effect to ensure it's called during the server session,
    # although in R it's called once during server initialization.
    exportTestValues(x=vals(), y=y())

    # output$url <- renderUI({
    #   url <- session$getTestSnapshotUrl(format="json")
    #   a(href = url, url)
    # })
    @render.ui
    def url():
        # Mock for session$getTestSnapshotUrl(format="json")
        # Since Python's session doesn't have this specific R shinytest method.
        url_val = "http://localhost:8000/snapshot.json"
        return ui.a(url_val, href=url_val)

    # output$values <- renderText({
    #   paste0("vals$x: ", vals$x, "\ny: ", y())
    # })
    @render.text
    def values():
        return f"vals$x: {vals()}\ny: {y()}"

app = App(app_ui, server)