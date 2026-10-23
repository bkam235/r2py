# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: timeCeiling.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 40

suppressPackageStartupMessages(library(timeDate))
# create a timeDate object
dts <- c("1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09")
tms <- c(  "23:12:55.13",   "10:34:02.23",   "08:30:00.33",   "11:18:23.53")
td <- timeDate(paste(dts, tms), format = "%Y-%m-%d %H:%M:%S",
               zone = "GMT", FinCenter = "GMT")

## timeCeiling
timeCeiling(td) # same as timeCeiling(td, "days")

timeCeiling(td, "secs")
timeCeiling(td, "mins")
timeCeiling(td, "hours")
timeCeiling(td, "days")
timeCeiling(td, "months")
timeCeiling(td, "years")

## rounding with "days" usually sets the time to midnight (the start of a day),
## but it may not exist
Sofia_to_DST_char <- c("1983-03-26 23:00:00",
    "1983-03-27 00:00:00", # change to DST; 0am doesn't exist in Sofia on this date
    "1983-03-27 01:00:00",
    "1983-03-27 02:00:00",
    "1983-03-27 03:00:00")

Sofia_to_DST <- timeDate(Sofia_to_DST_char, zone = "Sofia", FinCenter = "Sofia")
cbind(Sofia_to_DST_char, format(Sofia_to_DST@Data))

## on 27/03/1983 in Sofia the clock jumped at midnight to 1am, so the
## day started at 1am - hence the first time below.  the rest are on the
## next day, which starts at midnight.
timeCeiling(Sofia_to_DST) # same as timeCeiling(Sofia_to_DST, "days")

trunc(Sofia_to_DST)

## to avoid confusion, set non-existent times to NA
Sofia_to_DSTa <- timeDate(Sofia_to_DST_char, zone = "Sofia", FinCenter = "Sofia",
                          dst_gap = "NA")
Sofia_to_DSTa
timeCeiling(Sofia_to_DSTa)