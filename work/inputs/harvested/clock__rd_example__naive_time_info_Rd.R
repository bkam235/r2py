# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: naive_time_info.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 64

suppressPackageStartupMessages(library(clock))
library(vctrs)

x <- year_month_day(1970, 04, 26, 02, 30, 00)
x <- as_naive_time(x)

# Maps uniquely to a time in London
naive_time_info(x, "Europe/London")

# This naive-time never existed in New York!
# A DST gap jumped the time from 01:59:59 -> 03:00:00,
# skipping the 2 o'clock hour
zone <- "America/New_York"
info <- naive_time_info(x, zone)
info

# You can recreate various `nonexistent` strategies with this info
as_zoned_time(x, zone, nonexistent = "roll-forward")
as_zoned_time(info$first$end, zone)

as_zoned_time(x, zone, nonexistent = "roll-backward")
as_zoned_time(info$first$end - 1, zone)

as_zoned_time(x, zone, nonexistent = "shift-forward")
as_zoned_time(as_sys_time(x) - info$first$offset, zone)

as_zoned_time(x, zone, nonexistent = "shift-backward")
as_zoned_time(as_sys_time(x) - info$second$offset, zone)

# ---------------------------------------------------------------------------
# Normalizing to UTC

# Imagine you had the following printed times, and knowledge that they
# are to be interpreted as in the corresponding time zones
df <- data_frame(
  x = c("2020-01-05 02:30:00", "2020-06-03 12:20:05"),
  zone = c("America/Los_Angeles", "Europe/London")
)

# The times are assumed to be naive-times, i.e. if you lived in the `zone`
# at the moment the time was recorded, then you would have seen that time
# printed on the clock. Currently, these are strings. To convert them to
# a time based type, you'll have to acknowledge that R only lets you have
# 1 time zone in a vector of date-times at a time. So you'll need to
# normalize these naive-times. The easiest thing to normalize them to
# is UTC.
df$naive <- naive_time_parse(df$x)

# Get info about the naive times using a vector of zones
info <- naive_time_info(df$naive, df$zone)
info

# We'll assume that some system generated these naive-times with no
# chance of them ever being nonexistent or ambiguous. So now all we have
# to do is use the offset to convert the naive-time to a sys-time. The
# relationship used is:
# offset = naive_time - sys_time
df$sys <- as_sys_time(df$naive) - info$first$offset
df

# At this point, both times are in UTC. From here, you can convert them
# both to either America/Los_Angeles or Europe/London as required.
as_zoned_time(df$sys, "America/Los_Angeles")
as_zoned_time(df$sys, "Europe/London")