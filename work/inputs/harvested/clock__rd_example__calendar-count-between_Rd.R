# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: calendar-count-between.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 7

suppressPackageStartupMessages(library(clock))
# Number of whole years between these dates
x <- year_month_day(2000, 01, 05)
y <- year_month_day(2005, 01, 04:06)

# Note that `2000-01-05 -> 2005-01-04` is only 4 full years
calendar_count_between(x, y, "year")