# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date-group.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 11

suppressPackageStartupMessages(library(clock))
x <- as.Date("2019-01-01") + -3:5
x

# Group by 2 days of the current month.
# Note that this resets at the beginning of the month, creating day groups
# of [29, 30] [31] [01, 02] [03, 04].
date_group(x, "day", n = 2)

# Group by month
date_group(x, "month")