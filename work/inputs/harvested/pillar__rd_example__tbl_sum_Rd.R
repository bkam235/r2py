# r2py crawler metadata
# package: pillar
# source_type: rd_example
# topic: tbl_sum.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\help
# lines: 7

suppressPackageStartupMessages(library(pillar))
tbl_sum(1:10)
tbl_sum(matrix(1:10))
tbl_sum(data.frame(a = 1))
tbl_sum(Sys.Date())
tbl_sum(Sys.time())
tbl_sum(mean)