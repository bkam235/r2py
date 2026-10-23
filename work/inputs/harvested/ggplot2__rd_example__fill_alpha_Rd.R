# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: fill_alpha.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 8

suppressPackageStartupMessages(library(ggplot2))
# Typical colour input
fill_alpha("red", 0.5)

if (utils::packageVersion("grid") > "4.2") {
  # Pattern input
  fill_alpha(list(grid::linearGradient()), 0.5)
}