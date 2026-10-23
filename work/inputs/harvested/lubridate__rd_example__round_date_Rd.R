# r2py crawler metadata
# package: lubridate
# source_type: rd_example
# topic: round_date.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\help
# lines: 80

suppressPackageStartupMessages(library(lubridate))
## print fractional seconds
options(digits.secs = 6)

x <- ymd_hms("2009-08-03 12:01:59.23")
round_date(x, ".5s")
round_date(x, "sec")
round_date(x, "second")
round_date(x, "minute")
round_date(x, "5 mins")
round_date(x, "hour")
round_date(x, "2 hours")
round_date(x, "day")
round_date(x, "week")
round_date(x, "month")
round_date(x, "bimonth")
round_date(x, "quarter") == round_date(x, "3 months")
round_date(x, "halfyear")
round_date(x, "year")

x <- ymd_hms("2009-08-03 12:01:59.23")
floor_date(x, ".1s")
floor_date(x, "second")
floor_date(x, "minute")
floor_date(x, "hour")
floor_date(x, "day")
floor_date(x, "week")
floor_date(x, "month")
floor_date(x, "bimonth")
floor_date(x, "quarter")
floor_date(x, "season")
floor_date(x, "halfyear")
floor_date(x, "year")

x <- ymd_hms("2009-08-03 12:01:59.23")
ceiling_date(x, ".1 sec") # imprecise representation at 0.1 sec !!!
ceiling_date(x, "second")
ceiling_date(x, "minute")
ceiling_date(x, "5 mins")
ceiling_date(x, "hour")
ceiling_date(x, "day")
ceiling_date(x, "week")
ceiling_date(x, "month")
ceiling_date(x, "bimonth") == ceiling_date(x, "2 months")
ceiling_date(x, "quarter")
ceiling_date(x, "season")
ceiling_date(x, "halfyear")
ceiling_date(x, "year")

## Period unit argument
floor_date(x, days(2))
floor_date(x, years(1))

## As of R 3.4.2 POSIXct printing of fractional numbers is wrong
as.POSIXct("2009-08-03 12:01:59.3") ## -> "2009-08-03 12:01:59.2 CEST"
ceiling_date(x, ".1 sec") ## -> "2009-08-03 12:01:59.2 CEST"

## behaviour of `change_on_boundary`
## As per default behaviour `NULL`, instants on the boundary remain the
## same but dates are rounded up
ceiling_date(ymd_hms("2000-01-01 00:00:00"), "month")
ceiling_date(ymd("2000-01-01"), "month")

## If `TRUE`, both instants and dates on the boundary are rounded up
ceiling_date(ymd_hms("2000-01-01 00:00:00"), "month", change_on_boundary = TRUE)
ceiling_date(ymd("2000-01-01"), "month")

## If `FALSE`, both instants and dates on the boundary remain the same
ceiling_date(ymd_hms("2000-01-01 00:00:00"), "month", change_on_boundary = FALSE)
ceiling_date(ymd("2000-01-01"), "month")

x <- ymd_hms("2000-01-01 00:00:00")
ceiling_date(x, "month")
ceiling_date(x, "month", change_on_boundary = TRUE)

## For Date objects first day of the month is not on the
## "boundary". change_on_boundary applies to instants only.
x <- ymd("2000-01-01")
ceiling_date(x, "month")
ceiling_date(x, "month", change_on_boundary = TRUE)