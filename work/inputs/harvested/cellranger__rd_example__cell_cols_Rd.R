# r2py crawler metadata
# package: cellranger
# source_type: rd_example
# topic: cell_cols.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cellranger\help
# lines: 9

suppressPackageStartupMessages(library(cellranger))
cell_cols(c(NA, 3))
cell_cols(c(7, NA))
cell_cols(4:16)
cell_cols(c(3, NA, 10))

cell_cols("C:G")
cell_cols(c("B", NA))
cell_cols(LETTERS)