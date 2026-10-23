# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: within-interval.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 31

suppressPackageStartupMessages(library(lubridate))
int <- interval(ymd("2001-01-01"), ymd("2002-01-01"))
int2 <- interval(ymd("2001-06-01"), ymd("2002-01-01"))

ymd("2001-05-03") %within% int # TRUE
int2 %within% int # TRUE
ymd("1999-01-01") %within% int # FALSE

## recycling (carefully note the difference between using a vector of
## intervals and list of intervals for the second argument)
dates <- ymd(c("2014-12-20", "2014-12-30", "2015-01-01", "2015-01-03"))
blackout_vector <- c(
  interval(ymd("2014-12-30"), ymd("2014-12-31")),
  interval(ymd("2014-12-30"), ymd("2015-01-03"))
)
dates %within% blackout_vector

## within ANY of the intervals of a list
dates <- ymd(c("2014-12-20", "2014-12-30", "2015-01-01", "2015-01-03"))
lst <- list(
  interval(ymd("2014-12-30"), ymd("2014-12-31")),
  interval(ymd("2014-12-30"), ymd("2015-01-03"))
)
dates %within% lst

## interval within a list of intervals
int <- interval(
  ymd("2014-12-20", "2014-12-30"),
  ymd("2015-01-01", "2015-01-03")
)
int %within% lst