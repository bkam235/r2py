# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: as-zoned-time-sys-time.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 14

suppressPackageStartupMessages(library(clock))
x <- as_sys_time(year_month_day(2019, 02, 01, 02, 30, 00))
x

# Since sys-time is interpreted as UTC, converting to a zoned-time with
# a zone of UTC retains the printed time
x_utc <- as_zoned_time(x, "UTC")
x_utc

# Converting to a different zone results in a different printed time,
# which corresponds to the exact same point in time, just in a different
# part of the work
x_ny <- as_zoned_time(x, "America/New_York")
x_ny