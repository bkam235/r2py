# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: date_decimal.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 4

suppressPackageStartupMessages(library(lubridate))
date <- ymd("2009-02-10")
decimal <- decimal_date(date) # 2009.11
date_decimal(decimal) # "2009-02-10 UTC"