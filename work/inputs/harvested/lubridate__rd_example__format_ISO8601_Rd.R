# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: format_ISO8601.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 4

suppressPackageStartupMessages(library(lubridate))
format_ISO8601(as.Date("02-01-2018", format = "%m-%d-%Y"))
format_ISO8601(as.POSIXct("2018-02-01 03:04:05", tz = "America/New_York"), usetz = TRUE)
format_ISO8601(as.POSIXct("2018-02-01 03:04:05", tz = "America/New_York"), precision = "ymdhm")