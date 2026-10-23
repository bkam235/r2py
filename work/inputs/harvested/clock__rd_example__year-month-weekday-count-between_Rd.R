# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-month-weekday-count-between.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 11

suppressPackageStartupMessages(library(clock))
# Compute the number of months between two dates
x <- year_month_weekday(2001, 2)
y <- year_month_weekday(2021, c(1, 3))

calendar_count_between(x, y, "month")

# Remember that day precision or finer year-month-weekday objects
# are not comparable, so this won't work
x <- year_month_weekday(2001, 2, 1, 1)
try(calendar_count_between(x, x, "month"))