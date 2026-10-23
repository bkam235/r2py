# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: week.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 6

suppressPackageStartupMessages(library(lubridate))
x <- ymd("2012-03-26")
week(x)
week(x) <- 1
week(x) <- 54
week(x) > 3