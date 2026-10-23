# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year-month-weekday-group.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 6

suppressPackageStartupMessages(library(clock))
x <- year_month_weekday(2019, 1:12, clock_weekdays$sunday, 1, 00, 05, 05)
x

# Group by 3 months - drops more precise components!
calendar_group(x, "month", n = 3)