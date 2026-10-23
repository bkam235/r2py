# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-week-day-widen.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 12

suppressPackageStartupMessages(library(clock))
# Week precision
x <- year_week_day(2019, 1, start = clock_weekdays$monday)
x

# Widen to day precision
# In this calendar, the first day of the week is a Monday
calendar_widen(x, "day")

# Or second precision
sec <- calendar_widen(x, "second")
sec