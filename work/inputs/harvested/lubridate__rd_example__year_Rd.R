# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: year.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 5

suppressPackageStartupMessages(library(lubridate))
x <- ymd("2012-03-26")
year(x)
year(x) <- 2001
year(x) > 1995