# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: radioButtons.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 49

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  radioButtons("dist", "Distribution type:",
               c("Normal" = "norm",
                 "Uniform" = "unif",
                 "Log-normal" = "lnorm",
                 "Exponential" = "exp")),
  plotOutput("distPlot")
)

server <- function(input, output) {
  output$distPlot <- renderPlot({
    dist <- switch(input$dist,
                   norm = rnorm,
                   unif = runif,
                   lnorm = rlnorm,
                   exp = rexp,
                   rnorm)

    hist(dist(500))
  })
}

shinyApp(ui, server)

ui <- fluidPage(
  radioButtons("rb", "Choose one:",
               choiceNames = list(
                 icon("calendar"),
                 HTML("<p style='color:red;'>Red Text</p>"),
                 "Normal text"
               ),
               choiceValues = list(
                 "icon", "html", "text"
               )),
  textOutput("txt")
)

server <- function(input, output) {
  output$txt <- renderText({
    paste("You chose", input$rb)
  })
}

shinyApp(ui, server)
}