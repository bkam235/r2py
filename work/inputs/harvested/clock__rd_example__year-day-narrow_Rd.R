# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-day-narrow.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 23

suppressPackageStartupMessages(library(clock))
# Hour precision
x <- year_day(2019, 3, 4)
x

# Narrowed to day precision
calendar_narrow(x, "day")

# Or year precision
calendar_narrow(x, "year")

# Subsecond precision can be narrowed to second precision
milli <- calendar_widen(x, "millisecond")
micro <- calendar_widen(x, "microsecond")
milli
micro

calendar_narrow(milli, "second")
calendar_narrow(micro, "second")

# But once you have "locked in" a subsecond precision, it can't be
# narrowed to another subsecond precision
try(calendar_narrow(micro, "millisecond"))