# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: icon.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 9

suppressPackageStartupMessages(library(shiny))
# add an icon to a submit button
submitButton("Update View", icon = icon("redo"))

navbarPage("App Title",
  tabPanel("Plot", icon = icon("bar-chart-o")),
  tabPanel("Summary", icon = icon("list-alt")),
  tabPanel("Table", icon = icon("table"))
)