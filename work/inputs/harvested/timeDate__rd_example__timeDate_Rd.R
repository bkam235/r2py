# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: timeDate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 83

suppressPackageStartupMessages(library(timeDate))
## character vector strings:
dts <- c("1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09")
tms <- c(  "23:12:55",   "10:34:02",   "08:30:00",   "11:18:23")

dts; tms

t1 <- timeDate(dts, format = "%Y-%m-%d", FinCenter = "GMT" )
t1

stopifnot(identical(t1, timeDate(dts, FinC = "GMT"))) # auto-format

timeDate(dts, format = "%Y-%m-%d", FinCenter = "Europe/Zurich")

timeDate(paste(dts, tms), format = "%Y-%m-%d %H:%M:%S",
     zone = "GMT", FinCenter = "GMT")

timeDate(paste(dts, tms), 
     zone = "Europe/Zurich", FinCenter = "Europe/Zurich")

timeDate(paste(dts, tms), format = "%Y-%m-%d %H:%M:%S",
     zone = "GMT", FinCenter = "Europe/Zurich")

## non standard format:
timeDate(paste(20:31, "03.2005", sep="."), format = "%d.%m.%Y")

## ISO and American formats are auto-detected:
timeDate("2004-12-31", FinCenter = "GMT")
timeDate("12/11/2004", FinCenter = "GMT")
timeDate("1/31/2004") # auto-detect American format

## ... from POSIX?t, and containing NAs:
lsec <- as.POSIXlt(.leap.seconds)
lsec
lsec[c(2,4:6)] <- NA
timeDate(lsec)

dtms <- paste(dts,tms)
dtms[2:3] <- NA
timeDate(dtms, FinCenter = "Europe/Zurich")

## NAs in dates and/or times
dts2 <- c("1989-09-28", NA, "2004-08-30", "1990-02-09")
tms2 <- c(  "23:12:55",   "10:34:02",   NA,   "11:18:23")
## this throws error (since NAs are converted to the string "NA"):
## timeDate(paste(dts,tms), FinCenter = "Europe/Zurich")
## ## Error in midnightStandard2(charvec, format) :
## ##   'charvec' has non-NA entries of different number of characters
##
## these work:
td1 <- timeDate(pasteMat(cbind(dts, tms)), FinCenter = "Europe/Zurich")
td2 <- timeDate(pasteMat(dts, tms), FinCenter = "Europe/Zurich")
identical(td1, td2) ## TRUE

## NA's that appear due to non-existent times;
## on 27/03/1983 in Sofia the clock jumped at midnight to 1am
Sofia_to_DST_char <- c("1983-03-26 23:00:00",
    "1983-03-27 00:00:00", # change to DST; 0am doesn't exist in Sofia on this date
    "1983-03-27 01:00:00",
    "1983-03-27 02:00:00",
    "1983-03-27 03:00:00")

## by default, the non-existent time is moved to the next valid time,
## this is equivalent to dst_gap = "+"
Sofia_to_DST <- timeDate(Sofia_to_DST_char, zone = "Sofia", FinCenter = "Sofia")

## use dst_gap = "NA" to turn invalid times into NA's
Sofia_to_DSTa <- timeDate(Sofia_to_DST_char, zone = "Sofia", FinCenter = "Sofia",
                          dst_gap = "NA")
Sofia_to_DSTa

cbind(Sofia_to_DST_char,
      Sofia_to_DST = format(Sofia_to_DST),
      Sofia_to_DSTa = format(Sofia_to_DSTa)
      )

## dst_gap = "-" rolls the invalid time back
Sofia_to_DSTb <- timeDate(Sofia_to_DST_char, zone = "Sofia", FinCenter = "Sofia",
                          dst_gap = "-")
Sofia_to_DSTb

## Coerce a 'Date' object into a 'timeDate' object:
as.timeDate(Sys.Date())