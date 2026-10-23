# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year_month_day_parse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 39

suppressPackageStartupMessages(library(clock))
x <- "2019-01-01"

# Default parses at day precision
year_month_day_parse(x)

# Can parse at less precise precisions too
year_month_day_parse(x, precision = "month")
year_month_day_parse(x, precision = "year")

# Even invalid dates can be round-tripped through format<->parse calls
invalid <- year_month_day(2019, 2, 30)
year_month_day_parse(format(invalid))

# Can parse with time of day
year_month_day_parse(
  "2019-01-30T02:30:00.123456789",
  precision = "nanosecond"
)

# Can parse using multiple format strings, which will be tried
# in the order they are provided
x <- c("2019-01-01", "2020-01-01", "2021/2/3")
formats <- c("%Y-%m-%d", "%Y/%m/%d")
year_month_day_parse(x, format = formats)

# Can parse using other format tokens as well
year_month_day_parse(
  "January, 2019",
  format = "%B, %Y",
  precision = "month"
)

# Parsing a French year-month-day
year_month_day_parse(
  "octobre 1, 2000",
  format = "%B %d, %Y",
  locale = clock_locale("fr")
)