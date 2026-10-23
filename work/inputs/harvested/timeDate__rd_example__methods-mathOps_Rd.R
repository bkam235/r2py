# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: methods-mathOps.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 12

suppressPackageStartupMessages(library(timeDate))
## create some data
dts <- c("1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09")
tms <- c(  "23:12:55",   "10:34:02",   "08:30:00",   "11:18:23")
GMT <- timeDate(dts, zone = "GMT", FinCenter = "GMT")
ZUR <- timeDate(dts, zone = "GMT", FinCenter = "Europe/Zurich")
   
## add one day 
GMT + 24*3600

## subtract
ZUR[2] - ZUR[1]