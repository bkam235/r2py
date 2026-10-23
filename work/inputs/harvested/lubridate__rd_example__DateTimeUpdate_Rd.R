# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: DateTimeUpdate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 7

suppressPackageStartupMessages(library(lubridate))
date <- ymd("2009-02-10")
update(date, year = 2010, month = 1, mday = 1)

update(date, year = 2010, month = 13, mday = 1)

update(date, minute = 10, second = 3)