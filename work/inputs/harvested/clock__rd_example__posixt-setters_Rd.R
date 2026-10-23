# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: posixt-setters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 25

suppressPackageStartupMessages(library(clock))
x <- as.POSIXct("2019-02-01", tz = "America/New_York")

# Set the day
set_day(x, 12:14)

# Set to the "last" day of the month
set_day(x, "last")

# You cannot set a date-time to an invalid date like you can with
# a year-month-day. Instead, the default strategy is to error.
try(set_day(x, 31))
set_day(as_year_month_day(x), 31)

# You can resolve these issues while setting the day by specifying
# an invalid date resolution strategy with `invalid`
set_day(x, 31, invalid = "previous")

y <- as.POSIXct("2020-03-08 01:30:00", tz = "America/New_York")

# Nonexistent and ambiguous times must be resolved immediately when
# working with R's native date-time types. An error is thrown by default.
try(set_hour(y, 2))
set_hour(y, 2, nonexistent = "roll-forward")
set_hour(y, 2, nonexistent = "roll-backward")