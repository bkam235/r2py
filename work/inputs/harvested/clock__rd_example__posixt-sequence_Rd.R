# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: posixt-sequence.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 78

suppressPackageStartupMessages(library(clock))
zone <- "America/New_York"

from <- date_time_build(2019, 1, zone = zone)
to <- date_time_build(2019, 1, second = 50, zone = zone)

# Defaults to second precision sequence
date_seq(from, to = to, by = 7)

to <- date_time_build(2019, 1, 5, zone = zone)

# Use durations to change to alternative precisions
date_seq(from, to = to, by = duration_days(1))
date_seq(from, to = to, by = duration_hours(10))
date_seq(from, by = duration_minutes(-2), total_size = 3)

# Note that components of `to` more precise than the precision of `by`
# must match `from` exactly. For example, this is not well defined:
from <- date_time_build(2019, 1, 1, 0, 1, 30, zone = zone)
to <- date_time_build(2019, 1, 1, 5, 2, 20, zone = zone)
try(date_seq(from, to = to, by = duration_hours(1)))

# The minute and second components of `to` must match `from`
to <- date_time_build(2019, 1, 1, 5, 1, 30, zone = zone)
date_seq(from, to = to, by = duration_hours(1))

# ---------------------------------------------------------------------------

# Invalid dates must be resolved with the `invalid` argument
from <- date_time_build(2019, 1, 31, zone = zone)
to <- date_time_build(2019, 12, 31, zone = zone)

try(date_seq(from, to = to, by = duration_months(1)))
date_seq(from, to = to, by = duration_months(1), invalid = "previous-day")

# Compare this to the base R result, which is often a source of confusion
seq(from, to = to, by = "1 month")

# This is equivalent to the overflow invalid resolution strategy
date_seq(from, to = to, by = duration_months(1), invalid = "overflow")

# ---------------------------------------------------------------------------

# This date-time is 2 days before a daylight saving time gap that occurred
# on 2021-03-14 between 01:59:59 -> 03:00:00
from <- as.POSIXct("2021-03-12 02:30:00", "America/New_York")

# So creating a daily sequence lands us in that daylight saving time gap,
# creating a nonexistent time
try(date_seq(from, by = duration_days(1), total_size = 5))

# Resolve the nonexistent time with `nonexistent`. Note that this importantly
# allows times after the gap to retain the `02:30:00` time.
date_seq(from, by = duration_days(1), total_size = 5, nonexistent = "roll-forward")

# Compare this to the base R behavior, where the hour is adjusted from 2->3
# as you cross the daylight saving time gap, and is never restored. This is
# equivalent to always using sys-time (rather than naive-time, like clock
# uses for daily sequences).
seq(from, by = "1 day", length.out = 5)

# You can replicate this behavior by generating a second precision sequence
# of 86,400 seconds. Seconds always add in sys-time.
date_seq(from, by = duration_seconds(86400), total_size = 5)

# ---------------------------------------------------------------------------

# Usage of `to` and `total_size` must generate a non-fractional sequence
# between `from` and `to`
from <- date_time_build(2019, 1, 1, 0, 0, 0, zone = "America/New_York")
to <- date_time_build(2019, 1, 1, 0, 0, 3, zone = "America/New_York")

# These are fine
date_seq(from, to = to, total_size = 2)
date_seq(from, to = to, total_size = 4)

# But this is not!
try(date_seq(from, to = to, total_size = 3))