# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-week-day-group.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 10

suppressPackageStartupMessages(library(clock))
x <- year_week_day(2019, 1:52)

# Group by 3 weeks
calendar_group(x, "week", n = 3)

y <- year_week_day(2000:2020, 1, 1)

# Group by 2 years
calendar_group(y, "year", n = 2)