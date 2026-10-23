# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year_month_day.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 13

suppressPackageStartupMessages(library(clock))
# Just the year
x <- year_month_day(2019:2025)

# Year-month type
year_month_day(2020, 1:12)

# The most common use case involves year, month, and day fields
x <- year_month_day(2020, clock_months$january, 1:5)
x

# Precision can go all the way out to nanosecond
year_month_day(2019, 1, 2, 2, 40, 45, 200, subsecond_precision = "nanosecond")