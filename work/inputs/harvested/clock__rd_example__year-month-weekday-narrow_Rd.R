# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-month-weekday-narrow.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 7

suppressPackageStartupMessages(library(clock))
# Day precision
x <- year_month_weekday(2019, 1, 1, 2)
x

# Narrowed to month precision
calendar_narrow(x, "month")