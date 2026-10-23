# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date-count-between.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 77

suppressPackageStartupMessages(library(clock))
start <- date_parse("2000-05-05")
end <- date_parse(c("2020-05-04", "2020-05-06"))

# Age in years
date_count_between(start, end, "year")

# Number of "whole" months between these dates. i.e.
# `2000-05-05 -> 2020-04-05` is 239 months
# `2000-05-05 -> 2020-05-05` is 240 months
# Since 2020-05-04 occurs before the 5th of that month,
# it gets a count of 239
date_count_between(start, end, "month")

# Number of "whole" quarters between (same as `"month"` with `n * 3`)
date_count_between(start, end, "quarter")
date_count_between(start, end, "month", n = 3)

# Number of days between
date_count_between(start, end, "day")

# Number of full 3 day periods between these two dates
date_count_between(start, end, "day", n = 3)

# Essentially the truncated value of this
date_count_between(start, end, "day") / 3

# ---------------------------------------------------------------------------

# Breakdown into full years, months, and days between
x <- start

years <- date_count_between(x, end, "year")
x <- add_years(x, years)

months <- date_count_between(x, end, "month")
x <- add_months(x, months)

days <- date_count_between(x, end, "day")
x <- add_days(x, days)

data.frame(
  start = start,
  end = end,
  years = years,
  months = months,
  days = days
)

# Note that when breaking down a date like that, you may need to
# set `invalid` during intermediate calculations
start <- date_build(2019, c(3, 3, 4), c(30, 31, 1))
end <- date_build(2019, 5, 05)

# These are 1 month apart (plus a few days)
months <- date_count_between(start, end, "month")

# But adding that 1 month to `start` results in an invalid date
try(add_months(start, months))

# You can choose various ways to resolve this
start_previous <- add_months(start, months, invalid = "previous")
start_next <- add_months(start, months, invalid = "next")

days_previous <- date_count_between(start_previous, end, "day")
days_next <- date_count_between(start_next, end, "day")

# Resulting in slightly different day values.
# No result is "perfect". Choosing "previous" or "next" both result
# in multiple `start` dates having the same month/day breakdown values.
data.frame(
  start = start,
  end = end,
  months = months,
  days_previous = days_previous,
  days_next = days_next
)