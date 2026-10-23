# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: observe.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 17

suppressPackageStartupMessages(library(shiny))
values <- reactiveValues(A=1)

obsB <- observe({
  print(values$A + 1)
})

# To store expressions for later conversion to observe, use rlang::quo()
myquo <- rlang::quo({ print(values$A + 3) })
obsC <- rlang::inject(observe(!!myquo))

# (Legacy) Can use quoted expressions
obsD <- observe(quote({ print(values$A + 2) }), quoted = TRUE)

# In a normal Shiny app, the web client will trigger flush events. If you
# are at the console, you can force a flush with flushReact()
shiny:::flushReact()