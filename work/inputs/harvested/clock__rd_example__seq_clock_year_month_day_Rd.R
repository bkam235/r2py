# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: seq.clock_year_month_day.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 11

suppressPackageStartupMessages(library(clock))
# Monthly sequence
x <- seq(year_month_day(2019, 1), year_month_day(2020, 12), by = 1)
x

# Which we can then set the day of to get a sequence of end-of-month values
set_day(x, "last")

# Daily sequences are not allowed. Use a naive-time for this instead.
try(seq(year_month_day(2019, 1, 1), by = 2, length.out = 2))
seq(as_naive_time(year_month_day(2019, 1, 1)), by = 2, length.out = 2)