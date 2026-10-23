# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: year_month_weekday.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 15

suppressPackageStartupMessages(library(clock))
# All Fridays in January, 2019
# Note that there was no 5th Friday in January
x <- year_month_weekday(
  2019,
  clock_months$january,
  clock_weekdays$friday,
  1:5
)
x

invalid_detect(x)

# Resolve this invalid date by using the previous valid date
invalid_resolve(x, invalid = "previous")