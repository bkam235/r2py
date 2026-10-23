# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: base-rev.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 5

suppressPackageStartupMessages(library(timeDate))
dts <- c("1989-09-28", "2001-01-15", "2004-08-30", "1990-02-09")
ZUR <- timeDate(dts, zone = "GMT", FinCenter = "Europe/Zurich")
ZUR
rev(ZUR)