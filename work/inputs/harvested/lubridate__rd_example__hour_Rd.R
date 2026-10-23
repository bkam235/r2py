# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: hour.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 6

suppressPackageStartupMessages(library(lubridate))
x <- ymd("2012-03-26")
hour(x)
hour(x) <- 1
hour(x) <- 25
hour(x) > 2