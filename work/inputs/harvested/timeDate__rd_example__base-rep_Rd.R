# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: base-rep.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 7

suppressPackageStartupMessages(library(timeDate))
## rep
dts = c("1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09")
ZUR = timeDate(dts, zone = "GMT", FinCenter = "Europe/Zurich")

rep(ZUR[2], times = 3)
rep(ZUR[2:3], times = 2)