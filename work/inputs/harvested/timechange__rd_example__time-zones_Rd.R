# r2py crawler metadata
# package: timechange
# source_type: rd_example
# topic: time-zones.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timechange\help
# lines: 39

suppressPackageStartupMessages(library(timechange))
x <- as.POSIXct("2009-08-07 00:00:00", tz = "America/New_York")
time_at_tz(x, "UTC")
time_force_tz(x, "UTC")
time_force_tz(x, "Europe/Amsterdam")


## DST skip:

y <- as.POSIXct("2010-03-14 02:05:05", tz = "UTC")
time_force_tz(y, "America/New_York", roll = "boundary")
time_force_tz(y, "America/New_York", roll = "post")
time_force_tz(y, "America/New_York", roll = "pre")
time_force_tz(y, "America/New_York", roll = "NA")


## DST skipped and repeated

y <- as.POSIXct(c("2010-03-14 02:05:05 UTC", "2014-11-02 01:35:00"), tz = "UTC")
time_force_tz(y, "America/New_York", roll_dst = c("NA", "pre"))
time_force_tz(y, "America/New_York", roll_dst = c("boundary", "post"))

## Heterogeneous time-zones:

x <- as.POSIXct(c("2009-08-07 00:00:01", "2009-08-07 01:02:03"), tz = "UTC")
time_force_tz(x, tz = c("America/New_York", "Europe/Amsterdam"))
time_force_tz(x, tz = c("America/New_York", "Europe/Amsterdam"), tzout = "America/New_York")

x <- as.POSIXct("2009-08-07 00:00:01", tz = "UTC")
time_force_tz(x, tz = c("America/New_York", "Europe/Amsterdam"))

## Local clock:
x <- as.POSIXct(c("2009-08-07 01:02:03", "2009-08-07 10:20:30"), tz = "UTC")
time_clock_at_tz(x, units = "secs")
time_clock_at_tz(x, units = "hours")
time_clock_at_tz(x, "Europe/Amsterdam")

x <- as.POSIXct("2009-08-07 01:02:03", tz = "UTC")
time_clock_at_tz(x, tz = c("America/New_York", "Europe/Amsterdam", "Asia/Shanghai"), unit = "hours")