# r2py crawler metadata
# package: cellranger
# source_type: rd_example
# topic: cell_rows.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cellranger\help
# lines: 7

suppressPackageStartupMessages(library(cellranger))
cell_rows(c(NA, 3))
cell_rows(c(7, NA))
cell_rows(4:16)
cell_rows(c(3, NA, 10))

dim(cell_rows(1:5))