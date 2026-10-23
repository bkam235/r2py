# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: time-point-arithmetic.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 44

suppressPackageStartupMessages(library(clock))
library(magrittr)

# Say you started with this zoned time, and you want to add 1 day to it
x <- as_naive_time(year_month_day(1970, 04, 25, 02, 30, 00))
x <- as_zoned_time(x, "America/New_York")
x

# Note that there was a daylight saving time gap on 1970-04-26 where
# we jumped from 01:59:59 -> 03:00:00.

# You can choose to add 1 day in "system time", by first converting to
# sys-time (the equivalent UTC time), adding the day, then converting back to
# zoned time. If you sat still for exactly 86,400 seconds, this is the
# time that you would see after daylight saving time adjusted the clock
# (note that the hour field is shifted forward by the size of the gap)
as_sys_time(x)

x %>%
  as_sys_time() %>%
  add_days(1) %>%
  as_zoned_time(zoned_time_zone(x))

# Alternatively, you can add 1 day in "naive time". Naive time represents
# a clock time with a yet-to-be-specified time zone. It tries to maintain
# smaller units where possible, so adding 1 day would attempt to return
# "1970-04-26T02:30:00" in the America/New_York time zone, but...
as_naive_time(x)

try({
x %>%
  as_naive_time() %>%
  add_days(1) %>%
  as_zoned_time(zoned_time_zone(x))
})

# ...this time doesn't exist in that time zone! It is "nonexistent".
# You can resolve nonexistent times by setting the `nonexistent` argument
# when converting to zoned time. Let's roll forward to the next available
# moment in time.
x %>%
  as_naive_time() %>%
  add_days(1) %>%
  as_zoned_time(zoned_time_zone(x), nonexistent = "roll-forward")