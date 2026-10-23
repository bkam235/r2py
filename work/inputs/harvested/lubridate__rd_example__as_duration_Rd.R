# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: as.duration.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 7

suppressPackageStartupMessages(library(lubridate))
span <- interval(ymd("2009-01-01"), ymd("2009-08-01")) # interval
as.duration(span)
as.duration(10) # numeric
dur <- duration(hours = 10, minutes = 6)
as.numeric(dur, "hours")
as.numeric(dur, "minutes")