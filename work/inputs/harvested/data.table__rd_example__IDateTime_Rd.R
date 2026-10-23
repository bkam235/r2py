# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: IDateTime.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 58

suppressPackageStartupMessages(library(data.table))
# create IDate:
(d <- as.IDate("2001-01-01"))

# S4 coercion also works
identical(as.IDate("2001-01-01"), methods::as("2001-01-01", "IDate"))

# create ITime:
(t <- as.ITime("10:45"))

# S4 coercion also works
identical(as.ITime("10:45"), methods::as("10:45", "ITime"))

(t <- as.ITime("10:45:04"))

(t <- as.ITime("10:45:04", format = "%H:%M:%S"))

# "24:00:00" is parsed as "00:00:00"
as.ITime("24:00:00")

# Workaround for end-of-day: add 1 second to "23:59:59"
as.ITime("23:59:59") + 1L

as.POSIXct("2001-01-01") + as.ITime("10:45")

datetime <- seq(as.POSIXct("2001-01-01"), as.POSIXct("2001-01-03"), by = "5 hour")
(af <- data.table(IDateTime(datetime), a = rep(1:2, 5), key = c("a", "idate", "itime")))

af[, mean(a), by = "itime"]
af[, mean(a), by = list(hour = hour(itime))]
af[, mean(a), by = list(wday = factor(weekdays(idate)))]
af[, mean(a), by = list(wday = wday(idate))]

as.POSIXct(af$idate)
as.POSIXct(af$idate, time = af$itime)
as.POSIXct(af$idate, af$itime)
as.POSIXct(af$idate, time = af$itime, tz = "GMT")

as.POSIXct(af$itime, af$idate)
as.POSIXct(af$itime) # uses today's date

(seqdates <- seq(as.IDate("2001-01-01"), as.IDate("2001-08-03"), by = "3 weeks"))
round(seqdates, "months")

(seqtimes <- seq(as.ITime("07:00"), as.ITime("08:00"), by = 20))
round(seqtimes, "hours")
trunc(seqtimes, "hours")

# Examples for isoyear() and isoweek()
d1 = as.IDate("2019-12-30")
year(d1)
isoweek(d1)
isoyear(d1)

d2 = as.IDate("2016-01-01")
year(d2)
isoweek(d2)
isoyear(d2)