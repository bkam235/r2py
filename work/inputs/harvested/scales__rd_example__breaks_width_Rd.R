# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: breaks_width.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 34

suppressPackageStartupMessages(library(scales))
demo_continuous(c(0, 100))
demo_continuous(c(0, 100), breaks = breaks_width(10))
demo_continuous(c(0, 100), breaks = breaks_width(20, -4))
demo_continuous(c(0, 100), breaks = breaks_width(20, 4))

# This is also useful for dates
one_month <- as.POSIXct(c("2020-05-01", "2020-06-01"))
demo_datetime(one_month)
demo_datetime(one_month, breaks = breaks_width("1 week"))
demo_datetime(one_month, breaks = breaks_width("5 days"))
# This is so useful that scale_x_datetime() has a shorthand:
demo_datetime(one_month, date_breaks = "5 days")

# hms times also work
one_hour <- hms::hms(hours = 0:1)
demo_time(one_hour)
demo_time(one_hour, breaks = breaks_width("15 min"))
demo_time(one_hour, breaks = breaks_width("600 sec"))

# Offets are useful for years that begin on dates other than the 1st of
# January, such as the UK financial year, which begins on the 1st of April.
three_years <- as.POSIXct(c("2020-01-01", "2021-01-01", "2022-01-01"))
demo_datetime(
  three_years,
  breaks = breaks_width("1 year", offset = "3 months")
)

# The offset can be a vector, to create offsets that have compound units,
# such as the UK fiscal (tax) year, which begins on the 6th of April.
demo_datetime(
  three_years,
  breaks = breaks_width("1 year", offset = c("3 months", "5 days"))
)