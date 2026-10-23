# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: seq.clock_year_quarter_day.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 7

suppressPackageStartupMessages(library(clock))
# Quarterly sequence
x <- seq(year_quarter_day(2020, 1), year_quarter_day(2026, 3), by = 2)
x

# Which we can then set the day of the quarter of
set_day(x, "last")