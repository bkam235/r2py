# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date-rounding.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 27

suppressPackageStartupMessages(library(clock))
x <- as.Date("2019-03-31") + 0:5
x

# Flooring by 2 days, note that this is not tied to the current month,
# and instead counts from the specified `origin`, so groups can cross
# the month boundary
date_floor(x, "day", n = 2)

# Compare to `date_group()`, which groups by the day of the month
date_group(x, "day", n = 2)

y <- as.Date("2019-01-01") + 0:20
y

# Flooring by week uses an implicit `origin` of 1970-01-01, which
# is a Thursday
date_floor(y, "week")
as_weekday(date_floor(y, "week"))

# If you want to round by weeks with a different week start, supply an
# `origin` that falls on the weekday you care about. This uses a Monday.
origin <- as.Date("1970-01-05")
as_weekday(origin)

date_floor(y, "week", origin = origin)
as_weekday(date_floor(y, "week", origin = origin))