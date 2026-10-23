# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: Date-arithmetic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 17

suppressPackageStartupMessages(library(clock))
x <- as.Date("2019-01-01")

add_years(x, 1:5)

y <- as.Date("2019-01-31")

# Adding 1 month to `y` generates an invalid date. Unlike year-month-day
# types, R's native Date type cannot handle invalid dates, so you must
# resolve them immediately. If you don't you get an error:
try(add_months(y, 1:2))
add_months(as_year_month_day(y), 1:2)

# Resolve invalid dates by specifying an invalid date resolution strategy
# with the `invalid` argument. Using `"previous"` here sets the date to
# the previous valid date - i.e. the end of the month.
add_months(y, 1:2, invalid = "previous")