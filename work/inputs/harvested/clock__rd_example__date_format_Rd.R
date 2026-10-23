# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date_format.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 5

suppressPackageStartupMessages(library(clock))
# See method specific documentation for more examples

x <- as.Date("2019-01-01")
date_format(x, format = "year: %Y, month: %m, day: %d")