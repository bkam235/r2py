# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: calendar_widen.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 10

suppressPackageStartupMessages(library(clock))
# Month precision
x <- year_month_day(2019, 1)
x

# Widen to day precision
calendar_widen(x, "day")

# Or second precision
calendar_widen(x, "second")