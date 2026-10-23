# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: class-timeDate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 85

suppressPackageStartupMessages(library(timeDate))
## Examples for Objects of class 'timeDate'

## Sys.timeDate()           # direct
## timeDate(Sys.time())     # transformed from "POSIX(c)t"

## local time in Zurich
## timeDate(Sys.time(), FinCenter = "Zurich")  

## character vector strings for the examples below
dts <- c("1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09")
tms <- c(  "23:12:55",   "10:34:02",   "08:30:00",   "11:18:23")

t1 <- timeDate(dts, format = "%Y-%m-%d", FinCenter = "GMT" )
t1a <- timeDate(dts, FinCenter = "GMT")  # auto-format
identical(t1, t1a)

t1

timeDate(dts, format = "%Y-%m-%d", FinCenter = "Europe/Zurich")

timeDate(paste(dts, tms), format = "%Y-%m-%d %H:%M:%S",
  zone = "GMT", FinCenter = "GMT")

timeDate(paste(dts, tms), 
  zone = "Europe/Zurich", FinCenter = "Europe/Zurich")

timeDate(paste(dts, tms), format = "%Y-%m-%d %H:%M:%S",
  zone = "GMT", FinCenter = "Europe/Zurich")

## non standard format
timeDate(paste(20:31, "03.2005", sep="."), format = "%d.%m.%Y")

## Note, ISO and American formats are auto-detected
timeDate("2004-12-31", FinCenter = "GMT")
timeDate("12/11/2004", FinCenter = "GMT")
timeDate("1/31/2004") # auto-detect American format

## ... from POSIX?t, and Using NAs:
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
## this throws error (since NAs are converted to the string NA):
timeDate(paste(dts,tms), FinCenter = "Europe/Zurich")
## Error in midnightStandard2(charvec, format) :
##   'charvec' has non-NA entries of different number of characters

## these work:
td1 <- timeDate(pasteMat(cbind(dts, tms)), FinCenter = "Europe/Zurich")
td2 <- timeDate(pasteMat(dts, tms), FinCenter = "Europe/Zurich")
identical(td1, td2) ## TRUE

## timeCalendar
## getRmetricsOptions("currentYear")
timeCalendar()  # 12 months of current year
timeCalendar(2022) # 12 months of 2022
timeCalendar(y = c(1989, 2001, 2004, 1990), 
    m = c(9, 1, 8, 2), d = c(28, 15, 30, 9), FinCenter = "GMT")
timeCalendar(y = c(1989, 2001, 2004, 1990),
    m = c(9, 1, 8, 2), d = c(28, 15, 30, 9), FinCenter = "Europe/Zurich")

## timeCalendar(h = c(9, 14), min = c(15, 23))
timeCalendar(2022, h = c(9, 14), min = c(15, 23))

## timeSequence
timeSequence(from = "2004-03-12", to = "2004-04-11",
  format = "%Y-%m-%d", FinCenter = "GMT")
timeSequence(from = "2004-03-12", to = "2004-04-11",
  format = "%Y-%m-%d", FinCenter = "Europe/Zurich")

## print, summary, format
tC = timeCalendar(2022)
tC
print(tC)
summary(tC)
format(tC)