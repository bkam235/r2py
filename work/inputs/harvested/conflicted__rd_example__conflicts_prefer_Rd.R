# r2py crawler metadata
# package: conflicted
# source_type: rd_example
# topic: conflicts_prefer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\conflicted\help
# lines: 11

suppressPackageStartupMessages(library(conflicted))
conflicts_prefer(
  dplyr::filter(),
  dplyr::lag(),
)

# or
conflicts_prefer(
  dplyr::filter,
  dplyr::lag,
)