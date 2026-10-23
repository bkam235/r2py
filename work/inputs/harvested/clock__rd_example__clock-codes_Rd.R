# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: clock-codes.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 8

suppressPackageStartupMessages(library(clock))
weekday(clock_weekdays$wednesday)

year_month_weekday(2019, clock_months$april, clock_weekdays$monday, 1:4)

year_week_day(2020, 52, start = clock_weekdays$monday)

iso_year_week_day(2020, 52, clock_iso_weekdays$thursday)