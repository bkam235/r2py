# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-quarter-day-count-between.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 11

suppressPackageStartupMessages(library(clock))
# Compute the number of whole quarters between two dates
x <- year_quarter_day(2020, 3, 91)
y <- year_quarter_day(2025, 4, c(90, 92))
calendar_count_between(x, y, "quarter")

# Note that this is not always the same as the number of whole 3 month
# periods between two dates
x <- as_year_month_day(x)
y <- as_year_month_day(y)
calendar_count_between(x, y, "month", n = 3)