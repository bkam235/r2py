# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: varSelectInput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 36

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

library(ggplot2)

# single selection
shinyApp(
  ui = fluidPage(
    varSelectInput("variable", "Variable:", mtcars),
    plotOutput("data")
  ),
  server = function(input, output) {
    output$data <- renderPlot({
      ggplot(mtcars, aes(!!input$variable)) + geom_histogram()
    })
  }
)


# multiple selections

shinyApp(
 ui = fluidPage(
   varSelectInput("variables", "Variable:", mtcars, multiple = TRUE),
   tableOutput("data")
 ),
 server = function(input, output) {
   output$data <- renderTable({
      if (length(input$variables) == 0) return(mtcars)
      mtcars %>% dplyr::select(!!!input$variables)
   }, rownames = TRUE)
 }
)

}