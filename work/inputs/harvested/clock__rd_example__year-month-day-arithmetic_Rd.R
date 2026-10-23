# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-month-day-arithmetic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 22

suppressPackageStartupMessages(library(clock))
x <- year_month_day(2019, 1, 1)

add_years(x, 1:5)

y <- year_month_day(2019, 1, 31)

# Adding 1 month to `y` generates an invalid date
y_plus <- add_months(y, 1:2)
y_plus

# Invalid dates are fine, as long as they are eventually resolved
# by either manually resolving, or by calling `invalid_resolve()`

# Resolve by returning the previous / next valid moment in time
invalid_resolve(y_plus, invalid = "previous")
invalid_resolve(y_plus, invalid = "next")

# Manually resolve by setting to the last day of the month
invalid <- invalid_detect(y_plus)
y_plus[invalid] <- set_day(y_plus[invalid], "last")
y_plus