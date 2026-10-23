# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: insertUI.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 43

suppressPackageStartupMessages(library(shiny))
## Only run this example in interactive R sessions
if (interactive()) {
# Define UI
ui <- fluidPage(
  actionButton("add", "Add UI")
)

# Server logic
server <- function(input, output, session) {
  observeEvent(input$add, {
    insertUI(
      selector = "#add",
      where = "afterEnd",
      ui = textInput(paste0("txt", input$add),
                     "Insert some text")
    )
  })
}

# Complete app with UI and server components
shinyApp(ui, server)
}

if (interactive()) {
# Define UI
ui <- fluidPage(
  actionButton("rmv", "Remove UI"),
  textInput("txt", "This is no longer useful")
)

# Server logic
server <- function(input, output, session) {
  observeEvent(input$rmv, {
    removeUI(
      selector = "div:has(> #txt)"
    )
  })
}

# Complete app with UI and server components
shinyApp(ui, server)
}