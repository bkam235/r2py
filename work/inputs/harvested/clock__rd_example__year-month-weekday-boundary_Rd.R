# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-month-weekday-boundary.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 7

suppressPackageStartupMessages(library(clock))
# Month precision
x <- year_month_weekday(2019, 1:5)
x

# Compute the last month of the year
calendar_end(x, "year")