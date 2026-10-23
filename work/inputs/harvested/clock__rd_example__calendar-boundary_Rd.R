# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: calendar-boundary.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 10

suppressPackageStartupMessages(library(clock))
# Hour precision
x <- year_month_day(2019, 2:4, 5, 6)
x

# Compute the start of the month
calendar_start(x, "month")

# Or the end of the month, notice that the hour value is adjusted as well
calendar_end(x, "month")