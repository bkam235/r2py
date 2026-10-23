# r2py crawler metadata
# package: timechange
# source_type: rd_example
# topic: time_update.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timechange\help
# lines: 19

suppressPackageStartupMessages(library(timechange))
date <- as.Date("2009-02-10")
time_update(date, year = 2010, month = 1, mday = 1)
time_update(date, year = 2010, month = 13, mday = 1)
time_update(date, minute = 10, second = 3)
time_update(date, minute = 10, second = 3, tz = "America/New_York")

time <- as.POSIXct("2015-02-03 01:02:03", tz = "America/New_York")
time_update(time, month = 2, mday = 31, roll_month = "preday")
time_update(time, month = 2, mday = 31, roll_month = "boundary")
time_update(time, month = 2, mday = 31, roll_month = "postday")
time_update(time, month = 2, mday = 31, exact = TRUE)
time_update(time, month = 2, mday = 31, exact = FALSE)

## DST skipped
time <- as.POSIXct("2015-02-03 01:02:03", tz = "America/New_York")
time_update(time, year = 2016, yday = 10)
time_update(time, year = 2016, yday = 10, tz = "Europe/Amsterdam")
time_update(time, second = 30,  tz = "America/New_York")