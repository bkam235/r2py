# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: fileInput.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 30

suppressPackageStartupMessages(library(shiny))
## Only run examples in interactive R sessions
if (interactive()) {

ui <- fluidPage(
  sidebarLayout(
    sidebarPanel(
      fileInput("file1", "Choose CSV File", accept = ".csv"),
      checkboxInput("header", "Header", TRUE)
    ),
    mainPanel(
      tableOutput("contents")
    )
  )
)

server <- function(input, output) {
  output$contents <- renderTable({
    file <- input$file1
    ext <- tools::file_ext(file$datapath)

    req(file)
    validate(need(ext == "csv", "Please upload a csv file"))

    read.csv(file$datapath, header = input$header)
  })
}

shinyApp(ui, server)
}