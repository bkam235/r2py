# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date-time-zone.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 39

suppressPackageStartupMessages(library(clock))
library(magrittr)

# Cannot set or get the zone of Date.
# clock assumes that Dates are naive types, like naive-time.
x <- date_parse("2019-01-01")
try(date_time_zone(x))
try(date_time_set_zone(x, "America/New_York"))

x <- date_time_parse("2019-01-02 01:30:00", "America/New_York")
x

date_time_zone(x)

# If it is 1:30am in New York, what time is it in Los Angeles?
# Same underlying duration, new printed time
date_time_set_zone(x, "America/Los_Angeles")

# If you want to retain the printed time, but change the underlying duration,
# convert to a naive-time to drop the time zone, then convert back to a
# date-time. Be aware that this requires that you handle daylight saving time
# irregularities with the `nonexistent` and `ambiguous` arguments to
# `as_date_time()`!
x %>%
  as_naive_time() %>%
  as_date_time("America/Los_Angeles")

y <- date_time_parse("2021-03-28 03:30:00", "America/New_York")
y

y_nt <- as_naive_time(y)
y_nt

# Helsinki had a daylight saving time gap where they jumped from
# 02:59:59 -> 04:00:00
try(as_date_time(y_nt, "Europe/Helsinki"))

as_date_time(y_nt, "Europe/Helsinki", nonexistent = "roll-forward")
as_date_time(y_nt, "Europe/Helsinki", nonexistent = "roll-backward")