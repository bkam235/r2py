# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: as_date.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 10

suppressPackageStartupMessages(library(lubridate))
dt_utc <- ymd_hms("2010-08-03 00:50:50")
dt_europe <- ymd_hms("2010-08-03 00:50:50", tz = "Europe/London")
c(as_date(dt_utc), as.Date(dt_utc))
c(as_date(dt_europe), as.Date(dt_europe))
## need not supply origin
as_date(10)
## Will replace invalid date format with NA
dt_wrong <- c("2009-09-29", "2012-11-29", "2015-29-12")
as_date(dt_wrong)