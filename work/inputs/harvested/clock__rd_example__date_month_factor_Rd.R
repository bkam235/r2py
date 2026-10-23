# r2py crawler metadata
# package: clock
# source_type: rd_example
# topic: date_month_factor.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\help
# lines: 6

suppressPackageStartupMessages(library(clock))
x <- add_months(as.Date("2019-01-01"), 0:11)

date_month_factor(x)
date_month_factor(x, abbreviate = TRUE)
date_month_factor(x, labels = "fr")