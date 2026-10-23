# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: seq.clock_year_day.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 11

suppressPackageStartupMessages(library(clock))
# Yearly sequence
x <- seq(year_day(2020), year_day(2040), by = 2)
x

# Which we can then set the day of to get a sequence of end-of-year values
set_day(x, "last")

# Daily sequences are not allowed. Use a naive-time for this instead.
try(seq(year_day(2019, 1), by = 2, length.out = 2))
as_year_day(seq(as_naive_time(year_day(2019, 1)), by = 2, length.out = 2))