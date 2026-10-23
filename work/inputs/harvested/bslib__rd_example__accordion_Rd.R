# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: accordion.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 30

if (rlang::is_interactive()) withAutoprint({ # examplesIf
items <- lapply(LETTERS, function(x) {
  accordion_panel(paste("Section", x), paste("Some narrative for section", x))
})

# First shown by default
accordion(!!!items)
# Nothing shown by default
accordion(!!!items, open = FALSE)
# Everything shown by default
accordion(!!!items, open = TRUE)

# Show particular sections
accordion(!!!items, open = "Section B")
accordion(!!!items, open = c("Section A", "Section B"))

# Provide an id to create a shiny input binding
library(shiny)
library(bslib)

ui <- page_fluid(
  accordion(!!!items, id = "acc")
)

server <- function(input, output) {
  observe(print(input$acc))
}

shinyApp(ui, server)
}) # examplesIf