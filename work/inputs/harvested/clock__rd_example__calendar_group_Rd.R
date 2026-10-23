# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: calendar_group.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 10

suppressPackageStartupMessages(library(clock))
# See the calendar specific help pages for more examples
x <- year_month_day(2019, c(1, 1, 2, 2, 3, 3, 4, 4), 1:8)
x

# Group by two months
calendar_group(x, "month", n = 2)

# Group by two days of the month
calendar_group(x, "day", n = 2)