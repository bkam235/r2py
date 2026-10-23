# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: posixt-formatting.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 18

suppressPackageStartupMessages(library(clock))
x <- date_time_parse(
  c("1970-04-26 01:30:00", "1970-04-26 03:30:00"),
  zone = "America/New_York"
)

# Default
date_format(x)

# Which is parseable by `date_time_parse_complete()`
date_time_parse_complete(date_format(x))

date_format(x, format = "%B %d, %Y %H:%M:%S")

# By default, `%Z` uses the full zone name, but you can switch to the
# abbreviated name
date_format(x, format = "%z %Z")
date_format(x, format = "%z %Z", abbreviate_zone = TRUE)