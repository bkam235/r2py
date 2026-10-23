# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-quarter-day-arithmetic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 16

suppressPackageStartupMessages(library(clock))
x <- year_quarter_day(2019, 1:3)
x

add_quarters(x, 2)

# Make the fiscal year start in March
y <- year_quarter_day(2019, 1:2, 1, start = 3)
y

add_quarters(y, 1)

# What year-month-day does this correspond to?
# Note that the fiscal year doesn't necessarily align with the Gregorian
# year!
as_year_month_day(add_quarters(y, 1))