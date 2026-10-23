# r2py crawler metadata
# package: reshape2
# source_type: rd_example
# topic: colsplit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\reshape2\help
# lines: 5

suppressPackageStartupMessages(library(reshape2))
x <- c("a_1", "a_2", "b_2", "c_3")
vars <- colsplit(x, "_", c("trt", "time"))
vars
str(vars)