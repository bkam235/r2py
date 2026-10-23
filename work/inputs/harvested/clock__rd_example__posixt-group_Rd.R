# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: posixt-group.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 18

suppressPackageStartupMessages(library(clock))
x <- as.POSIXct("2019-01-01", "America/New_York")
x <- add_days(x, -3:5)

# Group by 2 days of the current month.
# Note that this resets at the beginning of the month, creating day groups
# of [29, 30] [31] [01, 02] [03, 04].
date_group(x, "day", n = 2)

# Group by month
date_group(x, "month")

# Group by hour of the day
y <- as.POSIXct("2019-12-30", "America/New_York")
y <- add_hours(y, 0:12)
y

date_group(y, "hour", n = 3)