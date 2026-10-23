# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: Date-setters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 17

suppressPackageStartupMessages(library(clock))
x <- as.Date("2019-02-01")

# Set the day
set_day(x, 12:14)

# Set to the "last" day of the month
set_day(x, "last")

# You cannot set a Date to an invalid day like you can with
# a year-month-day. Instead, the default strategy is to error.
try(set_day(x, 31))
set_day(as_year_month_day(x), 31)

# You can resolve these issues while setting the day by specifying
# an invalid date resolution strategy with `invalid`
set_day(x, 31, invalid = "previous")