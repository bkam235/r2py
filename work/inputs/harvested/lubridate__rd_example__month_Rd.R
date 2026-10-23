# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: month.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 11

suppressPackageStartupMessages(library(lubridate))
x <- ymd("2012-03-26")
month(x)
month(x) <- 1
month(x) <- 13
month(x) > 3

month(ymd(080101))
month(ymd(080101), label = TRUE)
month(ymd(080101), label = TRUE, abbr = FALSE)
month(ymd(080101) + months(0:11), label = TRUE)