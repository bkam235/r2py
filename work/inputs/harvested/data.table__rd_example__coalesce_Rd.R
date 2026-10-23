# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: coalesce.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 10

suppressPackageStartupMessages(library(data.table))
x = c(11L, NA, 13L, NA, 15L, NA)
y = c(NA, 12L, 5L, NA, NA, NA)
z = c(11L, NA, 1L, 14L, NA, NA)
fcoalesce(x, y, z)
fcoalesce(list(x,y,z))   # same
fcoalesce(x, list(y,z))  # same
x_num = c(NaN, NA_real_, 3.0)
fcoalesce(x_num, 1)           # default: NaN treated as missing -> c(1, 1, 3)
fcoalesce(x_num, 1, nan=NaN)  # preserve NaN -> c(NaN, 1, 3)