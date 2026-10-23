# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: showTab.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 42

suppressPackageStartupMessages(library(shiny))
## Only run this example in interactive R sessions
if (interactive()) {

ui <- navbarPage("Navbar page", id = "tabs",
  tabPanel("Home",
    actionButton("hideTab", "Hide 'Foo' tab"),
    actionButton("showTab", "Show 'Foo' tab"),
    actionButton("hideMenu", "Hide 'More' navbarMenu"),
    actionButton("showMenu", "Show 'More' navbarMenu")
  ),
  tabPanel("Foo", "This is the foo tab"),
  tabPanel("Bar", "This is the bar tab"),
  navbarMenu("More",
    tabPanel("Table", "Table page"),
    tabPanel("About", "About page"),
    "------",
    "Even more!",
    tabPanel("Email", "Email page")
  )
)

server <- function(input, output, session) {
  observeEvent(input$hideTab, {
    hideTab(inputId = "tabs", target = "Foo")
  })

  observeEvent(input$showTab, {
    showTab(inputId = "tabs", target = "Foo")
  })

  observeEvent(input$hideMenu, {
    hideTab(inputId = "tabs", target = "More")
  })

  observeEvent(input$showMenu, {
    showTab(inputId = "tabs", target = "More")
  })
}

shinyApp(ui, server)
}