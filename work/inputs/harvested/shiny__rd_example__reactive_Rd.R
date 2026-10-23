# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: reactive.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 28

suppressPackageStartupMessages(library(shiny))
library(rlang)
values <- reactiveValues(A=1)

reactiveB <- reactive({
  values$A + 1
})
# View the values from the R console with isolate()
isolate(reactiveB())
# 2

# To store expressions for later conversion to reactive, use quote()
myquo <- rlang::quo(values$A + 2)
# Unexpected value! Sending a quosure directly will not work as expected.
reactiveC <- reactive(myquo)
# We'd hope for `3`, but instead we get the quosure that was supplied.
isolate(reactiveC())

# Instead, the quosure should be `rlang::inject()`ed
reactiveD <- rlang::inject(reactive(!!myquo))
isolate(reactiveD())
# 3

# (Legacy) Can use quoted expressions
expr <- quote({ values$A + 3 })
reactiveE <- reactive(expr, quoted = TRUE)
isolate(reactiveE())
# 4