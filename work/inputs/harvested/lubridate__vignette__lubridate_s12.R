# r2py crawler metadata
# package: lubridate
# source_type: vignette
# topic: lubridate_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lubridate\doc\lubridate.R
# lines: 8

suppressPackageStartupMessages(library(lubridate))
leap_year(2011) ## regular year
ymd(20110101) + dyears(1)
ymd(20110101) + years(1)

leap_year(2012) ## leap year
ymd(20120101) + dyears(1)
ymd(20120101) + years(1)