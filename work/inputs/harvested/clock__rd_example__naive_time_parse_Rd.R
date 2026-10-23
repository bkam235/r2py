# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: naive_time_parse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 37

suppressPackageStartupMessages(library(clock))
naive_time_parse("2020-01-01T05:06:07")

# Day precision
naive_time_parse("2020-01-01", precision = "day")

# Nanosecond precision, but using a day based format
naive_time_parse("2020-01-01", format = "%Y-%m-%d", precision = "nanosecond")

# Remember that the `%z` and `%Z` commands are ignored entirely!
naive_time_parse(
  "2020-01-01 -4000 America/New_York",
  format = "%Y-%m-%d %z %Z"
)

# ---------------------------------------------------------------------------
# Fractional seconds and POSIXct

# If you have a string with fractional seconds and want to convert it to
# a POSIXct, remember that clock treats POSIXct as a second precision type.
# Ideally, you'd use a clock type that can support fractional seconds, but
# if you really want to parse it into a POSIXct, the correct way to do so
# is to parse the full fractional time point with the correct `precision`,
# then round to seconds using whatever convention you require, and finally
# convert that to POSIXct.
x <- c("2020-01-01T00:00:00.123", "2020-01-01T00:00:00.555")

# First, parse string with full precision
x <- naive_time_parse(x, precision = "millisecond")
x

# Then round to second with a floor, ceiling, or round to nearest
time_point_floor(x, "second")
time_point_round(x, "second")

# Finally, convert to POSIXct
as_date_time(time_point_round(x, "second"), zone = "UTC")