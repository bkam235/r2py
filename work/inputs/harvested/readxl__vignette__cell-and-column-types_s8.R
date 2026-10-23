# r2py crawler metadata
# package: readxl
# source_type: vignette
# topic: cell-and-column-types_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readxl\doc\cell-and-column-types.R
# lines: 4

suppressPackageStartupMessages(library(readxl))
(nms <- names(read_excel(readxl_example("datasets.xlsx"), n_max = 0)))
(ct <- ifelse(grepl("^Petal", nms), "text", "guess"))
read_excel(readxl_example("datasets.xlsx"), col_types = ct)