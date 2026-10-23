# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date-and-date-time-shifting.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 12

suppressPackageStartupMessages(library(clock))
# See the type specific documentation for more examples

x <- as.Date("2019-01-01") + 0:1

# A Tuesday and Wednesday
as_weekday(x)

monday <- weekday(clock_weekdays$monday)

# Shift to the next Monday
date_shift(x, monday)