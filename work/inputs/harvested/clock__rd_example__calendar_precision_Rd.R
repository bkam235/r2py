# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: calendar_precision.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 4

suppressPackageStartupMessages(library(clock))
calendar_precision(year_month_day(2019))
calendar_precision(year_month_day(2019, 1, 1))
calendar_precision(year_quarter_day(2019, 3))