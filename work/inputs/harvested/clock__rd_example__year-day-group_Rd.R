# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-day-group.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 7

suppressPackageStartupMessages(library(clock))
x <- seq(as_naive_time(year_month_day(2019, 1, 1)), by = 5, length.out = 20)
x <- as_year_day(x)
x

# Group by day of the current year
calendar_group(x, "day", n = 20)