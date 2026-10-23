# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-week-day-narrow.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 7

suppressPackageStartupMessages(library(clock))
# Day precision
x <- year_week_day(2019, 1, 5)
x

# Narrowed to week precision
calendar_narrow(x, "week")