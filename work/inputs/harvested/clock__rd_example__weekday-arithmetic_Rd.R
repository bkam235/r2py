# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: weekday-arithmetic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 6

suppressPackageStartupMessages(library(clock))
saturday <- weekday(clock_weekdays$saturday)
saturday

add_days(saturday, 1)
add_days(saturday, 2)