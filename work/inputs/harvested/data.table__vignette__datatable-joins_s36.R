# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-joins_s36
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-joins.R
# lines: 4

suppressPackageStartupMessages(library(data.table))
x <- data.table(x_int = 2:4, lower = letters[1:3])
i <- data.table(i_int = c(2L, 4L, 5L), UPPER = LETTERS[1:3])
x[i, on = .(x_int >= i_int)]