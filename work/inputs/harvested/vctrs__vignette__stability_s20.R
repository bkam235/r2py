# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: stability_s20
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\stability.R
# lines: 6

suppressPackageStartupMessages(library(vctrs))
date <- as.Date("2020-01-01")
datetime <- as.POSIXct("2020-01-01 09:00")

c(date, datetime)
c(datetime, date)