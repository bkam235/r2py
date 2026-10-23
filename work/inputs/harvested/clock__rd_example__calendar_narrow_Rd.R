# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: calendar_narrow.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 10

suppressPackageStartupMessages(library(clock))
# Hour precision
x <- year_month_day(2019, 1, 3, 4)
x

# Narrowed to day precision
calendar_narrow(x, "day")

# Or month precision
calendar_narrow(x, "month")