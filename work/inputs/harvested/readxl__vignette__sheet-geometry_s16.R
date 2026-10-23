# r2py crawler metadata
# package: readxl
# source_type: vignette
# topic: sheet-geometry_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readxl\doc\sheet-geometry.R
# lines: 6

suppressPackageStartupMessages(library(readxl))
read_excel(
  readxl_example("geometry.xlsx"),
  col_names = FALSE,
  range = cell_limits(c(5, 3), c(NA, NA))
)