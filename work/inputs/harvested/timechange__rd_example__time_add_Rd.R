# r2py crawler metadata
# package: timechange
# source_type: rd_example
# topic: time_add.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timechange\help
# lines: 68

suppressPackageStartupMessages(library(timechange))
# Addition

## Month gap
x <- as.POSIXct("2000-01-31 01:02:03", tz = "America/Chicago")
time_add(x, month = 1, roll_month = "postday")
time_add(x, month = 1, roll_month = "preday")
time_add(x, month = 1, roll_month = "boundary")
time_add(x, month = 1, roll_month = "full")
time_add(x, month = 1, roll_month = "NA")
time_add(x, month = 1, day = 3,  roll_month = "postday")
time_add(x, month = 1, day = 3,  roll_month = "preday")
time_add(x, month = 1, day = 3,  roll_month = "boundary")
time_add(x, month = 1, day = 3,  roll_month = "full")
time_add(x, month = 1, day = 3,  roll_month = "NA")

## DST gap
x <- as.POSIXlt("2010-03-14 01:02:03", tz = "America/Chicago")
time_add(x, hour = 1, minute = 50, roll_dst = "pre")
time_add(x, hour = 1, minute = 50, roll_dst = "boundary")
time_add(x, hour = 1, minute = 50, roll_dst = "post")
##' time_add(x, hours = 1, minutes = 50, roll_dst = "NA")

## DST repeated time with cross-first and cross-last
(tt <- as.POSIXct(c("2014-11-02 00:15:00", "2014-11-02 02:15:00"), tz = "America/New_York"))
time_add(tt, hours = c(1, -1), roll_dst = "pre")
time_add(tt, hours = c(1, -1), roll_dst = "post")
time_add(tt, hours = c(1, -1), roll_dst = "xfirst")
time_add(tt, hours = c(1, -1), roll_dst = "xlast")

## DST skip with cross-first and cross-last
cst <- as.POSIXlt("2010-03-14 01:02:03", tz = "America/Chicago")
cdt <- as.POSIXlt("2010-03-14 03:02:03", tz = "America/Chicago")
time_add(cst, hour = 1, roll_dst = "xfirst")
time_add(cst, hour = 1, roll_dst = "xlast")
time_add(cdt, hour = -1, roll_dst = "xfirst")
time_add(cdt, hour = -1, roll_dst = "xlast")

# WARNING:
# In the following example the overall period is treated as a negative period
# because the largest unit (hour) is negative. Thus `xfirst` roll_dst results in the
# "post" time. To avoid such confusing behavior either avoid supplying multiple
# units with heterogeneous sign.
time_add(cst, hour = -1, minute = 170, roll_dst = "xfirst")

# SUBTRACTION

## Month gap
x <- as.POSIXct("2000-03-31 01:02:03", tz = "America/Chicago")
time_subtract(x, month = 1, roll_month = "postday")
time_subtract(x, month = 1, roll_month = "preday")
time_subtract(x, month = 1, roll_month = "boundary")
time_subtract(x, month = 1, roll_month = "full")
time_subtract(x, month = 1, roll_month = "NA")
time_subtract(x, month = 1, day = 0, roll_month = "postday")
time_subtract(x, month = 1, day = 3, roll_month = "postday")
time_subtract(x, month = 1, day = 0, roll_month = "preday")
time_subtract(x, month = 1, day = 3, roll_month = "preday")
time_subtract(x, month = 1, day = 3, roll_month = "boundary")
time_subtract(x, month = 1, day = 3, roll_month = "full")
time_subtract(x, month = 1, day = 3, roll_month = "NA")

## DST gap
y <- as.POSIXlt("2010-03-15 01:02:03", tz = "America/Chicago")
time_subtract(y, hour = 22, minute = 50, roll_dst = "pre")
time_subtract(y, hour = 22, minute = 50, roll_dst = "boundary")
time_subtract(y, hour = 22, minute = 50, roll_dst = "post")
time_subtract(y, hour = 22, minute = 50, roll_dst = "NA")