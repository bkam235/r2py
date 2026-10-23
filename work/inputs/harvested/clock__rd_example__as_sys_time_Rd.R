# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: as_sys_time.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 21

suppressPackageStartupMessages(library(clock))
x <- as.Date("2019-01-01")

# Dates are assumed to be naive, so the printed time is the same whether
# we convert it to sys-time or naive-time
as_sys_time(x)
as_naive_time(x)

y <- as.POSIXct("2019-01-01 01:00:00", tz = "America/New_York")

# The sys time displays the equivalent time in UTC (5 hours ahead of
# America/New_York at this point in the year)
as_sys_time(y)

ym <- year_month_day(2019, 02)

# A minimum of day precision is required
try(as_sys_time(ym))

ymd <- set_day(ym, 10)
as_sys_time(ymd)