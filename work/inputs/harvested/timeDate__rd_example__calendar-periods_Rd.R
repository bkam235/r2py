# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: calendar-periods.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 13

suppressPackageStartupMessages(library(timeDate))
## create time sequence
x <- timeSequence(from = "2001-01-01", to = "2009-01-01", by = "day")

## generate periods
periods(x, "12m", "1m")
periods(x, "52w", "4w")

## roll periodically
periodicallyRolling(x)

## roll monthly
monthlyRolling(x)