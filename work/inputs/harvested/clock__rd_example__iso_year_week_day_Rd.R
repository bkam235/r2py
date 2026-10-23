# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: iso_year_week_day.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 11

suppressPackageStartupMessages(library(clock))
# Year-week
x <- iso_year_week_day(2019:2025, 1)
x

# 2nd day of the first ISO week in multiple years
iso_days <- set_day(x, clock_iso_weekdays$tuesday)
iso_days

# What year-month-day is this?
as_year_month_day(iso_days)