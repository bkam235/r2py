# r2py crawler metadata
# package: lubridate
# source_type: vignette
# topic: lubridate_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\doc\lubridate.R
# lines: 4

suppressPackageStartupMessages(library(lubridate))
last_day <- function(date) {
  ceiling_date(date, "month") - days(1)
}