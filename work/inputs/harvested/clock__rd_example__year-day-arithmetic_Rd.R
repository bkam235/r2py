# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-day-arithmetic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 24

suppressPackageStartupMessages(library(clock))
x <- year_day(2019, 10)

add_years(x, 1:5)

# A valid day in a leap year
y <- year_day(2020, 366)
y

# Adding 1 year to `y` generates an invalid date
y_plus <- add_years(y, 1)
y_plus

# Invalid dates are fine, as long as they are eventually resolved
# by either manually resolving, or by calling `invalid_resolve()`

# Resolve by returning the previous / next valid moment in time
invalid_resolve(y_plus, invalid = "previous")
invalid_resolve(y_plus, invalid = "next")

# Manually resolve by setting to the last day of the year
invalid <- invalid_detect(y_plus)
y_plus[invalid] <- set_day(y_plus[invalid], "last")
y_plus