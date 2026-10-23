# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-month-weekday-arithmetic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 9

suppressPackageStartupMessages(library(clock))
# 2nd Friday in January, 2019
x <- year_month_weekday(2019, 1, clock_weekdays$friday, 2)
x

add_months(x, 1:5)

# These don't necessarily correspond to the same day of the month
as_year_month_day(add_months(x, 1:5))