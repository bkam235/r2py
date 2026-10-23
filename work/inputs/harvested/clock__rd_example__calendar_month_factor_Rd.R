# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: calendar_month_factor.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 6

suppressPackageStartupMessages(library(clock))
x <- year_month_day(2019, 1:12)

calendar_month_factor(x)
calendar_month_factor(x, abbreviate = TRUE)
calendar_month_factor(x, labels = "fr")