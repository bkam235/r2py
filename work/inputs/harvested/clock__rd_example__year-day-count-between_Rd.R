# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-day-count-between.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 9

suppressPackageStartupMessages(library(clock))
# Compute an individual's age in years
x <- year_day(2001, 100)
y <- year_day(2021, c(99, 101))

calendar_count_between(x, y, "year")

# Or in a whole number multiple of years
calendar_count_between(x, y, "year", n = 3)