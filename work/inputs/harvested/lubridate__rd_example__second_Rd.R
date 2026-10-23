# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: second.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 6

suppressPackageStartupMessages(library(lubridate))
x <- ymd("2012-03-26")
second(x)
second(x) <- 1
second(x) <- 61
second(x) > 2