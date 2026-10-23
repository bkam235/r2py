# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date_parse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 35

suppressPackageStartupMessages(library(clock))
date_parse("2020-01-01")

date_parse(
  "January 5, 2020",
  format = "%B %d, %Y"
)

# With a different locale
date_parse(
  "janvier 5, 2020",
  format = "%B %d, %Y",
  locale = clock_locale("fr")
)

# A neat feature of `date_parse()` is the ability to parse
# the ISO year-week-day format
date_parse("2020-W01-2", format = "%G-W%V-%u")

# ---------------------------------------------------------------------------
# Sub-daily components

# If you have a string with sub-daily components, but only require the date,
# first parse them as date-times to fully parse the sub-daily components,
# then round using whatever convention is required for your use case before
# converting to date.
x <- c("2019-01-01 11", "2019-01-01 12")

x <- date_time_parse(x, zone = "UTC", format = "%Y-%m-%d %H")
x

date_floor(x, "day")
date_round(x, "day")

as_date(date_round(x, "day"))