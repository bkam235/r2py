# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: minor_breaks_width.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 6

suppressPackageStartupMessages(library(scales))
demo_log10(c(1, 1e6))
if (FALSE) {
  # Requires https://github.com/tidyverse/ggplot2/pull/3591
  demo_log10(c(1, 1e6), minor_breaks = minor_breaks_n(10))
}