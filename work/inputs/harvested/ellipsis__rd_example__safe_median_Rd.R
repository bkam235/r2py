# r2py crawler metadata
# package: ellipsis
# source_type: rd_example
# topic: safe_median.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ellipsis\help
# lines: 10

suppressPackageStartupMessages(library(ellipsis))
x <- c(1:10, NA)
safe_median(x, na.rm = TRUE)
median(x, na.rm = TRUE)

try(median(x, na.mr = TRUE))
try(safe_median(x, na.mr = TRUE))

try(median(1, 2, 3))
try(safe_median(1, 2, 3))