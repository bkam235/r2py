# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: iso-year-week-day-count-between.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 5

suppressPackageStartupMessages(library(clock))
# Compute the number of whole ISO years between two dates
x <- iso_year_week_day(2001, 1, 2)
y <- iso_year_week_day(2021, 1, c(1, 3))
calendar_count_between(x, y, "year")