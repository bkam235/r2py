# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: zoned-parsing.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 59

suppressPackageStartupMessages(library(clock))
library(magrittr)

zoned_time_parse_complete("2019-01-01T01:02:03-05:00[America/New_York]")

zoned_time_parse_complete(
  "January 21, 2019 -0500 America/New_York",
  format = "%B %d, %Y %z %Z"
)

# Nanosecond precision
x <- "2019/12/31 01:05:05.123456700-05:00[America/New_York]"
zoned_time_parse_complete(
  x,
  format = "%Y/%m/%d %H:%M:%S%Ez[%Z]",
  precision = "nanosecond"
)

# The `%z` offset must correspond to the true offset that would be used
# if the input was parsed as a naive-time and then converted to a zoned-time
# with `as_zoned_time()`. For example, the time that was parsed above used an
# offset of `-05:00`. We can confirm that this is correct with:
year_month_day(2019, 1, 1, 1, 2, 3) %>%
  as_naive_time() %>%
  as_zoned_time("America/New_York")

# So the following would not parse correctly
zoned_time_parse_complete("2019-01-01T01:02:03-04:00[America/New_York]")

# `%z` is useful for breaking ties in otherwise ambiguous times. For example,
# these two times are on either side of a daylight saving time fallback.
# Without the `%z` offset, you wouldn't be able to tell them apart!
x <- c(
  "1970-10-25T01:30:00-04:00[America/New_York]",
  "1970-10-25T01:30:00-05:00[America/New_York]"
)

zoned_time_parse_complete(x)

# If you have date-time strings with time zone abbreviations,
# `zoned_time_parse_abbrev()` should be able to help. The `zone` must be
# provided, because multiple countries may use the same time zone
# abbreviation. For example:
x <- "1970-01-01 02:30:30 IST"

# IST = India Standard Time
zoned_time_parse_abbrev(x, "Asia/Kolkata")

# IST = Israel Standard Time
zoned_time_parse_abbrev(x, "Asia/Jerusalem")

# The time zone abbreviation is mainly useful for resolving ambiguity
# around daylight saving time fallbacks. Without the abbreviation, these
# date-times would be ambiguous.
x <- c(
  "1970-10-25 01:30:00 EDT",
  "1970-10-25 01:30:00 EST"
)
zoned_time_parse_abbrev(x, "America/New_York")