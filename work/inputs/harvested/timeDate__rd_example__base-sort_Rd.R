# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: base-sort.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 23

suppressPackageStartupMessages(library(timeDate))
## c
# create character vectors
dts = c("1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09")
dts
tms = c(  "23:12:55",   "10:34:02",   "08:30:00",   "11:18:23")
tms
   
## "+/-"
# add one day to a given timeDate object:
GMT = timeDate(dts, zone = "GMT", FinCenter = "GMT")
GMT
ZUR = timeDate(dts, zone = "GMT", FinCenter = "Europe/Zurich")
ZUR
   
## c
# concatenate and replicate timeDate objects
c(GMT[1:2], ZUR[1:2])
c(ZUR[1:2], GMT[1:2])
   
## rep
rep(ZUR[2], times = 3)
rep(ZUR[2:3], times = 2)