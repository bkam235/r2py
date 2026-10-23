# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: as_date.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 12

suppressPackageStartupMessages(library(clock))
x <- date_time_parse("2019-01-01 23:02:03", "America/New_York")

# R's `as.Date.POSIXct()` method defaults to changing the printed time
# to UTC before converting, which can result in odd conversions like this:
as.Date(x)

# `as_date()` will never change the printed time before converting
as_date(x)

# Can also convert from other clock types
as_date(year_month_day(2019, 2, 5))