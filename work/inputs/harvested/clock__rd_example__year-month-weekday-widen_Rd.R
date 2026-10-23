# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-month-weekday-widen.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 13

suppressPackageStartupMessages(library(clock))
# Month precision
x <- year_month_weekday(2019, 1)
x

# Widen to day precision
# Note that this sets both the day and index to 1,
# i.e. the first Sunday of the month.
calendar_widen(x, "day")

# Or second precision
sec <- calendar_widen(x, "second")
sec