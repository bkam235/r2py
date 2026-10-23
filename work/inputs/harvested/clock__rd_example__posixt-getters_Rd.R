# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: posixt-getters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 8

suppressPackageStartupMessages(library(clock))
x <- as.POSIXct("2019-01-01", tz = "America/New_York")

x <- add_days(x, 0:5)
x <- set_second(x, 10:15)

get_day(x)
get_second(x)