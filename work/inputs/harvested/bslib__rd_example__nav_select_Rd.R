# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: nav_select.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 45

suppressPackageStartupMessages(library(bslib))
can_browse <- function() rlang::is_interactive() && require("shiny")

# Selecting a tab
if (can_browse()) {
  shinyApp(
    page_fluid(
      radioButtons("item", "Choose", c("A", "B")),
      navset_hidden(
        id = "container",
        nav_panel_hidden("A", "a"),
        nav_panel_hidden("B", "b")
      )
    ),
    function(input, output) {
      observe(nav_select("container", input$item))
    }
  )
}

# Inserting and removing
if (can_browse()) {
  ui <- page_fluid(
    actionButton("add", "Add 'Dynamic' tab"),
    actionButton("remove", "Remove 'Foo' tab"),
    navset_tab(
      id = "tabs",
      nav_panel("Hello", "hello"),
      nav_panel("Foo", "foo"),
      nav_panel("Bar", "bar tab")
    )
  )
  server <- function(input, output) {
    observeEvent(input$add, {
      nav_insert(
        "tabs", target = "Bar", select = TRUE,
        nav_panel("Dynamic", "Dynamically added content")
      )
    })
    observeEvent(input$remove, {
      nav_remove("tabs", target = "Foo")
    })
  }
  shinyApp(ui, server)
}