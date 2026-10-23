# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-day-boundary.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 7

suppressPackageStartupMessages(library(clock))
# Day precision
x <- year_day(2019:2020, 5)
x

# Compute the last day of the year
calendar_end(x, "year")