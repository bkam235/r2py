# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year_day.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 12

suppressPackageStartupMessages(library(clock))
# Just the year
x <- year_day(2019:2025)
x

year_day(2020, 1:10)

# Last day of the year, accounting for leap years
year_day(2019:2021, "last")

# Precision can go all the way out to nanosecond
year_day(2019, 100, 2, 40, 45, 200, subsecond_precision = "nanosecond")