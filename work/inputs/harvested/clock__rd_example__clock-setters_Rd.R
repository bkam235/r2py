# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: clock-setters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 8

suppressPackageStartupMessages(library(clock))
x <- year_month_day(2019, 1:3)

# Set the day
set_day(x, 12:14)

# Set to the "last" day of the month
set_day(x, "last")