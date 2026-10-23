# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: checkboxGroupInput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 40

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  checkboxGroupInput("variable", "Variables to show:",
                     c("Cylinders" = "cyl",
                       "Transmission" = "am",
                       "Gears" = "gear")),
  tableOutput("data")
)

server <- function(input, output, session) {
  output$data <- renderTable({
    mtcars[, c("mpg", input$variable), drop = FALSE]
  }, rownames = TRUE)
}

shinyApp(ui, server)

ui <- fluidPage(
  checkboxGroupInput("icons", "Choose icons:",
    choiceNames =
      list(icon("calendar"), icon("bed"),
           icon("cog"), icon("bug")),
    choiceValues =
      list("calendar", "bed", "cog", "bug")
  ),
  textOutput("txt")
)

server <- function(input, output, session) {
  output$txt <- renderText({
    icons <- paste(input$icons, collapse = ", ")
    paste("You chose", icons)
  })
}

shinyApp(ui, server)
}