# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: as-zoned-time-Date.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 20

suppressPackageStartupMessages(library(clock))
x <- as.Date("2019-01-01")

# The resulting zoned-times have the same printed time, but are in
# different time zones
as_zoned_time(x, "UTC")
as_zoned_time(x, "America/New_York")

# Converting Date -> zoned-time is the same as naive-time -> zoned-time
x <- as_naive_time(year_month_day(2019, 1, 1))
as_zoned_time(x, "America/New_York")

# In Asia/Beirut, there was a DST gap from
# 2021-03-27 23:59:59 -> 2021-03-28 01:00:00,
# skipping the 0th hour entirely. This means there is no midnight value.
x <- as.Date("2021-03-28")
try(as_zoned_time(x, "Asia/Beirut"))

# To resolve this, set a `nonexistent` time resolution strategy
as_zoned_time(x, "Asia/Beirut", nonexistent = "roll-forward")