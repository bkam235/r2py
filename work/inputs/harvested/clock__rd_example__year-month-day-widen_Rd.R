# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-month-day-widen.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 21

suppressPackageStartupMessages(library(clock))
# Month precision
x <- year_month_day(2019, 1)
x

# Widen to day precision
calendar_widen(x, "day")

# Or second precision
sec <- calendar_widen(x, "second")
sec

# Second precision can be widened to subsecond precision
milli <- calendar_widen(sec, "millisecond")
micro <- calendar_widen(sec, "microsecond")
milli
micro

# But once you have "locked in" a subsecond precision, it can't
# be widened again
try(calendar_widen(milli, "microsecond"))