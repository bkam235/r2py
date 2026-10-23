# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_s48
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.R
# lines: 8

suppressPackageStartupMessages(library(tidyr))
multi <- tribble(
  ~id, ~choice1, ~choice2, ~choice3,
  1, "A", "B", "C",
  2, "C", "B",  NA,
  3, "D",  NA,  NA,
  4, "B", "D",  NA
)