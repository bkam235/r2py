# r2py crawler metadata
# package: htmltools
# source_type: rd_example
# topic: css.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\htmltools\help
# lines: 7

suppressPackageStartupMessages(library(htmltools))
padding <- 6
css(
  font.family = "Helvetica, sans-serif",
  margin = paste0(c(10, 20, 10, 20), "px"),
  "padding!" = if (!is.null(padding)) padding
)