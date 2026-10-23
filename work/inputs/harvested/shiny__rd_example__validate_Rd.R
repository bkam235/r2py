# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: validate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 24

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {
options(device.ask.default = FALSE)

ui <- fluidPage(
  checkboxGroupInput('in1', 'Check some letters', choices = head(LETTERS)),
  selectizeInput('in2', 'Select a state', choices = c("", state.name)),
  plotOutput('plot')
)

server <- function(input, output) {
  output$plot <- renderPlot({
    validate(
      need(input$in1, 'Check at least one letter!'),
      need(input$in2 != '', 'Please choose a state.')
    )
    plot(1:10, main = paste(c(input$in1, input$in2), collapse = ', '))
  })
}

shinyApp(ui, server)

}