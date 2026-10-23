# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: base-diff.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 12

suppressPackageStartupMessages(library(timeDate))
## create character vectors
dts <- c("1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09")
tms <- c(  "23:12:55",   "10:34:02",   "08:30:00",   "11:18:23")
## timeDate
GMT <- timeDate(dts, zone = "GMT", FinCenter = "GMT") + 24*3600
GMT

## suitably lagged and iterated differences
diff(GMT)
diff(GMT, lag = 2)
diff(GMT, lag = 1, diff = 2)