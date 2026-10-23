# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: as_date_time.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 31

suppressPackageStartupMessages(library(clock))
x <- as.Date("2019-01-01")

# `as.POSIXct()` will always treat Date as UTC, but will show the result
# of the conversion in your system time zone, which can be somewhat confusing
if (rlang::is_installed("withr")) {
  withr::with_timezone("UTC", print(as.POSIXct(x)))
  withr::with_timezone("Europe/Paris", print(as.POSIXct(x)))
  withr::with_timezone("America/New_York", print(as.POSIXct(x)))
}

# `as_date_time()` will treat Date as naive, which means that the original
# printed date will attempt to be kept wherever possible, no matter the
# time zone. The time will be set to midnight.
as_date_time(x, "UTC")
as_date_time(x, "Europe/Paris")
as_date_time(x, "America/New_York")

# In some rare cases, this is not possible.
# For example, in Asia/Beirut, there was a DST gap from
# 2021-03-27 23:59:59 -> 2021-03-28 01:00:00,
# skipping the 0th hour entirely.
x <- as.Date("2021-03-28")
try(as_date_time(x, "Asia/Beirut"))

# To resolve this, set a `nonexistent` time resolution strategy
as_date_time(x, "Asia/Beirut", nonexistent = "roll-forward")


# You can also convert to date-time from other clock types
as_date_time(year_month_day(2019, 2, 3, 03), "America/New_York")