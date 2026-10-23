# r2py crawler metadata
# package: profvis
# source_type: rd_example
# topic: profvis_ui.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\profvis\help
# lines: 22

suppressPackageStartupMessages(library(profvis))
# In order to avoid "Hit <Return> to see next plot" prompts,
# run this example with `example(profvis_ui, ask=FALSE)`

if(interactive()) {
  library(shiny)
  shinyApp(
    fluidPage(
      plotOutput("plot"),
      actionButton("new", "New plot"),
      profvis_ui("profiler")
    ),
    function(input, output, session) {
      callModule(profvis_server, "profiler")

      output$plot <- renderPlot({
        input$new
        boxplot(mpg ~ cyl, data = mtcars)
      })
    }
  )
}