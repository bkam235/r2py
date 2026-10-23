# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: base-round.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 27

suppressPackageStartupMessages(library(timeDate))
# create a timeDate object
dts <- c("1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09")
tms <- c(  "23:12:55.13",   "10:34:02.23",   "08:30:00.33",   "11:18:23.53")
td <- timeDate(paste(dts, tms), format = "%Y-%m-%d %H:%M:%S",
               zone = "GMT", FinCenter = "GMT")

## round
round(td) # same as round(td, "days")

round(td, "secs")
round(td, "mins")
round(td, "hours")
round(td, "days")
round(td, "months")
round(td, "years")


## truncate
trunc(td) # same as trunc(td, "days")

trunc(td, "secs")
trunc(td, "mins")
trunc(td, "hours")
trunc(td, "days")
trunc(td, "months")
trunc(td, "years")