# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: date.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 7

suppressPackageStartupMessages(library(lubridate))
x <- ymd_hms("2012-03-26 23:12:13", tz = "America/New_York")
date(x)
as.Date(x) # by default as.Date assumes you want to know the date in UTC
as.Date(x, tz = "America/New_York")
date(x) <- as.Date("2000-01-02")
x