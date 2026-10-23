# r2py crawler metadata
# package: readxl
# source_type: vignette
# topic: cell-and-column-types_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readxl\doc\cell-and-column-types.R
# lines: 5

suppressPackageStartupMessages(library(readxl))
(clippy <- 
   read_excel(readxl_example("clippy.xlsx"), col_types = c("text", "list")))
tibble::deframe(clippy)
sapply(clippy$value, class)