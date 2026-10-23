# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: isolate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 43

suppressPackageStartupMessages(library(shiny))
observe({
  input$saveButton  # Do take a dependency on input$saveButton

  # isolate a simple expression
  data <- get(isolate(input$dataset))  # No dependency on input$dataset
  writeToDatabase(data)
})

observe({
  input$saveButton  # Do take a dependency on input$saveButton

  # isolate a whole block
  data <- isolate({
    a <- input$valueA   # No dependency on input$valueA or input$valueB
    b <- input$valueB
    c(a=a, b=b)
  })
  writeToDatabase(data)
})

observe({
  x <- 1
  # x outside of isolate() is affected
  isolate(x <- 2)
  print(x) # 2

  y <- 1
  # Use local() to avoid affecting calling environment
  isolate(local(y <- 2))
  print(y) # 1
})



# Can also use isolate to call reactive expressions from the R console
values <- reactiveValues(A=1)
fun <- reactive({ as.character(values$A) })
isolate(fun())
# "1"

# isolate also works if the reactive expression accesses values from the
# input object, like input$x