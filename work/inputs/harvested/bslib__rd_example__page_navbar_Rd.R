# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: page_navbar.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 33

if (rlang::is_interactive()) withAutoprint({ # examplesIf
library(shiny)
library(bslib)

link_shiny <- tags$a(
  shiny::icon("github"), "Shiny",
  href = "https://github.com/rstudio/shiny",
  target = "_blank"
)
link_posit <- tags$a(
  shiny::icon("r-project"), "Posit",
  href = "https://posit.co",
  target = "_blank"
)

ui <- page_navbar(
  title = "My App",
  nav_panel(title = "One", p("First page content.")),
  nav_panel(title = "Two", p("Second page content.")),
  nav_panel("Three", p("Third page content.")),
  nav_spacer(),
  nav_menu(
    title = "Links",
    align = "right",
    nav_item(link_shiny),
    nav_item(link_posit)
  )
)

server <- function(...) { } # not used in this example

shinyApp(ui, server)
}) # examplesIf