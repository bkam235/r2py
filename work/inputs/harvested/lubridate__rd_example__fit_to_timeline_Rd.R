# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: fit_to_timeline.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 37

suppressPackageStartupMessages(library(lubridate))
tricky <- structure(list(
  sec = c(5, 0, 0, -1),
  min = c(0L, 5L, 5L, 0L),
  hour = c(2L, 0L, 2L, 2L),
  mday = c(4L, 4L, 14L, 4L),
  mon = c(10L, 10L, 2L, 10L),
  year = c(112L, 112L, 110L, 112L),
  wday = c(0L, 0L, 0L, 0L),
  yday = c(308L, 308L, 72L, 308L),
  isdst = c(1L, 0L, 0L, 1L)
),
.Names = c(
  "sec", "min", "hour", "mday", "mon",
  "year", "wday", "yday", "isdst"
),
class = c("POSIXlt", "POSIXt"),
tzone = c("America/Chicago", "CST", "CDT")
)

tricky
## [1] "2012-11-04 02:00:00 CDT" Doesn't exist because clocks "fall back" to 1:00 CST
## [2] "2012-11-04 00:05:00 CST" Times are still CDT, not CST at this instant
## [3] "2010-03-14 02:00:00 CDT" DST gap
## [4] "2012-11-04 01:59:59 CDT" Does exist, but has deceptive internal structure

fit_to_timeline(tricky)
## Returns:
## [1] "2012-11-04 02:00:00 CST" instant paired with correct tz & DST combination
## [2] "2012-11-04 00:05:00 CDT" instant paired with correct tz & DST combination
## [3] NA - fake time changed to NA (compare to as.POSIXct(tricky))
## [4] "2012-11-04 01:59:59 CDT" -real instant, left as is

fit_to_timeline(tricky, simple = TRUE)
## Returns valid time-dates by extrapolating CDT and CST zones:
## [1] "2012-11-04 01:00:05 CST" "2012-11-04 01:05:00 CDT"
## [3] "2010-03-14 03:05:00 CDT" "2012-11-04 01:59:59 CDT"