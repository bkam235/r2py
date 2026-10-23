# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-week-day-boundary.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 10

suppressPackageStartupMessages(library(clock))
x <- year_week_day(2019:2020, 5, 6, 10)
x

# Compute the last moment of the last week of the year
calendar_end(x, "year")

# Compare that to just setting the week to `"last"`,
# which doesn't affect the other components
set_week(x, "last")