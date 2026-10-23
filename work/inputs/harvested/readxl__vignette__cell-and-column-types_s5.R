# r2py crawler metadata
# package: readxl
# source_type: vignette
# topic: cell-and-column-types_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readxl\doc\cell-and-column-types.R
# lines: 6

suppressPackageStartupMessages(library(readxl))
read_excel(
  readxl_example("deaths.xlsx"),
  range = cell_rows(5:15),
  col_types = c("guess", "skip", "guess", "skip", "skip", "skip")
)