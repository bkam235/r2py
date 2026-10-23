# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: seq.clock_iso_year_week_day.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 8

suppressPackageStartupMessages(library(clock))
# Yearly sequence
x <- seq(iso_year_week_day(2020), iso_year_week_day(2026), by = 2)
x

# Which we can then set the week of.
# Some years have 53 ISO weeks, some have 52.
set_week(x, "last")