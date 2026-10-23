# r2py crawler metadata
# package: shiny
# source_type: rd_example
# topic: withOtelCollect.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shiny\help
# lines: 19

suppressPackageStartupMessages(library(shiny))
# Temporarily disable telemetry collection
withOtelCollect("none", {
  # Code here won't generate telemetry
  reactive({ input$x + 1 })
})

# Collect reactivity telemetry but not other events
withOtelCollect("reactivity", {
  # Reactive execution will be traced
  observe({ print(input$x) })
})

# Use local variant in a function
my_function <- function() {
  localOtelCollect("none")
  # Rest of function executes without telemetry
  reactive({ input$y * 2 })
}