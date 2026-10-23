# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date_leap_year.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 8

suppressPackageStartupMessages(library(clock))
x <- as.Date("2019-01-01")
x <- add_years(x, 0:5)
date_leap_year(x)

y <- as.POSIXct("2019-01-01", "America/New_York")
y <- add_years(y, 0:5)
date_leap_year(y)