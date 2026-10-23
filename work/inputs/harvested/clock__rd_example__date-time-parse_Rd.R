# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date-time-parse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 78

suppressPackageStartupMessages(library(clock))
# Parse with a known `zone`, even though that information isn't in the string
date_time_parse("2020-01-01 05:06:07", "America/New_York")

# Same time as above, except this is a completely unambiguous parse that
# doesn't require a `zone` argument, because the zone name and offset are
# both present in the string
date_time_parse_complete("2020-01-01T05:06:07-05:00[America/New_York]")

# Only day components
date_time_parse("2020-01-01", "America/New_York", format = "%Y-%m-%d")

# `date_time_parse()` may have issues with ambiguous times due to daylight
# saving time fallbacks. For example, there were two 1'oclock hours here:
x <- date_time_parse("1970-10-25 00:59:59", "America/New_York")

# First (earliest) 1'oclock hour
add_seconds(x, 1)
# Second (latest) 1'oclock hour
add_seconds(x, 3601)

# If you try to parse this ambiguous time directly, you'll get an error:
ambiguous_time <- "1970-10-25 01:00:00"
try(date_time_parse(ambiguous_time, "America/New_York"))

# Resolve it by specifying whether you'd like to use the
# `earliest` or `latest` of the two possible times
date_time_parse(ambiguous_time, "America/New_York", ambiguous = "earliest")
date_time_parse(ambiguous_time, "America/New_York", ambiguous = "latest")

# `date_time_parse_complete()` doesn't have these issues, as it requires
# that the offset and zone name are both in the string, which resolves
# the ambiguity
complete_times <- c(
  "1970-10-25T01:00:00-04:00[America/New_York]",
  "1970-10-25T01:00:00-05:00[America/New_York]"
)
date_time_parse_complete(complete_times)

# `date_time_parse_abbrev()` also doesn't have these issues, since it
# uses the time zone abbreviation name to resolve the ambiguity
abbrev_times <- c(
  "1970-10-25 01:00:00 EDT",
  "1970-10-25 01:00:00 EST"
)
date_time_parse_abbrev(abbrev_times, "America/New_York")

# ---------------------------------------------------------------------------
# RFC 3339

# Typical UTC format
x <- "2019-01-01T00:01:02Z"
date_time_parse_RFC_3339(x)

# With a UTC offset containing a `:`
x <- "2019-01-01T00:01:02+02:30"
date_time_parse_RFC_3339(x, offset = "%Ez")

# With a space between the date and time and no `:` in the offset
x <- "2019-01-01 00:01:02+0230"
date_time_parse_RFC_3339(x, separator = " ", offset = "%z")

# ---------------------------------------------------------------------------
# Sub-second components

# If you have a string with sub-second components, but only require up to
# seconds, first parse them into a clock type that can handle sub-seconds to
# fully capture that information, then round using whatever convention is
# required for your use case before converting to a date-time.
x <- c("2019-01-01T00:00:01.1", "2019-01-01T00:00:01.78")

x <- naive_time_parse(x, precision = "millisecond")
x

time_point_floor(x, "second")
time_point_round(x, "second")

as_date_time(time_point_round(x, "second"), "America/New_York")