# r2py crawler metadata
# package: cellranger
# source_type: rd_example
# topic: ra_ref.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cellranger\help
# lines: 5

suppressPackageStartupMessages(library(cellranger))
ra_ref()
ra_ref(row_ref = 3, col_ref = 2)
ra_ref(row_ref = 10, row_abs = FALSE, col_ref = 3, col_abs = TRUE)
ra_ref(sheet = "a sheet")