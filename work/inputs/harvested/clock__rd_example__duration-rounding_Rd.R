# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: duration-rounding.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 27

suppressPackageStartupMessages(library(clock))
x <- duration_seconds(c(86399, 86401))

duration_floor(x, "day")
duration_ceiling(x, "day")

# Can't floor from a chronological duration (seconds)
# to a calendrical duration (months)
try(duration_floor(x, "month"))

# Every 2 days, using an origin of day 0
y <- duration_seconds(c(0, 86400, 86400 * 2, 86400 * 3))
duration_floor(y, "day", n = 2)

# Shifting the origin to be day 1
origin <- duration_days(1)
duration_floor(y - origin, "day", n = 2) + origin

# Rounding will round ties up
half_day <- 86400 / 2
half_day_durations <- duration_seconds(c(half_day - 1, half_day, half_day + 1))
duration_round(half_day_durations, "day")

# With larger units
x <- duration_months(c(0, 15, 24))
duration_floor(x, "year")
duration_floor(x, "quarter")