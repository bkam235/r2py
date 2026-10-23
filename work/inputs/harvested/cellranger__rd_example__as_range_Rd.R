# r2py crawler metadata
# package: cellranger
# source_type: rd_example
# topic: as.range.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\cellranger\help
# lines: 8

suppressPackageStartupMessages(library(cellranger))
rgCL <- cell_limits(ul = c(1, 2), lr = c(7, 6))
as.range(rgCL)
as.range(rgCL, fo = "A1")

rgCL_ws <- cell_limits(ul = c(1, 2), lr = c(7, 6), sheet = "A Sheet")
as.range(rgCL_ws)
as.range(rgCL_ws, fo = "A1")