# r2py crawler metadata
# package: timeDate
# source_type: rd_example
# topic: timeDate-finCenter.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\timeDate\help
# lines: 9

suppressPackageStartupMessages(library(timeDate))
date <- timeDate("2008-01-01")
finCenter(date) <- "GMT"
date
format(date)

finCenter(date) <- "Zurich"
date
format(date)