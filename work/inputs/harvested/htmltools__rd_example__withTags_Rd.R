# r2py crawler metadata
# package: htmltools
# source_type: rd_example
# topic: withTags.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmltools\help
# lines: 24

suppressPackageStartupMessages(library(htmltools))
# Using tags$ each time
tags$div(class = "myclass",
  tags$h3("header"),
  tags$p("text")
)

# Equivalent to above, but using withTags
withTags(
  div(class = "myclass",
    h3("header"),
    p("text")
  )
)

# Setting .noWS for all tags in withTags()
withTags(
  div(
    class = "myclass",
    h3("header"),
    p("One", strong(span("two")), "three")
  ),
  .noWS = c("outside", "inside")
)