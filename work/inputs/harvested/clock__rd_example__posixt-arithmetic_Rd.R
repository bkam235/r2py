# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: posixt-arithmetic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 22

suppressPackageStartupMessages(library(clock))
x <- as.POSIXct("2019-01-01", tz = "America/New_York")

add_years(x, 1:5)

y <- as.POSIXct("2019-01-31 00:30:00", tz = "America/New_York")

# Adding 1 month to `y` generates an invalid date. Unlike year-month-day
# types, R's native date-time types cannot handle invalid dates, so you must
# resolve them immediately. If you don't you get an error:
try(add_months(y, 1:2))
add_months(as_year_month_day(y), 1:2)

# Resolve invalid dates by specifying an invalid date resolution strategy
# with the `invalid` argument. Using `"previous"` here sets the date-time to
# the previous valid moment in time - i.e. the end of the month. The
# time is set to the last moment in the day to retain the relative ordering
# within your input. If you are okay with potentially losing this, and
# want to retain your time of day, you can use `"previous-day"` to set the
# date-time to the previous valid day, while keeping the time of day.
add_months(y, 1:2, invalid = "previous")
add_months(y, 1:2, invalid = "previous-day")