# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: force_tz.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 32

suppressPackageStartupMessages(library(lubridate))
x <- ymd_hms("2009-08-07 00:00:01", tz = "America/New_York")
force_tz(x, "UTC")
force_tz(x, "Europe/Amsterdam")

## DST skip:
y <- ymd_hms("2010-03-14 02:05:05 UTC")
force_tz(y, "America/New_York", roll_dst = "NA")
force_tz(y, "America/New_York", roll_dst = "pre")
force_tz(y, "America/New_York", roll_dst = "boundary")
force_tz(y, "America/New_York", roll_dst = "post")

## DST repeat
y <- ymd_hms("2014-11-02 01:35:00", tz = "UTC")
force_tz(y, "America/New_York", roll_dst = "NA")
force_tz(y, "America/New_York", roll_dst = "pre")
force_tz(y, "America/New_York", roll_dst = "boundary")
force_tz(y, "America/New_York", roll_dst = "post")

## DST skipped and repeated
y <- ymd_hms("2010-03-14 02:05:05 UTC", "2014-11-02 01:35:00", tz = "UTC")
force_tz(y, "America/New_York", roll_dst = c("NA", "pre"))
force_tz(y, "America/New_York", roll_dst = c("boundary", "post"))

## Heterogeneous time-zones:

x <- ymd_hms(c("2009-08-07 00:00:01", "2009-08-07 01:02:03"))
force_tzs(x, tzones = c("America/New_York", "Europe/Amsterdam"))
force_tzs(x, tzones = c("America/New_York", "Europe/Amsterdam"), tzone_out = "America/New_York")

x <- ymd_hms("2009-08-07 00:00:01")
force_tzs(x, tzones = c("America/New_York", "Europe/Amsterdam"))