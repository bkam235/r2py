# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: sys-parsing.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 40

suppressPackageStartupMessages(library(clock))
sys_time_parse("2020-01-01T05:06:07")

# Day precision
sys_time_parse("2020-01-01", precision = "day")

# Nanosecond precision, but using a day based format
sys_time_parse("2020-01-01", format = "%Y-%m-%d", precision = "nanosecond")

# Multiple format strings are allowed for heterogeneous times
sys_time_parse(
  c("2019-01-01", "2019/1/1"),
  format = c("%Y/%m/%d", "%Y-%m-%d"),
  precision = "day"
)

# The `%z` command shifts the date-time by subtracting the UTC offset so
# that the returned sys-time can be interpreted as UTC
sys_time_parse(
  "2020-01-01 02:00:00 -0400",
  format = "%Y-%m-%d %H:%M:%S %z"
)

# Remember that the `%Z` command is ignored entirely!
sys_time_parse("2020-01-01 America/New_York", format = "%Y-%m-%d %Z")

# ---------------------------------------------------------------------------
# RFC 3339

# Typical UTC format
x <- "2019-01-01T00:01:02Z"
sys_time_parse_RFC_3339(x)

# With a UTC offset containing a `:`
x <- "2019-01-01T00:01:02+02:30"
sys_time_parse_RFC_3339(x, offset = "%Ez")

# With a space between the date and time and no `:` in the offset
x <- "2019-01-01 00:01:02+0230"
sys_time_parse_RFC_3339(x, separator = " ", offset = "%z")