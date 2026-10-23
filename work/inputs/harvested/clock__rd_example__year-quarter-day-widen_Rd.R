# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-quarter-day-widen.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 11

suppressPackageStartupMessages(library(clock))
# Quarter precision
x <- year_quarter_day(2019, 1)
x

# Widen to day precision
calendar_widen(x, "day")

# Or second precision
sec <- calendar_widen(x, "second")
sec