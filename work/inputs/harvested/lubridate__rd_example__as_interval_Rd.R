# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: as.interval.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 14

suppressPackageStartupMessages(library(lubridate))
diff <- make_difftime(days = 31) # difftime
as.interval(diff, ymd("2009-01-01"))
as.interval(diff, ymd("2009-02-01"))

dur <- duration(days = 31) # duration
as.interval(dur, ymd("2009-01-01"))
as.interval(dur, ymd("2009-02-01"))

per <- period(months = 1) # period
as.interval(per, ymd("2009-01-01"))
as.interval(per, ymd("2009-02-01"))

as.interval(3600, ymd("2009-01-01")) # numeric