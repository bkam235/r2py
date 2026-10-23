# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-quarter-day-setters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 41

suppressPackageStartupMessages(library(clock))
library(magrittr)

# Quarter precision vector
x <- year_quarter_day(2019, 1:4)
x

# Promote to day precision by setting the day
x <- set_day(x, 1)
x

# Or set to the last day of the quarter
x <- set_day(x, "last")
x

# What year-month-day is this?
as_year_month_day(x)

# Set to an invalid day of the quarter
# (not all quarters have 92 days)
invalid <- set_day(x, 92)
invalid

# Here are the invalid ones
invalid[invalid_detect(invalid)]

# Resolve the invalid dates by choosing the previous/next valid moment
invalid_resolve(invalid, invalid = "previous")
invalid_resolve(invalid, invalid = "next")

# Or resolve by "overflowing" by the number of days that you have
# gone past the last valid day
invalid_resolve(invalid, invalid = "overflow")

# This is similar to
days <- get_day(invalid) - 1L
invalid %>%
  set_day(1) %>%
  as_naive_time() %>%
  add_days(days) %>%
  as_year_quarter_day()