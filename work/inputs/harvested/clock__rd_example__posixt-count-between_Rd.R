# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: posixt-count-between.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 64

suppressPackageStartupMessages(library(clock))
start <- date_time_parse("2000-05-05 02:00:00", zone = "America/New_York")
end <- date_time_parse(
  c("2020-05-05 01:00:00", "2020-05-05 03:00:00"),
  zone = "America/New_York"
)

# Age in years
date_count_between(start, end, "year")

# Number of "whole" months between these dates. i.e.
# `2000-05-05 02:00:00 -> 2020-04-05 02:00:00` is 239 months
# `2000-05-05 02:00:00 -> 2020-05-05 02:00:00` is 240 months
# Since `2020-05-05 01:00:00` occurs before the 2nd hour,
# it gets a count of 239
date_count_between(start, end, "month")

# Number of seconds between
date_count_between(start, end, "second")

# ---------------------------------------------------------------------------
# Naive-time VS Sys-time interpretation

# The difference between whether `start` and `end` are converted to a
# naive-time vs a sys-time comes into play when dealing with daylight
# savings.

# Here are two times around a 1 hour DST gap where clocks jumped from
# 01:59:59 -> 03:00:00
x <- date_time_build(1970, 4, 26, 1, 50, 00, zone = "America/New_York")
y <- date_time_build(1970, 4, 26, 3, 00, 00, zone = "America/New_York")

# When treated like sys-times, these are considered to be 10 minutes apart,
# which is the amount of time that would have elapsed if you were watching
# a clock as it changed between these two times.
date_count_between(x, y, "minute")

# Lets add a 3rd date that is ~1 day ahead of these
z <- date_time_build(1970, 4, 27, 1, 55, 00, zone = "America/New_York")

# When treated like naive-times, `z` is considered to be at least 1 day ahead
# of `x`, because `01:55:00` is after `01:50:00`. This is probably what you
# expected.
date_count_between(x, z, "day")

# If these were interpreted like sys-times, then `z` would not be considered
# to be 1 day ahead. That would look something like this:
date_count_between(x, z, "second")
trunc(date_count_between(x, z, "second") / 86400)

# This is because there have only been 83,100 elapsed seconds since `x`,
# which isn't a full day's worth (86,400 seconds). But we'd generally
# consider `z` to be 1 day ahead of `x` (and ignore the DST gap), so that is
# how it is implemented.

# You can override this by converting directly to sys-time, then using
# `time_point_count_between()`
x_st <- as_sys_time(x)
x_st

z_st <- as_sys_time(z)
z_st

time_point_count_between(x_st, z_st, "day")