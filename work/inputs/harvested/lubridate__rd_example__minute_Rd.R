# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: minute.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 6

suppressPackageStartupMessages(library(lubridate))
x <- ymd("2012-03-26")
minute(x)
minute(x) <- 1
minute(x) <- 61
minute(x) > 2