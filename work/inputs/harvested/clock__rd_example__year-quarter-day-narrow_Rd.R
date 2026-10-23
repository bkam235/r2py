# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-quarter-day-narrow.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 7

suppressPackageStartupMessages(library(clock))
# Day precision
x <- year_quarter_day(2019, 1, 5)
x

# Narrow to quarter precision
calendar_narrow(x, "quarter")