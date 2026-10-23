# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: posixt-rounding.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 23

suppressPackageStartupMessages(library(clock))
x <- as.POSIXct("2019-03-31", "America/New_York")
x <- add_days(x, 0:5)

# Flooring by 2 days, note that this is not tied to the current month,
# and instead counts from the specified `origin`, so groups can cross
# the month boundary
date_floor(x, "day", n = 2)

# Compare to `date_group()`, which groups by the day of the month
date_group(x, "day", n = 2)

# Note that daylight saving time gaps can throw off rounding
x <- as.POSIXct("1970-04-26 01:59:59", "America/New_York") + c(0, 1)
x

# Rounding is done in naive-time, which means that rounding by 2 hours
# will attempt to generate a time of 1970-04-26 02:00:00, which doesn't
# exist in this time zone
try(date_floor(x, "hour", n = 2))

# You can handle this by specifying a nonexistent time resolution strategy
date_floor(x, "hour", n = 2, nonexistent = "roll-forward")