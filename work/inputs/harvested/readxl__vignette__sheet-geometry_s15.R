# r2py crawler metadata
# package: readxl
# source_type: vignette
# topic: sheet-geometry_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readxl\doc\sheet-geometry.R
# lines: 6

suppressPackageStartupMessages(library(readxl))
read_excel(
  readxl_example("geometry.xlsx"),
  col_names = paste("var", 1:4, sep = "_"),
  range = anchored("C5", c(3, 4))
)