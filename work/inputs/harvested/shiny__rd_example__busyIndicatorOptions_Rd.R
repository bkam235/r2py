# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: busyIndicatorOptions.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 48

suppressPackageStartupMessages(library(shiny))
if (rlang::is_interactive()) withAutoprint({ # examplesIf

library(bslib)

card_ui <- function(id, spinner_type = id) {
  card(
    busyIndicatorOptions(spinner_type = spinner_type),
    card_header(paste("Spinner:", spinner_type)),
    plotOutput(shiny::NS(id, "plot"))
  )
}

card_server <- function(id, simulate = reactive()) {
  moduleServer(
    id = id,
    function(input, output, session) {
      output$plot <- renderPlot({
        Sys.sleep(1)
        simulate()
        plot(x = rnorm(100), y = rnorm(100))
      })
    }
  )
}

ui <- page_fillable(
  useBusyIndicators(),
  input_task_button("simulate", "Simulate", icon = icon("refresh")),
  layout_columns(
    card_ui("ring"),
    card_ui("bars"),
    card_ui("dots"),
    card_ui("pulse"),
    col_widths = 6
  )
)

server <- function(input, output, session) {
  simulate <- reactive(input$simulate)
  card_server("ring", simulate)
  card_server("bars", simulate)
  card_server("dots", simulate)
  card_server("pulse", simulate)
}

shinyApp(ui, server)
}) # examplesIf