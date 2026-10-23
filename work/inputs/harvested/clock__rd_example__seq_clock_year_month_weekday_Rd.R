# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: seq.clock_year_month_weekday.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 7

suppressPackageStartupMessages(library(clock))
# Monthly sequence
x <- seq(year_month_weekday(2019, 1), year_month_weekday(2020, 12), by = 1)
x

# Which we can then set the indexed weekday of
set_day(x, clock_weekdays$sunday, index = "last")