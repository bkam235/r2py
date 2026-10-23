# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: quarter.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 9

suppressPackageStartupMessages(library(lubridate))
x <- ymd(c("2012-03-26", "2012-05-04", "2012-09-23", "2012-12-31"))
quarter(x)
quarter(x, type = "year.quarter")
quarter(x, type = "year.quarter", fiscal_start = 11)
quarter(x, type = "date_first", fiscal_start = 11)
quarter(x, type = "date_last", fiscal_start = 11)
semester(x)
semester(x, with_year = TRUE)