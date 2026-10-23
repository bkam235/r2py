# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: minor_breaks_log.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 11

suppressPackageStartupMessages(library(scales))
# Standard usage with log10 scale
demo_log10(c(1, 1e10), minor_breaks = minor_breaks_log())
# Increasing detail over many powers
demo_log10(c(1, 1e10), minor_breaks = minor_breaks_log(detail = 1))
# Adjusting until where to draw minor breaks
demo_continuous(
  c(-1000, 1000),
  transform = asinh_trans(),
  minor_breaks = minor_breaks_log(smallest = 1)
)