# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-month-day-count-between.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 11

suppressPackageStartupMessages(library(clock))
# Compute an individual's age in years
x <- year_month_day(2001, 2, 4)
today <- year_month_day(2021, 11, 30)
calendar_count_between(x, today, "year")

# Compute the number of months between two dates, taking
# into account the day of the month and time of day
x <- year_month_day(2000, 4, 2, 5)
y <- year_month_day(2000, 7, c(1, 2, 2), c(3, 4, 6))
calendar_count_between(x, y, "month")